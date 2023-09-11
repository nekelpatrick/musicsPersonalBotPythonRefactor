import os
import sys
import logging
from tqdm import tqdm
from pydub import AudioSegment

logging.basicConfig(level=logging.INFO)


def get_file_count(directory):
    """Returns the total number of valid audio files in the directory and all its subdirectories."""
    count = 0
    directories = []
    for root, dirs, files in os.walk(directory):
        directories.append(root)
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in [".mp3", ".flac", ".ogg", ".m4a", ".wma", ".wav"]:
                count += 1
    return count, directories


def convert_to_wav(directory: str) -> None:
    """Converts all audio files in the given directory to wav format."""
    total_files, all_directories = get_file_count(directory)
    processed_directories = []
    with tqdm(
        total=total_files, ncols=70, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"
    ) as pbar:
        for root, dirs, files in os.walk(directory):
            pbar.set_description(f"Processing {root.split('/')[-1]}")
            for file in files:
                file_path = os.path.join(root, file)
                file_name, ext = os.path.splitext(file)
                output_path = os.path.join(root, f"{file_name}.wav")

                # Skip the conversion if the file is already in .wav format
                if ext.lower() == ".wav":
                    logging.info(f"File {file} is already in .wav format. Skipping.")
                    continue

                # Skip the file if it's not an audio file
                if ext.lower() not in [
                    ".mp3",
                    ".flac",
                    ".ogg",
                    ".m4a",
                    ".wma",
                    ".webm",
                ]:
                    logging.warning(f"Unsupported file type: {file}. Skipping.")
                    continue

                try:
                    audio = AudioSegment.from_file(
                        file_path, format=ext.lower().replace(".", "")
                    )
                    audio = audio.set_channels(2)
                    audio = audio.set_frame_rate(44100)
                    audio.export(output_path, format="wav")
                    logging.info(f"Successfully converted: {file} to .wav")
                    processed_directories.append(root)
                except Exception as e:
                    logging.error(f"Error converting file: {file}. Error: {e}")
                    continue

                # Delete the original file after conversion
                try:
                    os.remove(file_path)
                    logging.info(f"Deleted original file: {file}")
                except Exception as e:
                    logging.error(f"Error deleting file: {file}. Error: {e}")

                pbar.update(1)

    processed_directories = list(set(processed_directories))
    logging.info(f"Total files processed: {pbar.n}")
    logging.info(f"Total directories processed: {len(processed_directories)}")
    logging.info(f"Directories processed: {processed_directories}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_to_wav.py [directory]")
        sys.exit(1)

    directory = sys.argv[1]
    convert_to_wav(directory)
