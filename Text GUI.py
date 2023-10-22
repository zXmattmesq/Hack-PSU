
filename = 'Nijika Pledge'

# Open the file for reading (use 'r' for reading mode)
with open(filename + ' (FULL).txt', 'r') as file:
    # Your code to read from the file goes here
    full_content = file.read()

# Open the file for reading (use 'r' for reading mode)
with open(filename + ' (BABY).txt', 'r') as file:
    # Your code to read from the file goes here
    baby_content = file.read()

import tkinter as tk
import os
from tkinter import ttk
from PIL import Image, ImageTk
from itertools import count, cycle
from gtts import gTTS

class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)

        

        frames = []

        try:
            for i in count(1):
                frame = im.copy()
                frame.thumbnail((200, 200))  # Resize the frame to the desired size
                frames.append(ImageTk.PhotoImage(frame))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

def button_click():
    global bald_people
    if bald_people % 2 == 0:
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)  # Clear the text
        text_widget.insert(tk.END, baby_content)  # Insert the new content
    else:
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)  # Clear the text
        text_widget.insert(tk.END, full_content)  # Insert the new content
    bald_people += 1
    text_widget.config(state=tk.DISABLED)

'''
def button_click():
    global bald_people
    if bald_people % 2 == 0:
        directory = os.listdir('/Users/milo/Desktop/BABY ARTICLES')
        populate_listbox()
        listbox.bind("<<ListboxSelect>>", display_selected_text)
    else:
        directory = os.listdir('/Users/milo/Desktop/FULL ARTICLES')
        populate_listbox()
        listbox.bind("<<ListboxSelect>>", display_selected_text)
    bald_people += 1
'''
def button2_click():
    global people_with_hair
    if people_with_hair % 2 == 0:
        root.configure(bg = "#202225")
        frm_buttons.configure(bg = "#202225")
        text_widget.config(bg = "#202225", foreground = "#eeeeee")
        listbox.config(bg = "#202225", foreground = "#eeeeee")
    else:
        root.configure(bg = "#e0e0e0")
        frm_buttons.configure(bg = "#e0e0e0")
        text_widget.config(bg = "#e0e0e0", foreground = "black")
        listbox.config(bg = "#e0e0e0", foreground = "black")
    people_with_hair += 1

def button3_click():
    tts = gTTS(text_widget.get("1.0", tk.END))
    tts.save("tts.mp3")
    os.system("afplay tts.mp3")



bald_people = 0
people_with_hair = 0

root = tk.Tk()
root.title(filename)
root.configure(bg = "tan")

root.rowconfigure(0, minsize=800, weight=1)
root.columnconfigure(1, minsize=800, weight=1)

frm_buttons = tk.Frame(root, relief=tk.RAISED, bd=2, background = "#e0e0e0")

font_tuple = ("Arial", 18)

# Create a Text widget for the text content
text_widget = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED, background = "#e0e0e0", foreground = "black")  # Set the state to "disabled"
text_widget.grid(row=0, column=1, sticky="nsew")
text_widget.config(font = font_tuple)

text_widget.config(state=tk.NORMAL)
text_widget.delete(1.0, tk.END)  # Clear the text
text_widget.insert(tk.END, full_content)  # Insert the new content
text_widget.config(state=tk.DISABLED)

listbox = tk.Listbox(frm_buttons, bg = "#e0e0e0", foreground = "black", font = font_tuple)
listbox.grid(row=5, column=0)

directory = os.listdir('/Users/milo/Desktop/hackathon')

def populate_listbox():
    text_files = [file for file in directory if file.endswith('.txt')]
    for file in text_files:
        listbox.insert(tk.END, file)

def display_selected_text(event):
    selected_index = listbox.curselection()
    if selected_index:
        selected_file = listbox.get(selected_index)
        with open(selected_file, 'r') as file:
            content = file.read()
            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, content)
            text_widget.config(state=tk.DISABLED)

populate_listbox()

listbox.bind("<<ListboxSelect>>", display_selected_text)

# Create a vertical scrollbar
vsb = tk.Scrollbar(root, orient="vertical", command=text_widget.yview)
vsb.grid(row=0, column=2, sticky="ns")

# Configure the Text widget to use the scrollbar
text_widget.config(yscrollcommand=vsb.set)

lbl = ImageLabel(frm_buttons)
lbl.config()
lbl.grid(row=2, column=0, sticky="ns")
lbl.load("clara.gif")

button = tk.Button(frm_buttons, text="CHANGE FORMAT", command=button_click, bg="blue")
button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

darkmodebutton = tk.Button(frm_buttons, text="TOGGLE DARK MODE", command=button2_click)
darkmodebutton.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

ttsbutton = tk.Button(frm_buttons, text="TEXT TO SPEECH", command=button3_click)
ttsbutton.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

frm_buttons.grid(row=0, column=0, sticky="ns")

root.mainloop()


