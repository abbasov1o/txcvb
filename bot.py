import logging
import requests
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

# Replace with your Telegram bot token
TOKEN = "1715456897:AAF4RTmQOKp9H-_y-T5UDwgOLuVZO379aDI"

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# TikTok downloader API
TIKTOK_API_URL = "https://tiktokio.com/api"

def download_tiktok_video(video_url):
    try:
        response = requests.get(f"{TIKTOK_API_URL}/download", params={"url": video_url})
        data = response.json()
        if data.get("status") == "success":
            return data["download_url"]
        else:
            return None
    except Exception as e:
        logging.error(f"Error fetching TikTok video: {e}")
        return None

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Send me a TikTok video link, and I'll download it without a watermark for you!")

@dp.message_handler()
async def handle_message(message: types.Message):
    video_url = message.text.strip()
    if "tiktok.com" not in video_url:
        await message.reply("Please send a valid TikTok video URL.")
        return
    
    await message.reply("Downloading video, please wait...")
    
    download_link = download_tiktok_video(video_url)
    if download_link:
        await message.reply_video(video=download_link, caption="Here is your video without watermark! 🎥")
    else:
        await message.reply("Failed to download the video. Please try again later.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
