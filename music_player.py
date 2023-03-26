from tkinter import *
from tkinter import Tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from pygame import mixer
from mutagen.mp3 import MP3
import os
import random
import time

#music player window initilaization
music_player = Tk()
music_player.title("Music Player")
music_player.geometry("1000x700")
music_player.configure(background = "light blue")
music_player.resizable(0, 0)
mixer.init()

# global variable necessary for properly playing music
global paused
paused = False

#functions
################################################################

#upload music files to player
def upload_music():
    path = filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs = os.listdir(path)
        for song in songs:
            if song.endswith(".mp3"):
                playlist.insert(END, song)
                song_list.append(song)
                dict_os[song] = path + "/" + song

#upload artwork file to album image     
def add_artwork(): 
    path = filedialog.askopenfilename()
    if path and (path.endswith('.png') or path.endswith('.jpeg') or path.endswith('.jpg')):
        art_img = Image.open(path)
        art_img = art_img.resize((200, 200))
        art_img = ImageTk.PhotoImage(art_img)
        artwork_image.configure(image=art_img)
        artwork_image.image = art_img

#pause music
def pause_music():
    global paused
    mixer.music.pause()
    paused = True
    # if paused == True:
    #     pass
    # elif paused == False:
    #     mixer.music.pause()
    #     paused = True

#play music function 
def play_music():
    global paused
    num = playlist.curselection()
    num = int(num[0])
    selected_song = song_list[num]
    cu_song = current_song['text']
    if mixer.music.get_pos() > 0 and selected_song == cu_song:
        mixer.music.unpause()
    else:
        music_name = playlist.get(ACTIVE)
        current_song['text'] = music_name
        mixer.music.load(playlist.get(ACTIVE))
        mixer.music.play()
        # mixer.music.play(loops = 0, start = int(slider.get()))
    if mixer.music.get_busy() == True and paused == True:
        paused = False
        return
    else:
        play_time()

#next song
#goes to the next song in the playlist
def next_music():
    cu_song = current_song['text']
    index = song_list.index(cu_song)
    playlist.selection_clear(index, index)
    if index >= len(song_list):
        index = 0
    new_index = index + 1
    cu_song = song_list[new_index]
    current_song['text'] = cu_song
    mixer.music.load(cu_song)
    mixer.music.play()
    selection_change()
    slider_position = int(song_length)
    slider.config(to=slider_position, value=0)

#previous song
#goes to the previous song in the playlist
def prev_music():
    cu_song = current_song['text']
    index = song_list.index(cu_song)
    playlist.selection_clear(index, index)
    if index != 0:
        new_index = index - 1
        cu_song = song_list[new_index]
        current_song['text'] = cu_song
        mixer.music.load(cu_song)
        mixer.music.play()
        selection_change()
        slider_position = int(song_length)
        slider.config(to=slider_position, value=0)

#shuffle playlist function
def shuffle_music():
    random.shuffle(song_list)
    if mixer.music.get_busy():
        play_time()
    playlist.delete(0,END)
    for item in song_list:
        playlist.insert(END, item)
    selection_change()

#repeat song function
#repeats current song
def repeat_music():
    cu_song = current_song['text']
    mixer.music.queue(cu_song, loops = -1)

#play time function
#keeps track of runtime of current song out of the length of the song
#also plays music continuously
def play_time():
    cu_time = mixer.music.get_pos() / 1000
    converted_cu_time = time.strftime('%M:%S', time.gmtime(cu_time))

    cu_song = current_song['text']
    song = f'{dict_os[cu_song]}'
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    cu_time += 1
    if int(slider.get()) == int(cu_time):
        slider_position = int(song_length)
        slider.config(to=slider_position, value=int(cu_time))
    elif paused == True:
        pass
    else:
        slider_position = int(song_length)
        slider.config(to=slider_position, value=int(slider.get()))
        converted_cu_time = time.strftime('%M:%S', time.gmtime(int(slider.get())))
        progress_bar.config(text = f'Time Elapsed: {converted_cu_time} of {converted_song_length}')
        next_time = int(slider.get()) + 1
        slider.config(value = next_time)

    if (int(converted_cu_time[3:])) == int(converted_song_length[3:]) and (int(converted_cu_time[0:2])) == int(converted_song_length[0:2]):
        next_music()
        play_time()
    else:
        progress_bar.after(1000, play_time)

#switches cursor from current song to the next song
def selection_change():
    cu_song = current_song['text']
    index = song_list.index(cu_song)
    playlist.selection_set(index, index)    

def slide(x):
    global paused
    mixer.music.load(current_song['text'])
    mixer.music.play(loops = 0, start = int(slider.get()))
    paused = False

#frames
#User frame 
left_frame = Frame(music_player, width = 500, height = 700, bg = "light blue")
left_frame.grid(row = 0, column = 0, padx = 0, pady = 1)

#playlist frame
right_frame = Frame(music_player, width = 500, height = 700, bg = "black")
right_frame.grid(row = 0, column = 1, columnspan = 5, padx = 0, pady = 1)

#music playlist
playlist = Listbox(right_frame, selectmode=SINGLE, font = ("times new roman", 12, "bold"), width = 81, height = 48, bg = "black", fg = "white")
playlist.grid(row = 0, column = 0)
scroll = Scrollbar(right_frame, bg = "white")
scroll.grid(row = 0, column = 1)
playlist.config(yscrollcommand = scroll.set)
scroll.config(command = playlist.yview)

#images/labels
# main image button
logo_img = Image.open("music_player_img.png")
logo_img = logo_img.resize((250, 200))
logo_img = ImageTk.PhotoImage(logo_img)
player_image = Label(left_frame, height = 200, image = logo_img, padx = 10, bg = "light blue")
player_image.place(x = 0, y = 0)

#current song label to display the current song playing
current_song = Label(left_frame, text = "Current Song", width = 53, height = 5, font = ("times new roman", 18, "bold"), padx = 10, bg = "light blue", fg = "black")
current_song.place(x = 0, y = 450)

#album artwork label to display artwork chosen
artwork_img = Image.open("album_default.png")
artwork_img = artwork_img.resize((200, 200))
artwork_img = ImageTk.PhotoImage(artwork_img)
artwork_image = Label(left_frame, width = 200, height = 200, image = artwork_img, padx = 10, bg = "light blue")
artwork_image.place(x = 150, y = 250)

# progress bar to display runtime
progress_bar = Label(left_frame, text = '', width = 33, height = 1, font = ("times new roman", 12, "bold"), bg = "light blue", fg = "black")
progress_bar.place(x = 150, y = 520)

# style for slider
style = ttk.Style()
style.configure('myStyle.Horizontal.TScale', background = "red")

#slider to change spot in song
slider = ttk.Scale(left_frame, style = 'myStyle.Horizontal.TScale', length= 300, from_=0, to=100, orient= HORIZONTAL, value=0, command= slide)
slider.place(x = 100, y = 550)
#buttons

#shuffle button
#sets image and places it with button on window
shuffle_img = Image.open("shuffle_button.png")
shuffle_img = shuffle_img.resize((75, 75))
shuffle_img = ImageTk.PhotoImage(shuffle_img)
shuffle_image = Button(left_frame, width = 75, height = 75, image = shuffle_img, padx = 10, bg = "light blue", command = shuffle_music)
shuffle_image.place(x = 10, y = 600)

#back button
#sets image and places it with button on window
back_img = Image.open("back_button.png")
back_img = back_img.resize((75, 75))
back_img = ImageTk.PhotoImage(back_img)
back_image = Button(left_frame, width = 75, height = 75, image = back_img, padx = 10, bg = "light blue", command = prev_music)
back_image.place(x = 90, y = 600)

#play button
#sets image and places it with button on window
play_img = Image.open("play_button.png")
play_img = play_img.resize((75, 75))
play_img = ImageTk.PhotoImage(play_img)
play_image = Button(left_frame, width = 75, height = 75, image = play_img, padx = 10, bg = "light blue", command = play_music)
play_image.place(x = 170, y = 600)

#pause button
#sets image and places it with button on window
pause_img = Image.open("pause_button.png")
pause_img = pause_img.resize((75, 75))
pause_img = ImageTk.PhotoImage(pause_img)
pause_image = Button(left_frame, width = 75, height = 75, image = pause_img, padx = 10, bg = "light blue", command = pause_music)
pause_image.place(x = 250, y = 600)

#next button
#sets image and places it with button on window
next_img = Image.open("next_button.png")
next_img = next_img.resize((75, 75))
next_img = ImageTk.PhotoImage(next_img)
next_image = Button(left_frame, width = 75, height = 75, image = next_img, padx = 10, bg = "light blue", command = next_music)
next_image.place(x = 330, y = 600)

#repeat button
#sets image and places it with button on window
repeat_img = Image.open("repeat_button.png")
repeat_img = repeat_img.resize((75, 75))
repeat_img = ImageTk.PhotoImage(repeat_img)
repeat_image = Button(left_frame, width = 75, height = 75, image = repeat_img, padx = 10, bg = "light blue", command = repeat_music)
repeat_image.place(x = 410, y = 600)

# add music button
Button(music_player, text="Add Music", width=25, height=5, font=("times new roman", 14 ,"bold"),fg="black", bg="light blue", command= upload_music).place(x=275, y=15)

# add artwork button
Button(music_player, text = "Add Artwork", width = 25, height = 5, font = ("times new roman", 14, "bold"), fg = "black", bg = "light blue", command= add_artwork).place(x = 275, y = 115)

# song list to store songs
song_list = []
# dictionary to store song path
dict_os= {}
# main loop to run music player
music_player.mainloop()
