import os
import subprocess
import sys
from datetime import datetime


def get_all_files(song_folder_name):
    """Gets a list of all the file names and extensions
    :param      song_folder_name: Name of the folder name that holds all of the wanted
        audio
    :type       song_folder_name: str
    :returns:   a list of strings of all file names and extensions in given folder
    :rtype:     list
    """
    all_songs = []
    for song in os.listdir(song_folder_name):
        all_songs.append(song)
    return all_songs

def find_the_differences(source_folder, destination_folder):
    """Gets a list of all songs that are in the source folder but not found in the
        destination folder
    :param      source_folder: Name of the folder that contains all audio
    :type       song_folder_name: str
    :param      destination_folder: Name of the folder to cross check all audio
    :type       destination_folder: str
    :returns:   a list of strings of all file names and extensions that are found in
        the source folder but not found in the destination folder
    :rtype:     list
    """
    songs1 = get_all_files(source_folder)
    songs2 = []
    differences = []
    for song in get_all_files(destination_folder):
        new_song = song.replace("SaR_", "")
        songs2.append(new_song)

    for song in songs1:
        if song not in songs2:
            differences.append(song)
    return differences

def create_folder_if_not_exists(folder_name):
    """Create a folder if the folder does not exist already
    :param      folder_name: A string of a folder name that should be created
    :type       folder_name: str
    :returns:   None
    :rtype:     None
    """
    # check to see if the folder has been created already
    if os.path.isdir(folder_name):
        print("{} already exists.".format(folder_name))
        return
    try:
        os.makedirs(folder_name, exist_ok=True)
        print("We've created {} successfully".format(folder_name))
    except OSError as error:
        print("We've encountered an error.")

def slow(source_folder, original, folder_name, tempo=0.8):
    """Create a slowed down version of the given audio file
    :param      source_folder: The folder where the audio comes from
    :type       song_folder_name: str
    :param      original: The audio file name and extension
    :type       original: str
    :param      folder_name: The name of the destination folder
    :type       folder_name: str
    :param      tempo: The percentage of the original speed to change to
    :type       tempo: float
    :returns:   name: The name of the slowed down version ("slowed.mp3")
    :rtype:     str
    """
    name = "slowed.mp3"
    command = 'ffmpeg -i "{}/{}" -filter:a "atempo={}" -vn "{}/{}"'.format(source_folder, original, tempo, folder_name, name)
    subprocess.call(command,shell=True)
    return name

def pitch_down(slowed, folder_name):
    # TODO: change this to be universal instead of "slowed" and "slowed_and_pitched_down"
    """Pitched down version of the audio file passed in
    :param      slowed: The slowed down audio
    :type       slowed: str
    :param      folder_name: The destination folder
    :type       folder_name: str
    :returns:   name: The name of the pitched down version ("slowed_and_pitched_down.mp3")
    :rtype:     str
    """
    name = "slowed_and_pitched_down.mp3"
    command = 'ffmpeg -i "{}/{}" -af "asetrate=44100*0.8,atempo=1.4,aresample=44100" "{}/{}"'.format(folder_name, slowed, folder_name, name)
    subprocess.call(command,shell=True)
    return name

def slowed_and_reverbed(original_audio, slowed_and_pitched, folder_name, choice=0, weights=10):
    """Add reverb to the audio
    :param      original_audio: The original audio's file name
    :type       slowed: str
    :param      slowed_and_pitched: The slowed and pitched down version of the original audio
    :type       slowed_and_pitched: str
    :param      folder_name: The destination folder
    :type       folder_name: str
    :param      choice: The choice to either use a small reverb fart or a big reverb fart
    :type       choice: int
    :param      weights: How many parts original audio to 1 parts reverb
    :type       weights: int
    :returns:   name: The name of reverbed audio 
    :rtype:     str
    """
    fart_sound = "fart_reverb.mp3" if choice == 0 else "fart_reverb2.mp3"
    final_name = original_audio.replace(".mp3", "")
    name = "SaR_{}.mp3".format(final_name)
    command = 'ffmpeg -i "{}/{}" -i "{}" -filter_complex "[0] [1] afir=dry=10:wet=10 [reverb]; [0] [reverb] amix=inputs=2:weights={} 1" "{}/{}"'.format(folder_name, slowed_and_pitched, fart_sound, weights, folder_name, name)
    subprocess.call(command,shell=True)
    return name

def delete_extras(folder_name, slowed_audio, slowed_and_pitched_audio):
    # TODO: change this to be more universal as well
    """Delete all the extra files that are not needed anymore
    :param      folder_name: The folder that holds the files to be deleted
    :type       folder_name: str
    :param      slowed_audio: The name of the slowed audio file
    :type       slowed_audio: str
    :param      slowed_and_pitched_audio: The name of the slowed and pitched audio
    :type       slowed_and_pitched_audio: str
    :returns:   None
    :rtype:     None
    """
    all_files = [slowed_audio, slowed_and_pitched_audio]
    for _file in all_files:
        os.remove("{}/{}".format(folder_name, _file))

def main_function(source_folder):
    """The main function of the script to run
    :param      source_folder: The source folder that holds all of the audio files
    :type       source_folder: str
    :returns:   None
    :rtype:     None
    """
    destination_folder = "{}SaR".format(source_folder)
    create_folder_if_not_exists(destination_folder)
    differences = find_the_differences(source_folder, destination_folder)
    for song in differences:
        # print(song)
        original_audio = song
        slowed_audio = slow(source_folder, original_audio, destination_folder, 0.93)
        slowed_and_pitched_audio = pitch_down(slowed_audio, destination_folder)
        slowed_and_reverbed_audio = slowed_and_reverbed(original_audio, slowed_and_pitched_audio, destination_folder, 1, 10)
        delete_extras(destination_folder, slowed_audio, slowed_and_pitched_audio)
        print("We've created {}".format(slowed_and_reverbed_audio))


if __name__ == "__main__":
    # send in the source folder
    if len(sys.argv) > 1:
        source_folder = sys.argv[1]
    else:
        source_folder = datetime.today().strftime("%Y-%m-%d")
    main_function(source_folder)
    