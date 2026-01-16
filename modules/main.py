import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess
import urllib.parse
import yt_dlp
import cloudscraper
from logs import logging
from bs4 import BeautifulSoup
import core as helper
from logs import logging
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN, LOG, auth_users
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

photologo = 'https://tinypic.host/images/2025/02/07/DeWatermark.ai_1738952933236-1.png'
photoyt = 'https://tinypic.host/images/2025/03/18/YouTube-Logo.wine.png'

async def show_random_emojis(message):
    emojis = ['🐼', '🐶', '🐅', '⚡️', '🚀', '✨', '💥', '☠️', '🥂', '🍾']
    emoji_message = await message.reply_text(' '.join(random.choices(emojis, k=1)))
    return emoji_message
    
credit ="🇳‌🇮‌🇰‌🇭‌🇮‌🇱‌" 
OWNER = int(os.environ.get("OWNER", 7385595817))
try: 
    ADMINS=[] 
    for x in (os.environ.get("ADMINS", "7385595817").split()):  
        ADMINS.append(int(x)) 
except ValueError: 
        raise Exception("Your Admins list does not contain valid integers.") 
ADMINS.append(OWNER)

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

cookies_file_path = "youtube_cookies.txt"
failed_links = []  # List to store failed links
fail_cap =f"**➜ This file Contain Failed Downloads while Downloding \n You Can Retry them one more time **"

# Define aiohttp routes
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("https://text-leech-bot-for-render.onrender.com/")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def start_bot():
    await bot.start()
    print("Bot is up and running")

async def stop_bot():
    await bot.stop()

async def main():
    if WEBHOOK:
        # Start the web server
        app_runner = web.AppRunner(await web_server())
        await app_runner.setup()
        site = web.TCPSite(app_runner, "0.0.0.0", PORT)
        await site.start()
        print(f"Web server started on port {PORT}")

    # Start the bot
    await start_bot()

    # Keep the program running
    try:
        while True:
            await bot.polling()  # Run forever, or until interrupted
    except (KeyboardInterrupt, SystemExit):
        await stop_bot()
    

async def start_bot():
    await bot.start()
    print("Bot is up and running")

async def stop_bot():
    await bot.stop()

async def main():
    if WEBHOOK:
        # Start the web server
        app_runner = web.AppRunner(await web_server())
        await app_runner.setup()
        site = web.TCPSite(app_runner, "0.0.0.0", PORT)
        await site.start()
        print(f"Web server started on port {PORT}")

    # Start the bot
    await start_bot()

    # Keep the program running
    try:
        while True:
            await asyncio.sleep(3600)  # Run forever, or until interrupted
    except (KeyboardInterrupt, SystemExit):
        await stop_bot()
        
import random

# Inline keyboard for start command
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="📞 Contact", url="https://t.me/Nikhil_saini_khe"),
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/+3k-1zcJxINYwNGZl"),
        ],
    ]
)

# Inline keyboard for busy status
Busy = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="📞 Contact", url="https://t.me/Nikhil_saini_khe"),
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/+3k-1zcJxINYwNGZl"),
        ],
    ]
)

# Image URLs for the random image feature
image_urls = [
    "https://tinypic.host/images/2025/02/07/IMG_20250207_224444_975.jpg",
    "https://tinypic.host/images/2025/02/07/DeWatermark.ai_1738952933236-1.png",
    # Add more image URLs as needed
        ]

@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    await m.reply_text(
        "Please upload the cookies file (.txt format).",
        quote=True
    )

    try:
        # Wait for the user to send the cookies file
        input_message: Message = await client.listen(m.chat.id)

        # Validate the uploaded file
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return

        # Download the cookies file
        downloaded_path = await input_message.download()

        # Read the content of the uploaded file
        with open(downloaded_path, "r") as uploaded_file:
            cookies_content = uploaded_file.read()

        # Replace the content of the target cookies file
        with open(cookies_file_path, "w") as target_file:
            target_file.write(cookies_content)

        await input_message.reply_text(
            "✅ Cookies updated successfully.\n📂 Saved in `youtube_cookies.txt`."
        )

    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

@bot.on_message(filters.command(["logs"]) )
async def send_logs(bot: Client, m: Message):
    try:
        with open("logs.txt", "rb") as file:
            sent= await m.reply_text("**📤 Sending you ....**")
            await m.reply_document(document=file)
            await sent.delete(True)
    except Exception as e:
        await m.reply_text(f"Error sending logs: {e}")        

@bot.on_message(filters.command(["h2t"]))
async def add_channel(client, message: Message):
    user_id = str(message.from_user.id)
    # Inform the user to send the HTML file and its name
    await message.reply_text(
        "Please send your **HTML file** to convert **.txt file**! 📁\n\n"
    )

    try:
        # Wait for user to send HTML file
        input_message: Message = await bot.listen(message.chat.id)
        if not input_message.document:
            await message.reply_text(
                "🚨 **Error**: You need to send a valid **HTML file**. Please send a file with the `.html` extension."
            )
            return

        html_file_path = await input_message.download()

        # Ask the user for a custom file name
        await message.reply_text(
            "🔤 **Now, please provide the file name (without extension)**\n\n"
            "🔄**Please wait..5sec...⏳ for use default**"
        )

        # Wait for the custom file name input with a timeout of 5 seconds
        try:
            file_name_input: Message = await bot.listen(message.chat.id, timeout=5)
            custom_file_name = file_name_input.text.strip()
            await file_name_input.delete(True)
        except asyncio.TimeoutError:
            custom_file_name = "output"

        # If the user didn't provide a name, use the default one
        if not custom_file_name:
            custom_file_name = "output"
            
        await file_name_input.delete(True)

        # Process the HTML file and extract data
        with open(html_file_path, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            tables = soup.find_all('table')
            if not tables:
                await message.reply_text(
                    "🚨 **Error**: No tables found in the HTML file. Please ensure the HTML file contains valid data."
                )
                return

            videos = []
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 2:  # Ensure there's both a name and link
                        name = cols[0].get_text().strip()
                        link = cols[1].find('a')['href']
                        videos.append(f'{name}: {link}')

        # Create and send the .txt file with the custom name
        txt_file = os.path.splitext(html_file_path)[0] + f'_{custom_file_name}.txt'
        with open(txt_file, 'w') as f:
            f.write('\n'.join(videos))

        # Send the generated text file to the user with a pretty caption
        await message.reply_document(
            document=txt_file,
            caption=f"`{custom_file_name}.txt`\n\n"
        )

        # Remove the temporary text file after sending
        os.remove(txt_file)

    except Exception as e:
        # In case of any error, send a generic error message
        await message.reply_text(
            f"🚨 **An unexpected error occurred**: {str(e)}.\nPlease try again or contact support if the issue persists."
        )

@bot.on_message(filters.command(["t2h"]))
async def txt_to_html(client, message: Message):
    user_id = str(message.from_user.id)
    # Inform the user to send the .txt file to convert to .html
    await message.reply_text(
        "Please send the **.txt file** for convert into an **.html file**.\n\n"
    )

    try:
        # Wait for the user to send the .txt file
        input_message: Message = await bot.listen(message.chat.id)
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await message.reply_text(
                "🚨 **Error**: Please send a valid **.txt file** to convert into an **.html** file."
            )
            return

        txt_file_path = await input_message.download()

        # Ask the user for the custom file name
        await message.reply_text(
            "🔤 **Now, please provide the file name (without extension)**\n\n"
            "🔄**Please wait..5sec...⏳ for use default**"
        )

        # Wait for the custom file name input with a timeout of 5 seconds
        try:
            file_name_input: Message = await bot.listen(message.chat.id, timeout=5)
            custom_file_name = file_name_input.text.strip()
            await file_name_input.delete(True)
        except asyncio.TimeoutError:
            custom_file_name = "output"

        # If the user didn't provide a name, use the default one
        if not custom_file_name:
            custom_file_name = "output"

        # Read the contents of the .txt file
        with open(txt_file_path, 'r') as f:
            txt_content = f.readlines()

        # Convert the .txt content to HTML
        html_content = "<html>\n<body>\n"
        for line in txt_content:
            line = line.strip()
            if line.startswith("http"):
                html_content += f'<a href="{line}">{line}</a><br/>\n'
            else:
                html_content += f"{line}<br/>\n"
        html_content += "</body>\n</html>"

        # Save the HTML content to a new file
        html_file_path = os.path.join("downloads", f"{custom_file_name}.html")
        os.makedirs(os.path.dirname(html_file_path), exist_ok=True)
        with open(html_file_path, 'w') as f:
            f.write(html_content)

        # Send the generated HTML file to the user with a pretty caption
        await message.reply_document(
            document=html_file_path,
            caption=f"**Here is your HTML file**: `{custom_file_name}.html`\n\n"
        )

        # Remove the temporary files after sending
        os.remove(txt_file_path)
        os.remove(html_file_path)

    except Exception as e:
        # In case of any error, send a generic error message
        await message.reply_text(
            f"🚨 **An unexpected error occurred**: {str(e)}.\nPlease try again or contact support if the issue persists."
        )

@bot.on_message(filters.command(["t2t"]))
async def text_to_txt(client, message: Message):
    user_id = str(message.from_user.id)
    # Inform the user to send the text data and its desired file name
    await message.reply_text(
        "Please send the **text** to convert into a `.txt` file.\n\n"
    )

    try:
        # Wait for the user to send the text data
        input_message: Message = await bot.listen(message.chat.id)

        # Ensure the message contains text
        if not input_message.text:
            await message.reply_text(
                "🚨 **Error**: Please send valid text data to convert into a `.txt` file."
            )
            return

        text_data = input_message.text.strip()

        # Ask the user for the custom file name
        await message.reply_text(
            "🔤 **Now, please provide the file name (without extension)**\n\n"
            "🔄**Please wait..5sec...⏳ for use default**"
        )

        # Wait for the custom file name input with a timeout of 5 seconds
        try:
            inputn: Message = await bot.listen(message.chat.id, timeout=5)
            raw_textn = inputn.text
            await inputn.delete(True)
        except asyncio.TimeoutError:
            raw_textn = 'txt_file'

        if raw_textn == 'txt_file':
            custom_file_name = 'txt_file'
        else:
            custom_file_name = raw_textn
            
        # Create and save the .txt file with the custom name
        txt_file = os.path.join("downloads", f'{custom_file_name}.txt')
        os.makedirs(os.path.dirname(txt_file), exist_ok=True)  # Ensure the directory exists
        with open(txt_file, 'w') as f:
            f.write(text_data)

        # Send the generated text file to the user with a pretty caption
        await message.reply_document(
            document=txt_file,
            caption=f"**Here is your text file**: `{custom_file_name}.txt`\n\n"
        )

        # Remove the temporary text file after sending
        os.remove(txt_file)

    except Exception as e:
        # In case of any error, send a generic error message
        await message.reply_text(
            f"🚨 **An unexpected error occurred**: {str(e)}.\nPlease try again or contact support if the issue persists."
        )

# Define paths for uploaded file and processed file
UPLOAD_FOLDER = '/path/to/upload/folder'
EDITED_FILE_PATH = '/path/to/save/edited_output.txt'


@bot.on_message(filters.command(["e2t"]))
async def edit_txt(client, message: Message):
    user_id = str(message.from_user.id)
    # Prompt the user to upload the .txt file
    await message.reply_text(
        "🎉 **Welcome to the .txt File Editor!**\n\n"
        "Please send your `.txt` file containing subjects, links, and topics."
    )

    # Wait for the user to upload the file
    input_message: Message = await bot.listen(message.chat.id)
    if not input_message.document:
        await message.reply_text("🚨 **Error**: Please upload a valid `.txt` file.")
        return

    # Get the file name
    file_name = input_message.document.file_name.lower()

    # Define the path where the file will be saved
    uploaded_file_path = os.path.join(UPLOAD_FOLDER, file_name)

    # Download the file
    uploaded_file = await input_message.download(uploaded_file_path)

    # After uploading the file, prompt the user for the file name or 'd' for default
    await message.reply_text(
        "🔄 **Send your .txt file name, or type '/default' for the default file name.**"
    )

    # Wait for the user's response
    user_response: Message = await bot.listen(message.chat.id)
    if user_response.text:
        user_response_text = user_response.text.strip().lower()
        if user_response_text == '/default':
            # Handle default file name logic (e.g., use the original file name)
            final_file_name = file_name
        else:
            final_file_name = user_response_text + '.txt'
    else:
        final_file_name = file_name  # Default to the uploaded file name

    # Read and process the uploaded file
    try:
        with open(uploaded_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to read the file.\n\nDetails: {e}")
        return

    # Parse the content into subjects with links and topics
    subjects = {}
    current_subject = None
    for line in content:
        line = line.strip()
        if line and ":" in line:
            # Split the line by the first ":" to separate title and URL
            title, url = line.split(":", 1)
            title, url = title.strip(), url.strip()

            # Add the title and URL to the dictionary
            if title in subjects:
                subjects[title]["links"].append(url)
            else:
                subjects[title] = {"links": [url], "topics": []}

            # Set the current subject
            current_subject = title
        elif line.startswith("-") and current_subject:
            # Add topics under the current subject
            subjects[current_subject]["topics"].append(line.strip("- ").strip())

    # Sort the subjects alphabetically and topics within each subject
    sorted_subjects = sorted(subjects.items())
    for title, data in sorted_subjects:
        data["topics"].sort()

    # Save the edited file to the defined path with the final file name
    try:
        final_file_path = os.path.join(UPLOAD_FOLDER, final_file_name)
        with open(final_file_path, 'w', encoding='utf-8') as f:
            for title, data in sorted_subjects:
                # Write title and its links
                for link in data["links"]:
                    f.write(f"{title}:{link}\n")
                # Write topics under the title
                for topic in data["topics"]:
                    f.write(f"- {topic}\n")
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to write the edited file.\n\nDetails: {e}")
        return

    # Send the sorted and edited file back to the user
    try:
        await message.reply_document(
            document=final_file_path,
            caption="🎉 **Here is your edited .txt file with subjects, links, and topics sorted alphabetically!**"
        )
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to send the file.\n\nDetails: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)  



@bot.on_message(filters.command(["title"]))
async def run_bot(bot: Client, m: Message):
      editable = await m.reply_text("**Send Your TXT file with links**\n")
      input: Message = await bot.listen(editable.chat.id)
      txt_file = await input.download()
      await input.delete(True)
      await editable.delete()
      
      with open(txt_file, 'r') as f:
          lines = f.readlines()
      
      cleaned_lines = [line.replace('(', '').replace(')', '') for line in lines]
      
      cleaned_txt_file = os.path.splitext(txt_file)[0] + '_cleaned.txt'
      with open(cleaned_txt_file, 'w') as f:
          f.write(''.join(cleaned_lines))
      
      await m.reply_document(document=cleaned_txt_file,caption="Here is your cleaned txt file.")
      os.remove(cleaned_txt_file)

def process_links(links):
    processed_links = []
    
    for link in links.splitlines():
        if "m3u8" in link:
            processed_links.append(link)
        elif "mpd" in link:
            # Remove everything after and including '*'
            processed_links.append(re.sub(r'\*.*', '', link))
    
    return "\n".join(processed_links)

@bot.on_message(filters.command(["ytm"]))
async def txt_handler(bot: Client, m: Message):
    editable = await m.reply_text("🔹**Send me the TXT file containing YouTube links.**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await bot.send_document(OWNER, x)
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        os.remove(x)
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    await m.reply_text(
        f"**🔹ᴛᴏᴛᴀʟ 🔗 ʟɪɴᴋs ғᴏᴜɴᴅ ᴀʀᴇ --__{len(links)}__--**\n"
    )
    
    await editable.edit("**🔹sᴇɴᴅ ғʀᴏᴍ ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ**\n\n**🔹Please wait..10sec...⏳**\n\n**🔹For Download from Starting**")
    try:
        input0: Message = await bot.listen(editable.chat.id, timeout=10)
        raw_text = input0.text
        await input0.delete(True)
    except asyncio.TimeoutError:
        raw_text = '1'
        
        await editable.delete()

    await m.reply_text(
        f"**⚡Dᴏᴡɴʟᴏᴀᴅɪɴɢ Sᴛᴀʀᴛᴇᴅ...⏳**\n"
    )
    arg = int(raw_text)
    count = int(raw_text)
    try:
        for i in range(arg-1, len(links)):  # Iterate over each link

            Vxy = links[i][1].replace("www.youtube-nocookie.com/embed", "youtu.be")
            url = "https://" + Vxy

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "")
            name = f'{name1[:60]} 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎'

            if "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp -x --audio-format mp3 --cookies {cookies_file_path} "{url}" -o "{name}.mp3"'
                print(f"Running command: {cmd}")
                os.system(cmd)
                if os.path.exists(f'{name}.mp3'):
                   print(f"File {name}.mp3 exists, attempting to send...")
                   try:
                       await bot.send_document(chat_id=m.chat.id, document=f'{name}.mp3', caption=f'**🎵 Title : **  {name}.mp3\n\n🔗**Video link** : {url}\n\n🌟** Extracted By** : 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎')
                       os.remove(f'{name}.mp3')
                   except Exception as e:
                       print(f"Error sending document: {str(e)}")
                else:
                     print(f"File {name}.mp3 does not exist.")                
    except Exception as e:
        await m.reply_text(f"🚨 **An error occurred**: {str(e)}")
    finally:
        await m.reply_text("🕊️Done Baby💞")

@bot.on_message(filters.command(["y2t"]))
async def youtube_to_txt(client, message: Message):
    user_id = str(message.from_user.id)
    
    await message.reply_text(
        "<pre><code>Welcome to the YouTube to .txt🗃️ Converter!</code></pre>\n"
        "<pre><code>Please Send YouTube Playlist link for convert into a `.txt` file.</code></pre>\n"
    )

    try:
        # Wait for the user to send the YouTube link
        input_message: Message = await bot.listen(message.chat.id, timeout=10)

        # Ensure the message contains a YouTube link
        if not input_message.text:
            await message.reply_text(
                "🚨 **Error**: Please send a valid YouTube Playlist link to convert into a `.txt` file."
            )
            return

        youtube_link = input_message.text.strip()

        # Fetch the YouTube information using yt-dlp with cookies
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'skip_download': True,
            'force_generic_extractor': True,
            'forcejson': True,
            'cookies': 'youtube_cookies.txt'  # Specify the cookies file
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                result = ydl.extract_info(youtube_link, download=False)
                if 'entries' in result:
                    title = result.get('title', 'youtube_playlist')
                else:
                    title = result.get('title', 'youtube_video')
            except yt_dlp.utils.DownloadError as e:
                await message.reply_text(
                    f"🚨 **Error**: {str(e)}.\nPlease ensure the link is valid and try again."
                )
                return

        # Ask the user for the custom file name
        file_name_message = await message.reply_text(
            f"🔤 **Send file name (without extension)**\n\n"
            f"If you're using default to **'{title}'**.\n\n"
            f"🔁...Please wait...10sec...⏳"
        )

        # Wait for the custom file name input with a timeout of 10 seconds
        try:
            file_name_input: Message = await bot.listen(message.chat.id, timeout=10)
            custom_file_name = file_name_input.text.strip()
            await file_name_input.delete(True)
        except asyncio.TimeoutError:
            custom_file_name = title

        # If the user didn't provide a name, use the default one
        if not custom_file_name:
            custom_file_name = title

        await file_name_message.delete(True)

        # Extract the YouTube links
        videos = []
        if 'entries' in result:
            for entry in result['entries']:
                video_title = entry.get('title', 'No title')
                url = entry['url']
                videos.append(f"{video_title}: {url}")
        else:
            video_title = result.get('title', 'No title')
            url = result['url']
            videos.append(f"{video_title}: {url}")

        # Create and save the .txt file with the custom name
        txt_file = os.path.join("downloads", f'{custom_file_name}.txt')
        os.makedirs(os.path.dirname(txt_file), exist_ok=True)  # Ensure the directory exists
        with open(txt_file, 'w') as f:
            f.write('\n'.join(videos))

        # Send the generated text file to the user with a pretty caption
        await message.reply_document(
            document=txt_file,
            caption=f'<a href="{youtube_link}">__**Click Here to open Playlist**__</a>\n<pre><code>{custom_file_name}.txt</code></pre>\n'
        )

        # Remove the temporary text file after sending
        os.remove(txt_file)

    except Exception as e:
        # In case of any error, send a generic error message
        await message.reply_text(
            f"🚨 **An unexpected error occurred**: {str(e)}.\nPlease try again or contact support if the issue persists."
        )

@bot.on_message(filters.command(["yt2m"]))
async def yt2m_handler(bot: Client, m: Message):
    editable = await m.reply_text(f"🔹**Send me the YouTube link**\n")
    input: Message = await bot.listen(editable.chat.id)
    youtube_link = input.text.strip()
    await input.delete(True)

    Show = f"**⚡Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ...⏳**\n\n🔗𝐔𝐑𝐋 »  {youtube_link}\n\n✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ 🇸‌🇦‌🇮‌🇳‌🇮‌🐦"
    await editable.edit(Show, disable_web_page_preview=True)
    await asyncio.sleep(10)

    arg = 1
    count = 1
    try:
        Vxy = youtube_link.replace("www.youtube-nocookie.com/embed", "youtu.be")
        url = Vxy

        # Fetch the YouTube video title using oEmbed
        oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
        response = requests.get(oembed_url)
        
        # Log the response content to debug
        print("Response content:", response.content)

        audio_title = response.json().get('title', 'YouTube Video')

        name = f'{audio_title[:60]} 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎'
        
        if "youtube.com" in url or "youtu.be" in url:
            cmd = f'yt-dlp -x --audio-format mp3 --cookies {cookies_file_path} "{url}" -o "{name}.mp3"'
            print(f"Running command: {cmd}")
            os.system(cmd)
            if os.path.exists(f'{name}.mp3'):
                print(f"File {name}.mp3 exists, attempting to send...")
                try:
                    await editable.delete()
                    await bot.send_document(chat_id=m.chat.id, document=f'{name}.mp3', caption=f'**🎵 Title : **  {name}.mp3\n\n🔗**Video link** : {url}\n\n🌟** Extracted By** : 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎')
                    os.remove(f'{name}.mp3')
                except Exception as e:
                    print(f"Error sending document: {str(e)}")
            else:
                print(f"File {name}.mp3 does not exist.")
    except Exception as e:
        await m.reply_text(f"🚨 **An error occurred**: {str(e)}")

@bot.on_message(filters.command(["help"]))
async def txt_handler(client: Client, m: Message):
    await bot.send_message(m.chat.id, text= (
        "<pre><code> 🎉Congrats! You are using 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎:</code></pre>\n┣\n"
        "┣⪼01. Send /start - To Check Bot \n┣\n"
        "┣⪼02. Send /yt2m - YT mp3 Downloader by link \n┣\n"
        "┣⪼03. Send /ytm - YT mp3 Downloader by .txt \n┣\n"
        "┣⪼04. Send /y2t - YouTube to .txt Convert\n┣\n"
        "┣⪼05. Send /cookies - To update YT cookies.\n┣\n"
        "┣⪼06. Send /doc- Pdf & jpg downloader\n┣\n"
        "┣⪼07. Send /id - Your Telegram ID\n┣\n"
        "┣⪼08. Send /info - Your Telegram Info\n┣\n"
        "┣⪼09. Send /h2t - HTML to .txt Convert\n┣\n"
        "┣⪼10. Send /e2t - Txt in Alphabetically\n┣\n"
        "┣⪼11. Send /t2t - Text to .txt Convert\n┣\n"
        "┣⪼12. Send /title - Title Clean from Symbol\n┣\n"
        "┣⪼13. Send /logs - To see Bot Working Logs\n┣\n"
        "┣⪼14. Send /stop - Stop the Running Task. 🚫\n┣\n"
        "┣⪼🔗  Direct Send Link For Extract (with https://)\n┣\n"
        "If you have any questions, feel free to ask! 💬"
        )
    ) 


@bot.on_message(filters.command(["logs"]) )
async def send_logs(bot: Client, m: Message):
    if m.chat.id not in auth_users:
        print(f"User ID not in auth_users", m.chat.id)
        await bot.send_message(m.chat.id, f"__**OOPS! You are not a Premium User.")
        return
        
    try:
        with open("logs.txt", "rb") as file:
            sent= await m.reply_text("**📤 Sending you ....**")
            await m.reply_document(document=file)
            await sent.delete(True)
    except Exception as e:
        await m.reply_text(f"Error sending logs: {e}")

# INFO command handler                          
@bot.on_message(filters.private & filters.command(["info"]))
async def info(bot: Client, m: Message):
    text = f"""__**———✦Information✦———**__

**🙋🏻‍♂️ Your Name :** {m.from_user.first_name} {m.from_user.last_name if m.from_user.last_name else 'None'}
**🧑🏻‍🎓 Your Username :** @{m.from_user.username}
**🆔 Your Telegram ID :** {m.from_user.id}
**🔗 Your Profile Link :** {m.from_user.mention}"""
    
    await m.reply_text(        
        text=text,
        disable_web_page_preview=True,
    )

# ID command handler
@bot.on_message(filters.private & filters.command(["id"]))
async def id(bot: Client, update: Message):
    if update.chat.type == "channel":
        await update.reply_text(
            text=f"This Channel's ID: {update.chat.id}",
            disable_web_page_preview=True
        )
    else:
        await update.reply_text(        
            text=f"Your Telegram ID: {update.from_user.id}",
            disable_web_page_preview=True,
        )


# Start command handler
@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    # Send a loading message
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Loading... ⏳🔄"
    )
  
    # Choose a random image URL
    random_image_url = random.choice(image_urls)
    
    # Caption for the image
    caption = (
        "🌟 Welcome {0}! 🌟\n\n"
        "➽ I am Powerful DRM Uploader Bot 📥\n\n➽ 𝐔𝐬𝐞 /drm for use this Bot.\n\n➽ **ᴊᴏɪɴ ᴏᴜʀ <a href='https://t.me/+1e-r94cF6yE3NzA1'>__TG Channel__</a>**\n➽ **Add me in <a href='http://t.me/Mynkl_txt_bot?startchannel=true'>__Your Channel__</a>**\n➽ **Add me in <a href='http://t.me/Mynkl_txt_bot?startgroup=true'>__Your Group__</a>**\n\n<pre><code> 𝐌𝐚𝐝𝐞 𝐁𝐲 : 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎 🦁</code></pre>"
    )

    await asyncio.sleep(1)
    await loading_message.edit_text(
        "Initializing Uploader bot... 🤖\n\n"
        "Progress: ⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%\n\n"
    )

    await asyncio.sleep(1)
    await loading_message.edit_text(
        "Loading features... ⏳\n\n"
        "Progress: 🟥🟥⬜⬜⬜⬜⬜⬜ 25%\n\n"
    )
    
    await asyncio.sleep(1)
    await loading_message.edit_text(
        "This may take a moment, sit back and relax! 😊\n\n"
        "Progress: 🟧🟧🟧🟧⬜⬜⬜⬜ 50%\n\n"
    )

    await asyncio.sleep(1)
    await loading_message.edit_text(
        "Checking Bot Status... 🔍\n\n"
        "Progress: 🟨🟨🟨🟨🟨🟨⬜⬜ 75%\n\n"
    )

    await asyncio.sleep(1)
    await loading_message.edit_text(
        "Checking status Ok... \n**ᴊᴏɪɴ ᴏᴜʀ <a href='https://t.me/+1e-r94cF6yE3NzA1'>ᴛᴇʟᴇɢʀᴀᴍ Group</a>**\n\n"
        "Progress:🟩🟩🟩🟩🟩🟩🟩🟩🟩 100%\n\n"
    )
        
    # Send the image with caption and buttons
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_image_url,
        caption=caption.format(message.from_user.mention),
        reply_markup=keyboard
    )

    # Delete the loading message
    await loading_message.delete()

@bot.on_message(filters.command(["stop"]) )
async def restart_handler(_, m):
    await m.reply_text("<pre><code>⌈✨『𝚂𝚃𝙾𝙿𝙿𝙴𝙳』✨⌋</code></pre>", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["drm"]))
async def help_handler(client: Client, m: Message):
    await bot.send_message(m.chat.id, text= (
        "<pre><code> 🎉 Welcome to DRM Bot! 🎉</code></pre>\n\n"
        "You can have access to download all Non-DRM+AES Encrypted URLs 🔐 including:\n\n"
        "Send /help for free users.\n\n"
        "• 📚 Appx Zip+Encrypted Url\n"
        "• 🎓 Classplus DRM+ NDRM\n"
        "• 🧑‍🏫 PhysicsWallah DRM\n"
        "• 📚 CareerWill + PDF\n"
        "• 🎓 Khan GS\n"
        "• 🎓 Study Iq DRM\n"
        "• 🚀 APPX + APPX Enc PDF\n"
        "• 🎓 Vimeo Protection\n"
        "• 🎓 Brightcove Protection\n"
        "• 🎓 Visionias Protection\n"
        "• 🎓 Zoom Video\n"
        "• 🎓 Utkarsh Protection(Video + PDF)\n"
        "• 🎓 All Non DRM+AES Encrypted URLs\n"
        "• 🎓 MPD URLs if the key is known (e.g., Mpd_url?key=key XX:XX)\n\n"
        "🚀 You are not subscribed to any plan yet!\n\n"
        "<pre><code>Contact to 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎 for buy membership.</code></pre>"
    ))



@bot.on_message(filters.command(["saini"]) )
async def txt_handler(bot: Client, m: Message):
    editable = await m.reply_text(f"<pre><code>🔹Hi I am Poweful TXT Downloader📥 Bot.\n🔹Send me the txt file and wait.</code></pre>")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    credit = f"𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎"
    pdf_count = 0
    img_count = 0
    zip_count = 0
    video_count = 0
    
    try:    
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        
        links = []
        for i in content:
            if "://" in i:
                url = i.split("://", 1)[1]
                links.append(i.split("://", 1))
                if ".pdf" in url or ".PDF" in url:
                    pdf_count += 1
                elif url.endswith((".png", ".jpeg", ".jpg")):
                    img_count += 1
                elif ".zip" in url:
                    zip_count += 1
                elif ".mpd" in url:
                    mpd_count += 1
                elif ".m3u8" in url:
                    m3u8_count += 1   
                elif ".youtu" in url:
                    youtu_count += 1      
                else:
                    other_count += 1
        os.remove(x)
    except:
        await m.reply_text("<pre><code>🔹Invalid file input.</code></pre>")
        os.remove(x)
        return
   
    await editable.edit(f"`🔹Total 🔗 links found are {len(links)}\n\n🔹Image links : {img_count}\n🔹pdf links : {pdf_count}\n🔹zip links : {zip_count}\n🔹mpd links : {mpd_count}\n🔹m3u8 links : {m3u8_count}\n🔹youtube links : {youtu_count}\n🔹other links : {other_count}\n\n🔹Send From where you want to download.`")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)
    try:
        arg = int(raw_text)
    except:
        arg = 1
        
    await editable.edit("<pre><code>🔹Enter Your Batch Name\n🔹Send 1 for use default.</code></pre>")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == '1':
        b_name = file_name
    else:
        b_name = raw_text0

    await editable.edit(f"╭━━━━❰ᴇɴᴛᴇʀ ʀᴇꜱᴏʟᴜᴛɪᴏɴ❱━━➣\n"
                        f"┣━━⪼ send `144`  for 144p\n"
                        f"┣━━⪼ send `240`  for 240p\n"
                        f"┣━━⪼ send `360`  for 360p\n"
                        f"┣━━⪼ send `480`  for 480p\n"
                        f"┣━━⪼ send `720`  for 720p\n"
                        f"┣━━⪼ send `1080` for 1080p\n"
                        f"╰━━⌈⚡[`🦋🇸‌🇦‌🇮‌🇳‌🇮‌🦋`]⚡⌋━━➣")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    quality = f"{raw_text2}p"
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"

    

    await editable.edit("<pre><code>🔹Enter Your Name,Link\n🔹Send 1 for use default</code></pre>")
    input3 = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    # Default credit message with link
    credit = "️[𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎 🕊️](https://t.me/+MdZ2996M2G43MWFl)"
    if raw_text3 == '1':
        CR = '[𝙎𝘼𝙞𝙉𝙄 𝘽𝙊𝙏𝙎 🕊️](https://t.me/+MdZ2996M2G43MWFl)'
    elif raw_text3:
        try:
            text, link = raw_text3.split(',')
            CR = f'[{text.strip()}]({link.strip()})'
        except ValueError:
            CR = raw_text3  # In case the input is not in the expected format, use the raw text
    else:
        CR = credit

    pw_token = f"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NDI4NDE2NDAuNTQyLCJkYXRhIjp7Il9pZCI6IjY1OWZjZWU5YmI4YjFkMDAxOGFmYTExZCIsInVzZXJuYW1lIjoiODUzOTkyNjE5MCIsImZpcnN0TmFtZSI6IlNoaXR0dSIsImxhc3ROYW1lIjoiU2luZ2giLCJvcmdhbml6YXRpb24iOnsiX2lkIjoiNWViMzkzZWU5NWZhYjc0NjhhNzlkMTg5Iiwid2Vic2l0ZSI6InBoeXNpY3N3YWxsYWguY29tIiwibmFtZSI6IlBoeXNpY3N3YWxsYWgifSwiZW1haWwiOiJzaGl0dHVrdW1hcjM3QGdtYWlsLmNvbSIsInJvbGVzIjpbIjViMjdiZDk2NTg0MmY5NTBhNzc4YzZlZiJdLCJjb3VudHJ5R3JvdXAiOiJJTiIsInR5cGUiOiJVU0VSIn0sImlhdCI6MTc0MjIzNjg0MH0.oIubH2nR-onRJrzCAGcGU96tsmAzRYyXEnlaA4oIvcU"
  #  await editable.edit("<pre><code>🔹Enter Working PW Token For 𝐌𝐏𝐃 𝐔𝐑𝐋\n🔹Send  0  for use default</code></pre>")
   # input4: Message = await bot.listen(editable.chat.id)
  #  raw_text4 = input4.text
 #   await input4.delete(True)
  #  if raw_text4 == '0':
 #       PW = pw_token
 #   else:
 #       PW = raw_text4
        
    await editable.edit(f"01. 🌅Send ☞ Direct **Thumb Photo**\n\n"
                        f"02. 🔗Send ☞ `Thumb URL` for **Thumbnail**\n\n"
                        f"03. 🎞️Send ☞ `no` for **video** format\n\n"
                        f"04. 📁Send ☞ `No` for **Document** format")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    await m.reply_text(
        f"<pre><code>**🎯Target Batch :** `{b_name}`</code></pre>"
    )

    failed_count =0 
    count =int(raw_text)    
    try:
        for i in range(arg-1, len(links)):
            Vxy = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + Vxy
            link0 = "https://" + Vxy
            urlcpvod = "https://dragoapi.vercel.app/video/https://" + Vxy
            
            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
                
            elif "tencdn.classplusapp" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url or "media-cdn.classplusapp" in url:
             headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
             params = (('url', f'{url}'),)
             response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
             url = response.json()['url']

            elif 'videos.classplusapp' in url or "tencdn.classplusapp" in url or "webvideos.classplusapp.com" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url or "videos.classplusapp.com" in url or "media-cdn-a.classplusapp" in url or "media-cdn.classplusapp" in url or "alisg-cdn-a.classplusapp" in url:
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9r'}).json()['url']

            elif "webvideos.classplusapp." in url:
             cmd = f'yt-dlp --add-header "referer:https://web.classplusapp.com/" --add-header "x-cdn-tag:empty" -f "{ytf}" "{url}" -o "{name}.mp4"'
                                        
            elif "d1d34p8vz63oiq" in url or "sec1.pw.live" in url:
             id =  url.split("/")[-2]
             url = f"https://dl.alphacbse.site/download/{id}/master.m3u8"
             #url = f"- https://anonymouspwplayerr-c96de7802811.herokuapp.com/pw?url={url}&token={pw_token}"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{name1[:60]}'
            
            #if 'cpvod.testbook.com' in url:
               #url = requests.get(f'http://api.masterapi.tech/akamai-player-v3?url={url}', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9r'}).json()['url']
               #url0 = f"https://dragoapi.vercel.app/video/{url}"
                
            if "/master.mpd" in url:
                cmd= f" yt-dlp -k --allow-unplayable-formats -f bestvideo.{quality} --fixup never {url} "
                print("counted")

            if "edge.api.brightcove.com" in url:
                bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                url = url.split("bcov_auth")[0]+bcov

            if 'khansirvod4.pc.cdn.bitgravity.com' in url:               
               parts = url.split('/')               
               part1 = parts[1]
               part2 = parts[2]
               part3 = parts[3] 
               part4 = parts[4]
               part5 = parts[5]
               
               print(f"PART1: {part1}")
               print(f"PART2: {part2}")
               print(f"PART3: {part3}")
               print(f"PART4: {part4}")
               print(f"PART5: {part5}")
               url = f"https://kgs-v4.akamaized.net/kgs-cv/{part3}/{part4}/{part5}"
                   
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
            
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'

            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}".mp4'

            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:  
                cc = f'**——— ✨ [{str(count).zfill(3)}]({link0}) ✨ ———**\n\n🎞️𝐓𝐢𝐭𝐥𝐞 » `{name1}`\n**├── 𝙴𝚡𝚝𝚎𝚗𝚜𝚒𝚘𝚗 »**  🇳‌🇮‌🇰‌🇭‌🇮‌🇱‌.mkv\n**├── 𝚁𝚎𝚜𝚘𝚕𝚞𝚝𝚒𝚘𝚗 »** `[{res}]`\n\n<pre><code>📚 Course » {b_name}</code></pre>\n\n🌟𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 » {CR}\n'
                cc1 = f'**——— ✨ [{str(count).zfill(3)}]({link0}) ✨ ———**\n\n📕𝐓𝐢𝐭𝐥𝐞 » `{name1}`\n**├── 𝙴𝚡𝚝𝚎𝚗𝚜𝚒𝚘𝚗 »**  🇸‌🇦‌🇮‌🇳‌🇮‌.pdf\n\n<pre><code>📚 Course » {b_name}</code></pre>\n\n🌟𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 » {CR}\n'
                cczip = f'**——— ✨ [{str(count).zfill(3)}]({link0}) ✨ ———**\n\n📁𝐓𝐢𝐭𝐥𝐞 » `{name1}`\n**├── 𝙴𝚡𝚝𝚎𝚗𝚜𝚒𝚘𝚗 »**  🇳‌🇮‌🇰‌🇭‌🇮‌🇱‌.zip\n\n<pre><code>📚 Course » {b_name}</code></pre>\n\n🌟𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 » {CR}\n'
                ccimg = f'**——— ✨ [{str(count).zfill(3)}]({link0}) ✨ ———**\n\n🖼️𝐓𝐢𝐭𝐥𝐞 » `{name1}`\n**├── 𝙴𝚡𝚝𝚎𝚗𝚜𝚒𝚘𝚗 »**  🇸‌🇦‌🇮‌🇳‌🇮‌.jpg\n\n<pre><code>📚 Course » {b_name}</code></pre>\n\n🌟𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 » {CR}\n'
                ccyt = f'**——— ✨ [{str(count).zfill(3)}]({link0}) ✨ ———**\n\n🎞️𝐓𝐢𝐭𝐥𝐞 » `{name1}`\n**├── 𝙴𝚡𝚝𝚎𝚗𝚜𝚒𝚘𝚗 »**  🇳‌🇮‌🇰‌🇭‌🇮‌🇱‌.mkv\n**├── Resolution :** `[{res}]`\n**├── Video link :** {url}\n\>📚 Course » {b_name}\n\n🌟𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 » {CR}\n'
                ccm = f'**——— ✨ [{str(count).zfill(3)}]({link0}) ✨ ———**\n\n🎞️🎵𝐢𝐭𝐥𝐞 » `{name1}`\n**├── 𝙴𝚡𝚝𝚎𝚗𝚜𝚒𝚘𝚗 »**  🇸‌🇦‌🇮‌🇳‌🇮‌.mp3\n\n<pre><code>📚 Course » {b_name}</code></pre>\n\n🌟𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 » {CR}\n'
                cccpvod = f'——— ✨ [{str(count).zfill(3)}]({link0}) ✨ ———\n\n🎞️𝐓𝐢𝐭𝐥𝐞 » `{name1}` .mp4\n\n<a href="{urlcpvod}">__**Click Here to Watch Stream**__</a>\n🔗𝐋𝐢𝐧𝐤 » {link0}\n\n<pre><code>📚 Course : {b_name}</code></pre>\n\n🌟𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 » {CR}\n'
                
                
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count+=1
                        continue

                elif ".pdf*" in url:
                    try:
                        url_part, key_part = url.split("*")
                        url = f"https://dragoapi.vercel.app/pdf/{url_part}*{key_part}"
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        continue   

                elif ".pdf" in url:
                    try:
                        await asyncio.sleep(4)
                        url = url.replace(" ", "%20")
                        scraper = cloudscraper.create_scraper()
                        response = scraper.get(url)
                        if response.status_code == 200:
                            with open(f'{name}.pdf', 'wb') as file:
                                file.write(response.content)
                            await asyncio.sleep(4)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1
                            os.remove(f'{name}.pdf')
                        else:
                            await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        continue

                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        continue

                elif any(ext in url for ext in [".mp3", ".wav", ".m4a"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -x --audio-format {ext} -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        await bot.send_document(chat_id=m.chat.id, document=f'{name}.{ext}', caption=ccm)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif any(ext in url for ext in [".jpg", ".png", ".jpeg"]):
                    try:
                        cmd = f'yt-dlp -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_photo(chat_id=m.chat.id, document=f'{name}.{ext}', caption=ccimg)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        continue

                elif "cpvod.testbook.com" in url:
                    try:
                        await bot.send_photo(chat_id=m.chat.id, photo=photologo, caption=cccpvod)
                        count +=1
                    except Exception as e:
                        await m.reply_text(str(e))    
                        time.sleep(1)    
                        continue          

                #elif "youtu" in url:
                    #try:
                        #await bot.send_photo(chat_id=m.chat.id, photo=photoyt, caption=ccyt)
                        #count +=1
                    #except Exception as e:
                        #await m.reply_text(str(e))    
                        #time.sleep(1)    
                        #continue
     
                else:
                    remaining_links = len(links) - count
                    progress = (count / len(links)) * 100
                    emoji_message = await show_random_emojis(message)
                    Show = f"🚀𝐏𝐑𝐎𝐆𝐑𝐄𝐒𝐒 » {progress:.2f}%\n┃\n" \
                           f"┣🔗𝐈𝐧𝐝𝐞𝐱 » {str(count)}/{len(links)}\n┃\n" \
                           f"╰━🖇️𝐑𝐞𝐦𝐚𝐢𝐧𝐢𝐧𝐠 𝐋𝐢𝐧𝐤𝐬 » {remaining_links}\n\n" \
                           f"**⚡Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ...⏳**\n┃\n" \
                           f'┣💃𝐂𝐫𝐞𝐝𝐢𝐭 » {CR}\n┃\n' \
                           f'╰━📚𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 » `{b_name}`\n\n' \
                           f"📔𝐓𝐢𝐭𝐥𝐞 » `{name}`\n┃\n" \
                           f"┣🍁𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » {raw_text2}p\n┃\n" \
                           f'┣━🔗𝐋𝐢𝐧𝐤 » <a href="{url}">__**Click Here to Open Link**__</a>\n┃\n' \
                           f'╰━━🖼️𝐓𝐡𝐮𝐦𝐛𝐧𝐚𝐢𝐥 » <a href="{raw_text6}">__**Thumb Link**__</a>\n\n' \
                           f"➽ 𝐔𝐬𝐞 /stop for stop the Bot.\n\n" \
                           f"➽ 𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ `𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎🐦`"
                    prog = await m.reply_text(Show, disable_web_page_preview=True)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await emoji_message.delete()
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(f'——— ✨ [{str(count).zfill(3)}]({link0}) ✨ ———\n\n'
                                   f'👹 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝\n\n'
                                   f'📔 𝐓𝐢𝐭𝐥𝐞 » `{name}`\n\n'
                                   f'🔗 𝐋𝐢𝐧𝐤 » <a href="{link0}">__**Click Here to See Link**__</a>\n\n'
                                   f'📚 𝐂𝐨𝐮𝐫𝐬𝐞 » `{b_name}`\n\n'
                                   f'✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ `🇸‌🇦‌🇮‌🇳‌🇮‌🐦`')
                failed_links.append(f"{name1} : {link0}")
                count += 1
                failed_count += 1
                continue

    except Exception as e:
        await m.reply_text(e)
    time.sleep(2)

    if failed_links:
     error_file_send = await m.reply_text("**📤 Sending you Failed Downloads List **")
     with open("failed_downloads.txt", "w") as f:
        for link in failed_links:
            f.write(link + "\n")
    # After writing to the file, send it
     await m.reply_document(document="failed_downloads.txt", caption=fail_cap)
     await error_file_send.delete()
     failed_links.clear()
     os.remove(f'failed_downloads.txt')
    await m.reply_text(f"`✨𝙱𝚊𝚝𝚌𝚑 𝚂𝚞𝚖𝚖𝚊𝚛𝚢✨\n"
                       f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                       f"🔢𝙸𝚗𝚍𝚎𝚡 𝚁𝚊𝚗𝚐𝚎 » ({raw_text} to {len(links)})\n"
                       f"📚𝙱𝚊𝚝𝚌𝚑 𝙽𝚊𝚖𝚎 » {b_name}\n"
                       f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                       f"✨𝚃𝚡𝚝 𝚂𝚞𝚖𝚖𝚊𝚛𝚢✨ : {len(links)}\n"
                       f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                       f"🔹𝚉𝙸𝙿 » {zip_count}  🔹𝙿𝙳𝙵 » {pdf_count}\n"
                       f"🔹𝙸𝚖𝚐 » {img_count}  🔹𝚈𝚃 » {youtu_count}\n"
                       f"🔹𝙼𝚙𝚍 » {mpd_count}  🔹𝙾𝚝𝚑𝚎𝚛 » {other_count}\n"
                       f"🔹𝙼𝟹𝚞𝟾 » {m3u8_count}\n"
                       f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                       f"🔹𝙵𝚊𝚒𝚕𝚎𝚍 𝙻𝚒𝚗𝚔𝚜 » {failed_count}\n"
                       f"✅𝚂𝚝𝚊𝚝𝚞𝚜 » 𝙲𝚘𝚖𝚙𝚕𝚎𝚝𝚎𝚍`")
    await m.reply_text("<pre><code>Downloaded By ⌈✨『𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎』✨⌋</code></pre>")

    
    
@bot.on_message(filters.command(["doc"]) )
async def txt_handler(bot: Client, m: Message):
    editable = await m.reply_text(f"**🔹Hi I am TXT to Doc Downloader📥 Bot.**\n🔹**Send me the TXT file and wait.**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await bot.send_document(OWNER, x)
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    credit = f"𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎"
    pw_token = f"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3Mzk5MzM0MzkuMzQxLCJkYXRhIjp7Il9pZCI6IjYyM2ZjYjY5YjYxZTYzMDAxMWYyZWYzNiIsInVzZXJuYW1lIjoiOTYyMjE5NDczNCIsImZpcnN0TmFtZSI6Ik1vaGQiLCJsYXN0TmFtZSI6IlJpendhbiIsIm9yZ2FuaXphdGlvbiI6eyJfaWQiOiI1ZWIzOTNlZTk1ZmFiNzQ2OGE3OWQxODkiLCJ3ZWJzaXRlIjoicGh5c2ljc3dhbGxhaC5jb20iLCJuYW1lIjoiUGh5c2ljc3dhbGxhaCJ9LCJlbWFpbCI6Im1yaXp1dXUxMjNAZ21haWwuY29tIiwicm9sZXMiOlsiNWIyN2JkOTY1ODQyZjk1MGE3NzhjNmVmIl0sImNvdW50cnlHcm91cCI6IklOIiwidHlwZSI6IlVTRVIifSwiaWF0IjoxNzM5MzI4NjM5fQ.D3pMPQYyeNVI-TsmaBo3fquey5ys5UY_lQ44HqKnj1Q"
    try:    
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        os.remove(x)
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return
    
    await editable.edit(f"**🔹ᴛᴏᴛᴀʟ 🔗 ʟɪɴᴋs ғᴏᴜɴᴅ ᴀʀᴇ --__{len(links)}__--**\n\n**🔹sᴇɴᴅ ғʀᴏᴍ ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ**\n\n**🔹Please wait..10sec...⏳**\n\n**🔹For Download from Starting**")
    try:
        input0: Message = await bot.listen(editable.chat.id, timeout=10)
        raw_text = input0.text
        await input0.delete(True)
    except asyncio.TimeoutError:
        raw_text = '1'

        try:
            arg = int(raw_text)
        except:
            arg = 1

    await editable.edit(f"**🔹Enter Batch Name**\n\n**🔹Please wait...10sec...⏳ for use**\n\n🔹𝐍𝐚𝐦𝐞 » __**{file_name}__**")
    try:
        input1: Message = await bot.listen(editable.chat.id, timeout=10)
        raw_text0 = input1.text
        await input1.delete(True)
    except asyncio.TimeoutError:
        raw_text0 = '/default'
    
    if raw_text0 == '/default':
        b_name = file_name
    else:
        b_name = raw_text0
    
    await editable.edit("**🔹Enter Your Name**\n\n**🔹Please wait..10sec...⏳ for use default**")
    try:
        input3: Message = await bot.listen(editable.chat.id, timeout=10)
        raw_text3 = input3.text
        await input3.delete(True)
    except asyncio.TimeoutError:
        raw_text3 = '/admin'

    # Default credit message
    credit = "️𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎 🕊️⁪⁬⁮⁮⁮"
    if raw_text3 == '/admin':
        CR = '𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎 🕊️'
    elif raw_text3:
        CR = raw_text3
    else:
        CR = credit
        
    await editable.delete()
    await m.reply_text(
        f"__**🎯Target Batch :  {b_name} **__"
    )

    count =int(raw_text)    
    try:
        for i in range(arg-1, len(links)):
            Vxy = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + Vxy

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{name1[:60]} 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎'

            try:  
                cc1 = f'**[📕]Pdf Id  ➠** {str(count).zfill(3)}\n**[📁]Tᴏᴘɪᴄ ➠** `{name1} .pdf`\n\n<pre><code>**📚 Course ➠** {b_name}</code></pre>\n\n** 🌟 Extracted By : {CR}**'                 
                ccimg = f'**——— ✦  {str(count).zfill(3)} ✦ ———**\n\n** Title : **  `{name1} .jpg`\n\n<pre><code>**📚 Course :** {b_name}</code></pre>\n\n**🌟 Extracted By : {CR}**' 
                ccm = f'**——— ✦  {str(count).zfill(3)} ✦ ———**\n\n**🎵 Title : **  `{name1} .mp3`\n\n<pre><code>**📚 Course :** {b_name}</code></pre>\n\n**🌟 Extracted By : {CR}**' 
            
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count+=1
                        pass

                elif ".pdf*" in url:
                    try:
                        url_part, key_part = url.split("*")
                        url = f"https://dragoapi.vercel.app/pdf/{url_part}*{key_part}"
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        pass

                elif ".pdf" in url:
                    try:
                        await asyncio.sleep(4)
        # Replace spaces with %20 in the URL
                        url = url.replace(" ", "%20")
 
        # Create a cloudscraper session
                        scraper = cloudscraper.create_scraper()

        # Send a GET request to download the PDF
                        response = scraper.get(url)

        # Check if the response status is OK
                        if response.status_code == 200:
            # Write the PDF content to a file
                            with open(f'{name}.pdf', 'wb') as file:
                                file.write(response.content)

            # Send the PDF document
                            await asyncio.sleep(4)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1

            # Remove the PDF file after sending
                            os.remove(f'{name}.pdf')
                        else:
                            await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        pass

                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        pass

                elif any(ext in url for ext in [".mp3", ".wav", ".m4a"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -x --audio-format {ext} -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        await bot.send_document(chat_id=m.chat.id, document=f'{name}.{ext}', caption=ccm)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        pass

                elif any(ext in url for ext in [".jpg", ".jpeg", ".png"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_photo(chat_id=m.chat.id, photo=f'{name}.{ext}', caption=ccimg)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        pass
                                
            except Exception as e:
                    Error= f"⚠️ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝\n\n"
                    await m.reply_text(Error, disable_web_page_preview=True)
                    count += 1
                    pass

    except Exception as e:
        await m.reply_text(e)

@bot.on_message(filters.text & filters.private)
async def text_handler(bot: Client, m: Message):
    if m.from_user.is_bot:
        return
    links = m.text
    match = re.search(r'https?://\S+', links)
    if match:
        link = match.group(0)
    else:
        await m.reply_text("<pre><code>Invalid link format.</code></pre>")
        return
        
    editable = await m.reply_text(f"<pre><code>**🔹Processing your link...\n🔁Please wait...⏳**</code></pre>")
    await m.delete()

    await editable.edit(f"╭━━━━❰ᴇɴᴛᴇʀ ʀᴇꜱᴏʟᴜᴛɪᴏɴ❱━━➣\n"
                        f"┣━━⪼ send `144`  for 144p\n"
                        f"┣━━⪼ send `240`  for 240p\n"
                        f"┣━━⪼ send `360`  for 360p\n"
                        f"┣━━⪼ send `480`  for 480p\n"
                        f"┣━━⪼ send `720`  for 720p\n"
                        f"┣━━⪼ send `1080` for 1080p\n"
                        f"╰━━⌈⚡[`🦋🇸‌🇦‌🇮‌🇳‌🇮‌🦋`]⚡⌋━━➣")
    input2: Message = await bot.listen(editable.chat.id, filters=filters.text & filters.user(m.from_user.id))
    raw_text2 = input2.text
    quality = f"{raw_text2}p"
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
          
    pw_token = f"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NDI4NDE2NDAuNTQyLCJkYXRhIjp7Il9pZCI6IjY1OWZjZWU5YmI4YjFkMDAxOGFmYTExZCIsInVzZXJuYW1lIjoiODUzOTkyNjE5MCIsImZpcnN0TmFtZSI6IlNoaXR0dSIsImxhc3ROYW1lIjoiU2luZ2giLCJvcmdhbml6YXRpb24iOnsiX2lkIjoiNWViMzkzZWU5NWZhYjc0NjhhNzlkMTg5Iiwid2Vic2l0ZSI6InBoeXNpY3N3YWxsYWguY29tIiwibmFtZSI6IlBoeXNpY3N3YWxsYWgifSwiZW1haWwiOiJzaGl0dHVrdW1hcjM3QGdtYWlsLmNvbSIsInJvbGVzIjpbIjViMjdiZDk2NTg0MmY5NTBhNzc4YzZlZiJdLCJjb3VudHJ5R3JvdXAiOiJJTiIsInR5cGUiOiJVU0VSIn0sImlhdCI6MTc0MjIzNjg0MH0.oIubH2nR-onRJrzCAGcGU96tsmAzRYyXEnlaA4oIvcU"
   # await editable.edit("<pre><code>**Enter Your PW Token For 𝐌𝐏𝐃 𝐔𝐑𝐋**</code></pre>\n<pre><code>Send  `0`  for use default</code></pre>")
#    input4: Message = await bot.listen(editable.chat.id, filters=filters.text & filters.user(m.from_user.id))
#    raw_text4 = input4.text
#    await input4.delete(True)
 #   if raw_text4 == '0':
#        PW = pw_token
#    else:
  #      PW = raw_text4
        
    await editable.edit(f"01. 🌅Send ☞ Direct **Thumb Photo**\n\n"
                        f"02. 🔗Send ☞ `Thumb URL` for **Thumbnail**\n\n"
                        f"03. 🎞️Send ☞ `no` for **video** format\n\n"
                        f"04. 📁Send ☞ `No` for **Document** format")
    input6 = message = await bot.listen(editable.chat.id, filters=filters.text & filters.user(m.from_user.id))
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    count =1 
    arg =1
    try:
            Vxy = link.replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = Vxy
            linkcpvod = "https://dragoapi.vercel.app/video/" + Vxy
        
            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
                

            elif "tencdn.classplusapp" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url or "media-cdn.classplusapp" in url:
             headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
             params = (('url', f'{url}'),)
             response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
             url = response.json()['url']

            elif 'videos.classplusapp' in url or "tencdn.classplusapp" in url or "webvideos.classplusapp.com" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url or "videos.classplusapp.com" in url or "media-cdn-a.classplusapp" in url or "media-cdn.classplusapp" in url or "alisg-cdn-a.classplusapp" in url:
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9r'}).json()['url']

            elif "webvideos.classplusapp." in url:
             cmd = f'yt-dlp --add-header "referer:https://web.classplusapp.com/" --add-header "x-cdn-tag:empty" -f "{ytf}" "{url}" -o "{name}.mp4"'

            elif "d1d34p8vz63oiq" in url or "sec1.pw.live" in url:
             id =  url.split("/")[-2]
             url = f"https://dl.alphacbse.site/download/{id}/master.m3u8"
             #url = f"https://anonymouspwplayer-b99f57957198.herokuapp.com/pw?url={url}?token={PW}"

            name1 = links.replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{name1[:20]}'
            
            #if 'cpvod.testbook.com' in url:
               #data = requests.get(f"https://api.masterapi.tech/get/get-hls-key?token=eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9r").json()
               #url = f"http://api.masterapi.tech/akamai-player-v3?url={url}&hls-key={data}"
               #url0 = f"https://dragoapi.vercel.app/video/{url}"
                
            if "/master.mpd" in url:
                cmd= f" yt-dlp -k --allow-unplayable-formats -f bestvideo.{quality} --fixup never {url} "
                print("counted")

            if "edge.api.brightcove.com" in url:
                bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                url = url.split("bcov_auth")[0]+bcov
                
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
            
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'

            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}".mp4'

            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:
                cc = f'🎞️𝐓𝐢𝐭𝐥𝐞 » `{name}` [{res}].mp4\n🔗𝐋𝐢𝐧𝐤 » <a href="{link}">__**CLICK HERE**__</a>\n\n🌟𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 » `𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎`'
                cc1 = f'📕𝐓𝐢𝐭𝐥𝐞 » `{name}`\n🔗𝐋𝐢𝐧𝐤 » <a href="{link}">__**CLICK HERE**__</a>\n\n🌟𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 » `𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎`'
                ccyt = f'🎞️𝐓𝐢𝐭𝐥𝐞 » `{name}` .mp4\n🔗𝐋𝐢𝐧𝐤 » <a href="{link}">__**Click Here to Watch Stream**__</a>\n\n🌟𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 » `𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎`'
                cccpvod = f'🎞️𝐓𝐢𝐭𝐥𝐞 » `{name}` .mp4\n<a href="{linkcpvod}">__**Click Here to Watch Stream**__</a>\n🔗𝐋𝐢𝐧𝐤 » {link}\n🌟𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 » `𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎`'
                
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count+=1
                        pass

                elif ".pdf*" in url:
                    try:
                        url_part, key_part = url.split("*")
                        url = f"https://dragoapi.vercel.app/pdf/{url_part}*{key_part}"
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        pass    

                elif ".pdf" in url:
                    try:
                        await asyncio.sleep(4)
        # Replace spaces with %20 in the URL
                        url = url.replace(" ", "%20")
 
        # Create a cloudscraper session
                        scraper = cloudscraper.create_scraper()

        # Send a GET request to download the PDF
                        response = scraper.get(url)

        # Check if the response status is OK
                        if response.status_code == 200:
            # Write the PDF content to a file
                            with open(f'{name}.pdf', 'wb') as file:
                                file.write(response.content)

            # Send the PDF document
                            await asyncio.sleep(4)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1

            # Remove the PDF file after sending
                            os.remove(f'{name}.pdf')
                        else:
                            await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        pass

                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        pass    

                elif "cpvod.testbook.com" in url:
                    try:
                        await bot.send_photo(chat_id=m.chat.id, photo=photologo, caption=cccpvod)
                        count +=1
                    except Exception as e:
                        await m.reply_text(str(e))    
                        time.sleep(1)    
                        pass          

                #elif "youtu" in url:
                    #try:
                        #await bot.send_photo(chat_id=m.chat.id, photo=photoyt, caption=ccyt)
                        #count +=1
                    #except Exception as e:
                        #await m.reply_text(str(e))    
                        #time.sleep(1)    
                        #pass

                elif ".zip" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.zip" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.zip', caption=cc1)
                        count += 1
                        os.remove(f'{name}.zip')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        pass    

                elif any(ext in url for ext in [".mp3", ".wav", ".m4a"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -x --audio-format {ext} -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        await bot.send_document(chat_id=m.chat.id, document=f'{name}.{ext}', caption=cc1)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        pass

                elif any(ext in url for ext in [".jpg", ".jpeg", ".png"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_photo(chat_id=m.chat.id, photo=f'{name}.{ext}', caption=cc1)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        pass
                                
                else:
                    emoji_message = await show_random_emojis(message)
                    Show = f"<pre><code>**⚡Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ...⏳**</code></pre>\n🔗𝐋𝐢𝐧𝐤 » `{link}`\n<pre><code>✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ `🇸‌🇦‌🇮‌🇳‌🇮‌🐦`</code></pre>"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await emoji_message.delete()
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                    Error= f"<pre><code>⚠️𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝</code></pre>\n📚𝐓𝐢𝐭𝐥𝐞 » `{name}`\n\n🔗𝐋𝐢𝐧𝐤 » `{link}`\n<pre><code>✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ `🇸‌🇦‌🇮‌🇳‌🇮‌🐦`</code></pre>"
                    await m.reply_text(Error)
                    count += 1
                    pass

    except Exception as e:
        await m.reply_text(e)   
                     
bot.run()
if __name__ == "__main__":
    asyncio.run(main())
