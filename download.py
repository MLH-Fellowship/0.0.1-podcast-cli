import requests
import urllib.request
import os
import sys
from pathlib import Path

def download_podcast(directory, url_path):
    '''
    accepts path of podcast episode, and {directory} for download
    downloads the mp3 file to local machine in specified dir.
    '''
    full_url = f"https://dev.to/{url_path}"

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    return urllib.request.urlretrieve(full_url, f"{directory}/{url_path}.mp3") 


def create_dir(directory):
    '''
    Attempts to save the downloaded podcast file to the location {directory}
    '''

    if not os.path.exists(directory):
        os.system(f"mkdir {directory}")


if __name__ == "__main__":
    directory = os.path.expanduser("~/mp3_files")
    create_dir(directory)
    podcast_name, episode_name = os.path.split(sys.argv[1]) 
    if podcast_name != None:
        create_dir(directory + "/" + podcast_name)
    download_podcast(directory, sys.argv[1])

