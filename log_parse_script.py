
import re
import json
import pandas as pd

timestamp_regular_expression = re.compile(r'(\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})')

def parse_logs_to_excel(log_file_path, json_rules_path, excel_file_path):
    # Load the JSON rules from the file
    with open(json_rules_path, 'r') as json_file:
        rules = json.load(json_file)

    # Initialize a dictionary to store the parsed data
    parsed_data = {name: [] for name in rules.keys()}

    # Read the log file and apply the filter rules
    with open(log_file_path, 'r') as file:
        for line in file:
            # Match and extract the timestamp
            timestamp_match = re.search(timestamp_regular_expression, line)
            if timestamp_match:
                timestamp = timestamp_match.group(1)

                # Apply each pattern and store the data
                for rule in rules:
                    re_match_flag = False
                    data = {"timestamp" : timestamp}
                    for pattern in rules[rule]:
                        regular_expression = re.compile(pattern['pattern'])
                        pattern_group_index = pattern['group_index'] if 'group_index' in pattern else 0
                        match_data = regular_expression.search(line)
                        if match_data:
                            re_match_flag = True
                            data[pattern['name']] = match_data.groups()[pattern_group_index]
                    if re_match_flag:
                        parsed_data[rule].append(data)

    # Create a Pandas Excel writer and write each category of data to a different worksheet
    with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
        for rule in rules:
            # Concatenate dataframes that belong to the same rule category
            category_frames = []
            df = pd.DataFrame(parsed_data[rule])
            category_frames.append(df)

            # # Combine all DataFrames for the current rule category
            if category_frames:
                category_df = pd.concat(category_frames, axis=1)
                # Write the combined DataFrame to a worksheet named after the rule category
                category_df.to_excel(writer, sheet_name=rule, index=False)

# Example usage:
log_file_path = 'system.log' # Replace with the path to your log file
json_rules_path = 'parse_rules.json' # Replace with the path to your rules JSON file
excel_file_path = 'output_excel.xlsx' # Replace with the path to your output Excel file
parse_logs_to_excel(log_file_path, json_rules_path, excel_file_path)
