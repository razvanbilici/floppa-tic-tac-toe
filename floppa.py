import PIL.Image, PIL.ImageTk
import pygame
import customtkinter as ct
from customtkinter import *
from tkinter import messagebox
import random as rd

# ----------------

basedir = os.path.curdir
ct.set_appearance_mode("Dark")

floppa_sound_path = "sounds\\floppa\\"
sogga_sound_path = "sounds\\sogga\\"
bg_sound_path = "sounds\\bg_songs\\"
not_playing = os.listdir(bg_sound_path)
current_song = rd.choice(os.listdir(bg_sound_path))
not_playing.remove(current_song)

game_matrix = []
winning_slices = [slice(0, 3),
                  slice(3, 6),
                  slice(6, 9),
                  slice(0, 9, 3),
                  slice(1, 9, 3),
                  slice(2, 9, 3),
                  slice(0, 9, 4),
                  slice(2, 8, 2)]

winning_position = slice(None)

floppa_score, sogga_score = 0, 0
turn = None
total_moves = 0

root = ct.windows.CTk()
root.iconbitmap(os.path.join(basedir, "images//flop.ico"))
root.title("Floppa Tic Tac Toe")

pygame.mixer.init()
fx_sounds = pygame.mixer.Channel(0)
bg_music = pygame.mixer.Channel(1)

floppa_pic = ct.CTkImage(PIL.Image.open(os.path.join(basedir, "images\\floppa.png")), size=(130, 120))
sogga_pic = ct.CTkImage(PIL.Image.open(os.path.join(basedir, "images\\sogga.png")), size=(100, 120))


# --------------------------
# Functions

def setup():
    global total_moves, game_matrix, turn, winning_position

    for button in buttons:
        button.configure(height=160, width=160, border_width=2, fg_color="transparent", corner_radius=0,
                         state=ACTIVE, image=None, bg_color="transparent")

    game_matrix = ['', '', '',
                   '', '', '',
                   '', '', '']
    total_moves = 0
    winning_position = slice(None)

    turn = rd.choice(["Floppa", "Sogga"])

    turn_label.configure(text="{}'s turn".format(turn), text_color='Gold')


def exit_game():
    if messagebox.askokcancel(";(", "Quit?"):
        messagebox.showinfo(title='boop thanxx 4 playing', message='Made by bilici©2023')
        root.destroy()


def play_again():
    if messagebox.askquestion("Game Over", "Play Again?") == "yes":
        return setup()

    messagebox.showinfo(title='beep boop', message='Made by bilici©2023')
    root.destroy()


# Check if 3 winning-position symbols are alike
def symbol_chain(list_var, winning_slice):
    global winning_position

    # If all symbols are alike and the symbols are not ''
    if len(set(list_var)) == 1 and list_var[0] != '':
        winning_position = winning_slice
        return list_var[0]

    return False


def check_win():
    global floppa_score, sogga_score, buttons, turn_label

    result = (symbol_chain(game_matrix[0:3], winning_slices[0])
              or symbol_chain(game_matrix[3:6], winning_slices[1])
              or symbol_chain(game_matrix[6:9], winning_slices[2])
              or symbol_chain(game_matrix[0:9:3], winning_slices[3])
              or symbol_chain(game_matrix[1:9:3], winning_slices[4])
              or symbol_chain(game_matrix[2:9:3], winning_slices[5])
              or symbol_chain(game_matrix[0:9:4], winning_slices[6])
              or symbol_chain(game_matrix[2:8:2], winning_slices[7]))

    if result in ["F", "S"]:

        for button in buttons[winning_position]:
            button.configure(bg_color='yellow')

        if result == "F":
            floppa_score += 1

            turn_label.configure(text="Floppa wins!", text_color="red")
            score_label.configure(text="Floppa {} - {} Sogga".format(floppa_score, sogga_score))

            messagebox.showinfo("FLOPPA WINS!", "*happy hissing noises*")

            return play_again()

        sogga_score += 1

        turn_label.configure(text="Sogga wins!", text_color="green")
        score_label.configure(text="Floppa {} - {} Sogga".format(floppa_score, sogga_score))

        messagebox.showinfo("SOGGA WINS", "*happy pizzer noises*")

        return play_again()

    if total_moves == 9:

        for button in buttons:
            button.configure(state=DISABLED, bg_color='grey')

        turn_label.configure(text="Draw", text_color="blue")

        messagebox.showinfo("DRAW", ";(")
        return play_again()


def click(clicked_button):
    global turn, turn_label, total_moves

    pygame.mixer.Channel(0).stop()

    if game_matrix[buttons.index(clicked_button)] != "":
        messagebox.showerror("Tic Tac Toe", "Smt else bruh")
        return

    if turn == "Floppa":
        fx_sounds.set_volume(0.2)

        current_sound = os.path.join(basedir, floppa_sound_path + rd.choice(os.listdir(floppa_sound_path)))
        clicked_button.configure(image=floppa_pic, bg_color="red")
        turn_label.configure(text="Sogga's turn")

        game_matrix[buttons.index(clicked_button)] = "F"

        fx_sounds.play(pygame.mixer.Sound(current_sound))

        turn = "Sogga"
        total_moves += 1
        check_win()
        return

    fx_sounds.set_volume(1)

    current_sound = os.path.join(basedir, sogga_sound_path + rd.choice(os.listdir(sogga_sound_path)))
    clicked_button.configure(image=sogga_pic, bg_color="green")
    turn_label.configure(text="Floppa's turn")

    game_matrix[buttons.index(clicked_button)] = "S"

    fx_sounds.play(pygame.mixer.Sound(current_sound))

    turn = "Floppa"
    total_moves += 1
    check_win()


def volume(vol):
    bg_music.set_volume(.1 * vol * 2)


def mute():
    if mute_unmute.cget("text") == "Mute":
        bg_music.set_volume(0)
        mute_unmute.configure(text="Unmute", fg_color="red")
        return

    bg_music.set_volume(.1 * volume_slider.get() * 2)
    mute_unmute.configure(text="Mute", fg_color="green")


def change_song():
    global current_song

    song = rd.choice(not_playing)
    not_playing.append(current_song)
    current_song = song
    not_playing.remove(current_song)

    print(not_playing)

    bg_music.play(pygame.mixer.Sound(os.path.join(basedir, bg_sound_path + current_song)), loops=-1)


def close():
    messagebox.showinfo(title='Beep boop thanxx 4 playing', message='Made by bilici©2023')
    root.destroy()


root.protocol('WM_DELETE_WINDOW', exit_game)

# ------------------

# Buttons

b00 = ct.CTkButton(root, text=" ", command=lambda: click(b00))
b01 = ct.CTkButton(root, text=" ", command=lambda: click(b01))
b02 = ct.CTkButton(root, text=" ", command=lambda: click(b02))
b10 = ct.CTkButton(root, text=" ", command=lambda: click(b10))
b11 = ct.CTkButton(root, text=" ", command=lambda: click(b11))
b12 = ct.CTkButton(root, text=" ", command=lambda: click(b12))
b20 = ct.CTkButton(root, text=" ", command=lambda: click(b20))
b21 = ct.CTkButton(root, text=" ", command=lambda: click(b21))
b22 = ct.CTkButton(root, text=" ", command=lambda: click(b22))

buttons = [b00, b01, b02,
           b10, b11, b12,
           b20, b21, b22]

b00.grid(row=0, column=0)
b01.grid(row=0, column=1)
b02.grid(row=0, column=2)
b10.grid(row=1, column=0)
b11.grid(row=1, column=1)
b12.grid(row=1, column=2)
b20.grid(row=2, column=0)
b21.grid(row=2, column=1)
b22.grid(row=2, column=2)

# ------------------

turn_label = ct.CTkLabel(root, font=("Jokerman", 20))
turn_label.grid(row=3, columnspan=3)

score_label = ct.CTkLabel(root, text="Floppa 0 - 0 Sogga", font=("Jokerman", 20), text_color="Gold")
score_label.grid(row=4, columnspan=3)

change_song_button = ct.CTkButton(root, text="Change song", font=('Bell MT', 14), command=change_song)
change_song_button.grid(row=6, column=0)

mute_unmute = ct.CTkButton(root, text="Mute", fg_color="green", font=('Bell MT', 14), border_width=2,
                           border_color='Gray', command=mute)
mute_unmute.grid(row=6, column=1)

volume_label = ct.CTkLabel(root, text="Song Volume", font=('Bell MT', 14))
volume_label.grid(row=5, column=2)
volume_slider = ct.CTkSlider(root, width=160, height=16, border_width=5, command=volume)
volume_slider.grid(row=6, column=2)

empty_label = ct.CTkLabel(root, text='')
empty_label.grid(row=8)

exit_button = ct.CTkButton(root, text="Exit", command=exit_game, font=('Bell MT', 14))
exit_button.grid(columnspan=3, row=9)

# ------------
setup()
root.protocol('WM_DELETE_WINDOW', close)

bg_music.set_volume(.1)
bg_music.play(pygame.mixer.Sound(os.path.join(basedir, bg_sound_path + current_song)), loops=-1)

root.mainloop()

# ------------
