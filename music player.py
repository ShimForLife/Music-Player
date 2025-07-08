import pygame
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd

root = tk.Tk()
root.title("My Player")
root.geometry("400x245")

class Song:
    def __init__(self, title, path):
        self.title = title
        self.path = path
        self.next = None
        self.prev = None

class MyPlayList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.isPlaying = False
        self.isPaused = False

    def append(self, title, path):
        newSong = Song(title, path)
        if self.head:
            newSong.prev = self.tail
            newSong.next = self.head
            self.tail.next = newSong
            self.head.prev = newSong
            self.tail = newSong
        else:
            self.head = newSong
            self.tail = newSong
            self.head.next = self.head
            self.head.prev = self.head
            self.current = self.tail
        self.current = self.head

    def playButton(self):
        if not self.isPlaying and not self.isPaused:
            self.isPlaying = True
            pygame.mixer.music.load(self.current.path)
            pygame.mixer.music.play()
            self.updateSongLabel()
        elif not self.isPlaying and self.isPaused:
            self.isPlaying = True
            self.isPaused = False
            pygame.mixer.music.load(self.current.path)
            pygame.mixer.music.play()
            self.updateSongLabel()
        elif self.isPlaying and not self.isPaused:
            self.isPaused = True
            pygame.mixer.music.pause()
        elif self.isPlaying and self.isPaused:
            self.isPaused = False
            pygame.mixer.music.unpause()

    def nextButton(self):
        self.isPlaying = False
        self.current = self.current.next
        self.playButton()

    def prevButton(self):
        self.isPlaying = False
        self.current = self.current.prev
        self.playButton() 

    def checkMusicEnd(self):
        if self.isPlaying and not self.isPaused and not pygame.mixer.music.get_busy():
            self.nextButton()
        root.after(500, self.checkMusicEnd)

    def addButton(self):
        filePath = fd.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if filePath:
            titleToTheSong = filePath.split("/")[-1]
            playlist.append(titleToTheSong, filePath)
            songListbox.insert(tk.END, titleToTheSong)

    def updateSongLabel(self):
        display.config(text=f"Now Playing: {self.current.title}")


pygame.mixer.init()
playlist = MyPlayList()

display = ttk.Label(root, text="Now Playing: ", font=("Arial", 14))
display.pack(pady=10)

buttonFrame = tk.Frame(root)
buttonFrame.pack(pady=10)

prevButton = ttk.Button(buttonFrame, text="Previous", command=playlist.prevButton)
prevButton.pack(side=tk.LEFT, padx=5)

playButton = ttk.Button(buttonFrame, text="Play", command=playlist.playButton)
playButton.pack(side=tk.LEFT, padx=5)

nextButton = ttk.Button(buttonFrame, text="Next", command=playlist.nextButton)
nextButton.pack(side=tk.LEFT, padx=5)

listFrame = tk.Frame(root)
listFrame.pack(pady=10, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(listFrame, orient=tk.VERTICAL)
songListbox = tk.Listbox(listFrame, height=5, font=("Arial", 12), yscrollcommand=scrollbar.set)
scrollbar.config(command=songListbox.yview)

songListbox.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

addButton = ttk.Button(listFrame, text="Add Song", command=playlist.addButton, width=10)
addButton.grid(row=0, column=2, sticky="n", padx=10, pady=10)

listFrame.grid_rowconfigure(0, weight=1)
listFrame.grid_columnconfigure(0, weight=1)
listFrame.grid_columnconfigure(1, weight=0)
listFrame.grid_columnconfigure(2, weight=0)

root.after(500, playlist.checkMusicEnd)
root.mainloop()
