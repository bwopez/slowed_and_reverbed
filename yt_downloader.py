import os
import subprocess
import sys
import csv
from datetime import datetime

from slowed_and_reverbed import create_folder_if_not_exists


def get_audio_list(file_name):
    """Gets the list of audios from a specified .csv file
    :param      file_name: The file name of the .csv to get list form (including extension)
    :type       file_name: str
    :returns:   a list of dictionaries that hold the Title, Author, and the Youtube
        link of each audio
    :rtype:     list
    """
    audio_list = []
    with open(file_name, "r") as working_file:
        file = csv.DictReader(working_file)
        for col in file:
            if col["hasBeenDownloaded"] == "No":
                audio_list.append({
                    "Title": col["songName"],
                    "Author": col["author"],
                    "Link": col["link"]
                })
    return audio_list

def download_audio(audio_dict):
    """Extracts and Downloads the audio from the Youtube video given
    :param      audio_dict: A dictionary that contains the Title, Author, and 
        the Youtube link of the audio
    :type       audio_dict: dictionary
    :returns:   None
    :rtype:     None
    """
    current_dir = os.getcwd()
    path_to_save = os.path.join(current_dir, datetime.today().strftime("%Y-%m-%d"))
    create_folder_if_not_exists(path_to_save)
    # TODO: change this command to get the title, author, description, etc.
    command = 'youtube-dl -x --audio-format mp3 -o "{}\%(title)s.%(ext)s" {}'.format(path_to_save, audio_dict["Link"])
    subprocess.call(command)

if __name__ == "__main__":
    # send in the youtube link
    if len(sys.argv) > 1:
        download_audio({
            "Title": sys.argv[1],
            "Author": sys.argv[2],
            "Link": sys.argv[3]
        })
    else:
        audios = get_audio_list("{}-audio - Sheet1.csv".format(datetime.today().strftime("%Y-%m-%d")))
        for audio in audios:
            download_audio(audio)
            # print(audio)
            # print(type(audio))
    