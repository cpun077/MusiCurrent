from pytube import Playlist, YouTube
import os
import subprocess

def dlplaylist(url, dir):
    print("Playlist: ", url, " Directory: ", dir)
    try:
        p = Playlist(url)
        for video in p.videos:
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

def dlsong(url, dir):
    print("Song: ", url, " Directory: ", dir)
    try:
        s = YouTube(url)
        audios = s.streams.filter(only_audio=True).order_by('abr').desc()
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

# dlplaylist(
#     "https://music.youtube.com/playlist?list=PL4ckrlA4uj4tr28D-Dpn5QrrS0wxd2blM&si=Z_8eTkBKgvTQm-U3",
#     os.path.join(os.path.expanduser('~'), 'Downloads/Sounds')
#     )
        
# dlsong(
#     "https://music.youtube.com/watch?v=9B2EQe-fmh8&si=oMh1n90MIjGTEDA2",
#     os.path.join(os.path.expanduser('~'), 'Downloads/Sounds')
# )
        

