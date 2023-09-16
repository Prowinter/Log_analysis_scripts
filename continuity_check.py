import re
from datetime import datetime, timedelta

class Classical_DATA:
    def __init__(self, input_file_path, output_file_path, timestamp_format = "%Y-%m-%d %H:%M:%S", timestamp_regex = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.timestamp_format = timestamp_format
        self.timestamp_regex = re.compile(timestamp_regex)
        self.Heartbeat_last_time = None
        self.Heartbeat_last_line = None
        
    def Heartbeat_Check(self, regex_pattern, report_freq, time_tolerance):
        with open(self.input_file_path, 'r') as input_file, open(self.output_file_path, 'w') as output_file:
            for this_line in input_file:
                match = re.search(regex_pattern, this_line)
                if match:
                    # 从匹配中提取数字并赋值给变量
                    # values = int(match.group(1))
                    # 使用正则表达式查找时间戳
                    timestamp_match = re.search(self.timestamp_regex, this_line)
                    if timestamp_match:
                            # 提取时间戳字符串
                            timestamp_str = timestamp_match.group()
                            # 将时间戳字符串转换为datetime对象
                            this_time = datetime.strptime(timestamp_str, self.timestamp_format)
                            # 检查时间是否在指定的时间区间内
                            if self.Heartbeat_last_time != None and (((abs(self.Heartbeat_last_time - this_time)).total_seconds() > report_freq + time_tolerance) or ((abs(self.Heartbeat_last_time - this_time)).total_seconds() < report_freq - time_tolerance)):
                                # 如果在时间区间内，则打印日志行
                                output_file.write(self.Heartbeat_last_line)
                            self.Heartbeat_last_time = this_time
                self.Heartbeat_last_line = this_line

pattern = r'freq:(\d+)Hz'
data_rate = 1
time_tolerance = 0.1

BASE_LOG = Classical_DATA("merger_out.log", "merger_err_out.log")
BASE_LOG.Heartbeat_Check(r'freq:(\d+)Hz', 1, 0.1)