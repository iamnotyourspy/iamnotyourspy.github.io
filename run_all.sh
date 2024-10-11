OUTPUT="./index.md"

echo "# 分类型安调时长统计\n" > ${OUTPUT}

python3 get_statistics_result.py # >> ${OUTPUT}

time=$(TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M:%S')
echo "\n\n上次更新时间(UTC+8): ${time}" >> ${OUTPUT}
echo "\n\n诚邀您填写问卷: [问卷](https://forms.gle/bxUKH95Yq54SVNvp8)" >> ${OUTPUT}
