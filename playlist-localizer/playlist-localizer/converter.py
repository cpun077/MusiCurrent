from pytube import Playlist, YouTube
from moviepy.editor import AudioFileClip
import os, subprocess, platform

def processlink(url, dir):
    print("Link: ", url, " Dir:", dir)
    if "youtube.com/watch" in url:
        getYTsong(YouTube(url), dir)
    elif "youtube.com/playlist" in url:
        playlist = Playlist(url)
        for video in playlist.videos:
            getYTsong(video, dir)

def getYTsong(video, dir):
    audios = video.streams.filter(only_audio=True).order_by('abr').desc()
    best = audios[0]
    path = best.download(dir)
    print("Downloaded: ", best, " at ", path)

    if (platform.system() == 'Darwin'):
        if (path.endswith(('.webm', '.ogg'))):
            try:
                song = AudioFileClip(path)
                newpath = os.path.splitext(path)[0] + '.m4a'
                song.write_audiofile(newpath, codec='aac')
                os.remove(path)
                song.close()
                path = newpath
                print("File format converted to .m4a")
            except Exception as e:
                print("Conversion error: ", e)
                
        try:
            applescript = (
                'tell application "Music" to add (POSIX file "' + path + '") as alias'
            )
            subprocess.call(['osascript', '-e', applescript])
            print("AppleScript completed; song uploaded")
        except subprocess.CalledProcessError as e:
            print("Upload error: ", e)
    else:
        print("Skipped Apple Music upload; not on MacOS")
        
#playlist = "https://music.youtube.com/playlist?list=PL4ckrlA4uj4tr28D-Dpn5QrrS0wxd2blM&si=Z_8eTkBKgvTQm-U3"
#song = "https://music.youtube.com/watch?v=9B2EQe-fmh8&si=oMh1n90MIjGTEDA2"
#processlink(
#    playlist,
#    os.path.join(os.path.expanduser('~'), 'Downloads/Sounds')
#)
        

