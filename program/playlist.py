# Copyright (C) 2021 By Rishabh Music-Project
# Commit Start Date 1/11/2021
# Finished On 7/1/2022

from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BOT_USERNAME
from driver.filters import command, other_filters
from driver.queues import QUEUE, get_queue

keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🗑 mkapat", callback_data="cls")]]
)


@Client.on_message(
    command(["liste", f"liste@{BOT_USERNAME}", "sıra", f"sıra@{BOT_USERNAME}"])
    & other_filters
)
async def playlist(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await m.reply(
                f"💡 **akış:**\n\n• [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )
        else:
            QUE = f"💡 **akış:**\n\n• [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**📖 sıra listesi:**\n"
            l = len(chat_queue)
            for x in range(1, l):
                han = chat_queue[x][0]
                hok = chat_queue[x][2]
                hap = chat_queue[x][3]
                QUE = QUE + "\n" + f"**#{x}** - [{han}]({hok}) | `{hap}`"
            await m.reply(QUE, reply_markup=keyboard, disable_web_page_preview=True)
    else:
        await m.reply("❌ **Şu anda bir şey oynatılmıyor**")
