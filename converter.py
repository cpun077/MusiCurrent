from pytube import YouTube, Playlist
import os

def dlpl(pl, dir):
    p = Playlist(pl)
    for video in p.videos:
        video.streams.first().download(dir)
        
dlpl(
    "https://music.youtube.com/playlist?list=PL4ckrlA4uj4tr28D-Dpn5QrrS0wxd2blM&si=Z_8eTkBKgvTQm-U3",
    os.path.join(os.path.expanduser('~'), 'Downloads')
    )