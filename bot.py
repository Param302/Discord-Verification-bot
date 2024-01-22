import asyncio
import logging
from utils import TOKEN, IDs, EmailParser, CheckPresence, EmailVerifier
from discord import Intents, Client, Message, app_commands, Interaction, Object

__all__ = ["mybot"]

command_tree = None
server = None
mybot = None
parse_email = EmailParser()
check_presence = CheckPresence("./sep-23.csv")
verify_email = EmailVerifier()
email_tracker = {} # user_id : [email_id, gen_code]   -- deleted after verified
logger = logging.Logger("verified_emails")

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
        if message.author == self.user:
            return

        if message.channel.id == self.test_channel:
            await self.send_message(self.test_channel, f"Hello {message.author.mention}")
            return

        elif message.channel.id == self.verify_channel:
            await message.reply(f"Please verify your email id by using `/verify` command", delete_after=3)
            await message.delete(delay=1)
            return


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
    
    gen_code = verify_email(email)
    print(f"Code: {gen_code}")
    email_tracker[interaction.user.id] = [email, gen_code]
    print(email_tracker)

    await interaction.followup.send(content="We have sent you a verification code to your mail id.", ephemeral=True)
    await asyncio.sleep(3)
    await interaction.delete_original_response()



@command_tree.command(
        name="code", 
        description="Enter the code received in your mail",
        guild=server,
    )
@app_commands.describe(code="Please enter the verification code you received in your mail")
async def verify_code_slsh_cmd(interaction: Interaction, code: int):
    global email_tracker

    user = interaction.user
    print(f"Code provided: {code}")
    print(f"User id: {user.id}")
    print(f"Username: {user}")
    print(f"User's name: {user.display_name}")
    print(f"User's roles: {user.roles}")


    if email_tracker.get(user.id) is None:
        await interaction.response.send_message("Please use `/verify` command first to get the code", ephemeral=True)
        return
    await interaction.response.send_message("Verifying the code!", ephemeral=True)

    if email_tracker[user.id][1] != code:
        await interaction.edit_original_response(content=
                f"""### Invalid code!
                Please enter the correct 6-digit code."""
                )
        return
    await interaction.edit_original_response(content="### Code is Valid!")
    
    if not (details:=check_presence(email_tracker[user.id][0])):
        await interaction.followup.send(
            content=f"""# Welcome _{user.display_name}_ to our server. 
            Hope you will enjoy here. 😊""",
            ephemeral=True
            )
        return
    
    await interaction.followup.send(
        content=f"""# Welcome _{user.display_name}_ to our server. 😀
        You are **{details["dept"].upper()}** student of **`20{email_tracker[user.id][0][:2]}`** year.
        You belongs to Group **`{details["grp_no"]}`**.\n### _You will get access to exclusive channels_ :wink: :handshake:\n## As you are one of the Pichavites. 🌟""",
        ephemeral=True
        )
    
    await asyncio.sleep(3)
    await interaction.delete_original_response()

    del email_tracker[interaction.user.id]
    print(email_tracker)



if __name__ == "__main__":
    mybot.run(token=TOKEN)
