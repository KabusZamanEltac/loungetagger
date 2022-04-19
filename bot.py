import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

anlik_calisan = []

@client.on(events.NewMessage(pattern='^(?i)/Dur'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("**Dennizz_bot**, Grup veya kanaldaki neredeyse tüm üyelerden bahsedebilirim ★\nDaha fazla bilgi için **/help**'i tıklayın.",
                    buttons=(
                      [Button.url('🌟 Məni Grupa Apar', 'https://t.me/Dennizz_bot?startgroup=a'),
                      Button.url('📣 𝐒ə𝐧𝐝ə 𝐐𝐨ş𝐮𝐥 𝐁𝐢𝐳ə', 'https://t.me/WerabliAnlar'),
                      Button.url('🚀 Sahibim', 'https://t.me/Demon_NightT')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/info$"))
async def help(event):
  helptext = "**Dennizz_bot'un Kömək Menüsü**\n\nMenyu: /gel \n  Bu komutu, başqalarını istediyiniz mesajla birlikde işlədə bilərsiniz. \n`Örnek: /gel Günaydın!`  \nBu menyunu yanıt olarak kullanabilirsiniz. herhangi bir mesaj Bot, yanıtlanan iletiye kullanıcıları etiketleyecek"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('🌟 Məni Grupa Apar', 'http://t.me/Dennizz_bot?startgroup=a'),
                       Button.url('📣 𝐒ə𝐧𝐝ə 𝐐𝐨ş𝐮𝐥 𝐁𝐢𝐳ə', 'https://t.me/WerabliAnlar'),
                      Button.url('🚀 Sahibim', 'https://t.me/anteplibebekk')]
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern="^/gel ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("__Bu komut gruplarda ve kanallarda kullanılabilir.!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Yalnızca yöneticiler hamını tag edə bilər!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Eski mesajlar için üyelerden bahsedemem! (gruba eklemeden önce gönderilen mesajlar)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Bana bir argüman ver!__")
  else:
    return await event.respond("__Bir Mesaja Yanit Ver ve ya Sebeb Yaz!__")
    
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Durdum🌹 @WerabliAnlar ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Durdum🌹 @WerabliAnlar ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


print(">> Bot isleyir narahat olma 🚀 @Demon_NightT melumat ala bilirsən <<")
client.run_until_disconnected()
