import requests
import json
import random
import sys
import shutil
import os

from typing import List
from string_distance import recursive_levenshtein


# Link to the branch where work on this is happening: https://github.com/MLH-Fellowship/0.0.1-podcast-cli/tree/feat/use-python


# This is how Levensthein work. It falls short when comparing longer strings (e.g titles of podcasts).
# I think string matching can be improved (or rather fixed) using Dice Coefficient.
# This npm module I use (and it works perfectly) uses Dice Coefficient: https://www.npmjs.com/package/string-similarity.
# This whole thing might also be unnecessary. Consulting with The Shell Guys advised.
# print(recursive_levenshtein("bartek pacia", "bartk pcia"))
# print(recursive_levenshtein("bartek pacia", "bartek paci"))

# base_dir that stores all download images
IMG_DIR = "./images"

class PodcastEpisode:
    '''
    Represents a single podcast episode from the dev.to API.
    '''

    id = 0
    path = None
    title = None

    def __init__(self, id, path, title):
        self.id = id
        self.path = path
        self.title = title

    def __str__(self):
        return f"(PodcastEpisode) id={self.id} , path={self.path} , title={self.title}"


def parse_podcast_data(data):
    '''
    reusable method parses podcast json data returned by Dev.to API
    returns array of PodcastEpisode objects.
    '''
    podcast_episodes = []
    if not data:
        print("data is None. Something bad happened")

    for podcast_data in data:
        podcast_episode = PodcastEpisode(
            podcast_data["id"], podcast_data["path"], podcast_data["title"].lower()
        )

        podcast_episodes.append(podcast_episode)

    return podcast_episodes


def fetch_all_podcasts():
    '''
    fetches all podcasts available (up to 1000 most recent) via Dev.to API input
    no search param included
    '''
    response = requests.get(
        "https://dev.to/api/podcast_episodes?per_page=1000")
    data = json.loads(response.text)

    return parse_podcast_data(data)


def fetch_podcasts_by_title(username: str) -> List[PodcastEpisode]:
    '''
    Fetches a list of podcasts from the dev.to API. (up to 1000)

    Parameters
    ----------
    username - title of the whole podcast series
    '''
    username = username.strip().replace(" ", "")
    response = requests.get(
        f"https://dev.to/api/podcast_episodes?per_page=1000&username={username}")
    data = json.loads(response.text)

    return parse_podcast_data(data)


#  we can edit this to search the description as well.
#  a title search may be effective enough
#  this func returns a list.  If we want just the most recent one, we can
# invoke most_recent_podcast on the return val of this func.
def fetch_podcasts_by_keyword(keyword: str):
    '''
    accepts a string argument, key word
    returns list of PodcastEpisode object with that keyword in the title.
    '''

    keyword_title_matches = []
    podcast_episode_list = fetch_all_podcasts()

    for episode in podcast_episode_list:
        if keyword in episode.title.split():
            keyword_title_matches.append(episode)

    return keyword_title_matches


def fetch_random_podcast():
    '''
    fetches podcasts via Dev.to API call w/no search param. Returns a single
    random podcast episode from list of episodes returned by API.
    '''

    podcast_episode_list = fetch_all_podcasts()
    random_episode = random.choice(podcast_episode_list)

    return random_episode


def fetch_paginated_podcasts(page, per_page):
    '''
    fetches podcasts page by page

    - Precondition: page and per_page are integers or numeric strings
    '''
    
    response = requests.get(
        f"https://dev.to/api/podcast_episodes?page={page}&per_page={per_page}")
    data = json.loads(response.text)

    return parse_podcast_data(data)


def most_recent_podcast(list):
    '''
    returns most recent podcast in a list of PodcastEpisodes
    according to Dev.to response, this will be first in list
    '''
    return list[0]


def save(podcast_file):
    '''
    This will save the downloaded podcast file to "some" directory.
    e.g mp3-files2/ like in the shell script written by The Shell Guys.
    '''
    pass


def text_format(text, width):
    ''' 
    Returns a string with a length exactly equal to width. 
    If the original text is shorter than width, spaces are appended
    If the original text is longer than width, it is truncated with ellipses

    - Precondition: width > 3
    '''
    if len(text) <= width:
        text += ' ' * (width - len(text))
    else:
        text = text[:width - 3] + "..."
        
    assert len(text) == width
    return text

def print_podcast(podcast):
    title = text_format(podcast.title, 60)
    path = podcast.path
    print(f"{title}\t{path}")


def path_to_filepath(short_path: str, img_format="jpg", base_img_dir=IMG_DIR)-> (str, str):
    """:arg
    Given a dev.to short path, returns
    (1) a folder name (so it can be created) and
    (2) the relative full filepath.

    Given path = "/elixirmix/emx-095-adopting-elixir-at-findhotel-with-fernando-hamasaki-de-amorim"
    Returns
    ('./images/elixirmix',
    './images/elixirmix/emx-095-adopting-elixir-at-findhotel-with-fernando-hamasaki-de-amorim.jpg')
    """

    path_components = short_path.strip("/").split("/")
    folder = f"{base_img_dir}/{path_components[0]}"
    filename = "-".join(path_components[1:])
    filepath_out = f"{folder}/{filename}.{img_format}"

    return folder, filepath_out


def download_img(short_path: str, img_url: str):
    """:arg
    file_path: str - filepath where image is to be stored
    img_url: str - URL that points to the images

    Returns nothing
    """
    img_format = img_url.split(".")[-1]
    folder, file_path = path_to_filepath(short_path, img_format)

    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)

    if not os.path.exists(folder):
        os.makedirs(folder)

    r = requests.get(img_url, stream=True)
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(f"{file_path}", 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            print("Image successfully download:", file_path)


def podcast_info(short_path: str):
    pass


if __name__ == "__main__":
    if sys.argv[1] == "search":
        keyword = sys.argv[2].lower()
        podcasts = fetch_podcasts_by_keyword(keyword)
        for episode in podcasts:
            print_podcast(episode)          
    
    elif sys.argv[1] == "random":
        print_podcast(fetch_random_podcast())

    elif sys.argv[1] == "list":
        try:
            # check that the arguments are numeric
            val = int(sys.argv[2])
            if val < 0:
                print("podast list: please enter a positive integer for the page number")
                sys.exit(1)
            
            val = int(sys.argv[3])
            if val < 0:
                print("podast list: please enter a positive integer for the number of podcasts per page")
                sys.exit(1)
        
        except ValueError:
            print("podcast list: please enter an integer for the page number and podcasts per page") 
            sys.exit(1)
            
        podcasts = fetch_paginated_podcasts(sys.argv[2], sys.argv[3])
        for episode in podcasts:
            print_podcast(episode)

    elif sys.argv[1] == "info": 
        podcast_info(sys.argv[2])


# TESTING CODE BELOW- uncomment relevant piece to test functionality
# --------------------

# GENERATING RANDOM PODCAST
# ----------------------------
# episode = fetch_random_podcast()
# print(episode.title)


# RETURNING ALL PODCASTS
# -----------------------
# episodes = fetch_all_podcasts()
# print(len(episodes))


# RETURNING PODCASTS BY PODCAST TITLE
# ------------------------------------
# this will come from ZSH, I guess. For now, let's just use input().
# query_entered_by_the_user = input("Enter podcast name: ").lower()
# episodes = fetch_podcasts_by_title(query_entered_by_the_user)


# FETCH PODCASTS BY KEYWORD
# -----------------------------------
# keyword = input("Enter a keyword to search by: ").lower()
# returned_podcasts = fetch_podcasts_by_keyword(keyword)
#
# for episode in returned_podcasts:
#     print(episode.title)


# RETURNING MOST RECENT PODCAST BY ${PODCAST TITLE}
# --------------------------------------------------
# query_entered_by_the_user = input("Enter podcast name: ").lower()
# episodes = fetch_podcasts_by_title(query_entered_by_the_user)
# most_recent_episode = most_recent_podcast(episodes)
# print(most_recent_episode.title)


# RETURNING PODCAST BY PODCAST TITLE WITH EPISODE TITLE OF ___
# -------------------------------------------------------------
# query_entered_by_the_user = input("Enter podcast name: ").lower()
# episodes = fetch_podcasts_by_title(query_entered_by_the_user)
# # this might also come from ZSH side (?)
# podcast_episode_name = input("Enter podcast episode name (empty input will return all): ").lower()
#
# best_match_value = 0
# episode_with_best_match = None
#
# for podcast_episode in episodes:
#     match_value = recursive_levenshtein(
#         podcast_episode_name, podcast_episode.title)
#
#     if match_value > best_match_value:
#         best_match_value = match_value
#         episode_with_best_match = podcast_episode
#
#     # Used for debugging and testing how string similarity functionality works.
#     # Currently it works *bad*.
#     # print(f"match value for {podcast_episode.title}: {match_value}")
#
# print(f"{episode_with_best_match}: {match_value}")

# DOWNLOAD IMAGE
# -------------------------------------------------------------
# path = "/elixirmix/emx-095-adopting-elixir-at-findhotel-with-fernando-hamasaki-de-amorim"
# img_url = "https://dev-to-uploads.s3.amazonaws.com/uploads/podcast/image/78/0bff2d54-e4e4-4f3d-b9cc-6c67cdd195f4.jpg"
# download_img(path, img_url)
