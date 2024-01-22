import code
from math import e
from utils import TOKEN, IDs, EmailParser, CheckPresence, EmailVerifier, TrackEmail
from discord import Intents, Client, Message, app_commands, Interaction, Object

__all__ = ["mybot"]

command_tree = None
server = None
mybot = None
parse_email = EmailParser()
check_presence = CheckPresence("./sep-23.csv")
verify_email = EmailVerifier()
email_tracker = None
gen_code = None

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
        print("Message:", message)
        if message.author == self.user:
            return

        if message.channel.id == self.verify_channel:
            await self.send_message(self.verify_channel, f"Please verify your email id by using `/verify` command")


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
    global email_tracker

    await interaction.response.send_message("Verifying your email!", ephemeral=True)
    print(f"Email provided: {email}")

    if not parse_email(email):
        await interaction.edit_original_response(content=
                f"""## 👎 Invalid email!
                You entered: `{email}`
                Please enter a valid **IITM Student Mail Id** in this format:\n`<roll_no>@*study.iitm.ac.in`"""
                )
        return
    email_tracker = TrackEmail(email)
    email_tracker.gen_code = verify_email(email)
    print(f"Code: {email_tracker.gen_code}")

    await interaction.followup.send(content="We have sent you a verification code to your mail id.", ephemeral=True)


@command_tree.command(
        name="code", 
        description="Enter the code received in your mail",
        guild=server,
    )
@app_commands.describe(code="Please enter the verification code you received in your mail")
async def verify_code_slsh_cmd(interaction: Interaction, code: int):
    global email_tracker

    if email_tracker.gen_code is None:
        await interaction.response.send_message("Please use `/verify` command first to get the code", ephemeral=True)
        return
    email_tracker.user_code = code
    await interaction.response.send_message("Verifying the code!", ephemeral=True)

    user = interaction.user
    print(f"Code provided: {code}")
    print(f"User id: {user.id}")
    print(f"Username: {user}")
    print(f"User's name: {user.display_name}")
    print(f"User's roles: {user.roles}")

    if email_tracker.gen_code != email_tracker.user_code:
        await interaction.edit_original_response(content=
                f"""### 👎 Invalid code!
                Please enter the correct code"""
                )
        return

    await interaction.edit_original_response(content="### Code is Valid!")
    
    if not (details:=check_presence(email_tracker.email)):
        await interaction.followup.send(
            content=f"""# Welcome _{user.display_name}_ to our server. 
            Hope you will enjoy here. 😊""",
            ephemeral=True
            )
        return
    
    await interaction.followup.send(
        content=f"""# Welcome _{user.display_name}_ to our server. 😀
        You are **{details["dept"].upper()}** student of **`20{email_tracker.email[:2]}`** year.
        You belongs to Group **`{details["grp_no"]}`**.\n### _You will get access to exclusive channels_ :wink: :handshake:\n## As you are one of the Pichavities 🌟""",
        ephemeral=True
        )
    
    del email_tracker


if __name__ == "__main__":
    mybot.run(token=TOKEN)
