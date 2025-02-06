from pytubefix import Playlist, YouTube
from moviepy import AudioFileClip
import os, subprocess, platform

def processlink(url, dir):
    print("Link: ", url, " Dir:", dir)
    if "youtube.com/watch" in url or "youtu.be/" in url:
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
        filepath = best.download(dir)
        print("Downloaded: ", best)
        
        if (platform.system() == 'Darwin'):
            base, extension = os.path.splitext(filepath)

            # fix extension if pytubefix messes up
            if best.mime_type != "audio/mp4" and (extension == ".mp4" or extension == ".m4a"):
                newext = best.mime_type.split("/")[1]
                fixpath = base + '.' + newext
                os.rename(filepath, fixpath)
                filepath = fixpath
                print('fixed extension:', filepath)   

            # convert to aac format (.m4a) to prep for Apple Music
            if (filepath.endswith(('.webm', '.ogg'))):
                try:
                    song = AudioFileClip(filepath)
                    newpath = base + '.m4a'
                    song.write_audiofile(newpath, codec='aac', ffmpeg_params=["-ac", "2", "-b:a", "256k"])
                    song.close()
                    os.remove(filepath)
                    filepath = newpath
                    print("File format converted to .m4a")
                except Exception as e:
                    print("Conversion error: ", e)

            # automate importation to Apple Music
            try:
                applescript = (
                    'tell application "Music" to add (POSIX file "' + filepath + '") as alias'
                )
                subprocess.call(['osascript', '-e', applescript])
                print("AppleScript completed; song uploaded")
            except subprocess.CalledProcessError as e:
                print("Upload error: ", e)
        else:
            print("Skipped Apple Music upload; not on MacOS")
    except Exception as e:
        print("Download error", e)

# Isolated Script Testing
#        
# playlist = "https://music.youtube.com/playlist?list=PL4ckrlA4uj4tr28D-Dpn5QrrS0wxd2blM&si=Z_8eTkBKgvTQm-U3"
# song = "https://music.youtube.com/watch?v=3hgabcFcp4A&si=I7q2iJy5doH5Mr7Z"
# processlink(
# song,
# os.path.join(os.path.expanduser('~'), 'Downloads')
# )
        

