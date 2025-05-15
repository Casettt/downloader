import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import BOT_TOKEN, ADMIN_IDS
from utils.instagram import download_instagram_post, download_instagram_story

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Start command handler
@dp.message(Command("start"))
async def send_welcome(message: Message):
    welcome_text = """
    🤖 **ربات دانلودر اینستاگرام**\n
    لینک پست یا استوری اینستاگرام را برای من بفرستید تا آن را برای شما دانلود کنم.
    """
    await message.reply(welcome_text)

# Instagram URL handler
@dp.message(F.text.contains("instagram.com"))
async def handle_instagram_url(message: Message):
    url = message.text
    
    # Add reaction (typing action)
    await bot.send_chat_action(message.chat.id, "typing")
    
    try:
        # Check if it's a story or post
        if "/stories/" in url:
            # Download story
            media = await download_instagram_story(url)
            if media:
                if media['type'] == 'video':
                    await message.reply_video(media['url'], caption="استوری دانلود شد")
                else:
                    await message.reply_photo(media['url'], caption="استوری دانلود شد")
            else:
                await message.reply("❌ خطا در دانلود استوری. لطفاً مطمئن شوید لینک صحیح است.")
        
        else:
            # Download post
            media_list = await download_instagram_post(url)
            if media_list:
                media_group = []
                for media in media_list:
                    if media['type'] == 'video':
                        media_group.append(types.InputMediaVideo(media=media['url']))
                    else:
                        media_group.append(types.InputMediaPhoto(media=media['url']))
                
                # Send as media group (supports multiple photos/videos)
                await message.reply_media_group(media_group)
            else:
                await message.reply("❌ خطا در دانلود پست. لطفاً مطمئن شوید لینک صحیح است.")
    
    except Exception as e:
        print(f"Error: {e}")
        await message.reply("❌ خطایی رخ داد. لطفاً بعداً دوباره امتحان کنید.")

# Error handler
@dp.message()
async def handle_other_messages(message: Message):
    await message.reply("لطفاً فقط لینک پست یا استوری اینستاگرام را ارسال کنید.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())