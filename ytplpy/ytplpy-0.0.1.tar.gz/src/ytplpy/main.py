from pytube import YouTube
from pytube import Playlist
import os
import moviepy.editor as mp
import re

testurl = "https://www.youtube.com/watch?v=a_1tA0bpDQs&list=PLi_9g3NzCdCbddy5utX3fzqnULW1tlpju"


def downloadmp3playlist(url, directory=r"default\\"):
    assert isinstance(url, str), f"url Must Be String - it was {type(url)}"
    playlist = Playlist(url)
    if directory == r"default\\":
        directory = fr'{playlist.title.title()}\\'
    print(directory)
    for url in playlist:
        YouTube(url).streams.filter(only_audio=True).first().download()
    for url in playlist:
        YouTube(url).streams.first().download(directory)
    folder = directory
    for file in os.listdir(folder):
        if re.search('mp4', file):
            mp4_path = os.path.join(folder, file)
            mp3_path = os.path.join(folder, os.path.splitext(file)[0] + '.mp3')
            new_file = mp.AudioFileClip(mp4_path)
            new_file.write_audiofile(mp3_path)
            os.remove(mp4_path)
    print(os.listdir())
    for f in os.listdir():
        if f.endswith(".mp4"):
            os.remove(f)


def downloadmp4playlist(url, directory=r"default\\"):
    assert isinstance(url, str), f"url Must Be String - it was {type(url)}"
    playlist = Playlist(url)
    if directory == r"default\\":
        directory = fr'{playlist.title.title()}\\'
    print(directory)
    for url in playlist:
        YouTube(url).streams.filter().first().download()
    for url in playlist:
        YouTube(url).streams.first().download(directory)


if __name__ == '__main__':
    downloadmp3playlist("https://www.youtube.com/playlist?list=PLkCV0SkyKAS3DnlTLvWrpeoCsMo4zB-bF")
