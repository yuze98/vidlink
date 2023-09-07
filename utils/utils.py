'''
These script is taken from/// https://www.codespeedy.com/download-youtube-video-as-mp3-using-python/#:~:text=%E2%80%9Cpytube%E2%80%9D%20is%20a%20library%20written,to%20install%20the%20pytube%20library.
and tweaked over

All scripts in this directory are used in the App vidlink for converting and downloading 
youtube videos to mp3 or mp4 files/ or for downloads playlists

credits:[Youssef Hatem, yhmourad98@gmail.com]
the script will take a youtube video url, downloads it and converts it to mp3 or mp4 files
    pip install youtube_dl 
    pip install pytube
    pip install yt_dlp 
        ** yt_dlp is forked from youtube_dl with added features and more updated features **
        ** make sure to download the ffmpeg-git-full.7z master builds from https://www.gyan.dev/ffmpeg/builds/ **

'''

from pytube import Playlist
import os
import yt_dlp as ydl
from os.path import exists


''' desc:
    this function takes a youtube playlist, extracts all the urls and converts it to mp3
    saving it in a file of the playlist's name
    The _video_regex attribute is a way for the pytube library to specify the regex pattern used to find video URLs in the playlist source code.
    It's important to note that website structures can change over time, so this regex might need to be updated if YouTube's HTML structure changes.
'''
# types of conversion

def download_ytvid(video_url, out_folder='_out/', choice='1'):
    
    script_directory = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_folder = os.path.join(script_directory, 'ffmpeg/bin')

    # if its a song then set the config for it else its a video
    if(choice == '1' or choice == '2'):
        ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': out_folder+'%(title)s.%(ext)s',
    'ffmpeg_location': ffmpeg_folder  # Replace with actual path to ffmpeg
    }
    else:
        ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': out_folder+'%(title)s.%(ext)s',
        'ffmpeg_location': ffmpeg_folder  # Replace with actual path to ffmpeg
        }
    
    
        
    with ydl.YoutubeDL(ydl_opts) as ydl_instance:
        try:
            song_title = ydl_instance.extract_info(video_url,False)
        except Exception as e:
            print(e)
        # if its a song check if it already exists if not a song then check for the video
        if(choice == '1' or choice == '2'):
            if(exists(out_folder+song_title['title']+'.mp3')):
                print('el oghneya dih mawgooda yasta')
                return
        else:
            if(exists(out_folder+song_title['title']+'.mp4')):
                print('el video dih mawgooda yasta')
                return
        ydl_instance.download([video_url])
    print("Download complete...")

# extract video urls from a playlist 
def extract_urls(playlist_url):
    playlist = Playlist(playlist_url)
    playlist._video_regex = r"\"url\":\"(/watch\?v=[\w-]*)"
    return playlist


# main function to get called from app.py
def vidconv(which, url, directory,index='1'):
    print(directory)
    # option picker
    # which = input("pick a number[---(1)song---|---(2)song_pl---|---(3)video---|---(4)video_pl---]")
    if(which == '1' or which == '3'):
        # Do song/video fn        
        download_ytvid(video_url=url,out_folder= directory+'/_out/',choice=which )
    else:
        # Do song/video playlist fn
        # get the url of the playlist
        url_list = extract_urls(url)
        # loop over all the videos in the playlist and 
        for i, url in enumerate(url_list): 
            if(i >= (int(index)-1) and int(index) <= len(url_list)):
                try:
                    print('Downloaing... ',(i+1),'/',len(url_list))
                    download_ytvid(url,directory+'/'+url_list.title+'/',which)
                except Exception as e:
                    print(f"An error occurred while processing URL {url}: {e}")
