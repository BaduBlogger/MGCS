from tkinter import *
import tkinter as tk
import os
from pathlib import Path
from tkinter import filedialog	# import filedialog module
import subprocess
from PIL import Image, ImageTk
from tkinter import ttk  
import pickle
from tkinter import PhotoImage
from tkinter.messagebox import *
import pygame
from pygame import mixer
from itertools import count, cycle
import time
from music_model import run_model
from mp3towav import mp3_to_wav

cwd = os.getcwd()
path_dest = ""
res = ""
greet = "Bravooo!! Done"

def ChangeLabelText(path):
    #print("inside function")
    head_tail = os.path.split(path)
    #print("Tail of '% s:'" % path, head_tail[1], "\n")
    label.config(text = "File : "+head_tail[1])

def ChangeFolderText(path_dest):
    label_folder.config(text = path_dest)

def browseFiles():
    # Function for opening the file explorer window
    path = ""
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select any MP3 Song",
                                          filetypes=(("Audio Files", ".mp3 .wav"),("All Files", "*.*")))
    path = Path(filename)
    ChangeLabelText(path)
    bar()
    flag,prediction = run_model(song_path = str(path), path_dest = str(path_dest))
    if(flag):
        conversion_done = Label(home,text = "{} : {}".format(greet,prediction), fg = "white",bg = "#202121", font = "Times 12").place(x=950,y=470)
    else:
        conversion_done = Label(home,text = "Classification & Segragation Not Done", fg = "white",bg = "#202121", font = "Times 12").place(x=950,y=470)
	
def browseDestFolder():
    foldername = filedialog.askdirectory()
    #print(foldername)
    global path_dest 
    path_dest = Path(foldername)
    #print(path_dest)
    ChangeFolderText(path_dest)

window = Tk()					# Create the root window
window.title("MGC")				# Set window title
window.geometry("1365x800")		# Set window size
window.config(background = "#202121")	#Set window background color

tabControl = ttk.Notebook(window,width=500, height=500)		#tabs
tabControl.pack()
home = Frame(tabControl,bg = "#202121")
explore = Frame(tabControl,bg = "#202121")
about = Frame(tabControl,bg = "#202121")
tabControl.add(home, text ='Home')
tabControl.add(explore, text ='Explore')
tabControl.add(about, text ='About')
tabControl.pack(expand = 1, fill ="both",side = "left")

#-------------------Home Page Start-------------------------------------------------

progress = ttk.Progressbar(home, orient = HORIZONTAL,length = 200, mode = 'determinate')    #progress bar
def bar():
    progress.place(x=920,y=430)
    progress['value'] = 20
    home.update_idletasks()
    time.sleep(1)
  
    progress['value'] = 40
    home.update_idletasks()
    time.sleep(1)
  
    progress['value'] = 50
    home.update_idletasks()
    time.sleep(1)
  
    progress['value'] = 60
    home.update_idletasks()
    time.sleep(1)
  
    progress['value'] = 80
    home.update_idletasks()
    time.sleep(1)
    progress['value'] = 100

#Add title
Heading = Label(home,text = "Music Genre Classification & Segragation Using CNN", fg = "#66FCF1",bg = "#202121", font = "Times 22").place(relx = 0.5, rely = 0.08,anchor = CENTER)

images = ["images/no_music.jpg","images/no_music_1.jpg","images/no_music_2.jpg","images/no_music_3.png"]	#Image Slideshow
photos = cycle(ImageTk.PhotoImage(Image.open(image)) for image in images)

def slideShow():
  img = next(photos)
  displayCanvas.config(image=img,width=600,height=400,bg = "#202121")
  window.after(1000, slideShow) # 0.05 seconds


width = home.winfo_screenwidth()
height = home.winfo_screenwidth()

displayCanvas = tk.Label(home)
displayCanvas.pack()
window.after(10, lambda: slideShow())
displayCanvas.place(x=100,y=200)
  
# Create button and image
photoDest = PhotoImage(file = r"images/selectD.png")
photoUpload = PhotoImage(file = r"images/uploadS.png")

# create buttons     
button_destination = tk.Button(home,
                        image=photoDest,
                        command = browseDestFolder ,highlightthickness = 0, bd = 0) 
 

button_upload = tk.Button(home,
                        image=photoUpload,
                        command = browseFiles, highlightthickness = 0, bd = 0) 

label = ttk.Label(home, text="          No file found",background="#202121",foreground="white")
label.config(anchor=CENTER)
label.place(x=950,y=390)
	
label_folder = ttk.Label(home, text="          No file found",background="#202121",foreground="white")
label_folder.config(anchor=CENTER)
label_folder.place(x=950,y=290)	
										
button_destination.place(x = 950, y = 230)
button_upload.place(x = 950, y = 330)

#-------------------------------Explore Tab-------------------------------------------------------
class Player(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.config(background = "#202121")
        self.pack()
        mixer.init()

        self.statusMsg = tk.StringVar()

        if os.path.exists('songs.pickle'):
            with open('songs.pickle', 'rb') as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist=[]

        self.current = 0
        self.paused = True
        self.played = False

        self.create_frames()
        self.track_widgets()
        self.control_widgets()
        self.tracklist_widgets()

        self.statusBar = tk.Label(self, textvar=self.statusMsg, relief=tk.SUNKEN, anchor="w")
        self.statusBar.config()
        #self.statusBar.grid(row=3, column=0)

    def create_frames(self):
        self.track = tk.LabelFrame(self, text='Song Track',	font=("times new roman",15,"bold"),bg="#202121",fg="white",bd=0,relief=tk.GROOVE)
        self.track.config(width=400,height=300)     
        self.track.grid(row=0, column=0,padx=10,pady=10)      

        self.tracklist = tk.LabelFrame(self,text=f'PlayList - {str(len(self.playlist))}',font=("times new roman",15,"bold"),bg="#202121",fg="white",bd=2,relief=tk.GROOVE)
        self.tracklist.config(width=400,height=550)
        self.tracklist.grid(row=0, column=1)        

        self.controls = tk.LabelFrame(self,font=("times new roman",15,"bold"),bg="#202121",fg="white",bd=0,relief=tk.GROOVE)
        self.controls.config(width=410,height=80)
        self.controls.grid(row=2, column=0, pady=5, padx=10)
	
    def track_widgets(self):
        self.canvas = tk.Label(self.track, image=img, bg="#202121")
        self.canvas.configure(width=900, height=550)
        self.canvas.grid(row=0,column=0)
		
        self.songtrack = tk.Label(self.track, font=("times new roman",16,"bold"),bg="#202121",fg="white")
        self.songtrack['text'] = 'MP3 Player'
        self.songtrack.config(width=30, height=1)
        #self.songtrack.grid(row=1,column=0,padx=10)

    def control_widgets(self):
        self.loadSongs = tk.Button(self.controls, bg='#008B8B', fg='white', font=10)
        self.loadSongs['text'] = 'Load Songs'
        self.loadSongs['command'] = self.retrieve_songs
        self.loadSongs.grid(row=0, column=0, padx=10)

        self.prev = tk.Button(self.controls, image=prev, bg='#008B8B',highlightthickness = 0, bd = 0)
        self.prev['command'] = self.prev_song
        self.prev.grid(row=0, column=1)

        self.pause = tk.Button(self.controls, image=pause, bg='#008B8B',highlightthickness = 0, bd = 0)
        self.pause['command'] = self.pause_song
        self.pause.grid(row=0, column=2)

        self.next = tk.Button(self.controls, image=next_,highlightthickness = 0, bd = 0, bg='#008B8B')
        self.next['command'] = self.next_song
        self.next.grid(row=0, column=3)

        self.volume = tk.DoubleVar(self)
        self.slider = tk.Scale(self.controls, from_ = 0, to = 10, orient = tk.HORIZONTAL,bg="#202121",fg="white",bd=0,highlightthickness = 0)
        self.slider['variable'] = self.volume
        self.slider.set(8)
        mixer.music.set_volume(0.8)
        self.slider['command'] = self.change_volume
        self.slider.grid(row=0, column=4, padx=5)

    def tracklist_widgets(self):
        self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0,column=1, rowspan=5, sticky='ns')

        self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE,
                        yscrollcommand=self.scrollbar.set, selectbackground='#008b8b')
        self.enumerate_songs()
        self.list.config(height=22)
        self.list.bind('<Double-1>', self.play_song)

        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)

    # def retrieve_songs(self):
      #  self.songlist = []
      #  directory = filedialog.askdirectory()
      #  for root_, dirs, files in os.walk(directory):
      #          for file in files:
      #              if os.path.splitext(file)[1] == '.mp3':
      #                  path = (root_ + '/' + file).replace('\\','/')
      #                  self.songlist.append(path)

       # with open('songs.pickle', 'wb') as f:
       #     pickle.dump(self.songlist, f)
       # self.playlist = self.songlist
       # self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'
       # self.list.delete(0, tk.END)
       # self.enumerate_songs()

        # self.setStatusMessage(Message="Songs Retrieved")
        # print(self.getStatusMessage())

    def mp3_to_ogg(self,file,root_):
        path = ''
        if os.path.splitext(file)[1] == '.mp3':
            filename = os.path.splitext(file)[0]
            # os.system("ffmpeg -i '{}.mp3' '{}.ogg'".format(filename,filename))   
            cmd = "ffmpeg -i '{}.mp3' '{}.ogg'".format(filename,filename)
            s = subprocess.check_call(cmd, shell = True)   
            if s:
                path = (root_ + '/' + filename+'.ogg').replace('\\','/')
                print(path)
        else:
            path = (root_ + '/' + file).replace('\\','/')
        return path

    def retrieve_songs(self):
        windows,linux=0,1 # for linux
        self.songlist = []
        SongSet = set()
        directory = filedialog.askdirectory()
        for root_, dirs, files in os.walk(directory):
                for file in files:
                    if linux:
                        if os.path.splitext(file)[1] == '.mp3':
                            wav_file = mp3_to_wav((root_+"/"+file).replace('\\','/'))
                            if wav_file not in SongSet:
                                SongSet.add(wav_file)
                                self.songlist.append(wav_file)
                        elif os.path.splitext(file)[1] == '.wav':
                            wav_file = (root_ + '/' + file).replace('\\','/')
                            if wav_file not in SongSet:
                                SongSet.add(wav_file)
                                self.songlist.append(wav_file)
                    elif windows and os.path.splitext(file)[1] == '.mp3':
                        path = (root_ + '/' + file).replace('\\','/')
                        if wav_file not in SongSet:
                            SongSet.add(wav_file)
                            self.songlist.append(path)
        print(self.songlist)
        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.songlist, f)
        self.playlist = self.songlist
        self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'
        self.list.delete(0, tk.END)
        self.enumerate_songs()

        self.setStatusMessage(Message="Songs Retrieved")
        print(self.getStatusMessage())

    def enumerate_songs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))

    def play_song(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg="white")

        mixer.music.load(self.playlist[self.current])
        self.songtrack['anchor'] = 'w'
        self.songtrack['text'] = os.path.basename(self.playlist[self.current])

        self.pause['image'] = play
        self.paused = False
        self.played = True
        self.list.activate(self.current)
        self.list.itemconfigure(self.current, bg='#008b8b')

        mixer.music.play()

        self.setStatusMessage(Message="Play Song")
        print(self.getStatusMessage())

    def pause_song(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause['image'] = pause

            self.setStatusMessage(Message="Paused Song")
            print(self.getStatusMessage())
        else:
            if self.played == False:
                self.play_song()
            self.paused = False
            mixer.music.unpause()
            self.pause['image'] = play

            self.setStatusMessage(Message="Resumed Song")
            print(self.getStatusMessage())

    def prev_song(self):
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current + 1, bg='#008b8b')
        self.play_song()

    def next_song(self):
        if self.current < len(self.playlist) - 1:
            self.current += 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current - 1, bg='#008b8b')
        self.play_song()

    def change_volume(self, event=None):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v / 10)

    def setStatusMessage(self,Message="Not Ready"):
        self.statusMsg.set(Message)

    def getStatusMessage(self):
        return self.statusMsg.get()

def aboutGUI():
	showinfo("About App","MP3 Player from tkinter")


def exitGUI():
	print("Exit Application")
	window.destroy()
# ----------------------------- Main -------------------------------------------
img = None
next_ = None
prev = None
play = None
pause = None
print(os.getcwd())
cwd = os.getcwd()
#--------------------------------------------------------------------------------------------
img = PhotoImage(file=cwd+'/images/music_1.gif')
next_ = PhotoImage(file=cwd+'/images/nextSongbtn.png')
prev = PhotoImage(file=cwd+'/images/prevSongbtn.png')
play = PhotoImage(file=cwd+'/images/pauseBtn1.png')
pause = PhotoImage(file=cwd+'/images/playBtn.png')

App = Player(master=explore)
App.setStatusMessage(Message="Ready")
print(App.getStatusMessage())

#----------------------------------------About Page-------------------------------------------

eb=Image.open(cwd+'/images/exit.gif')
exit_image = eb.resize((40,40),Image.ANTIALIAS)
exit_photoimage=ImageTk.PhotoImage(exit_image)
ExitButton = tk.Button(about, text ="Exit",image = exit_photoimage, compound = TOP, bg ="#202121", fg="white", bd = 0, command = window.destroy)
ExitButton.place(relx = 0.99,rely = 0.01, x =-2, y = 2, anchor = NE)

Heading = Label(about,text = "Music Genre Classification & Segragation Using CNN", fg = "#66FCF1",bg = "#202121", font = "Times 22").place(relx = 0.5, rely = 0.08,anchor = CENTER)
guide_name = Label(about,text = "Head of Dept : Prof. Dr. Archana Chaugule", fg = "white",bg = "#202121", font = "Times 16").place(x = 50, y = 150)
guide_name = Label(about,text = "Project Guide : Prof. Shweta Koparde", fg = "white",bg = "#202121", font = "Times 16").place(x = 50, y = 200)
project_members = Label(about,text = "Project Members :", fg = "white",bg = "#202121", font = "Times 16").place(x = 50, y = 250)
gauri = Label(about,text = "BECOMP-A02  Gauri Basutkar", fg = "white",bg = "#202121", font = "Times 14").place(x = 100, y = 280)
vaishnavi = Label(about,text = "BECOMP-A03  Vaishnavi Bhadgaonkar", fg = "white",bg = "#202121", font = "Times 14").place(x = 100, y = 310)
kalyani = Label(about,text = "BECOMP-A52  Kalyani Patil", fg = "white",bg = "#202121", font = "Times 14").place(x = 100, y = 340)
dhanashri = Label(about,text = "BECOMP-A19  Dhanashri Gayke", fg = "white",bg = "#202121", font = "Times 14").place(x = 100, y = 370)
proposed_system = Label(about,text = "The proposed system includes a desktop application which is :", fg = "white",bg = "#202121", font = "Times 14").place(x = 50, y = 420)
pt_1 = Label(about,text = "   -    Desktop Application", fg = "white",bg = "#202121", font = "Times 14").place(x = 50, y = 450)
pt_2 = Label(about,text = "   -    Classifies Genre", fg = "white",bg = "#202121", font = "Times 14").place(x = 50, y = 480)
pt_3 = Label(about,text = "   -    Stores it in Destination Folder", fg = "white",bg = "#202121", font = "Times 14").place(x = 50, y = 510)
pt_4 = Label(about,text = "   -    Uploads .Mp3 and .wav files", fg = "white",bg = "#202121", font = "Times 14").place(x = 50, y = 540)

#window.resizable(0,0)	# Cannot Resize the window
#window.wm_iconbitmap(r'/home/dell/Desktop/MGCS/MGC_Final/images/biticon.ico')
  
window.mainloop()	# Let the window wait for any events
