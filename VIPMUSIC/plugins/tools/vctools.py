from pyrogram import Client, filters
from pyrogram.types import Message
from VIPMUSIC import app
from pyrogram import *
from pyrogram.types import *
from config import OWNER_ID
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall
from VIPMUSIC.utils.database import get_assistant


# vc on
@app.on_message(filters.video_chat_started)
async def brah(_, msg):
    await msg.reply("**😍ᴠɪᴅᴇᴏ ᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ🥳**")


# vc off
@app.on_message(filters.video_chat_ended)
async def brah2(_, msg):
    await msg.reply("**😕ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ💔**")


# invite members on vc
@app.on_message(filters.video_chat_members_invited)
async def brah3(app: app, message: Message):
    text = f"➻ {message.from_user.mention}\n\n**๏ ɪɴᴠɪᴛɪɴɢ ɪɴ ᴠᴄ ᴛᴏ :**\n\n**➻ **"
    x = 0
    for user in message.video_chat_members_invited.users:
        try:
            text += f"[{user.first_name}](tg://user?id={user.id}) "
            x += 1
        except Exception:
            pass

    try:
        invite_link = await app.export_chat_invite_link(message.chat.id)
        add_link = f"https://t.me/{app.username}?startgroup=true"
        reply_text = f"{text} 🤭🤭"

        await message.reply(
            reply_text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text="๏ ᴊᴏɪɴ ᴠᴄ ๏", url=add_link)],
                ]
            ),
        )
    except Exception as e:
        print(f"Error: {e}")


####


@app.on_message(filters.command("math", prefixes="/"))
def calculate_math(client, message):
    expression = message.text.split("/math ", 1)[1]
    try:
        result = eval(expression)
        response = f"ᴛʜᴇ ʀᴇsᴜʟᴛ ɪs : {result}"
    except:
        response = "ɪɴᴠᴀʟɪᴅ ᴇxᴘʀᴇssɪᴏɴ"
    message.reply(response)


@app.on_message(filters.command(["spg"], ["/", "!", "."]))
async def search(event):
    msg = await event.respond("Searching...")
    async with aiohttp.ClientSession() as session:
        start = 1
        async with session.get(
            f"https://content-customsearch.googleapis.com/customsearch/v1?cx=ec8db9e1f9e41e65e&q={event.text.split()[1]}&key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM&start={start}",
            headers={"x-referer": "https://explorer.apis.google.com"},
        ) as r:
            response = await r.json()
            result = ""

            if not response.get("items"):
                return await msg.edit("No results found!")
            for item in response["items"]:
                title = item["title"]
                link = item["link"]
                if "/s" in item["link"]:
                    link = item["link"].replace("/s", "")
                elif re.search(r"\/\d", item["link"]):
                    link = re.sub(r"\/\d", "", item["link"])
                if "?" in link:
                    link = link.split("?")[0]
                if link in result:
                    # remove duplicates
                    continue
                result += f"{title}\n{link}\n\n"
            prev_and_next_btns = [
                Button.inline("▶️Next▶️", data=f"next {start+10} {event.text.split()[1]}")
            ]
            await msg.edit(result, link_preview=False, buttons=prev_and_next_btns)
            await session.close()


from pyrogram import filters
from pyrogram.raw.functions.channels import EditAdmin
from pyrogram.raw.types import ChatAdminRights
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall


@app.on_message(filters.command("startvc") & filters.group)
async def start_voice_chat(client, message):
    userbot = await get_assistant(message.chat.id)
    chat_id = message.chat.id

    try:
        # Promote the assistant to admin with manage voice chat permissions
        await app.promote_chat_member(
            chat_id,
            userbot.id,
            privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=True,
                can_delete_messages=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=True,
                can_manage_video_chats=True,
            ),
        )

        # Create a new group call
        result = await userbot.start_group_call(chat_id)
        await message.reply("Voice chat started successfully!")
    except Exception as e:
        await message.reply(f"Failed to start voice chat: {e}")


@app.on_message(filters.command("endvc") & filters.group)
async def end_voice_chat(client, message):
    userbot = await get_assistant(message.chat.id)
    chat_id = message.chat.id

    try:
        # Promote the assistant to admin with manage voice chat permissions
        await app.promote_chat_member(
            chat_id,
            userbot.id,
            privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=True,
                can_delete_messages=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=True,
                can_manage_video_chats=True,
            ),
        )

        # Get the active group call
        group_call = await userbot.get_group_call(chat_id)

        if group_call:
            # Discard the active group call
            await userbot.invoke(
                DiscardGroupCall(
                    call=InputGroupCall(
                        id=group_call.id, access_hash=group_call.access_hash
                    )
                )
            )
            await message.reply("Voice chat ended successfully!")
        else:
            await message.reply("No active voice chat found.")
    except Exception as e:
        await message.reply(f"Failed to end voice chat: {e}")
