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
ext0 = ""
ffcmd0 = ""

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

    await event.respond('Hi!')
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
            ext0 = "aaa"
            ffcmd0 = "aaa"
        elif update.text and update.message.message.startswith(".") :
            ffcmd0 = "bbb"
        elif update.text and update.message.message.startswith("-") :
            ext0 = "bbb"
        else:
            url = update.text
            filename = os.path.join(download_path, os.path.basename(url))
            file_path = await download_file(update.text, filename, msg, start, bot)
            ext0 = "aaa"
            ffcmd0 = "aaa"
    except Exception as e:
        print(e)
        await msg.edit(f"Download link is invalid or not accessable \n\n **Error:** {e}")
    
    """ User Input Section """
    await asyncio.sleep(2)
    if ext0 == "aaa" and ffcmd0 == "aaa":
      mtemp = await msg.reply("**Enter Extension with dot: like .mkv .mp4 .mp3 .aac .mka**")
      async with bot.conversation(update.message.chat_id) as cv:
        ext1 = cv.wait_event(events.NewMessage(update.message.chat_id))
        ext2 = await ext1
        #await mtemp.delete()
        mtemp2 = await ext2.reply(
          f"**Enter FFmpeg Options: like **\n\n`-sn -vn -c:a copy` \n\n `-sn -vn -c:a libmp3lame -ar 48000 -ab 256k` \n\n `-c:s copy -c:a copy -c:v libx264` \n\n `-c:v libx264 -s 320*240 -c:a libmp3lame -ar 48000 -ab 64k`"
        )
    if ffcmd0 == "bbb":
      async with bot.conversation(update.message.chat_id) as cv:
        ext1 = cv.wait_event(events.NewMessage(update.message.chat_id))
        #await msg.edit(f"**Enter FFmpeg Options: like **\n\n`-sn -vn -c:a copy` \n\n `-sn -vn -c:a libmp3lame -ar 48000 -ab 256k` \n\n `-c:s copy -c:a copy -c:v libx264` \n\n `-c:v libx264 -s 320*240 -c:a libmp3lame -ar 48000 -ab 64k`")
        ffcmd1 = cv.wait_event(events.NewMessage(update.message.chat_id))
        ffcmd2 = await ffcmd1
        #await mtemp2.delete()
    
    """ Encoding Section """
    if ext0 == "bbb" and ffcmd0 == "bbb":
      await asyncio.sleep(2)
      ext3 = ext2.text
      ffcmd3 = ffcmd2.text
      ponlyname = os.path.splitext(file_path)[0]
      file_loc2 = f"{ponlyname}{ext3}"
      ffcmd4 = f"ffmpeg -i {file_path} {ffcmd3} {file_loc2} -y"
      await msg.edit(f"{ffcmd4}\n\nEncoding ...\n\n**plz wait😍...**")
      await asyncio.sleep(2)
      out, err, rcode, pid = await execute(f"'{ffcmd4}'")
      if rcode != 0:
        await msg.edit("**Error Occured. See Logs for more info.**")
        print(err)
              
      """ Uploading Media Section """
      await asyncio.sleep(2)
      size = os.path.getsize(file_loc2)
      size_of_file = get_size(size)
      name = os.path.basename(file_loc2)
      #onlyfilename = os.path.splitext(name)[0]

      await msg.edit(f"**Name: **`{name}`\n is Uploading ....**")
            
      c_time = time.time()    
      try:
        await bot.send_file(
          update.message.chat_id,
          file=file_loc2,
          caption=f"`{name}` \n `{size_of_file}`",
          reply_to=update.message
        )
      except Exception as e:
        print(e)
        await msg.edit(f"Uploading Failed\n\n**Error:** {e}")

      """ Cleaning Section """
      os.remove(file_path)
      os.remove(file_loc2)

def main():
    """Start the bot."""
    print("\nBot started ...\n")
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()
