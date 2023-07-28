import os
import re
import subprocess
import unicodedata
from typing import List
from rest_framework.parsers import BaseParser
from concurrent.futures import ThreadPoolExecutor


REMOVE_WORDS = [
    "karaoke",
    "playback",
    "oficial",
    "original",
    "qualidade",
    "melhor",
    "com letra",
    "musica com primeira voz e letra",
    "playback oficial melhor qualidade",
    "playback oficial com letra",
    "jn karaoke",
    "karaokê tcho",
    "2 tons abaixo",
    "playback oficial",
    "oficial",
    "jn",
    "tcho",
    "original c letra",
    "com vocais",
    "made popular by",
    "version",
    "medley",
]


def extract_youtube_urls(data: str) -> List[str]:
    """Extract YouTube URLs from a text string."""
    if not isinstance(data, str):
        raise TypeError("Input data is not a string.")
    regex = r'(https?:\/\/(www\.)?youtube\.com\/watch\?v=.{11}|https?:\/\/youtu.be\/.{11})'
    matches = re.findall(regex, data)
    if not matches:
        raise ValueError("No YouTube URLs found in the input data.")
    return [match[0] for match in matches]


class PlainTextParser(BaseParser):
    """Parser for plain text data."""
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read().decode('utf-8')


def format_file_name(file_name: str) -> str:
    """Format a file name by removing undesired characters and words."""
    file_name, ext = os.path.splitext(file_name)
    file_name = file_name.lower()
    file_name = unicodedata.normalize('NFD', file_name).encode(
        'ascii', 'ignore').decode("utf-8")
    file_name = re.sub(r"[&=@#/\(\)\[\]\{\},?!._]", " ", file_name)
    file_name = file_name.replace('mp3', '')
    for word in REMOVE_WORDS:
        file_name = re.sub(rf'\b{word}\b', '', file_name)
    file_name = re.sub(r'\b\d+\b$', '', file_name)
    file_name = re.sub(r'\s+', ' ', file_name).strip()
    file_name = ' '.join(word.capitalize() for word in file_name.split())
    file_name = re.sub(r'\s+-\s+-\s+', ' - ', file_name).strip()
    file_name = re.sub(r'\s+-$', '', file_name).strip()
    return file_name + ext


def download_from_youtube(urls: List[str]) -> bool:
    """Download YouTube videos as audio files."""

    def download_url(url: str):
        command = [
            "yt-dlp",
            "-x",  # Extract audio
            "--audio-format", "wav",  # Save as wav
            "--postprocessor-args", "-ac 2 -ar 44100",  # Set number of audio channels and sample rate
            "-o", "tmp/%(title)s.%(ext)s",  # Output file name format
            url,  # The URL to download
        ]
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode != 0:
            raise RuntimeError(f"'yt-dlp' command failed with output:\n{process.stdout}")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_url, urls)

    return True


def rename_files(files: List[str]) -> None:
    """Rename files using the format_file_name function."""
    for file in files:
        old_path = os.path.join('tmp', file)
        new_name = format_file_name(file)
        new_path = os.path.join('tmp', new_name)
        os.rename(old_path, new_path)


def rename_files_in_directory(directory: str) -> None:
    """Get a list of files in a directory and rename them."""
    files = os.listdir(directory)
    rename_files(files)
