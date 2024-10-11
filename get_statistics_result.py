from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from google.oauth2 import service_account
import pandas as pd
from datetime import datetime
import json
# import tabulate
pd.set_option('display.max_colwidth', None)

SCOPES = ["https://www.googleapis.com/auth/forms.responses.readonly", "https://www.googleapis.com/auth/forms"]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
SERVICE_ACCOUNT_FILE = './google_form_keys.json'
FORM_ID = "1v62CqeMpgjnMUYlMYXKooN950tR0Uf3QhS2plKdXfis"

question_id_to_name = {
    '28604f06': 'type',
    '2dc01b11': 'current_live_country', # 现居地
    '3f61c385': 'mail',
    '28d36a13': 'study_start_date',
    '586ff8ee': 'visa_submit_date',
    '7f4e519e': 'leave_family_due_to_security', # 是否由于安调与家人分开，分开多久
    '0d6f4db9': 'try_operation',
    '408966aa': 'huzhao_country',
    '2b879e06': 'study_degree',
    '0fa7018d': 'can_not_change_job_due_to_security', # 想换工作但是不能换
    '2a48c950': 'submit_address',
    '08f09ba7': 'leave_security_date',
    '1d5e52a5': 'last_operator_date',
    '01058234': 'enter_security_date',
    '060d1f5c': 'get_visa_date',
    '40a54065': 'gender_on_passport',
    '47de1bf3': 'major',
    '6b2dc6e1': 'ircc_last_update_time', # 多久没有收到移民部的消息
}


def request_api(demo = True):
    if demo == True:
        datas = open('./input.txt').read()
        return eval(datas)

    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = discovery.build(
        "forms",
        "v1",
        credentials=credentials,
        discoveryServiceUrl=DISCOVERY_DOC,
        static_discovery=False,
    )
    result = service.forms().responses().list(formId=FORM_ID).execute()
    return result


def main():
    datas = request_api(demo = False)['responses']
    dict_to_df = {}
    for k, v in question_id_to_name.items():
        dict_to_df[v] = []
    dict_to_df['lastSubmittedTime'] = []
    for data in datas:
        all_raws = list(dict_to_df.keys())
        dict_to_df['lastSubmittedTime'].append(data['lastSubmittedTime'])
        all_raws.remove('lastSubmittedTime')
        for key, value in data['answers'].items():
            val = value['textAnswers']['answers'][0]['value']
            key = question_id_to_name[key]
            dict_to_df[key].append(val)
            all_raws.remove(key)
        for key in all_raws:
            dict_to_df[key].append(None)
    df = pd.DataFrame.from_dict(dict_to_df)

    # rename columns values
    df['type'] = df['type'].map(lambda x: x.split(" / ")[0])

    df['security_days'] = df[['visa_submit_date', 'lastSubmittedTime']].apply(lambda x: \
        (datetime.strptime(str(x['lastSubmittedTime'])[: 10], '%Y-%m-%d') - \
            datetime.strptime(str(x['visa_submit_date']), '%Y-%m-%d')
        ).days, axis = 1) 
    statistics = df[['type', 'security_days']].groupby('type').\
            describe(percentiles = [.25, .5, .75, .9]).sort_values(by=('security_days', 'count'), ascending=False)
    statistics.columns = ['count','mean','std','min','25%','50%','75%', '90%','max']
    statistics = statistics.drop(['std', 'max'], axis = 1)
    statistics['count'] = statistics['count'].astype(int)
    statistics['mean'] = statistics['mean'].round(1)
    statistics['min'] = statistics['min'].astype(int)
    statistics['25%'] = statistics['25%'].astype(int)
    statistics['50%'] = statistics['50%'].astype(int)
    statistics['75%'] = statistics['75%'].astype(int)
    statistics['90%'] = statistics['90%'].astype(int)
    # statistics = statistics.reset_index()
    md = statistics.to_markdown()
    print (md)
    # print (res, type(res))

    # with open('./statistics_res.md', 'w') as convert_file: 
    #     convert_file.write(md)

if __name__ == "__main__":
    main()
