# vidlink

This mini project is developed to download youtube videos locally as an audio mp3 or mp4 format.
Also provides the option to download a playlist in one of the two formats.

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

### to produce an exe file run the following command
    
win        pyinstaller --onefile --noconsole --icon assets/favicon.ico --add-data "assets;assets" --add-data "utils;utils" app.py --name vidlink
unix       pyinstaller --onefile --noconsole --icon assets/favicon.ico --add-data "assets:assets" --add-data "utils:utils" app.py --name vidlink   