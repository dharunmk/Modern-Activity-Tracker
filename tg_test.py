import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from dotenv import load_dotenv
import os
load_dotenv()


async def get_user_bio(username_or_id):
    """Fetch bio for a user or channel"""
    async with TelegramClient('telethon_session', os.getenv('API_ID'), os.getenv('API_HASH')) as client:
        try:
            # Try to get entity (user or channel)
            entity = await client.get_entity(username_or_id)
            
            # Get full information including bio
            if hasattr(entity, 'username') or hasattr(entity, 'first_name'):
                # It's a user
                full_user = await client(GetFullUserRequest(entity))
                bio = full_user.full_user.about if full_user.full_user.about else "No bio available"
                return {
                    'type': 'user',
                    'username': getattr(entity, 'username', 'No username'),
                    'first_name': getattr(entity, 'first_name', ''),
                    'last_name': getattr(entity, 'last_name', ''),
                    'bio': bio
                }
          
                
        except Exception as e:
            return {'error': str(e)}

async def main():
    """Main function to demonstrate bio fetching"""
    # read from username.txt
    with open('username.txt', 'r') as file:
        username  = file.read()
    
    result = await get_user_bio(username)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Type: {result['type']}")
        if result['type'] == 'user':
            print(f"Name: {result['first_name']} {result['last_name']}")
            print(f"Username: {result['username']}")
        else:
            print(f"Title: {result['title']}")
            print(f"Username: {result['username']}")
        print(f"Bio: {result['bio']}")

if __name__ == "__main__":
    # Run the async function
    asyncio.run(main())
