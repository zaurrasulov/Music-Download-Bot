import telebot
import os
from config import *
import youtube_dl
import re
from PIL import Image
import time

Token = "1629831887:AAEFw7BCAgc5unKp2-xG7KDSCmD4cItfunw"
bot = telebot.TeleBot(Token)


@bot.message_handler(commands=["start"])
def start(message):
    hello_mess = f"Hello {message.from_user.first_name}!\n"
    bot.send_message(message.chat.id, hello_mess)
    desc_mess = "This bot is downloading the mp3 files from YouTube.\nWe kindly ask you to send a link and be patient.\nThanks for choosing us!"
    bot.send_message(message.chat.id,desc_mess)
   
    
@bot.message_handler(commands=["help"])
def help(message):
    help_mess = f"Dear {message.from_user.first_name},\nSend link from Youtube and wait for the song.\nPlease be patient and thanks for choosing us!\nGood luck!\n\nThe bot is done by @Zaur. Don't hesitate to contact us."
    bot.send_message(message.chat.id,help_mess)
    
@bot.message_handler(content_types=["text"])
def url(message):
    bot.delete_message(message.chat.id, message.message_id)
    url=message.text
    if url.find('youtu')!=-1:
        try:
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'format': 'bestaudio/best',
                'noplaylist': True,
                'writethumbnail': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '360',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info=ydl.extract_info(url)
            title=info['title']
            name=title.replace("/", "_").replace('"', "'")
            punct = '[—–-]+'
            listt = re.split(punct, title)
            if len(listt)!=1:
                performer = listt[0]
                song_title = listt[1]
            else: 
                performer = info['uploader']
                song_title = title
            k = open(name+'.mp3','r+b')
            try: 
                im=Image.open(name+'.jpg')
            except: 
                im=Image.open(name+'.webp')
            bot.send_photo(message.chat.id,im, caption='youtu.be/'+info['id'])
            bot.send_audio(message.chat.id,k,performer=performer, title=song_title)
            k.close()
            try: 
                os.remove(name+'.jpg')
            except: 
                os.remove(name+'.webp')
            os.remove(name+'.mp3')
        except:
            error = "Error!"
            bot.send_message(message.chat.id, error)
    else:
        undef = "Enter YouTube link."
        bot.send_message(message.chat.id,undef)

def welcome():
    print("Hello!\nBot is ready for work!")  
    time.sleep(5)     
    print("Bot is working!")
welcome()
bot.polling()