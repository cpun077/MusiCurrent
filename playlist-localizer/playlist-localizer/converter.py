from pytube import Playlist
import os
import subprocess

def dlpl(pl, dir):
    print("Playlist: ", pl, " Directory: ", dir)
    
    try:
        p = Playlist(pl)
        for video in p.videos:
            audios = video.streams.filter(only_audio=True)
            best = max(audios, key=lambda x: int(x.abr[:-4])) # remove the kbps suffix
            path = best.download(dir)
            #path = os.path.dirname(dir) + "/DAGOAT (INFINITY MONEY).mp3"
            applescript = (
                'tell application "Music" to add (POSIX file "' + path + '") as alias'
            )
            subprocess.call(['osascript', '-e', applescript])
        print("Completed downloading playlist")
    except Exception as e:
        print("Converter Error: ", e)

# def dlpl(pl, dir):
#     try:
#         p = Playlist(pl)
#         config = {
#             'format': 'bestaudio',
#             'outtmpl': f'{dir}/%(title)s.%(ext)s',
#         }
#         with YoutubeDL(config) as dl:
#             dl.download(p.video_urls)
#         print("completed")
#     except Exception as e:
#         print("error: ", e)

# dlpl(
#     "https://music.youtube.com/playlist?list=PL4ckrlA4uj4tr28D-Dpn5QrrS0wxd2blM&si=Z_8eTkBKgvTQm-U3",
#     os.path.join(os.path.expanduser('~'), 'Downloads/Sounds')
#     )

