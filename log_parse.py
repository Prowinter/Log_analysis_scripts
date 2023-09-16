import re
import os
from datetime import datetime, timedelta

class Log_Parse:
    def __init__(self, log_file, out_file = "out_file.log"):
        self.log_file = log_file
        self.out_file = out_file
        self.timestamp_format = "%Y-%m-%d %H:%M:%S"
        self.timestamp_pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')

    def log_merge(self, merge_log_start_with = "system", log_dir = ".", output_file = "merged_file.log"):
        # 获取日志文件列表并按后缀大小排序
        log_files = [f for f in os.listdir(log_dir) if f.startswith(merge_log_start_with)]
        log_files.sort(key=lambda x: int(x.split('.')[-1]) if x.split('.')[-1].isdigit() else -1)

        with open(output_file, 'w') as merged_log:
            for log_file in log_files:
                log_file_path = os.path.join(log_dir, log_file)
                with open(log_file_path, 'r') as log_content:
                    stripped_line = log_content.read().strip()
                    if stripped_line:
                        merged_log.write(stripped_line)
                        merged_log.write('\n')

    def time_tolerance(self, target_time_str, time_tolerance_minutes = 20):
        target_time = datetime.strptime(target_time_str, self.timestamp_format)
        time_tolerance = timedelta(minutes=time_tolerance_minutes)
        with open(self.log_file, 'r') as input_file, open(self.out_file, 'w') as output_file:
            for line in input_file:
                # 使用正则表达式查找时间戳
                timestamp_match = re.search(self.timestamp_pattern, line)
                if timestamp_match:
                    # 提取时间戳字符串
                    timestamp_str = timestamp_match.group()
                    # 将时间戳字符串转换为datetime对象
                    log_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    # 检查时间是否在指定时间点附近的时间区间内
                    if target_time - time_tolerance <= log_time <= target_time + time_tolerance:
                        # 如果在时间区间内，则打印日志行
                        output_file.write(line)

    def time_star_end(self, start_time_str, end_time_str):
        # 将时间字符串转换为datetime对象
        start_time = datetime.strptime(start_time_str, self.timestamp_format)
        end_time = datetime.strptime(end_time_str, self.timestamp_format)
        with open(self.log_file, 'r') as input_file, open(self.out_file, 'w') as output_file:
            for line in input_file:
                # 使用正则表达式查找时间戳
                timestamp_match = re.search(self.timestamp_pattern, line)
                if timestamp_match:
                    # 提取时间戳字符串
                    timestamp_str = timestamp_match.group()
                    # 将时间戳字符串转换为datetime对象
                    log_time = datetime.strptime(timestamp_str, self.timestamp_format)
                    # 检查时间是否在指定的时间区间内
                    if start_time <= log_time <= end_time:
                        # 如果在时间区间内，则打印日志行
                        output_file.write(line)

    # def Save_Parse(self):

BASE_LOG = Log_Parse("merged_file.log","filter_log.log")

# Filter logs for a certain period of time
# BASE_LOG.time_star_end("2023-09-05 18:40:25", "2023-09-05 18:45:25")


# Filter logs near a certain point in time
BASE_LOG.time_tolerance("2023-09-05 18:44:57",10)

# merge logs
#BASE_LOG.log_merge()
