from pytube import Playlist
from moviepy.editor import AudioFileClip
import os
import re

def dlpl(pl, dir):
    try:
        p = Playlist(pl)
        for video in p.videos:
            audios = video.streams.filter(only_audio=True)
            best = max(audios, key=lambda x: int(x.abr[:-4])) # remove the kbps suffix
            best.download(dir)
        for a in os.listdir(dir):
            if not re.search("mp3", a):
                path = os.path.join(dir, a)
                audio = AudioFileClip(path)
                newpath = os.path.splitext(path)[0] + '.mp3'
                audio.write_audiofile(newpath)
                os.remove(path)
        print("completed")
    except Exception as e:
        print("error: ", e)

dlpl(
    "https://music.youtube.com/playlist?list=PL4ckrlA4uj4tr28D-Dpn5QrrS0wxd2blM&si=Z_8eTkBKgvTQm-U3",
    os.path.join(os.path.expanduser('~'), 'Downloads/Sounds')
    )