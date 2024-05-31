import os
import logging
import sys
from pydub import AudioSegment

logging.basicConfig(level=logging.INFO)


def convert_to_wav(directory: str) -> None:
    logging.info(f"Starting conversion of files in {directory} to .wav format")

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_name, ext = os.path.splitext(file)
            output_path = os.path.join(root, f"{file_name}.wav")

            # Skip the conversion if the file is already in .wav format
            if ext.lower() == ".wav":
                logging.info(f"File {file} is already in .wav format. Skipping.")
                continue

            try:
                logging.info(f"Converting file {file} to .wav format")
                audio = AudioSegment.from_file(file_path, format=ext.lower().replace(".", ""))
                audio = audio.set_channels(2)
                audio = audio.set_channels(2)
                audio = audio.set_frame_rate(44100)
                audio.export(output_path, format="wav")
                logging.info(f"Successfully converted: {file} to .wav")
                # Optionally, delete the original file after conversion
                os.remove(file_path)
                logging.info(f"Deleted original file: {file}")
            except Exception as e:
                logging.error(f"Error converting file: {file}. Error: {e}")

    logging.info(f"Conversion of files in {directory} to .wav format completed")
    logging.info(f"Conversion of files in {directory} to .wav format completed")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_to_wav.py [directory]")
        sys.exit(1)

    directory = sys.argv[1]
    convert_to_wav(directory)
