import os
import pygame
from pygame import mixer
from tkinter import *
from tkinter import filedialog
from mutagen.mp3 import MP3
from ttkthemes import themed_tk as tk
from tkinter import ttk
import time
import threading
import tkinter.messagebox
root= tk.ThemedTk()
root.get_themes()
root.set_theme('arc')
root.resizable(0,0)
mixer.init()
root.title("PLAY MUSIC")
root.iconbitmap(r'bil.ico')
statusbar=ttk.Label(root, text="Welcome to PLAY MUSIC", relief=GROOVE, anchor=W,font='Constantia 8 italic')
statusbar.pack(side=BOTTOM, fill=X)
leftframe=Frame(root)
leftframe.pack(side=LEFT,padx=30)
rightframe=Frame(root)
rightframe.pack(side=RIGHT)
topframe=Frame(rightframe)
topframe.pack()

listname=ttk.Label(leftframe,text="Playlist")
listname.pack()
lengthlable=ttk.Label(topframe,text = "Total Length : --:--")
lengthlable.pack(pady=10)
currentlength=ttk.Label(topframe,text='Current Length : --:--')
currentlength.pack()
photo1=PhotoImage(file="play.png")
photo2=PhotoImage(file="stop-button.png")
photo3=PhotoImage(file="pause.png")
photo4=PhotoImage(file="previous.png")
playlistbox=Listbox(leftframe)
playlistbox.pack()
playlist=[]
def browse_file():
    global filename_path
    filename_path=filedialog.askopenfilename()
    add_to_playlist(filename_path)
def add_to_playlist(filename):
    filename=os.path.basename(filename)
    index=0
    playlistbox.insert(index,filename)
    playlist.insert(index,filename_path)
    index+=1

addbutton=ttk.Button(leftframe,text='Add',command=browse_file)
addbutton.pack(side=LEFT,pady=10)
def delete_song():
    selected_song=playlistbox.curselection()
    selected_song=int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

delbutton=ttk.Button(leftframe,text='Delete',command=delete_song)
delbutton.pack(side=LEFT,pady=10,padx=5)
def show_details(play_song):
    file_data=os.path.splitext(play_song)
    if file_data[1] == '.mp3':
        audio=MP3(play_song)
        totallength=audio.info.length
    else:
        a=mixer.sound(play_song)
        totallength=a.get_length()
    mins,secs=divmod(totallength,60)
    mins=round(mins)
    secs=round(secs)
    timeformat= '{:02d}:{:02d}'.format(mins,secs)
    lengthlable['text']="Total Length"+" - "+timeformat
    t1=threading.Thread(target=startcount,args=(totallength,))
    t1.start()
def startcount(t):
    global paused
    while t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,secs=divmod(t,60)
            mins=round(mins)
            secs=round(secs)
            timeformat= '{:02d}:{:02d}'.format(mins,secs)
            currentlength['text']="Current Length"+" - "+timeformat
            time.sleep(1)
            t-=1
def playmusic():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text']="music resumed...."
        paused=False
    else:
        try:
            stopmusic()
            time.sleep(1)
            selected_song=playlistbox.curselection()
            selected_song=int(selected_song[0])
            play_it=playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text']="Playing music..."+" "+os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror("Error","Failed to load the file")

def stopmusic():
    mixer.music.stop()
    statusbar['text']="music stopped..."
paused=False
def pausemusic():
    global paused
    paused=True
    mixer.music.pause()
    statusbar['text']="music paused..."

def set_vol(val):
    volume=float(val)/100
    mixer.music.set_volume(volume)
def about_us():
    tkinter.messagebox.showinfo("About us","PLAY MUSIC is built using python tkinter GUI by Nagabhushan")
def rewind_music():
    playmusic()
    statusbar['text']="music rewinded..."

muted=False
def mute_music():
    global muted
    print(muted)
    if muted:
        print(muted)
        mixer.music.set_volume(0.32)
        volumebtn.configure(image=volumephoto)
        scale.set(32)
        muted=False
    else:
        print(muted)
        mixer.music.set_volume(0)
        volumebtn.configure(image=mutephoto)
        scale.set(0)
        muted=True
middleframe=Frame(rightframe)
middleframe.pack(padx=30,pady=10)
bottomframe=Frame(rightframe)
bottomframe.pack(padx=10,pady=10)


playbtn=ttk.Button(middleframe,image=photo1,command=playmusic)
playbtn.grid(row=0,column=0,padx=10)
stopbtn=ttk.Button(middleframe,image=photo2,command=stopmusic)
stopbtn.grid(row=0,column=1,padx=10)
pausebtn=ttk.Button(middleframe,image=photo3,command=pausemusic)
pausebtn.grid(row=0,column=2,padx=10)
rewindbtn=ttk.Button(bottomframe,image=photo4,command=rewind_music)
rewindbtn.grid(row=0,column=0)
mutephoto=PhotoImage(file="volume.png")
volumephoto=PhotoImage(file="naga.png")
volumebtn=ttk.Button(bottomframe,image=volumephoto,command=mute_music)
volumebtn.grid(row=0,column=1,padx=10)
#menu bar
menubar=Menu(root)
root.config(menu=menubar)
#create a submenu
submenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label="file",menu=submenu)
submenu.add_command(label="Open", command=browse_file)
submenu.add_command(label="Exit", command=root.destroy)
helpmenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help",menu=helpmenu)
helpmenu.add_command(label="About us", command=about_us)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(32)
mixer.music.set_volume(0.32)
scale.grid(row=0,column=2,padx=20)
def on_closing():
    if tkinter.messagebox.askyesno("Close","Do you really want to close")==True:
        stopmusic()
        root.destroy()
    else:
        pass
root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()
