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

# TODO: fetch bio from telegram


# save bio to file for later use
def fetch_bio():
    username = app.get_me().username
    chat = app.get_chat('@' + username)
    current_bio = chat.bio.split('|')[-1].strip()
    with open('bio.txt', 'w') as file:
        file.write(current_bio)
    return current_bio
# check if bio.txt exists
if os.path.exists('bio.txt'):
    with open('bio.txt', 'r') as file:
        current_bio = file.read()
else:
    current_bio = fetch_bio()


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
last_activity_ts = None
# humanize time
import humanize
def humanize_time(seconds):
    return humanize.naturaldelta(seconds)

def set_activity(index):
    global current_activity, last_index
    current_activity = activities[index].lower()
    timestamp = datetime.now()
    ts = timestamp.strftime('%I:%M %p')
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
    # set last activity timestamp
    global last_activity_ts
    if last_activity_ts is not None:
        time_elapsed = timestamp - last_activity_ts
        last_activity_label.config(text=f'Last activity: {current_activity} for {humanize_time(time_elapsed)}')
    last_activity_ts = timestamp


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




root.title('Activity Tracker')
# set window size
root.geometry('300x320')
# add heading
heading = Label(root, text='Choose your activity', font=('Arial', 15))
heading.pack()
# add break
def add_break(text = '\n'):
    break_label = Label(root, text=text)
    break_label.pack()
add_break()
# add frame
frame = Frame(root)
frame.pack()
activity_chooser()
activity_label = Label(root, text='-', font=('Helvetica', 10))
activity_label.pack()
last_activity_label = Label(root, text='-', font=('Helvetica', 10))
last_activity_label.pack()
add_break()
made_with_love_text ='Made with ❤️ by ம🥰'
made_with_love_img = open('made.png', 'rb')
made_with_love = PhotoImage(data=made_with_love_img.read())
# reduce image size by 70%
made_with_love = made_with_love.subsample(2, 2)
made_with_love_label = Label(root, image=made_with_love, compound=LEFT)
made_with_love_label.pack()
add_break()
add_break()
add_break()
add_break('-')
root.mainloop()
