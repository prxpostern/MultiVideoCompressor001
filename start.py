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
##############################################################
    try:
        if not os.path.isdir(download_path):
            os.mkdir(download_path)
            
        start = time.time()
        
        if not update.message.message.startswith("/") and not update.message.message.startswith("http") and update.message.media:
            await msg.edit("**Downloading starting😉...**")
            file_path = await bot.download_media(update.message, download_path, progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, msg, start)))
            tgfilemsg = await bot.send_message(f"Telegram File is Downloaded in : \n\n {file_path}")
        else:
            url = update.text
            filename = os.path.join(download_path, os.path.basename(url))
            file_path = await download_file(update.text, filename, msg, start, bot)
            urlfilemsg = await bot.send_message(f"URL File is Downloaded in : \n\n {file_path}")
    except Exception as e:
        print(e)
        await msg.edit(f"Download link is invalid or not accessable !\n\n**Error:** {e}")
##############################################################
    await msg.edit(f"**Enter The Extension with . : like .mkv, .m4a, .wmv, .mp3 ...\n\n for video files use video extension and for audio use audio extension**")
    async with bot.conversation(update.message.chat_id) as cv:
      ext1 = cv.wait_event(events.NewMessage(update.message.chat_id))
      ext2 = await ext1
      ext = ext2.text
      return (ext)
    
    await msg.edit("**Enter FFmpeg Commands : must include -c:s -c:v -c:a**")
    async with bot.conversation(update.message.chat_id) as cv2:
      ffcmd = cv2.wait_event(events.NewMessage(update.message.chat_id))
      ffcmd2 = await ffcmd
      ffcmd3 = ffcmd2.text
      return (ffcmd3)
    
    #await asyncio.sleep(30)
    await msg.edit(f"Encoding ...\n\n**plz wait😍...**")
  
    ponlyname = os.path.splitext(file_path)[0]
    file_loc2 = f"{ponlyname}{ext}"
    finalcmd = f"ffmpeg -i '{file_path}' {ffcmd3} '{file_loc2}' -y"
    
    await msg.edit(f"{finalcmd}\n\nEncoding ...\n\n**plz wait😍...**")
##############################################################
    try:
      out, err, rcode, pid = await execute(f"{finalcmd}")
      if rcode != 0:
      await msg.edit("**Error Occured. See Logs for more info.**")
      print(err)

      size = os.path.getsize(file_loc2)
      size_of_file = get_size(size)
      bonlyname = os.path.basename(file_loc2)[0]
      #name1 = os.path.basename(newName)
      #onlyfilename = os.path.splitext(name1)[0]
            
      #await msg.edit(f"**Name: **`{bonlyname}`\n is Uploading ....**")
            
      #c_time = time.time()
    except Exception as e:
      print(e)
      await msg.edit(f"Encoding Failed\n\n**Error:** {e}")
##############################################################      
    try:
      await bot.send_file(
        update.message.chat_id,
        file=file_loc2,
        caption=f"**Filename: **`{bonlyname}` \n\n **Size: **`{size_of_file}`",
        reply_to=update.message
      )
    except Exception as e:
      print(e)
      await msg.edit(f"Uploading Failed\n\n**Error:** {e}")
##############################################################
    try:
      os.remove(file_path)
      os.remove(file_loc2)
    except:
       pass
##############################################################
def main():
    """Start the bot."""
    print("\nBot started ...\n")
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()
