'''
project [VIDLINK]

choose from downloading:
    - song
    - video
    - song playlist
    - video playlist

then provide a youtube video link to download it locally on your computer.
'''

import tkinter as tk
from utils.utils import vidconv
from tkinter import ttk
import threading  # Import the threading module for running tasks in the background
from tkinter import filedialog
from tkinter import messagebox
import os
import atexit

'''
TODO: terminate the downloading thread when we quit from the loading screen
TODO: make the loading/downloading message box write some of the terminal outputs to keep track of things
'''


## helper function

def on_exit():
    # Add code here to terminate or clean up any background processes
    app.quit()

def err_handler(entry,err_code=0):
    if not entry:
        if(err_code == 1 ):
            messagebox.showerror("Error", "Please enter the folder path.")
        elif(err_code == 2):
            messagebox.showerror("Error", "Please enter the YouTube URL.")
        else:
            messagebox.showerror("Error", "Default Error")
        return True
    return False

def show_loading_screen():
    loading_window = tk.Toplevel(app)
    loading_window.title("Downloading...")

    loading_label = tk.Label(loading_window, text="Please wait while the video is being processed.")
    loading_label.pack(pady=10)

    progress = ttk.Progressbar(loading_window, mode="indeterminate")
    progress.pack(pady=10)
    progress.start()

    # Return the loading window so you can close it later
    return loading_window

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, tk.END)  # Clear the current entry
        folder_entry.insert(0, folder_path)  # Insert the selected path into the Entry widget

def toggle_index():
    if format_var_type.get() == 'PLAYLIST':
        index_entry.pack()
        index_label.pack()
    else:
        index_entry.pack_forget()  # Use pack_forget() to hide the widget
        index_label.pack_forget()

def disable_button():
    download_button.config(state='disabled')

def enable_button():
    download_button.config(state='normal')

## main app ui
app = tk.Tk()
app.title("vidlink")

# label for the url
url_label = tk.Label(app, text="Enter YouTube URL:")
url_label.pack()

# variable to store the url
url_entry = tk.Entry(app)
url_entry.pack()

# default is a single song
format_var = tk.StringVar()
format_var.set('MP3')  # Default format

format_var_type = tk.StringVar()
format_var_type.set('SINGLE')  # Default format

mp4_radio = tk.Radiobutton(app, text='MP4', variable=format_var, value='MP4')
mp4_radio.pack()

mp3_radio = tk.Radiobutton(app, text='MP3', variable=format_var, value='MP3')
mp3_radio.pack()

single_radio = tk.Radiobutton(app, text='SINGLE', variable=format_var_type, value='SINGLE',command=toggle_index)
single_radio.pack()

playlist_radio = tk.Radiobutton(app, text='PLAYLIST', variable=format_var_type, value='PLAYLIST',command=toggle_index)
playlist_radio.pack()

# label for the url
index_label = tk.Label(app, text="Enter YouTube playlist start INDEX: ")
index_label.pack()

# variable to store the url
index_entry = tk.Entry(app)
index_entry.insert(0, '1')
index_entry.pack()

# default index view
toggle_index()

# set the current directory as default
current_directory = os.getcwd()

# choose the location of the download video
browse_button = tk.Button(app, text="Browse", command=browse_folder)
browse_button.pack()

folder_entry = tk.Entry(app)
folder_entry.insert(0, current_directory)
folder_entry.pack()

# Function to initiate the download
# "pick a number[---(1)song---|---(2)song_pl---|---(3)video---|---(4)video_pl---]"
def download():
    # handle errors
    video_url = url_entry.get()
    folder_path = folder_entry.get()
    index = index_entry.get()

    # returns True if there is an actual error
    if(err_handler(folder_path,1) or err_handler(video_url,2)):
        return
    
 # Determine the value of 'which' based on user's choices
    if format_var.get() == 'MP3':
        if format_var_type.get() == 'SINGLE':
            which = '1'
        else:
            which = '2'
    else:
        if format_var_type.get() == 'SINGLE':
            which = '3'
        else:
            which = '4'

    # Show the loading screen
    loading_window = show_loading_screen()
    # disable the download button
    disable_button()

    # Define a function to run in a separate thread
    def download_it():
        vidconv(which, video_url,folder_path,index=index)
        # Close the loading screen when the task is complete
        loading_window.destroy()
        messagebox.showinfo("Info", "Download Completed :)")
        enable_button()

    # Start a new thread to download the video
    download_thread = threading.Thread(target=download_it)
    download_thread.start()

download_button = tk.Button(app, text="Download", command=download)
download_button.pack()


# Register the on_exit function to run when the application is closed

atexit.register(on_exit)
app.protocol("WM_DELETE_WINDOW", on_exit)  # Handle window close button click

app.mainloop()