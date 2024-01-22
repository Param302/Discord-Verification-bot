from utils import TOKEN, IDs, EmailParser, CheckPresence
from discord import Intents, Client, Message, app_commands, Interaction, Object

__all__ = ["mybot"]

command_tree = None
server = None
mybot = None
parse_email = EmailParser()
check_presence = CheckPresence("./sep-23.csv")

class Bot(Client, IDs):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)

    async def on_ready(self):
        await self.wait_until_ready()
        await command_tree.sync(guild=server)

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
            ):
            await message.reply("Thanks for replying. 🙂")


# ================ Bot Setup ====================
def bot_setup():
    global command_tree, server, mybot
    intents = Intents.default()
    intents.message_content = True
    intents.members = True

    mybot = Bot(intents=intents)
    server = Object(id=IDs.server)

bot_setup()

command_tree = app_commands.CommandTree(mybot)
# ================ Slash Commands ====================
@command_tree.command(
        name="ping", 
        description="Ping the bot", 
        guild=server,
    )
async def ping_slash_cmd(interaction: Interaction):
    await interaction.response.send_message("Pong!")

@command_tree.command(
        name="verify", 
        description="Verify yourself",
        guild=server,
    )
@app_commands.describe(email="Please enter your IITM Student mail id")
async def verify_slash_cmd(interaction: Interaction, email: str):
    await interaction.response.send_message("Verifying your email!", ephemeral=True)

    user = interaction.user
    print(f"Email provided: {email}")
    print(f"User id: {user.id}")
    print(f"Username: {user}")
    print(f"User's name: {user.display_name}")
    print(f"User's roles: {user.roles}")

    if not parse_email(email):
        await interaction.edit_original_response(content=
                f"""## 👎 Invalid email!
                You entered: `{email}`
                Please enter a valid **IITM Student Mail Id** ending with `study.iitm.ac.in`"""
                )
        return
    
    await interaction.edit_original_response(content="Email verified!")

    if not (details:=check_presence(email)):
        await interaction.followup.send(
            content=f"""# Welcome _{user.display_name}_ to our server. 
            Hope you will enjoye here. 😊""",
            ephemeral=True
            )
        return
    
    await interaction.followup.send(
        content=f"""# Welcome _{user.display_name}_ to our server. 😀
        You are **{details["dept"].upper()}** student of **`20{email[:2]}`** year.
        You belongs to Group **`{details["grp_no"]}`**.\n### _You will get access to exclusive channels_ :wink: :handshake:\n## As you are one of the Pichavities 🌟""",
        ephemeral=True
        )


if __name__ == "__main__":
    mybot.run(token=TOKEN)
