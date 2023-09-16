import re
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

input_file = "merger_out.log" 
pattern = r'freq:(\d+)Hz'
timestamps = []
values = []
with open(input_file, 'r') as inputs:
    for line in inputs:
        timestamp_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
        if timestamp_match:
            # 提取时间戳字符串
            timestamp_str = timestamp_match.group()
            # 将时间戳字符串转换为datetime对象
            timestamps.append(datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S"))
            # 检查时间是否在指定时间点附近的时间区间内

        match = re.search(pattern, line)
        if match:
            # 从匹配中提取数字并赋值给变量
            values.append(int(match.group(1)))



# 使用正则表达式查找时间戳



plt.figure(figsize=(10, 6))
plt.scatter(timestamps, values, label='data point', color='blue', s=0.5)
print(timestamps[1:10])
# 设置X轴标签为时间戳，并进行日期格式化
plt.xlabel('time')

# 设置Y轴标签
plt.ylabel('value')


plt.ylim(0, 250)

# 显示图形
plt.show()

# plt.plot(timestamps, values, linewidth=0.6)#s-:方形
# plt.ylim(0, 250)
# plt.show()