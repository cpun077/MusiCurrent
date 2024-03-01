from pytube import Playlist
import os

def dlpl(pl, dir):
    try:
        p = Playlist(pl)
        for video in p.videos:
            audios = video.streams.filter(only_audio=True)
            best = max(audios, key=lambda x: int(x.abr[:-4])) # remove the kbps suffix
            best.download(dir)
        print("completed")
    except Exception as e:
        print("error: ", e)

def testConnect(msg):
    print(msg)

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
