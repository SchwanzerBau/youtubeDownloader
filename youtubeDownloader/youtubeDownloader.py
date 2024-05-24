import os
from pathlib import Path
from pytube import YouTube
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar
import threading
import logging

# Logging konfigurieren
logging.basicConfig(filename='youtubeDownloadLog.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def Download(url, path):
    yt = YouTube(url)
    yt = yt.streams.get_highest_resolution()
    try:
        if path != str(Path.home()):
            yt.download(path)
        else:
            path = os.path.join(Path.home(), 'Downloads')
            yt.download(path)
        messagebox.showinfo("Erfolg", "Download Fertiggestellt")
        e1.delete(0, tk.END)
        e2.delete(0, tk.END)
        logging.info('Download erfolgreich abgeschlossen.')
    except Exception as e:
        messagebox.showerror("Fehler", f"Download Fehlgeschlagen: {e}")
        logging.error(f'Download fehlgeschlagen: {e}')
    finally:
        progress.stop()
        progress.grid_forget()


def startDownloadThread(url, path):
    threading.Thread(target=Download, args=(url, path)).start()




def downloadVideo():
    link = e1.get()
    desiredPath = e2.get().strip()
    if not desiredPath:
        path = str(Path.home())
    else:
        desiredPath = desiredPath.replace('Dokumente', 'Documents').replace('dokumente', 'Documents').replace(
            'documents', 'Documents')
        path = os.path.join(Path.home(), desiredPath)

    progress.grid(row=2, columnspan=2, padx=10, pady=5)
    progress.start()
    startDownloadThread(link, path)



master = tk.Tk()
master.title("YouTube Video Downloader")

tk.Label(master, text="YouTube Link").grid(row=0)
tk.Label(master, text="Speicherort (Leerlassen Falls nicht spezifiziert)").grid(row=1)

e1 = tk.Entry(master, width=50)
e2 = tk.Entry(master, width=50)

e1.grid(row=0, column=1, padx=10, pady=5)
e2.grid(row=1, column=1, padx=10, pady=5)

progress = Progressbar(master, orient=tk.HORIZONTAL, length=300, mode='indeterminate')

tk.Button(master, text='Beenden', command=master.quit).grid(row=3, column=0, sticky=tk.W, pady=4)
tk.Button(master, text='Herunterladen', command=downloadVideo).grid(row=3, column=1, sticky=tk.W, pady=4)

master.mainloop()
