from utils import TOKEN, IDs, EmailParser, CheckPresence
from discord import Intents, Client, Message, app_commands, Interaction, Object


class Bot(Client, IDs):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)

    async def on_ready(self):
        await self.wait_until_ready()
        await tree.sync(guild=server)

        print(f"{self.user} has connected to Discord!")

        await self.send_startup_message(self.test_channel)
        print("Startup message sent")
    
    async def send_startup_message(self, channel: int):
        msg = await self.get_channel(channel).send(
            """## Hello, I am a Pichu. I am here to help you.
            ### <@531398388516651029> created me."""
            )
        self.first_msg_id = msg.id
    
    async def send_message(self, channel:int, message:str):
        await self.get_channel(channel).send(message)

    async def on_message(self, message: Message):
        if (message.reference is not None 
            and message.reference.message_id == self.first_msg_id
            and message.author.id in (self.param, self.arnold, self.rupkatha)
            ):
            await message.reply("Thanks for replying. 🙂")
    


# Bot Setup
intents = Intents.default()
intents.message_content = True
intents.members = True
server = Object(id=1182668463496499240)

mybot = Bot(intents=intents)
tree = app_commands.CommandTree(mybot)


@tree.command(name="ping", description="Ping the bot", guild=server)
async def ping_slash_cmd(interaction: Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(
        name="verify", 
        description="Verify yourself",
        guild=server,
    )
@app_commands.describe(email="Please enter your IITM Student mail id")
async def verify_slash_cmd(interaction: Interaction, email: str):
    await interaction.response.send_message("Verifying your email!", ephemeral=True)
    print(email)

    await interaction.edit_original_response(content="Email verified!")


if __name__ == "__main__":
    mybot.run(token=TOKEN)