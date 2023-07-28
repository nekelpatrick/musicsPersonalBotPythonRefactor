import re

def extract_urls(data):
    if not isinstance(data, str):
        raise TypeError("Input data is not a string.")
    regex = r'(https?:\/\/(www\.)?youtube\.com\/watch\?v=.{11}|https?:\/\/youtu.be\/.{11})'
    matches = re.findall(regex, data)
    if not matches:
        raise ValueError("No YouTube URLs found.")
    return [match[0] for match in matches]  # Returns only the URL part of each match
