import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
# from responses import get_response


# Loading Token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
print(TOKEN)

# Bot Setup
intents = Intents.default()
intents.message_content = True
intents.members = True

client = Client(intents=intents)

# Handling startup of Bot
@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

# Handling messages
@client.event
async def on_message(message: Message):

    if message.channel.id != 1198395844391604419:
        return
    
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = message.content[1:]
    channel = str(message.channel)

    print(f"{username} sent a message in {channel}: {user_message}")
    await message.add_reaction("👍")
    print("Added reaction")
    await send_message(message, message.content)
    print("Messages are sent")
    await message.channel.send("# Byeeeeeeeee :wave:")
    await message.channel.send(f"Have a nice morning\n <@762015770728202243> and <@1187052225441316916> :wink:")


async def send_message(message: Message, user_message: str):
    if not user_message:
        print("Message is empty")
        return
    

    if is_private:=user_message[0] == "&":
        user_messsage = user_message[1:]

    if user_message == "Final test":
        param = client.get_user(531398388516651029)
        arnold = client.get_user(762015770728202243)
        rupkatha = client.get_user(1187052225441316916)
        print("Param is:", param)
        await param.send("Testing this message")
        await param.send("Let's disturb arnold now!")
        await arnold.send("Hi Arnold!\n:D")
        await arnold.send("Param here! :wave:")
        await arnold.send("I hope you can see this message!")
        await arnold.send("I have started this bot if you can see these messages")
        await arnold.send("So, now it's time to disturb Rupkatha!")
        await arnold.send("Yayyyy!!!!!!!!!! :rofl:")

        await rupkatha.send("Hi Rupkatha!\n:D")
        await rupkatha.send("Param here! :wave:")
        await rupkatha.send("I hope you can see this message!")
        await rupkatha.send("I have started this bot if you can see these messages")
        await rupkatha.send("Please don't kill me for disturbing you :pleading_face:")
        await rupkatha.send("I am just testing this bot")
        for _ in range(10):
            await rupkatha.send("I will be offline after this message")
        await rupkatha.send(":wink:")

        await arnold.send("If I am not alive, means rupkatha killed me :sob:")
        await arnold.send("Just to let you know, call me when you see this.")
        await arnold.send("bot is currently offline, as I am running it locally.")
        await arnold.send("Send me 1.5 dollars per month to host it. 💸💸💸")
        await arnold.send("# Byeeeeeeeee :wave:")

        await param.send("Done! :D")
    
    try:
        await message.author.send("Hi hello! (shh!)") if is_private else await message.channel.send("Hi hello!\n:D")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    client.run(token=TOKEN)