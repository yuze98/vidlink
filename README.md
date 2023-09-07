# vidlink
<img src="assets/android-chrome-512x512.png" alt="vidlink" width="200"/>

This mini project is developed to download youtube videos locally as an audio mp3 or mp4 format.
Also provides the option to download a playlist in one of the two formats.
utils for vidlink is a script that downloads and converts youtube videos in to mp4 or mp3.
There's also the choice for choosing one single video/song or a playlist to download.
All script functions in this directory are used in the App vidlink for converting and downloading 
youtube videos to mp3 or mp4 files/ or for downloads playlists.

credits:[Youssef Hatem, yhmourad98@gmail.com]


## Use cases

    - Listen to music without internet by downloading it on their computer.
    - studying via downloading the needed courses available on youtube for free.
    - you could make a custom playlist on youtube and set it to public and then download it.

## requirements

`you'd need to install these python packages first`

- pytube
- os
- yt_dlp
- tkinter

## lib used
the script will take a youtube video url, downloads it and converts it to mp3 or mp4 files

    * pip install youtube_dl
    * pip install pytube
    * pip install yt_dlp 
        * yt_dlp is forked from youtube_dl with added features and more updated features

### To produce an exe file run the following command
        pyinstaller --onefile --noconsole --icon assets/favicon.ico --add-data "assets;assets" --add-data "utils;utils" app.py
        
### NOTE
   make sure to download the [ffmpeg-git-full.7z master builds](https://www.gyan.dev/ffmpeg/builds/)
   and add it inside the utils folder



    
