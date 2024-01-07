import subprocess
import eyed3
import os
import json
import logging
from tinytag import TinyTag
import pathlib

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_playlist_name(youtube_playlist):
    command = [
        'yt-dlp',
        '--flat-playlist',
        '--get-title',
        youtube_playlist
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, check=True)
    playlist_name = result.stdout.decode('utf-8').strip()

    return playlist_name

def download_playlist(youtube_playlist, root_dir):
    # Debug: Print the original root_dir
    print(f"Original root_dir: {root_dir}")

    # Add a double slash at the beginning of the path
    # root_dir = '//' + root_dir

    # Debug: Print the modified root_dir
    print(f"Modified root_dir: {root_dir}")

    # Download the first video
    command = [
        'yt-dlp',
        '-f', 'ba',
        '-x',
        '--audio-format', 'mp3',
        '--audio-quality', '0',
        '--add-metadata',
        '--embed-thumbnail',
        '--restrict-filenames',
        '-o', f"{root_dir}/%(title)s.%(ext)s",
        '--playlist-start', '1',
        '--playlist-end', '1',
        youtube_playlist
    ]

    subprocess.run(command, check=True)
    # ... rest of the function

    # Get the artist tag from the MP3 file
    mp3_files = [f for f in os.listdir(root_dir) if f.endswith('.mp3')]
    first_video_file = mp3_files[0]
    tag = TinyTag.get(os.path.join(root_dir, first_video_file))
    first_video_artist = tag.artist

    # Create the output directory if it doesn't exist
    output_dir = f"{root_dir}/{first_video_artist}"
    # Convert to Windows-style path if needed
    if os.name == 'nt':  # Only for Windows
        output_dir = output_dir.replace('/', '\\')
    os.makedirs(output_dir, exist_ok=True)

    # Move the first video to the output directory
    os.rename(os.path.join(root_dir, first_video_file), os.path.join(output_dir, first_video_file))

    # Download the rest of the videos
    command = [
        'yt-dlp',
        '-f', 'ba',
        '-x',
        '--audio-format', 'mp3',
        '--audio-quality', '0',
        '--add-metadata',
        '--embed-thumbnail',
        '--restrict-filenames',
        '-o', f'{output_dir}\\%(title)s.%(ext)s',
        '--playlist-start', '2',
        youtube_playlist
    ]

    logging.info(f'Downloading playlist: {youtube_playlist} to {output_dir}')
    subprocess.run(command, check=True)
    # Return the first video artist for further use
    return output_dir

def modify_mp3_tags(file_path, track_number):
    audiofile = eyed3.load(file_path)

    if audiofile.tag is None:
        audiofile.initTag()

    audiofile.tag.track_num = track_number
    audiofile.tag.save()

    logging.info(f'Set track number for {file_path} to {track_number}')

# Load the YouTube playlist URL and root directory from config.json
with open('config.json') as f:
    config = json.load(f)

youtube_playlist = config['youtube_playlist']
root_dir = config['root_dir']

# Use the functions
output_dir = download_playlist(youtube_playlist, root_dir)

#mp3_files = [f for f in os.listdir(output_dir) if f.endswith('.mp3')]

# Get the list of MP3 files from the output directory, sorted by creation date (oldest first)
mp3_files = sorted([f for f in os.listdir(output_dir) if f.endswith('.mp3')],
                   key=lambda x: os.path.getctime(os.path.join(output_dir, x)))

for i, file in enumerate(mp3_files, start=1):
    file = os.path.join(output_dir, file)
    modify_mp3_tags(file, i)