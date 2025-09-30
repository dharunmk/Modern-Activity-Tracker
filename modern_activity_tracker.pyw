from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.account import UpdateEmojiStatusRequest
from telethon.tl.types import EmojiStatus
import traceback
from pymsgbox import alert, prompt
from datetime import *
from tkinter import *
import os
import asyncio
from hc import toggle_fan
from sys_utils import set_mute, monitor_off
from dotenv import load_dotenv
load_dotenv()

account = 'telethon_session'
app = TelegramClient(account, os.getenv('API_ID'), os.getenv('API_HASH'))

# Initialize the client properly
async def init_client():
    await app.start()

# Run the async initialization
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(init_client())

# save bio to file for later use
async def fetch_bio():
    chat = await app.get_entity('@' + username)
    current_bio = chat.about.split('|')[-1].strip()
    with open('bio.txt', 'w') as file:
        file.write(current_bio)
    return current_bio

# check if username.txt exists
if os.path.exists('username.txt'):
    with open('username.txt', 'r') as file:
        username = file.read()
else:
    # Get username asynchronously
    async def get_username():
        me = await app.get_me()
        return me.username
    
    username = asyncio.run(get_username())
    with open('username.txt', 'w') as file:
        file.write(username)

# check if bio.txt exists
if os.path.exists('bio.txt'):
    with open('bio.txt', 'r') as file:
        current_bio = file.read()
else:
    current_bio = asyncio.run(fetch_bio())

# choices Eating, Sleeping, Yoga, Bathing, Sun bathing
# tkinter button for choosing the activity
root = Tk()
buttons = []
activities = [
    'Sunbathe',
    'Bathe',
    'Oil bathe',
    'Do yoga',
    'Sleep',
    'Eat',
    'Walk',
    'Work',
    'Play',
    'Meeting',
    'Custom',
    'Fan',
    'Screen',
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

async def update_telegram_profile(new_bio, custom_emoji_id):
    try:
        with open('logs.txt', 'a') as file:
            file.write(f'{datetime.now()}: About to update profile with bio: {new_bio}\n')
        await app(UpdateProfileRequest(about=new_bio))
        if custom_emoji_id:
            await app(UpdateEmojiStatusRequest(EmojiStatus(document_id=custom_emoji_id)))
    except Exception as e:
        alert('MAT'+str(e))
        with open('logs.txt', 'a') as file:
            e=traceback.format_exc()
            print(e, file=file)

def set_activity(index):
    try:
        global last_activity_ts
        global last_activity
        global current_activity, last_index
        current_activity = activities[index].lower()
        with open('current_activity.txt', 'w') as file:
            file.write(current_activity)
        if current_activity == 'fan':
            toggle_fan()
            return
        if current_activity == 'screen':
            monitor_off()
            return
        if current_activity == 'custom':
            current_activity = enter_custom_activity()
        timestamp = datetime.now()
        work_activities = ['work', 'meeting']
        if current_activity in work_activities or last_activity in work_activities:
            try:
                toggle_fan()
            except Exception as e:
                with open('logs.txt', 'a') as file:
                    e=traceback.format_exc()
                    print(e, file=file)

        dnd_activities = ['eat','sleep', 'do yoga', ]
        if current_activity in dnd_activities:
            if current_activity == 'sleep' and 0:
                with open('logs.txt', 'a') as log:
                    log.write(f'{datetime.now()}: About to call monitor_off() for {current_activity}\n')
                monitor_off()
            with open('logs.txt', 'a') as log:
                log.write(f'{datetime.now()}: monitor_off() completed for {current_activity}\n')
            with open('logs.txt', 'a') as log:
                log.write(f'{datetime.now()}: About to call set_mute(True) for {current_activity}\n')
            set_mute(True)
            with open('logs.txt', 'a') as log:
                log.write(f'{datetime.now()}: set_mute(True) completed for {current_activity}\n')
        elif last_activity in dnd_activities:
            with open('logs.txt', 'a') as log:
                log.write(f'{datetime.now()}: About to call set_mute(False) for {last_activity}\n')
            set_mute(False)
            with open('logs.txt', 'a') as log:
                log.write(f'{datetime.now()}: set_mute(False) completed for {last_activity}\n')
        ts = timestamp.strftime('%I:%M %p')
        date = datetime.now().strftime('%d-%b-%Y %I:%M:%p')
        if last_index is not None:
            buttons[last_index].config(bg='brown')
        buttons[index].config(bg='green')
        
        # Prepare the new bio and emoji status
        if current_activity == 'meeting':
            new_bio = f'In a call with manoj at {ts}'
        else:
            new_bio = f'Went to {current_activity} at {ts}'
        if current_bio:
            new_bio += ' | ' + current_bio
            
        custom_emojis = {
            'sunbathe': 5431766464040283359, # 😎
            'bathe': 5336864316912051427, # 🛀
            'oil bathe': 5469629946534043706, # 🛁
            'do yoga': 5253555484811610534, # 🧘
            'sleep': 5440456175017532988, # 😴
            'eat': 5224200886581992369, # 😋
            'walk': 5420631872994553493, # 🚶
            'work': 5319161050128459957, # 👨‍💻
            'meeting': 5453957997418004470, # 👥
        }
        custom_emoji_id = custom_emojis.get(current_activity)
        
        # Run the async update in a new event loop
        try:
            loop.run_until_complete(update_telegram_profile(new_bio, custom_emoji_id))
        except Exception as e:
            alert('MAT'+str(e))
            with open('logs.txt', 'a') as file:
                e=traceback.format_exc()
                print(e, file=file)
                
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
                current_activity_now = 'in a call with manoj'
            else:
                current_activity_now = current_activity+'ing' if current_activity[-1] != 'e' else current_activity[:-1]+'ing'
        activity_label.config(text=f'You are now {current_activity_now} from {ts}')
        # set last activity timestamp
        
        if last_activity_ts is not None:
            time_elapsed = timestamp - last_activity_ts
            last_activity_label.config(text=f'Last activity: {last_activity} for {humanize_time(time_elapsed)}')
        last_activity_ts = timestamp
        # set last activity
        last_activity = current_activity
    except Exception as e:
        alert(f'MAT: {str(e)}')
        with open('logs.txt', 'a') as file:
            e=traceback.format_exc()
            print(e, file=file)


def activity_chooser():
    for k,i in enumerate(activities):
        # add button
        button = Button(frame, text=i.upper(), command=lambda k=k: set_activity(k), width=20, bg='brown', fg='white')
        buttons.append(button)
    
    first_n = 5
    # first four buttons in two rows
    for i in range(first_n):
        buttons[i].grid(row=i//2, column=i%2)
    #  line break
    Label(frame, text='\n').grid(row=first_n//2 + 1, column=0)
    # last 3 button in the third row
    for i in range(first_n, len(activities)):
        buttons[i].grid(row=first_n + (i-1)//2, column=(i-1) % 2)




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
try:
    with open('made.png', 'rb') as made_with_love_img:
        made_with_love = PhotoImage(data=made_with_love_img.read())
    # reduce image size by 70%
    made_with_love = made_with_love.subsample(2, 2)
    made_with_love_label = Label(root, image=made_with_love, compound=LEFT, background='black')
    made_with_love_label.pack()
except Exception as e:
    # If image fails to load, just show text
    made_with_love_label = Label(root, text=made_with_love_text, background='black', fg='white')
    made_with_love_label.pack()
    with open('logs.txt', 'a') as file:
        file.write(f'{datetime.now()}: Image loading failed: {str(e)}\n')
add_break()
add_break('-')
# button to reload app
def reload_app():
    root.destroy()
    import webbrowser
    webbrowser.open(r'C:\Users\smart\Documents\Modern-Activity-Tracker\modern_activity_tracker.pyw')
    # os.system(r'cd C:\Users\smart\Documents\Modern-Activity-Tracker && py modern_activity_tracker.pyw &')


if username == 'SmartManoj':
    reload_button = Button(root, text='Reload', command=reload_app)
    reload_button.pack()
    root.geometry('300x500')

try:
    root.mainloop()
except Exception as e:
    alert(f'MAT: {str(e)}')
    with open('logs.txt', 'a') as file:
        e=traceback.format_exc()
        print(e, file=file)
