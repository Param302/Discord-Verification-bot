import asyncio
import logging
from utils import TOKEN, IDs, EmailParser, CheckPresence, EmailVerifier
from discord import Intents, Client, Message, utils, app_commands, Interaction, Object, Activity, ActivityType

__all__ = ["mybot"]

command_tree = None
server = None
mybot = None
verification_msg = None
parse_email = EmailParser()
check_presence = CheckPresence("./sep-23.csv")
email_code_gen = EmailVerifier()
email_tracker = {} # user_id : [email_id, gen_code]   -- deleted after verified

# ================ Logger Setup ====================
logger = logging.getLogger("discord")
logger.setLevel(logging.CRITICAL)
log_handler = logging.FileHandler(filename="discord-bot.log", encoding="utf-8", mode="w")
log_handler.setFormatter(logging.Formatter(fmt="%(asctime)s - %(levelname)s: %(name)s - %(message)s", datefmt="%Y-%d %H:%M:%S"))
logger.addHandler(log_handler)


# ================ Bot ====================
class Bot(Client, IDs):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        logger.info("Bot initialized")
        self.startup_msg = "## Hello, I am a . I am here to help you.\n### <@531398388516651029> created me."

    async def on_ready(self):
        await self.wait_until_ready()
        await command_tree.sync(guild=server)
        logger.info("Bot has connected to Discord!")
        await self.change_presence(activity=Activity(
            name="/verify",
            type=ActivityType.listening,
        ))
        await self.send_startup_message(self.test_channel)
        # logger.info(f"Startup message sent")
    
    async def send_startup_message(self, channel: int):
        msg = await self.get_channel(channel).send(self.startup_msg)
        self.first_msg_id = msg.id
    
    async def send_message(self, channel:int, message:str):
        await self.get_channel(channel).send(message)

    async def on_message(self, message: Message):
        global email_tracker
        if message.author == self.user or message.channel.id not in (self.test_channel, self.verify_channel):
            return

        logger.info(f"Message received - chnanel: {message.channel.name} by: {message.author}({message.author.id})\tMessage ({message.id}): '{message.content}'")

        if message.channel.id == self.test_channel:
            await self.send_message(self.test_channel, f"Hello {message.author.mention}")

        elif message.channel.id == self.verify_channel:
            if email_tracker.get(message.author.id) is None:
                await message.reply(f"Please verify your email id by using **`/verify`** command", delete_after=3)
            elif email_tracker[message.author.id][0]:
                await message.reply(f"Please enter the verification code by using **`/code`** command", delete_after=3)

            await message.delete(delay=1)
            logger.info(f"Deleted message ({message.id})")


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
        name="verify", 
        description="Verify yourself",
        guild=server,
    )
@app_commands.describe(email="Please enter your IITM Student mail id")
async def verify_slash_cmd(interaction: Interaction, email: str):
    global mybot, verification_msg, email_tracker

    if interaction.user.get_role(IDs.not_verified_role) is None:
        await interaction.response.send_message("### You are already verified.", ephemeral=True, delete_after=3)
        return

    if interaction.channel_id != IDs.verify_channel:
        logger.warning(f"User ({interaction.user.id}) tried to use /verify command in wrong channel")
        await interaction.response.send_message("### You are not allowed to use this command.", ephemeral=True, delete_after=3)
        return

    if email_tracker.get(interaction.user.id) is not None:
        logger.warning(f"User ({interaction.user.id}) tried to use /verify command AGAIN with email: '{email}'")
        await interaction.response.send_message("You have already used **`/verify`** command\nIf you think you've entered wrong mail, use **`/reset`** command.", ephemeral=True, delete_after=7)
        return

    logger.info(f"User ({interaction.user.id}) used /verify command with email: '{email}'")
    await interaction.response.send_message("## Validating email id ⏳", ephemeral=True)
    await mybot.send_message(mybot.log_channel, f"**{interaction.user.name}** is verifying.")

    if not parse_email(email):
        logger.warning(f"User ({interaction.user.id}) entered invalid email.")
        await interaction.edit_original_response(content=
                f"""### Invalid email!\nYou entered: `{
                    email if len(email) < 40 else f"{email[:40]}..."
                }`\nPlease enter a valid **IITM Student Mail Id** in this format: `<roll_no>@*study.iitm.ac.in`"""
                )
        await asyncio.sleep(7)
        await interaction.delete_original_response()
        return
    

    gen_code = email_code_gen(email)
    logger.info(f"Generated code - {gen_code} sent to '{email}'")

    email_tracker[interaction.user.id] = [email, gen_code]
    logger.info(f"Emails in queue: {len(email_tracker)}")

    verification_msg = await interaction.edit_original_response(content="## Verification\nWe have sent the verification code in your email.\nUse **`/code`** command to enter the latest code.\n\n**Note:** Check spam folder if not present in inbox.")
    print(verification_msg)


@command_tree.command(
        name="code", 
        description="Enter the code received in your mail",
        guild=server,
    )
@app_commands.describe(code="Please enter the verification code received in your mail")
async def verify_code_slsh_cmd(interaction: Interaction, code: int):
    global mybot, verification_msg, email_tracker

    if interaction.user.get_role(IDs.not_verified_role) is None:
        await interaction.response.send_message("### You are already verified.", ephemeral=True, delete_after=3)
        return

    if interaction.channel_id != IDs.verify_channel:
        await interaction.response.send_message("### You are not allowed to use this command.", ephemeral=True, delete_after=3)
        return


    user = interaction.user
    logger.info(f"User ({user.id}) used /code command with code: {code}")

    if email_tracker.get(user.id) is None:
        logger.warning(f"User ({user.id}) used /code command WITHOUT using /verify command first")
        await interaction.response.send_message("Please use **`/verify`** command first to get the code", ephemeral=True, delete_after=5)
        return
    email = email_tracker[user.id][0]
    await verification_msg.delete(delay=3)

    await interaction.response.send_message("## Verifying the code!", ephemeral=True)

    if email_tracker[user.id][1] != code:
        logger.warning(f"User ({user.id}) entered invalid code: {code}\nCorrect code: {email_tracker[user.id][1]}")

        await interaction.edit_original_response(content=
                f"""### Invalid code!\nPlease enter the correct 6-digit code."""
                )
        await asyncio.sleep(5)
        await interaction.delete_original_response()
        return
    
    await interaction.edit_original_response(content="### Code is Valid!\n## You are Verified!")

    await mybot.send_message(mybot.log_channel, f"**{user.name}** is verified. ✅")

    not_verified_role = utils.get(user.guild.roles, id=IDs.not_verified_role)
    iitm_role = utils.get(user.guild.roles, id=IDs.verified_iitm_role)
    branch_role = utils.get(user.guild.roles,
                            id=IDs.ds_role if "ds" in email.lower() else IDs.es_role
                            )
    await user.add_roles(iitm_role)
    await user.add_roles(branch_role)
    if not (details:=check_presence(email)):

        logger.warning(f"User ({user.id}) verified with email: '{email}' but is not from Pichavaram House")
        await interaction.followup.send(
            content=f"""# Welcome _{user.display_name}_ to our server. 
            Hope you will enjoy here. 😊""",
            ephemeral=True
            )
        await user.remove_roles(not_verified_role)
        return

    pichavaram_role = utils.get(user.guild.roles, id=IDs.pichavaram_role)
    grp_role = utils.get(user.guild.roles, id=IDs.group_no[details["grp_no"]])


    await user.add_roles(pichavaram_role)
    await user.add_roles(grp_role)

    if details["GL"]=="YES":
        await user.add_roles(utils.get(user.guild.roles, id=IDs.GL[details["grp_no"]]))

    logger.info(f"User ({user.id}) verified with email: '{email}' and is from Pichavaram House")
    await interaction.followup.send(
        content=f"""# Welcome _{user.display_name}_ to our server. 😀
        You are **{details["dept"].upper()}** student of **`20{email[:2]}`** year.
        You belongs to Group **`{details["grp_no"]}`**.\n_You will get access to exclusive channels_ :wink: :handshake:\n### As you are one of the Pichavites. 🌟""",
        ephemeral=True
        )
    
    await user.remove_roles(not_verified_role)
    await asyncio.sleep(3)
    await interaction.delete_original_response()
    del email_tracker[interaction.user.id]
    logger.info(f"Emails in queue: {len(email_tracker)}")


@command_tree.command(
        name="reset", 
        description="Reset Email Verification",
        guild=server,
    )
async def reset_slash_cmd(interaction: Interaction):
    global verification_msg, email_tracker

    if interaction.user.get_role(IDs.not_verified_role) is None:
        await interaction.response.send_message("### You are already verified.", ephemeral=True, delete_after=3)
        return

    if interaction.channel_id != IDs.verify_channel:
        await interaction.response.send_message("### You are not allowed to use this command.", ephemeral=True, delete_after=3)
        return

    if None in (verification_msg, email_tracker.get(interaction.user.id)):
        logger.warning(f"User ({interaction.user.id}) used /reset command WITHOUT using /verify command first")
        await interaction.response.send_message("You have not provided email yet.\nPlease use **`/verify`** command first.", ephemeral=True, delete_after=5)
        return
    
    await verification_msg.delete(delay=3)
    await interaction.response.send_message("## Resetting your verification!", ephemeral=True)

    del email_tracker[interaction.user.id]
    logger.info(f"User ({interaction.user.id}) reset the email verification")
    logger.info(f"Emails in queue: {len(email_tracker)}")
    await interaction.edit_original_response(content="## Verification Reset Successful!\nYou can use **`/verify`** command again.")

    await mybot.send_message(mybot.log_channel, f"{interaction.user.name} has reset their verification.")
    await asyncio.sleep(5)
    await interaction.delete_original_response()


if __name__ == "__main__":
    mybot.run(token=TOKEN)
