from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
import threading
import queue
import os
from datetime import datetime
import traceback
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
import humanize

# Load environment variables
try:
    load_dotenv()
except:
    pass

# Initialize FastAPI app
app = FastAPI(title="Modern Activity Tracker")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global variables
username = None
current_bio = None
telegram_loop = None
telegram_thread = None
telegram_queue = queue.Queue()
last_activity_ts = None
last_activity = None
current_activity = None

# Activities list
activities = [
    'Movies/Series',
    'Watching YouTube',
    'Gym', 
    'Sleep',
    'Eat',
    'Walk',
    'Travel',
    'Work',
    'Play',
    'Meeting',
    'Internet Scroll',
    'Learn',
    'Custom'
]

# Initialize Telegram client
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
telegram_app = None

if api_id and api_hash:
    account = 'telethon_session'
    telegram_app = TelegramClient(account, api_id, api_hash)
else:
    print("Warning: API_ID and API_HASH not found in environment variables.")
    print("Telegram functionality will be disabled.")

# Telegram functions (copied from original app)
async def initialize_app():
    global username, current_bio
    
    if not telegram_app:
        print("Telegram client not initialized - skipping initialization")
        return
    
    try:
        await telegram_app.start()
        
        if os.path.exists('username.txt'):
            with open('username.txt', 'r') as file:
                username = file.read()
        else:
            me = await telegram_app.get_me()
            username = me.username
            with open('username.txt', 'w') as file:
                file.write(username)
        
        if os.path.exists('bio.txt'):
            with open('bio.txt', 'r') as file:
                current_bio = file.read()
        else:
            try:
                chat = await telegram_app.get_entity('@' + username)
                current_bio = chat.about.split('|')[-1].strip() if chat.about else ""
                with open('bio.txt', 'w') as file:
                    file.write(current_bio)
            except Exception as e:
                current_bio = ""
                with open('logs.txt', 'a') as file:
                    file.write(f'{datetime.now()}: Failed to fetch bio: {str(e)}\n')
        
        print(f"Telegram client initialized successfully. Username: {username}, Bio: {current_bio}")
    except Exception as e:
        print(f"Failed to initialize Telegram client: {e}")
        with open('logs.txt', 'a') as file:
            file.write(f'{datetime.now()}: Initialization failed: {str(e)}\n')

async def update_telegram_profile(new_bio):
    if not telegram_app:
        print("Telegram client not available - skipping profile update")
        return
    
    try:
        # Ensure client is connected
        if not telegram_app.is_connected():
            await telegram_app.connect()
        
        with open('logs.txt', 'a') as file:
            file.write(f'{datetime.now()}: About to update profile with bio: {new_bio}\n')
        await telegram_app(UpdateProfileRequest(about=new_bio))
        print(f"Successfully updated Telegram profile: {new_bio}")
    except Exception as e:
        error_msg = f"Failed to update Telegram profile: {str(e)}"
        print(error_msg)
        with open('logs.txt', 'a') as file:
            file.write(f'{datetime.now()}: {error_msg}\n')
            file.write(f'{datetime.now()}: {traceback.format_exc()}\n')

def run_telegram_async(coro):
    if telegram_loop and not telegram_loop.is_closed():
        future = asyncio.run_coroutine_threadsafe(coro, telegram_loop)
        try:
            return future.result(timeout=30)
        except Exception as e:
            print(f"Telegram operation failed: {e}")
            return None
    else:
        print("Telegram event loop not available")
        return None

def init_telegram():
    global telegram_loop, telegram_thread
    
    if not telegram_app:
        print("Skipping Telegram initialization - no credentials")
        return
    
    def run_telegram_loop():
        global telegram_loop
        telegram_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(telegram_loop)
        telegram_loop.run_forever()
    
    telegram_thread = threading.Thread(target=run_telegram_loop, daemon=True)
    telegram_thread.start()
    
    import time
    time.sleep(0.2)
    
    try:
        run_telegram_async(initialize_app())
    except Exception as e:
        print(f"Initialization error: {e}")
        with open('logs.txt', 'a') as file:
            file.write(f'{datetime.now()}: Initialization error: {str(e)}\n')

def humanize_time(seconds):
    return humanize.precisedelta(seconds, minimum_unit='minutes')

# Initialize Telegram on startup
init_telegram()

# Web routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "activities": activities,
        "current_activity": current_activity,
        "last_activity": last_activity,
        "last_activity_ts": last_activity_ts,
        "cache_buster": int(datetime.now().timestamp())
    })

@app.post("/set_activity")
async def set_activity(activity: str = Form(...)):
    global current_activity, last_activity_ts, last_activity
    
    try:
        current_activity = activity.lower()
        
        # Save current activity
        with open('current_activity.txt', 'w') as file:
            file.write(current_activity)
        
        timestamp = datetime.now()
        ts = timestamp.strftime('%I:%M %p')
        date = datetime.now().strftime('%d-%b-%Y %I:%M:%p')
        
        # Update Telegram profile
        if current_activity == 'movies/series':
            new_bio = f'Watching movies/series at {ts}'
        elif current_activity == 'watching youtube':
            new_bio = f'Watching YouTube at {ts}'
        else:
            new_bio = f'Went to {current_activity} at {ts}'
        if current_bio:
            new_bio += ' | ' + current_bio
        
        try:
            run_telegram_async(update_telegram_profile(new_bio))
        except Exception as e:
            error_msg = f"Failed to run Telegram update: {str(e)}"
            print(error_msg)
            with open('logs.txt', 'a') as file:
                file.write(f'{datetime.now()}: {error_msg}\n')
        
        # Log activity
        with open('modern_activity_tracker.txt', 'a') as file:
            print(date, current_activity, file=file, sep=', ')
        
        # Update last activity info
        if last_activity_ts is not None:
            time_elapsed = timestamp - last_activity_ts
            elapsed_text = humanize_time(time_elapsed.total_seconds())
        else:
            elapsed_text = "N/A"
        
        last_activity_ts = timestamp
        last_activity = current_activity
        
        return {
            "success": True,
            "message": f"Activity set to: {current_activity}",
            "timestamp": ts,
            "elapsed_time": elapsed_text
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

@app.get("/status")
async def get_status():
    elapsed_text = "N/A"
    if last_activity_ts is not None:
        time_elapsed = datetime.now() - last_activity_ts
        elapsed_text = humanize_time(time_elapsed.total_seconds())
    
    return {
        "current_activity": current_activity,
        "last_activity": last_activity,
        "elapsed_time": elapsed_text,
        "username": username
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
