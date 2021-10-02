from telethon import TelegramClient, events, Button
from download_from_url import download_file, get_size
from file_handler import send_to_transfersh_async, progress
import os
import cryptg   #For Increasing speed of File Downloading
import time
import datetime
import aiohttp
import asyncio
from tools import execute

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token =os.environ.get("BOT_TOKEN")
                          
download_path = "Downloads/"

bot = TelegramClient('Uploader bot', api_id, api_hash).start(bot_token=bot_token)


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    dict_ = {
            "Updates Channel":"https://t.me/disneygrou",
            "Support Group":"https://t.me/disneyteamchat",
            "Developer":"https://t.me/Doreamonfans2",
            "Backup Channel":"https://t.me/disneygroubackup"}
    buttons = [[Button.url(k, v)] for k,v in dict_.items()]

    await event.respond('Hi!\nMy Name Is Disney Team Transfer Uploader Bot Send me any file or direct download link and I upload and get the transfer.sh download link Bot Made by ❤ In 🇮🇳India by [Doreamonfans](https://t.me/doreamonfans2)', buttons=buttons)
    raise events.StopPropagation

@bot.on(events.NewMessage)
async def echo(update):
    """Echo the user message."""
    msg = await update.respond("Processing Plz Wait😁...")
    
    try:
        if not os.path.isdir(download_path):
            os.mkdir(download_path)
            
        start = time.time()
        
        if not update.message.message.startswith("/") and not update.message.message.startswith("http") and update.message.media:
            await msg.edit("**Downloading starting😉...**")
            file_path = await bot.download_media(update.message, download_path, progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, msg, start)))
        else:
            url = update.text
            filename = os.path.join(download_path, os.path.basename(url))
            file_path = await download_file(update.text, filename, msg, start, bot)
            
        print(f"file downloaded to {file_path}")
        try:
            await msg.edit("Encoding ...\n\n**plz wait😍...**")
            out, err, rcode, pid = await execute(f"ffmpeg -i '{file_path}' -vn -sn -c:a libmp3lame -ab 256k '{file_path}_.mp3' -y")
            if rcode != 0:
              await msg.edit("**Error Occured. See Logs for more info.**")
              print(err)
            
            file_loc2 = f"{file_path}_.mp3"
            size = os.path.getsize(file_loc2)
            size_of_file = get_size(size)
            name = os.path.basename(file_path)
            onlyfilename = os.path.splitext(name)[0]
            
            await bot.send_message(update, f"{size_of_file}")
            
            await msg.edit(f"**Name: **`{name}`\n is Uploading ....**")
            
            c_time = time.time()    
            try:
              await bot.send_file(
                update,
                file=file_loc2,
                file_size=size_of_file,
                caption=f"`{onlyfilename}.mp3` \n `{size_of_file}`"
              )
            except Exception as e:
              print(e)
        except Exception as e:
            print(e)
            await msg.edit(f"Uploading Failed\n\n**Error:** {e}")
        finally:
            os.remove(file_path)
            os.remove(f"{file_path}_.mp3")
    except Exception as e:
        print(e)
        await msg.edit(f"Download link is invalid or not accessable contact my [owner](https://t.me/doreamonfans1)\n\n**Error:** {e}")

def main():
    """Start the bot."""
    print("\nBot started ...\n")
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()
