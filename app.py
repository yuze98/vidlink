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
import sys
from tkinter.font import Font

'''
TODO: terminate the downloading thread when we quit from the loading screen
TODO: make the loading/downloading message box write some of the terminal outputs to keep track of things(DONE)
'''

## COLORS

MAIN_BG = '#FAF1E4'
LABEL = '#FF0000'
TEXT_BOX = '#FFF5E0'
BLACK = '#000000'
WHITE = '#FFFFFF'

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

    loading_label = tk.Label(loading_window, text="Please wait while the video is being processed.\n")
    loading_label.pack(pady=10)

    progress = ttk.Progressbar(loading_window, mode="indeterminate")
    progress.pack(pady=10)
    progress.start()

    message_text = tk.Text(loading_window, height=10,width=40)
    message_text.pack(pady=10)

     # Create a custom stream to redirect stdout to the message_text widget
    class StdoutRedirector:
        def __init__(self, text_widget):
            self.text_widget = text_widget

        def write(self, text):
            self.text_widget.insert(tk.END, text)
            self.text_widget.see(tk.END)
        def flush(self):
            pass  # Define a minimal flush method that does nothing

    # Redirect stdout to the custom stream
    sys.stdout = StdoutRedirector(message_text)

    # Return the loading window so you can close it later
    return loading_window

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.configure(text = folder_path)  # Insert the selected path into the Entry widget

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

# Set the window size (width x height)
app.geometry("400x600")  # Adjust the width and height to your preference
app.configure(bg=MAIN_BG)

# set the current directory as default
current_directory = os.getcwd()
# set familiar font
bold_font = Font(family="Helvetica", size=10, weight="bold")  # Adjust font settings as needed

style = ttk.Style()
style.theme_use("clam")  # Replace "clam" with the name of the desired theme (e.g., "default", "alt", "vista")

# label for the url
url_label = tk.Label(app, text="Enter YouTube URL:", bg=TEXT_BOX, font=bold_font, fg=LABEL)
url_label.pack(pady=(30,0), anchor="n")

# variable to store the url
url_entry = tk.Entry(app,width=50,bg=TEXT_BOX , font=bold_font, fg=BLACK)
url_entry.pack(pady=5)

folder_entry = tk.Label(app,width=50,bg=TEXT_BOX,text=current_directory, borderwidth=0,fg=BLACK)
folder_entry.pack(pady=10)

# default is a single song
format_var = tk.StringVar()
format_var.set('MP3')  # Default format

format_var_type = tk.StringVar()
format_var_type.set('SINGLE')  # Default format

frame = tk.Frame(app)
frame.pack(expand=False,pady=10)
ps_frame = tk.Frame(app)
ps_frame.pack(expand=False,pady=10)

mp4_radio = tk.Radiobutton(frame, text='MP4', variable=format_var,indicatoron=False, value='MP4', width=10, bg= MAIN_BG)
mp4_radio.pack(side='left', padx=5)

mp3_radio = tk.Radiobutton(frame, text='MP3', variable=format_var,indicatoron=False, value='MP3',width=10,bg= MAIN_BG)
mp3_radio.pack(side='left', padx=5)

single_radio = tk.Radiobutton(ps_frame, text='SINGLE', variable=format_var_type,indicatoron=False, value='SINGLE',command=toggle_index,width=10,bg= MAIN_BG)
single_radio.pack(side='right', padx=5)

playlist_radio = tk.Radiobutton(ps_frame, text='PLAYLIST', variable=format_var_type,indicatoron=False, value='PLAYLIST',command=toggle_index,width=10,bg= MAIN_BG)
playlist_radio.pack(side='right', padx=5)



# choose the location of the download video
browse_button = tk.Button(app, text="Browse",
                            command=browse_folder,
                            width=20,
                            height=2,
                            fg='#FF0000',
                            font=bold_font,
                            borderwidth=2,  # Adjust the border width as needed
                            relief="solid",  # Set the relief style to "solid" for a solid border
                            highlightthickness=2)
browse_button.pack(pady=10)



# Function to initiate the download
# "pick a number[---(1)song---|---(2)song_pl---|---(3)video---|---(4)video_pl---]"
def download():
    # handle errors
    video_url = url_entry.get()
    folder_path = folder_entry.cget("text")
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

    # disable the download button
    disable_button()

    # Define a function to run in a separate thread
    def download_it():
        # Show the loading screen
        loading_window = show_loading_screen()

        vidconv(which, video_url, folder_path, index=index)
    
        # Close the loading screen when the task is complete
        loading_window.destroy()
        messagebox.showinfo("Info", "Download Completed :)")
        enable_button()

    # Start a new thread to download the video
    download_thread = threading.Thread(target=download_it)
    download_thread.start()

download_button = tk.Button(app,
                            text="Download",
                            width=20,
                            height=2,
                            command=download,
                            fg='#FF0000',
                            font=bold_font,
                            borderwidth=2,  # Adjust the border width as needed
                            relief="solid",  # Set the relief style to "solid" for a solid border
                            highlightthickness=2)

# download_button.configure(bg='#FF0000')
download_button.pack()

# frame for the index input and lable
in_frame = tk.Frame(app,background=MAIN_BG)
in_frame.pack(expand=False,pady=10)
# label for the url
index_label = tk.Label(in_frame, text="Enter YouTube playlist start INDEX: ",width=50,bg=TEXT_BOX, borderwidth=0,fg=BLACK)
index_label.pack(pady=10)

# variable to store the index of the playlist
index_entry = tk.Entry(in_frame,width=5,bg=TEXT_BOX , font=bold_font, fg=BLACK)
index_entry.insert(0, '1')
index_entry.pack(pady=(10,10))
# default index view
toggle_index()
# Register the on_exit function to run when the application is closed

atexit.register(on_exit)
app.protocol("WM_DELETE_WINDOW", on_exit)  # Handle window close button click

app.mainloop()