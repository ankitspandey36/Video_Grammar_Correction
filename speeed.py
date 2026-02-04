

import librosa
import soundfile as sf

def change_audio_speed(input_audio_path, output_audio_path, target_duration):
    # Load the audio file
    audio, sample_rate = librosa.load(input_audio_path, sr=None)

    # Get the original duration of the audio (in seconds)
    original_duration = librosa.get_duration(y=audio, sr=sample_rate)

    # Calculate the speed factor (ratio of original duration to target duration)
    speed_factor = original_duration / target_duration

    # Change the speed of the audio without changing pitch
    audio_stretched = librosa.effects.time_stretch(audio, rate=speed_factor)

    # Export the modified audio
    sf.write(output_audio_path, audio_stretched, sample_rate)

# Example usage
# input_audio = "path/to/input_audio.wav"
# output_audio = "path/to/output_audio.wav"
# target_duration_sec = 30  # Target duration in seconds

# change_audio_speed_librosa(input_audio, output_audio, target_duration_sec)


# # Example usage
# input_audio = "path/to/input_audio.wav"
# output_audio = "path/to/output_audio.wav"
# target_duration_ms = 30000  # Target duration in milliseconds (e.g., 30 seconds)

# change_audio_speed(input_audio, output_audio, target_duration_ms)
