import subprocess

# File paths
video_file_path = "/Users/apple/django-backend-projects/commdem_warriors_django/static/38_205_2023-09-03_06:52:10.119495_mp4.mp4"  # noqa: E501
audio_file_path = "/Users/apple/django-backend-projects/commdem_warriors_django/static/daily_workout_audio_file.mp3"  # noqa: E501


# Define the start and end duration for the audio in seconds
start_duration = 10  # Replace with your desired start duration
end_duration = 20  # Replace with your desired end duration

# Define the FFmpeg command as a list of arguments
ffmpeg_command = [
    "ffmpeg",  # Command
    "-ss",
    str(0),  # Specify the start time for video
    "-i",
    video_file_path,  # Input video file
    "-ss",
    str(start_duration),  # Specify the start time for audio
    "-i",
    audio_file_path,  # Input audio file
    "-c:v",
    "copy",  # Copy video codec
    "-t",
    str(end_duration - start_duration),  # Specify the duration of the output video
    "-map",
    "0",  # Map video from input 0
    "-map",
    "1",  # Map audio from input 1
    "output_video.mp4",  # Output video file
]

# Run the FFmpeg command
subprocess.run(ffmpeg_command, check=True)
