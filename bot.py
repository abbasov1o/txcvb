import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to download TikTok video
def download_tiktok_video(url: str) -> str:
    try:
        response = requests.get(f"https://api.tiktokio.com/v1/video?url={url}")
        response.raise_for_status()
        data = response.json()
        video_url = data['video']['url']
        return video_url
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        return None

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me a TikTok video link, and I will download it for you!')

# Message handler for video links
def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    if 'tiktok.com' in url:
        video_url = download_tiktok_video(url)
        if video_url:
            update.message.reply_text('Here is your video:')
            context.bot.send_video(chat_id=update.message.chat_id, video=video_url)
        else:
            update.message.reply_text('Sorry, I could not download the video. Please try again.')
    else:
        update.message.reply_text('Please send a valid TikTok video link.')

def main() -> None:
    # Replace 'YOUR_TOKEN' with your bot's token
    updater = Updater("1715456897:AAF4RTmQOKp9H-_y-T5UDwgOLuVZO379aDI")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command and message handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
