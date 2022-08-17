import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
FRONT_FRENCH_SIDE = False
CURRENT_FRENCH_WORD = ''
CURRENT_ENGLISH_WORD = ''
REMEMBERED_WORDS = []
RIGHT_BUTTON_CLICKED = False


# --------------------- Flash Card ------------------/

def wrong_button():
    next_word()


def right_button():
    global RIGHT_BUTTON_CLICKED

    if not RIGHT_BUTTON_CLICKED:
        RIGHT_BUTTON_CLICKED = True
        save_to_known()
        next_word()
        window.after(3000, show_english_side)


def show_english_side():
    # It seems like window.after does not pause the current method, and right_button() execute all the code instantly.
    # Codes after window.after() are executed even window.after() have not called "show_english_side" yet
    # So the lock has to be unlocked in this method
    global RIGHT_BUTTON_CLICKED
    flip_flash_card()
    change_word()
    change_language()
    RIGHT_BUTTON_CLICKED = False


def save_to_known():
    global WORDS_DICTIONARY

    with open('known.csv', 'a') as known_words:
        known_words.write(f"\n{CURRENT_FRENCH_WORD},{CURRENT_ENGLISH_WORD}")

    REMEMBERED_WORDS.append(CURRENT_FRENCH_WORD)
    WORDS_DICTIONARY.pop(CURRENT_FRENCH_WORD)


def next_word():
    global FRONT_FRENCH_SIDE

    if not FRONT_FRENCH_SIDE:
        flip_flash_card()

    choose_a_word()
    change_word()


def flip_flash_card():
    global FRONT_FRENCH_SIDE

    if FRONT_FRENCH_SIDE:
        card_canvas.itemconfig(image_container, image=back_card_img)
        FRONT_FRENCH_SIDE = False
    else:
        card_canvas.itemconfig(image_container, image=front_card_img)
        FRONT_FRENCH_SIDE = True

    change_language()


def change_language():
    global FRONT_FRENCH_SIDE

    if FRONT_FRENCH_SIDE:
        card_canvas.itemconfig(language_container, text="French", fill="black")
    else:
        card_canvas.itemconfig(language_container, text="English", fill="white")


def change_word():
    global FRONT_FRENCH_SIDE, CURRENT_FRENCH_WORD, CURRENT_ENGLISH_WORD

    if FRONT_FRENCH_SIDE:
        card_canvas.itemconfig(word_container, text=f"{CURRENT_FRENCH_WORD}", fill="black")
    else:
        card_canvas.itemconfig(word_container, text=f"{CURRENT_ENGLISH_WORD}", fill="white")


def choose_a_word():
    global CURRENT_FRENCH_WORD, CURRENT_ENGLISH_WORD

    CURRENT_FRENCH_WORD = random.choice(list(WORDS_DICTIONARY))
    CURRENT_ENGLISH_WORD = WORDS_DICTIONARY[CURRENT_FRENCH_WORD]


# --------------------- Read data from csv----------------/


with open("data/french_words.csv", 'r') as data_file:
    dataframe = pandas.read_csv(data_file)

    WORDS_DICTIONARY = {row['French']: row['English'] for (index, row) in dataframe.iterrows()}
    choose_a_word()

try:
    with open('known.csv', 'r') as know_words:
        know_words_df = pandas.read_csv(know_words)
except FileNotFoundError:
    with open('known.csv', 'w') as know_words:
        know_words.write("French,English")
else:
    REMEMBERED_WORDS = [row['French'] for (index, row) in know_words_df.iterrows()]
    for word in REMEMBERED_WORDS:
        WORDS_DICTIONARY.pop(word)

# --------------------- UI Set Up-------------------/

window = Tk()
window.title("Flash Card")
window.geometry("+800+150")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)

# Two sides of flash card
front_card_img = PhotoImage(file="images/card_front.png")
back_card_img = PhotoImage(file="images/card_back.png")

card_canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
image_container = card_canvas.create_image(400, 263, image=back_card_img)
language_container = card_canvas.create_text(400, 150,
                                             text="\n\n\n\n\nWelcome use Flash Card\n\nClick checker button "
                                                  "\nto start remembering words",
                                             fill="white",
                                             font="Helvetica 40 italic")

word_container = card_canvas.create_text(400, 270, text="", fill='white',
                                         font="Helvetica 60 bold", anchor="center")

card_canvas.grid(row=0, column=0, columnspan=4)

# Buttons
check_img = PhotoImage(file="images/right.png")
check_button = Button(bg=BACKGROUND_COLOR, highlightthickness=0, image=check_img, command=right_button)
check_button.grid(row=1, column=3)

cross_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=cross_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=wrong_button)
wrong_button.grid(row=1, column=0)

window.mainloop()
