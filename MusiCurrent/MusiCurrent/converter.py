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
            
    print("Completed Task.")

def getYTsong(video, dir):
    try:
        print("Thumbnail: ", video.thumbnail_url)
        print("Metadata: ", video.metadata)
        audios = video.streams.filter(only_audio=True).order_by('abr').desc()
        best = audios[0]
        filepath = best.download(dir).encode("UTF-8")
        print("Downloaded: ", best)
    except Exception as e:
        print("Download error", e)

    if (platform.system() == 'Darwin'):
        filepath = filepath.decode("UTF-8")
        base, extension = os.path.splitext(filepath)
        if (extension.endswith(('.webm', '.ogg'))):
            try:
                song = AudioFileClip(filepath)
                newpath = (base + '.m4a').encode("UTF-8")
                song.write_audiofile(newpath, codec='aac')
                os.remove(filepath)
                song.close()
                filepath = newpath
                print("File format converted to .m4a")
            except Exception as e:
                print("Conversion error: ", e)

#        try:
#            applescript = (
#                'tell application "Music" to add (POSIX file "' + filepath.decode("UTF-8") + '") as alias'
#            )
#            subprocess.call(['osascript', '-e', applescript])
#            print("AppleScript completed; song uploaded")
#        except subprocess.CalledProcessError as e:
#            print("Upload error: ", e)
    else:
        print("Skipped Apple Music upload; not on MacOS")
        
#playlist = "https://music.youtube.com/playlist?list=PL4ckrlA4uj4tr28D-Dpn5QrrS0wxd2blM&si=Z_8eTkBKgvTQm-U3"
#song = "https://music.youtube.com/watch?v=9B2EQe-fmh8&si=oMh1n90MIjGTEDA2"
#processlink(
#    playlist,
#    os.path.join(os.path.expanduser('~'), 'Downloads/Sounds')
#)
        

