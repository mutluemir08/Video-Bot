from datetime import datetime
from sys import version_info
from time import time

from pyrogram import Client
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import __version__ as pytover

from config import (
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from driver.filters import command
from driver.jennie import user
from program import __version__

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_photo("https://telegra.ph/file/84c3fa6685479f7e1a5a6.jpg")
    await message.reply_text(
        f"""✨ **Merhaba{message.from_user.mention()} !**
💭 [{BOT_NAME}](https://t.me/{BOT_USERNAME}) **botu sesli sohbetlerde canlı yayın video ve müzik akışını sağlar !**

❂ **Detaylı bilgi ve tüm komutlar için komutlar butonuna tıklayın !**

❂ **Botun temel komutları için temel komutlar butonuna tıklayın**
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Gruba ekle ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("❓ Basit komutlar", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("📚 komutlar", callback_data="cbcmds"),
                ],
                [InlineKeyboardButton("🌐 Sohbet Grubu", url="https://t.me/gycyolcu")],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(
    command(["alive", f"alive@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def alive(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✨ Destek Grup", url=f"https://t.me/{GROUP_SUPPORT}"
                ),
                InlineKeyboardButton(
                    "📣 Kanal Destek", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )

    alive = f"**Merhaba {message.from_user.mention()}, ben {BOT_NAME}**\n\n✨ Bot düzgün çalışıyor\n🍀 Sahip: [{ALIVE_NAME}](https://t.me/{OWNER_NAME})\n✨ Bot Version: `v{__version__}`\n🍀 Pyrogram Version: `{pyrover}`\n✨ Python Version: `{__python_version__}`\n🍀 PyTgCalls version: `{pytover.__version__}`\n✨ Uptime Status: `{uptime}`\n\n**Beni Buraya eklediğiniz için teşekkürler** ❤"

    await message.reply_photo(
        photo=f"{ALIVE_IMG}",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `PONG!!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 bot durumu:\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **başlat zaman:** `{START_TIME_ISO}`"
    )


@Client.on_message(filters.new_chat_members)
async def new_chat(c: Client, m: Message):
    ass_uname = (await user.get_me()).username
    bot_id = (await c.get_me()).id
    for member in m.new_chat_members:
        if member.id == bot_id:
            return await m.reply(
                "❤️ **Beni Gruba eklediğin için teşekkür ederim!**\n\n"
                "**Asistanı çağırmak için /katil komutunu kullanın veya el ile ekleyin.**\n\n"
                "**daha sonra** /yenile",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "📣 Destek kanal", url=f"https://t.me/{UPDATES_CHANNEL}"
                            ),
                            InlineKeyboardButton(
                                "💭 Destek Grup", url=f"https://t.me/{GROUP_SUPPORT}"
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                "👤 asistan", url=f"https://t.me/{ass_uname}"
                            )
                        ],
                    ]
                ),
            )
