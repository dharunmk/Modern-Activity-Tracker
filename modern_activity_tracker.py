from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pymsgbox import *
from datetime import *
from tkinter import *
import os
from tg_secrets import *

account = 'me'
app = Client(account, api_id=API_ID, api_hash=API_HASH)
app.start()
current_bio = '@SmartManojChannel'
ts = datetime.now().strftime('%I:%M')
# choices Eating, Sleeping, Yoga, Bathing, Sun bathing
# tkinter button for choosing the activity
root = Tk()
buttons = []
activities = [
    'Sunbathing',
    'Bathing',
    'Doing yoga',
    'Sleeping',
    'Eating',
    'Walking',
    'Working',
]

last_index = None
testing = 0
def set_activity(index):
    global current_activity, last_index
    current_activity = activities[index].lower()
    ts = datetime.now().strftime('%I:%M')
    date = datetime.now().strftime('%d-%b-%Y %I:%M:%p')
    if last_index is not None:
        buttons[last_index].config(bg='brown')
    buttons[index].config(bg='green')
    try:
        app.update_profile(bio=f'Went to {current_activity} at {ts} | {current_bio}')
    except Exception as e:
        alert(str(e))
    if not testing:
        with open('modern_activity_tracker.txt', 'a') as file:
            print(date, current_activity, file=file, sep=', ')
    print(current_activity)
    last_index = index
    # set label text
    activity_label.config(text=f'You are now {current_activity} from {ts}')


def activity_chooser():
    for k,i in enumerate(activities):
        # add button
        button = Button(frame, text=i.upper(), command=lambda k=k: set_activity(k), width=20, bg='brown', fg='white')
        buttons.append(button)
    
    # first four buttons in two rows
    for i in range(4):
        buttons[i].grid(row=i//2, column=i%2)
    #  line break
    Label(frame, text='\n').grid(row=3, column=0)
    # last 3 button in the third row
    for i in range(4, 7):
        buttons[i].grid(row=4+i//2, column=i % 2)





# set window size
root.geometry('300x300')
# add heading
heading = Label(root, text='Choose your activity', font=('Arial', 15))
heading.pack()
# add break
break_label = Label(root, text='\n')
break_label.pack()
# add frame
frame = Frame(root)
frame.pack()
activity_chooser()
activity_label = Label(root, text='-', font=('Helvetica', 10))
activity_label.pack()
root.mainloop()
