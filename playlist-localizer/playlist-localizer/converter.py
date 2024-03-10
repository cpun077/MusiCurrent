from pytube import Playlist, YouTube
import os
import subprocess

def processlink(url, dir):
    print("Link: ", url, " Dir:", dir)
    if "youtube.com/watch" in url:
        getYTsong(YouTube(url), dir)
    elif "youtube.com/playlist" in url:
        playlist = Playlist(url)
        for video in playlist.videos:
            getYTsong(video, dir)

def getYTsong(video, dir):
    try:
        audios = video.streams.filter(only_audio=True).order_by('abr').desc()
        best = audios[0]
        print(best)
        path = best.download(dir)
        print("Downloading completed")
        #path = os.path.dirname(dir) + "/DAGOAT (INFINITY MONEY).mp3"
        applescript = (
            'tell application "Music" to add (POSIX file "' + path + '") as alias'
        )
        subprocess.call(['osascript', '-e', applescript])
        print("Uploading completed")
    except Exception as e:
        print("Converter Error: ", e)
        
playlist = "https://music.youtube.com/playlist?list=PL4ckrlA4uj4tr28D-Dpn5QrrS0wxd2blM&si=Z_8eTkBKgvTQm-U3"
song = "https://music.youtube.com/watch?v=9B2EQe-fmh8&si=oMh1n90MIjGTEDA2"
processlink(
    playlist,
    os.path.join(os.path.expanduser('~'), 'Downloads/Sounds')
)
        

