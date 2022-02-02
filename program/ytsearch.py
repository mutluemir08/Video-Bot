import logging
from config import BOT_USERNAME
from driver.filters import command, other_filters
from pyrogram import Client
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from youtube_search import YoutubeSearch

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(isim)s - %(syisim)s - %(message)s")
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(command(["ara", f"ara@{BOT_USERNAME}"]))
async def ytsearch(_, message: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🗑 mkapat", callback_data="cls",
                )
            ]
        ]
    )

    try:
        if len(message.command) < 2:
            await message.reply_text("/ara **komutu argümana ihtiyac duyar !**")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("🔎 **aranıyor...**")
        results = YoutubeSearch(query, max_results=5).to_dict()
        i = 0
        text = ""
        while i < 5:
            text += f"🏷 **isim:** __{results[i]['başlık']}__\n"
            text += f"⏱ **süre:** `{results[i]['süre']}`\n"
            text += f"👀 **görüntüleme:** `{results[i]['görüntüleme']}`\n"
            text += f"📣 **Kanal:** {results[i]['kanal']}\n"
            text += f"🔗: https://www.youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.edit(text, reply_markup=keyboard, disable_web_page_preview=True)
    except Exception as e:
        await m.edit(str(e))
