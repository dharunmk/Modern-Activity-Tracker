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

# save bio to file for later use
def fetch_bio():
    chat = app.get_chat('@' + username)
    current_bio = chat.bio.split('|')[-1].strip()
    with open('bio.txt', 'w') as file:
        file.write(current_bio)
    return current_bio

# check if username.txt exists
if os.path.exists('username.txt'):
    with open('username.txt', 'r') as file:
        username = file.read()
else:
    username = app.get_me().username
    with open('username.txt', 'w') as file:
        file.write(username)

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
    'Sunbathe',
    'Bathe',
    'Do yoga',
    'Sleep',
    'Eat',
    'Walk',
    'Work',
    'Play',
    'Meeting',
    'Custom',
]

last_index = None
testing = 0
last_activity_ts = None
last_activity = None
# humanize time
import humanize
def humanize_time(seconds):
    return humanize.precisedelta(seconds, minimum_unit='minutes')

def enter_custom_activity():
    # options
    options = ['rest due to fever']
    # add option as numbered list
    text = 'Enter custom activity\n'
    for k,i in enumerate(options):
        text += f'{k+1}. {i}\n'
    # get option number
    option = int(prompt(text=text, title='Custom activity', default='1'))
    return options[option-1]

def set_activity(index):
    global current_activity, last_index
    current_activity = activities[index].lower()
    if current_activity == 'custom':
        current_activity = enter_custom_activity()
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
    if 'do' in current_activity:
        current_activity_now = current_activity.replace('do','doing')
    else:
        # split due and add ing
        if 'due' in current_activity:
            _ = current_activity.split(' due')
            current_activity_now = _[0] + 'ing due' + _[1]
        elif current_activity == 'meeting':
            current_activity_now = 'in a meeting'
        else:
            current_activity_now = current_activity+'ing' if current_activity[-1] != 'e' else current_activity[:-1]+'ing'
    activity_label.config(text=f'You are now {current_activity_now} from {ts}')
    # set last activity timestamp
    global last_activity_ts
    global last_activity
    if last_activity_ts is not None:
        time_elapsed = timestamp - last_activity_ts
        last_activity_label.config(text=f'Last activity: {last_activity} for {humanize_time(time_elapsed)}')
    last_activity_ts = timestamp
    # set last activity
    last_activity = current_activity


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
    for i in range(4, len(activities)):
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
made_with_love_label = Label(root, image=made_with_love, compound=LEFT, background='black')
made_with_love_label.pack()
add_break()
add_break()
add_break()
add_break('-')
# button to reload app
def reload_app():
    root.destroy()
    os.system('cd C:\Users\smart\Documents\Modern-Activity-Tracker; python3 modern_activity_tracker.py &')

if username == 'SmartManoj':
    reload_button = Button(root, text='Reload', command=reload_app)
    reload_button.pack()

root.mainloop()
