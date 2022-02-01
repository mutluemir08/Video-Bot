# Copyright (C) 2021 By RishabhMusicProject

from driver.queues import QUEUE
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **Merhaba[{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**\n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) Botu sesli sohbetlerde video ve müzik akışını sağlar  !**

❂ **Detaylı bilgi ve tüm komutları görmek için komutlar düğmesine tıklayın !**

❂ **Botun temel komutları için temel komutlar butonuna tıklayın !**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Gruba Ekle ➕",
                        url=f"https://t.me/Legend_mzk_bot/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("❓ Temel komutlar", callback_data="kılavuz")],
                [
                    InlineKeyboardButton("🧐 komutlar", callback_data="cbcmds"),
                    InlineKeyboardButton("❤ sahip", url=f"https://t.me/evetbenim38/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "👥 Destek Grup", url=f"https://t.me/botdestekk/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 Kanal destek", url=f"https://t.me/legenddestek/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🌐 Sohbet grubu", url="https://t.me/gycyolcu"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("kılavuz"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ **Başlangıç aşağıdaki adımları uygulayın:**

1.) **başlangıç beni gruba ekle.**
2.) **bana yetki verin aonim yetkisi vermeyin.**
3.) **Ardından /reload komutu ile admin listesini yenileyin .**
3.) **grubunuza @{ASSISTANT_NAME} ekleyin veya /katil komutuyla davet edin.**
4.) **botu başlatmadan önce sesli sohbeti açın .**
5.) **Bazen /reload komutunu kullanarak botu daha sağlıklı bir hale getirebilirsiniz .**

📌 **bot sesli sohbete katılmadıysa sesli sohbetin açık olup olmadığını kontrol edin veya /ayril yapıp tekrar /katil yapın .**

💡 **çözüm ve önerileriniz için iletişime geçebilirsiniz : @{GROUP_SUPPORT}**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 geri git", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **Hello [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**

» **aşağıdaki butonları kullanarak mevcut komutları görebilirsiniz !**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👷🏻 Admin komut", callback_data="cbadmin"),
                    InlineKeyboardButton("🧙🏻 geliştirci", callback_data="cbsudo"),
                ],[
                    InlineKeyboardButton("📚 basit komut", callback_data="cbbasic")
                ],[
                    InlineKeyboardButton("🔙 geri dön", callback_data="cbstart")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 Basit komutlar listesi:

» /oynat istediğiniz şarkıyı direk bulup oynatır
» /voynat isteidğin videoyu direk bulup oynatır 
» /atla sıradaki şarkıya geçer
» /video videoyu bulup indirir 
» /indir müziği bulup indirir 
» /devam duraklatığınız şarkıyı devam ettirir
» /durdur akışı durdurur
» /bitir akışı bitirip sesli sohbetten ayrılır 


⚡️ __Powered by {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 admin komutu:

» /durdur - akışı durdurur 
» /devam - akışa devam eder 
» /atla - sıradaki parçaya geçer
» /son - sonlandırır
» /kapat - asistanın sesini kapatır 
» /ac - asistanın sesini açar 

⚡️ __Powered by {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri Git", callback_data="cbcmds")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 geliştirci komutları:

» bu komutlar sadece geliştirciye aittir bilgi ve destek @legenddestek

⚡ __Powered by {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri git", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Bir Anonim Yöneticisiniz !\n\n» Anonim kullanıcılara hizmet edilmeyecek şekilde tasarlandım üzgünüm .")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Sadece adminler !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
          await query.edit_message_text(
              f"⚙️ **ayarlar kapat** {query.message.chat.title}\n\n⏸ : durdur\n▶️ : devam et\n🔇 : sesize al\n🔊 : sesi ac asistan\n⏹ : Bitir
              reply_markup=InlineKeyboardMarkup(
                  [[
                      InlineKeyboardButton("⏹", callback_data="bitir"),
                      InlineKeyboardButton("⏸", callback_data="durdur"),
                      InlineKeyboardButton("▶️", callback_data="devam"),
                  ],[
                      InlineKeyboardButton("🔇", callback_data="kapat"),
                      InlineKeyboardButton("🔊", callback_data="ac"),
                  ],[
                      InlineKeyboardButton("🗑 mkapat", callback_data="mkpt")],
                  ]
             ),
         )
    else:
        await query.answer("❌ **Zaten bir şey oynatılmıyor**")", show_alert=True)


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Sadece adminler !", show_alert=True)
    await query.message.delete()
