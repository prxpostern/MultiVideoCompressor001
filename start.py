from telethon import TelegramClient, events, Button
from download_from_url import download_file, get_size
from file_handler import send_to_transfersh_async, progress
import os
import time
import datetime
import aiohttp
import asyncio

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

@bot.on(events.NewMessage(pattern='/encode'))
async def echo(update):
    """Echo the user message."""
    msg = await update.respond("Send Your Media or URL Link to Start Encoding...")
    async with bot.conversation(update.message.chat_id) as cv:
        update2 = await cv.wait_event(events.NewMessage(update.message.chat_id))

    try:
        if not os.path.isdir(download_path):
            os.mkdir(download_path)
            
        start = time.time()
        
        if not update2.message.message.startswith("/") and not update2.message.message.startswith("http") and update2.message.media:
            await msg.edit("**Downloading starting😉...**")
            file_path = await bot.download_media(update2.message, download_path, progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, msg, start)))
        else:
            url = update2.text
            filename = os.path.join(download_path, os.path.basename(url))
            file_path = await download_file(update2.text, filename, msg, start, bot)
            
        print(f"file downloaded to {file_path}")
        try:
            await msg.edit(f"{file_path}")

        except Exception as e:
            print(e)
            await msg.edit(f"Uploading Failed\n\n**Error:** {e}")
        finally:
            os.remove(file_path)
            print("Deleted file :", file_path)
    except Exception as e:
        print(e)
        await msg.edit(f"Download link is invalid or not accessable contact my [owner](https://t.me/doreamonfans1)\n\n**Error:** {e}")

def main():
    """Start the bot."""
    print("\nBot started visit @disneygrou For more updates...\n")
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()
