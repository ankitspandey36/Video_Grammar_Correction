from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

def mute_video_and_add_audio(video_path, output_path, audio_clips_info):
    """
    Mute the video, add specific audio at given times, and save the result.

    :param video_path: Path to the input video
    :param output_path: Path to save the output video
    :param audio_clips_info: List of tuples with audio file paths and their start times in seconds
    """
    # Load the video file and mute it
    video = VideoFileClip(video_path)
    video = video.without_audio()  # Mute the video

    # Create a list to hold all the audio clips to add
    audio_clips = []

    # Loop over the audio files and start times, and add them to the video
    for audio_path, start_time in audio_clips_info:
        audio_clip = AudioFileClip(audio_path).set_start(start_time)
        audio_clips.append(audio_clip)

    # Combine all audio clips into one composite audio
    composite_audio = CompositeAudioClip(audio_clips)

    # Set the composite audio to the video
    final_video = video.set_audio(composite_audio)

    # Export the final video
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

# # Example usage
# video_path = "path/to/your/video.mp4"
# output_path = "path/to/output/video_with_audio.mp4"

# # List of audio clips and their start times (in seconds)
# audio_clips_info = [
#     ("path/to/audio1.mp3", 5),  # Place audio1.mp3 at 5 seconds
#     ("path/to/audio2.mp3", 20), # Place audio2.mp3 at 20 seconds
# ]

# mute_video_and_add_audio(video_path, output_path, audio_clips_info)
