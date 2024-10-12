OUTPUT="./index.md"
python3 get_statistics_result.py


echo "# 安调时长分布(已出安调)\n" > ${OUTPUT}
cat ./statistics_leave_security.md >> ${OUTPUT}
echo "\n\n口径：出安调时间 - 签证递交时间" >> ${OUTPUT}


echo "\n\n# 等待时长分布(仍在等待)\n" >> ${OUTPUT}
cat ./statistics_still_security.md >> ${OUTPUT}
echo "\n\n口径：最新更新问卷时间 - 签证递交时间" >> ${OUTPUT}


time=$(TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M:%S')
echo "\n\n上次更新时间(UTC+8): ${time}" >> ${OUTPUT}
echo "\n\n您的填写将使数据更加准确与可信，诚邀您参与填写问卷: [问卷](https://forms.gle/bxUKH95Yq54SVNvp8)" >> ${OUTPUT}