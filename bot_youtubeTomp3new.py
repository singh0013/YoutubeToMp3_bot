import os
import youtube_dl
import telebot
from tqdm import tqdm

# Create a new Telegram bot using your API token
bot = telebot.TeleBot("5848003129:AAHcUEm1Rzn_x-XROPMPyMssASJjL3vJ70I")
# updates = bot.get_updates()
# chat_id = updates[-1].message.chat.id
print(bot.get_me())
# print(bot.get_updates())

print("Bot Started..")
bot.send_message(chat_id="1015451798",text="Send the Youtube Link To Download..😈")

# Handle the '/start' command
# @bot.message_handler(commands=['start'])
# def download_video(message):
    # try:
        # # chat_id = message.chat.id
        # # print(chat_id)
        # msg = bot.send_message(chat_id=message.chat.id,
                            # text="Send the Youtube Link To Download..😈"
                            # )
               
        # bot.register_next_step_handler(msg,get_url)
        
    # except Exception as e:
        # # Handle the exception
        # bot.send_message(message.chat.id, "Error 🤔 : " + str(e))


# bot.register_next_step_handler(msg,get_url)      

@bot.message_handler(content_types=['text'])
def get_url(message):
    # try:
        url = str(message.text)
        # sent_message = bot.send_message(message.chat.id, "Converting to Audio...😎")
        # sent_message = bot.send_message(message.chat.id, "Converting")
        sent_message = bot.send_message(message.chat.id, "Download started")

        # Set up youtube-dl options to download the best audio quality in mp3 format                        
        ydl_opts = {
            'format': 'bestaudio[ext=mp3]/bestaudio',
            'outtmpl': './audio/%(title)s.mp3',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'progress_hooks': [lambda d: progress_hook(d, message , sent_message)],
            # 'ratelimit': '256k',
            # 'postprocessor_args': ['-rate-limit', '100m'],
        }

        # Send a message to the user that the download has started
        
        
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # info = ydl
            file_path = ydl.prepare_filename(info)
            if os.path.isfile(file_path):
                bot.send_audio(message.chat.id, open(file_path, 'rb'))
                
            else:
                bot.send_message(message.chat.id, "Error: File not found or not named correctly..🤔")
                
       
        # bot.send_message(message.chat.id, "Download complete!")
        bot.send_message(message.chat.id, "Send Me Next url..😈")
        
    # except Exception as e:
        # # Handle the exception
        # bot.send_message(message.chat.id, "Error 🤔 : " + str(e))
        # bot.send_message(message.chat.id, "Send the YouTube url..😈")
    
prev_message = None
def progress_hook(d, message, sent_message):
    global prev_message
    if d['status'] == 'downloading':
        # check if the message has already been edited
        if prev_message != f"Converting to Audio  {d['_percent_str']}":
            bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text= f"Converting to Audio  {d['_percent_str']}")
            prev_message = f"Converting to Audio  {d['_percent_str']}"
    elif d['status'] == 'finished':
        message.reply_text("Download completed")


# def progress_hook(d,message,sent_message):

    # # sent_message = bot.send_message(message.chat.id, "Download started")
    # # message_id = sent_message.message_id
        
    # if d['status'] == 'downloading':        
        
        # bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text= f"Converting to Audio...😎  {d['_percent_str']}")
        
    # elif d['status'] == 'finished':
        # # Send a message to the user to confirm that the download is complete
        # # bot.send_message(message.chat.id, "Converted Successfully 💪🏻😎\nUploading to Telegram Chat")
        # bot.send_message(message.chat.id, "Uploading to Telegram Chat.. 😎")
        # # message.reply_text("Download completed")
                

# Start polling for new messages
bot.polling()
