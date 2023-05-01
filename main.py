import pandas
from tkinter import *
from PIL import Image
from random import choice

FILE = "./data/french_words.csv"
LEARN_FILE = "./data/word_to_learn.csv"
FRONT_IMAGE = "./images/card_front.png"
BACK_IMAGE = "./images/card_back.png"
IMAGE_RIGHT = "./images/right.png"
IMAGE_WRONG = "./images/wrong.png"
BACKGROUND_COLOR = "#B1DDC6"

open_image = Image.open(FRONT_IMAGE)
width, height = open_image.size
random_word = {}

window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flash Card Game")

try:
    data_word = pandas.read_csv(LEARN_FILE)
except FileNotFoundError:
    data_word = pandas.read_csv(FILE)
    data_word_dict = data_word.to_dict(orient="records")
else:
    data_word_dict = data_word.to_dict(orient="records")


def next_card():
    global random_word, flip_timer

    window.after_cancel(flip_timer)

    random_word = choice(data_word_dict)

    canvas_image.itemconfig(canvas_create_image, image=front_card_image)
    canvas_image.itemconfig(canvas_create_title, text="French", fill="black", font=("Arial", 40, "italic"))
    canvas_image.itemconfig(canvas_create_word, text=f"{random_word['French']}", fill="black", font=("Arial", 60, "bold"))

    flip_timer = window.after(3000, flip_card)


def word_know():
    data_word_dict.remove(random_word)
    data_word_learn = pandas.DataFrame(data_word_dict)
    data_word_learn.to_csv("./data/word_to_learn.csv", index=False)

    next_card()


def flip_card():
    canvas_image.itemconfig(canvas_create_image, image=back_card_image)
    canvas_image.itemconfig(canvas_create_title, text="English", fill="white", font=("Arial", 40, "italic"))
    canvas_image.itemconfig(canvas_create_word, text=f"{random_word['English']}", fill="white", font=("Arial", 60, "bold"))


flip_timer = window.after(3000, flip_card)

canvas_image = Canvas(width=width, height=height, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card_image = PhotoImage(file=FRONT_IMAGE)

back_canvas = Canvas(width=width, height=height, bg=BACKGROUND_COLOR, highlightthickness=0)
back_card_image = PhotoImage(file=BACK_IMAGE)

canvas_create_image = canvas_image.create_image(width // 2, height // 2, image=front_card_image)
canvas_create_title = canvas_image.create_text(400, 150, fill="black", font=("Arial", 40, "italic"))
canvas_create_word = canvas_image.create_text(400, 263, fill="black", font=("Arial", 60, "bold"))
canvas_image.grid(column=0, row=0, columnspan=2)

right_image = PhotoImage(file=IMAGE_RIGHT)
right_button = Button(image=right_image, highlightthickness=0, command=word_know)
right_button.grid(column=1, row=1)

wrong_image = PhotoImage(file=IMAGE_WRONG)
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

next_card()

window.mainloop()
