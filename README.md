# YouTube Playlist Downloader and MP3 Tag Modifier

## Description
This script automates the process of downloading audio from a YouTube playlist, converting them to MP3 format, and then modifying their ID3 tags. It downloads the first video from the playlist, extracts the artist name, creates a directory for the artist, and then downloads the rest of the playlist into this directory. Each MP3 file's track number is then set based on its order in the playlist.

## Requirements
- Python 3.x
- `yt-dlp`
- `eyed3`
- `TinyTag`
- A configuration file named `config.json` in the same directory as the script.

## Installation

### Install Python Dependencies
```bash
pip install yt-dlp eyed3 TinyTag
```

### Clone Repository
Clone this repository to your local machine:
```bash
git clone [URL to the repository]
```

### Configuration
Create a `config.json` file with the following structure:
```json
{
    "youtube_playlist": "YOUR_YOUTUBE_PLAYLIST_LINK",
    "root_dir": "YOUR_DESIRED_ROOT_DIRECTORY_PATH"
}
```
Replace `YOUR_YOUTUBE_PLAYLIST_LINK` with the link to the YouTube playlist you want to download and `YOUR_DESIRED_ROOT_DIRECTORY_PATH` with the path where you want to save the MP3 files.

## Usage
Run the script with Python:
```bash
python youtube_playlist_downloader.py
```

The script will download the first video from the specified YouTube playlist, create an artist-named directory, download the rest of the playlist into this directory, and then update the MP3 tags.

## Note
Ensure that the `config.json` file is correctly set up before running the script. The script relies on this configuration for the playlist URL and the root directory for downloads.
