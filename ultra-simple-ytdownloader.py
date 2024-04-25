import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pytube import YouTube
from ttkthemes import ThemedStyle
from pathlib import Path
import threading

def choose_save_path():
    save_path = filedialog.askdirectory()
    save_path_entry.delete(0, tk.END)
    save_path_entry.insert(0, save_path)
    
def download_video():
    url = url_entry.get()
    save_path = save_path_entry.get()
    
    if not url:
        show_invalid_url_error()
        return

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    download_thread = threading.Thread(target=download_video_thread, args=(url, save_path))
    download_thread.start()
    toggle_buttons_state(True)

def download_video_thread(url, save_path):
    progress_bar['value'] = 0
    try:
        yt_video = YouTube(url, on_progress_callback=on_progress)
        video = yt_video.streams.filter(progressive=True, file_extension='mp4').first()
        video.download(save_path)
        messagebox.showinfo("Success", "Download completed.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while downloading: {e}")
    finally:
        toggle_buttons_state(False)

def download_audio():
    url = url_entry.get()
    save_path = save_path_entry.get()
    
    if not url:
        show_invalid_url_error()
        return

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    download_thread = threading.Thread(target=download_audio_thread, args=(url, save_path))
    download_thread.start()
    toggle_buttons_state(True)

def download_audio_thread(url, save_path):
    progress_bar['value'] = 0
    try:
        yt_audio = YouTube(url, on_progress_callback=on_progress)
        audio = yt_audio.streams.filter(only_audio=True, file_extension='mp4').first()
        audio.download(save_path)
        messagebox.showinfo("Success", "Download completed.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while downloading: {e}")
    finally:
        toggle_buttons_state(False)

def toggle_buttons_state(disable):
    state = "disabled" if disable else "normal"
    download_button_video.config(state=state)
    download_button_audio.config(state=state)
    choose_path_button.config(state=state)
    if disable:
        progress_bar.grid(row=3, column=0, columnspan=3, pady=5)
    else:
        progress_bar.grid_forget()

def on_progress(stream, chunk, bytes_remaining):
    percent = round((1 - bytes_remaining / stream.filesize) * 100)
    progress_bar['value'] = percent

def show_invalid_url_error():
    messagebox.showerror("Error", "Enter a valid URL.")

root = tk.Tk()
root.title("ultra-simple-ytdownloader")
root.resizable(False, False)
root.configure(bg="#212121")

style = ThemedStyle(root)
style.theme_use('arc')
style.configure("TLabel",
                background="#212121",
                foreground="#dedede",
                )
style.configure("TButton",
                background="#212121",
                foreground="#212121",
                )

url_label = ttk.Label(root, text="URL:")
url_label.grid(row=0, column=0, padx=(15, 0), pady=15)
url_entry = ttk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=15, pady=15)

save_path_label = ttk.Label(root, text="Download path:")
save_path_label.grid(row=1, column=0, padx=(15, 0), pady=15)
save_path_entry = ttk.Entry(root, width=50)
save_path_entry.grid(row=1, column=1, padx=15, pady=15)

desktop_path = str(Path.home() / "Desktop")
save_path_entry.insert(0, desktop_path)

choose_path_button = ttk.Button(root, text="Choose...", command=choose_save_path, width=10, takefocus=False)
choose_path_button.grid(row=1, column=2, padx=5, pady=5)

download_button_video = ttk.Button(root, text="Download video", command=download_video, takefocus=False)
download_button_video.grid(row=2, column=0, columnspan=2, pady=15, padx=(0, 50))

download_button_audio = ttk.Button(root, text="Download audio", command=download_audio, takefocus=False)
download_button_audio.grid(row=2, column=1, columnspan=2, pady=15, padx=(50, 0))

progress_bar = ttk.Progressbar(root, mode='determinate', length=300)

root.mainloop()
