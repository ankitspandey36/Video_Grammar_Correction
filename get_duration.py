import subprocess

def get_audio_duration(file_path):
    try:
        # Run the ffprobe command and capture the output
        result = subprocess.run(
            ['ffprobe', '-i', file_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv="p=0"'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Extract duration from the result
        duration_in_seconds = float(result.stdout.strip())
        return duration_in_seconds
    except Exception as e:
        print(f"Error getting duration: {e}")
        return None