import glob
import os

def merge_logs():
    # Find all log files with names matching 'system*.log' and sort them in reverse order
    log_files = sorted(glob.glob('*.log'), reverse=True)

    # Name of the final merged log file
    merged_log_name = 'final_merged_system.log'

    # Open the merged log file in write mode
    with open(merged_log_name, 'w', encoding='utf-8') as merged_file:
        # Iterate over each log file
        for log_file in log_files:
            try:
                # Try to open each log file in read mode with utf-8 encoding
                with open(log_file, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
            except UnicodeDecodeError:
                # If utf-8 decoding fails, try latin-1 encoding
                with open(log_file, 'r', encoding='latin-1') as file:
                    lines = file.readlines()
            
            # Ensure the last line ends with a newline character
            if lines and not lines[-1].endswith('\n'):
                lines[-1] += '\n'
            # Write the reversed lines to the merged file
            merged_file.writelines(reversed(lines))

    print(f"Logs have been merged into {merged_log_name}")

if __name__ == "__main__":
    merge_logs()
