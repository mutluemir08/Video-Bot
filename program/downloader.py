from __future__ import unicode_literals

import asyncio
import math
import os
import time
from random import randint
from typing import List, Union
from urllib.parse import urlparse

import aiofiles
import aiohttp
import requests
import wget
import yt_dlp
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified
from telegraph.aio import Telegraph
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL

from config import BOT_USERNAME as bn


def humanbytes(size):
    """baytları Baytlara Dönüştür ki İnsan Okuyabilsin"""
    if not size:
        return ""
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def command(commands: Union[str, List[str]]):
    return filters.command(commands, "/")


ydl_opts = {
    "format": "best",
    "keepvideo": True,
    "prefer_ffmpeg": False,
    "geo_bypass": True,
    "outtmpl": "%(title)s.%(ext)s",
    "quite": True,
}


@Client.on_message(command(["bul", f"bul@{bn}"]) & ~filters.edited)
def bul(_, message):
    query = " ".join(message.command[1:])
    m = message.reply("🔎 Aranıyor..")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        m.edit("❌ şarkı bulunamadı.\n\nlütfen geçerli bir şarkı adı verin.")
        print(str(e))
        return
    m.edit("⏱️ Sorgulanıyor...")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"**🎵 İndirildi.**"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("📥 Yüklüyorum...")
        message.reply_audio(
            audio_file,
            caption=rep,
            thumb=thumb_name,
            parse_mode="md",
            title=title,
            duration=dur,
        )
        m.delete()
    except Exception as e:
        m.edit("❌ hatanın, düzelmesini bekleyiniz.")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)


async def progress(current, total, message, start, type_of_ps, file_name=None):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join("🔴" for _ in range(math.floor(percentage / 10))),
            "".join("🔘" for _ in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )

        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            try:
                await message.edit(
                    "{}\n**File Name:** `{}`\n{}".format(type_of_ps, file_name, tmp)
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass
        else:
            try:
                await message.edit("{}\n{}".format(type_of_ps, tmp))
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


def time_formatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
        + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]


def get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]


async def download_song(url):
    song_name = f"{randint(6969, 6999)}.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(song_name, mode="wb")
                await f.write(await resp.read())
                await f.close()
    return song_name


def time_to_seconds(times):
    stringt = str(times)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


@Client.on_message(
    command(["vbul", f"vbul@{bn}", "video", f"video@{bn}"]) & ~filters.edited
)
async def vsong(client, message):
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]
        message.from_user.mention
    except Exception as e:
        print(e)
    try:
        msg = await message.reply("📥 **video indiriyorum...**")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"🚫 **error:** {e}")
    preview = wget.download(thumbnail)
    await msg.edit("📤 **video yüklüyorum...**")
    await message.reply_video(
        file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=ytdl_data["title"],
    )
    try:
        os.remove(file_name)
        await msg.delete()
    except Exception as e:
        print(e)


telegraph = Telegraph()


@Client.on_message(command(["soz", "lyric", f"lyric@{bn}"]) & ~filters.edited)
async def lyrics(c: Client, message):
    ment = message.from_user.mention
    message.chat.id
    try:
        if len(message.command) < 2:
            await message.reply_text(
                f"» {ment}<b>lütfen şarkı sözlerini arayabilmem için bana bir şarkı ismi ver.</b>"
            )
            return
        query = message.text.split(None, 1)[1]
        rep = await message.reply_text(
            f"{ment} <b>sizin için</b> <code>{query}</code> <b>şarkınızın sözlerini arıyorum...</b> 🔎",
            parse_mode="html",
        )
        resp = requests.get(
            f"https://api-tede.herokuapp.com/api/lirik?l={query}"
        ).json()
        result = f"{resp['data']}"
        if len(result) < 4030:
            await rep.edit(
                f"""<b><i> İşte Şarkınızın Sözleri: </i></b>
            
            <i>{result}</i>""",
                parse_mode="html",
            )
        if len(result) > 4030:
            TELEGRAPH_AUTHOR_NAME = "Legend Müzik"
            TELEGRAPH_AUTHOR_LİNK = "https://t.me/G4rip"
            try:
                await rep.edit(
                    f"<b> Şarkı sözleri fazla uzun, sizin için Telegraph'a yapıştırıyorum... Lütfen bekleyin. </b>"
                )
                await telegraph.create_account(
                    short_name="G4rip",
                    author_name=f"{TELEGRAPH_AUTHOR_NAME}",
                    author_url=f"{TELEGRAPH_AUTHOR_LİNK}",
                )
                response = await telegraph.create_page(
                    "<b><i> İşte şarkınızın sözleri </i></b>",
                    html_content=f"<p>{result}</p>",
                )
                await rep.edit(
                    f"<i> Bu şarkının sözleri göndermek için fazla uzun!\
            Bu yüzden sizin için Telegraph'a yapıştırdım.</i>\
               <b>🔗 Link:</i> {response['url']}",
                    parse_mode="html",
                    disable_web_page_preview=False,
                )
            except Exception as e:
                await rep.edit(
                    f"{ment}<i> şarkınızın sözlerini Telegraph'a yapıştırırken bir hata oluştu! Lütfen tekrar deneyin, hatanın devam etmesi durumunda sahibime ulaşın. </i>"
                )
                print(e)
    except Exception:
        await rep.edit(
            "❌ Herhangi bir sonuç bulunamadı! Lütfen doğru kelimelerle tekrar deneyin, hatanın devam etmesi durumunda sahibime yazın."
        )
