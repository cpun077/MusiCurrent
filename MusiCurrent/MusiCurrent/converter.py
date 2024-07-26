from pytube import Playlist, YouTube
from moviepy.editor import AudioFileClip
import os, subprocess, platform
# temporary fix to get_throttling_function_name error
from pytube import cipher
import re

def get_throttling_function_name(js: str) -> str:
    """Extract the name of the function that computes the throttling parameter.

    :param str js:
        The contents of the base.js asset file.
    :rtype: str
    :returns:
        The name of the function used to compute the throttling parameter.
    """
    function_patterns = [
        # https://github.com/ytdl-org/youtube-dl/issues/29326#issuecomment-865985377
        # https://github.com/yt-dlp/yt-dlp/commit/48416bc4a8f1d5ff07d5977659cb8ece7640dcd8
        # var Bpa = [iha];
        # ...
        # a.C && (b = a.get("n")) && (b = Bpa[0](b), a.set("n", b),
        # Bpa.length || iha("")) }};
        # In the above case, `iha` is the relevant function name
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
    #logger.debug('Finding throttling function name')
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            #logger.debug("finished regex search, matched: %s", pattern)
            if len(function_match.groups()) == 1:
                return function_match.group(1)
            idx = function_match.group(2)
            if idx:
                idx = idx.strip("[]")
                array = re.search(
                    r'var {nfunc}\s*=\s*(\[.+?\]);'.format(
                        nfunc=re.escape(function_match.group(1))),
                    js
                )
                if array:
                    array = array.group(1).strip("[]").split(",")
                    array = [x.strip() for x in array]
                    return array[int(idx)]

    raise RegexMatchError(
        caller="get_throttling_function_name", pattern="multiple"
    )

cipher.get_throttling_function_name = get_throttling_function_name

def processlink(url, dir):
    print("Link: ", url, " Dir:", dir)
    if "youtube.com/watch" in url or "youtu.be/" or "music.youtube.com/watch" in url:
        getYTsong(YouTube(url), dir)
    elif "youtube.com/playlist" or "music.youtube.com/playlist" in url:
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

            try:
                applescript = (
                    'tell application "Music" to add (POSIX file "' + filepath.decode("UTF-8") + '") as alias'
                )
                subprocess.call(['osascript', '-e', applescript])
                print("AppleScript completed; song uploaded")
            except subprocess.CalledProcessError as e:
                print("Upload error: ", e)
        else:
            print("Skipped Apple Music upload; not on MacOS")
    except Exception as e:
        print("Download error", e)
        
#playlist = "https://music.youtube.com/playlist?list=PL4ckrlA4uj4tr28D-Dpn5QrrS0wxd2blM&si=Z_8eTkBKgvTQm-U3"
#song = "https://music.youtube.com/watch?v=9B2EQe-fmh8&si=oMh1n90MIjGTEDA2"
#processlink(
#    playlist,
#    os.path.join(os.path.expanduser('~'), 'Downloads/Sounds')
#)
        

