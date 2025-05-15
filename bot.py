import os
import logging
import requests
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.getenv('7020297371:AAG8AbBUngQCJgwkg2NM8QapNjqWgNndNC8')  # توکن از متغیر محیطی گرفته می‌شود

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def get_instagram_download_links(insta_url):
    api_url = 'https://save-insta.app/api/ajaxSearch'
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'x-requested-with': 'XMLHttpRequest',
        'origin': 'https://save-insta.app',
        'referer': 'https://save-insta.app/en/',
    }
    data = {
        'q': insta_url,
        't': 'media',
        'lang': 'en'
    }

    response = requests.post(api_url, headers=headers, data=data)
    
    try:
        json_data = response.json()
        items = json_data['medias']
        results = []
        for item in items:
            results.append({
                'type': item['type'],
                'url': item['url'],
                'preview': item.get('thumbnail', item['url'])
            })
        return results
    except Exception as e:
        print(f"Error parsing response: {e}")
        return None

@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text(message: types.Message):
    if "instagram.com" not in message.text:
        await message.reply("لطفاً یک لینک معتبر از اینستاگرام بفرست 🌐")
        return

    await message.reply("در حال دریافت اطلاعات...⏳")

    links = get_instagram_download_links(message.text)

    if not links:
        await message.reply("متأسفم، نشد اطلاعات این لینک رو بگیرم ❌")
        return

    for item in links:
        caption = f"✅ نوع: {'ویدیو 🎥' if item['type'] == 'video' else 'عکس 🖼️'}"
        await message.reply_photo(photo=item['preview'], caption=caption + f"\n📥 [دانلود فایل]({item['url']})", parse_mode='Markdown')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
