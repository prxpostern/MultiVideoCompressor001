from telethon import TelegramClient, events, Button
from download_from_url import download_file, get_size
from file_handler import send_to_transfersh_async, progress
import os
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

    await event.respond(f"Hi!\nSend /encode and follow the steps")
    raise events.StopPropagation

@bot.on(events.NewMessage(pattern='/encode'))
async def echo(update):
    """Echo the user message."""
    msg1 = await update.respond(f"Step1: Send Your Media File or URL")
    async with bot.conversation(update.message.chat_id) as cv:
        update2 = await cv.wait_event(events.NewMessage(update.message.chat_id))

    await msg1.delete()
    msg2 = await update.respond("Downloading...")
    try:
        """Downloading Section."""
        if not os.path.isdir(download_path):
            os.mkdir(download_path)
            
        start = time.time()
        if not update2.message.message.startswith("/") and not update2.message.message.startswith("http") and update2.message.media:
            await msg2.edit("**Downloading starting😉...**")
            file_path = await bot.download_media(update2.message, download_path, progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, msg2, start)))
        else:
            url = update2.text
            filename = os.path.join(download_path, os.path.basename(url))
            file_path = await download_file(update2.text, filename, msg2, start, bot)
            
        print(f"file downloaded to {file_path}")
        try:
            """ User Input Section """
            await msg2.edit(f"Successfully Downloaded to : `{file_path}`")
            msg3 = await update2.reply("**Enter Extension with dot: like .mkv .mp4 .mp3 .aac .mka**")
            async with bot.conversation(update.message.chat_id) as cv:
              ext1 = await cv.wait_event(events.NewMessage(update.message.chat_id))
            await msg3.delete()
            msg4 = await ext1.reply(
              f"**Enter FFmpeg Options: like **\n\n`-sn -vn -c:a copy` \n\n `-sn -vn -c:a libmp3lame -ar 48000 -ab 256k` \n\n `-c:s copy -c:a copy -c:v libx264` \n\n `-c:v libx264 -s 320*240 -c:a libmp3lame -ar 48000 -ab 64k`"
            )
            async with bot.conversation(update.message.chat_id) as cv:
              ffcmd1 = await cv.wait_event(events.NewMessage(update.message.chat_id))
            await msg4.delete()  
            
            """ Encoding Section """
            ext2 = ext1.text
            ffcmd2 = ffcmd1.text
            ponlyname = os.path.splitext(file_path)[0]
            file_loc2 = f"{ponlyname}{ext2}"
            size = os.path.getsize(file_loc2)
            size_of_file = get_size(size)
            name = os.path.basename(file_loc2)
            ffcmd4 = f"ffmpeg -i {file_path} {ffcmd2} {file_loc2} -y"
            msg5 = await ffcmd1.reply(f"{ffcmd4}\n\nEncoding ...\n\n{size_of_file}\n\n**plz wait😍...**")
            #await asyncio.sleep(2)
      
            out, err, rcode, pid = await execute(f"{ffcmd4}")
            if rcode != 0:
              await msg5.edit("**Error Occured. See Logs for more info.**")
              print(err)
            """Uploading Section."""
            await msg5.edit(f"**Name: **`{name}`\n is Uploading ....**")
            try:
              await bot.send_file(
                update.message.chat_id,
                file=file_loc2,
                caption=f"`{name}` \n `{size_of_file}`",
                reply_to=update.message
              )
            except Exception as e:
              print(e)
              await msg5.edit(f"Uploading Failed\n\n**Error:** {e}")
              """ Cleaning Section """
            finally:
                os.remove(file_path)
                os.remove(file_loc2)
                print("Deleted file :", file_path)
                print("Deleted file :", file_loc2)
    except Exception as e:
        print(e)
        await msg.edit(f"Download link is invalid or not accessable\n\n**Error:** {e}")

def main():
    """Start the bot."""
    print("\nBot started visit @disneygrou For more updates...\n")
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()
