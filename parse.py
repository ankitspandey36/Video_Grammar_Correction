import re
# file_path="silence_log.txt"
# Function to parse the FFmpeg silence detection log file
def parse_silence_log(file_path):
    silences = []
    
    # Regular expressions to match silence_start and silence_end lines
    silence_start_re = re.compile(r"silence_start: (\d+(\.\d+)?)")
    silence_end_re = re.compile(r"silence_end: (\d+(\.\d+)?) \| silence_duration: (\d+(\.\d+)?)")
    
    with open(file_path, 'r') as f:
        for line in f:
            # Look for silence_start
            start_match = silence_start_re.search(line)
            if start_match:
                silence_start = float(start_match.group(1))
                
            # Look for silence_end
            end_match = silence_end_re.search(line)
            if end_match:
                silence_end = float(end_match.group(1))
                silence_duration = float(end_match.group(3))
                
                # Append the start, end, and duration of each silence period
                silences.append({
                    "start": silence_start,
                    "end": silence_end,
                    "duration": silence_duration
                })
    
    return silences

# Example usage
# log_file = "silence_log.txt"
# parsed_silences = parse_silence_log(log_file)

# # Print the results
# for silence in parsed_silences:
#     print(f"Silence from {silence['start']} to {silence['end']} (Duration: {silence['duration']} seconds)")
