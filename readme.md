# Discord Verification Bot

A Discord verification bot made for Pichavaram House's Discord server.

It is use to verify the users who joins the Pichavaram Discord server, by verifying their student email id with the otp, and assign roles based on the email id. It also keep logs of the verification process.

## Index

-   [About Pichavaram House](#about-pichavaram-house)
-   [How to use](#how-to-use)
    -   [Application Commands](#application-commands)
    -   [How it works](#how-it-works)
    -   [Requirements](#requirements)
    -   [How to run](#how-to-run)
    -   [File Structure](#file-structure)
-   [Checklist](#checklist)
-   [Want to contribute?](#want-to-contribute)
    -   [How to contribute?](#how-to-contribute)

### About Pichavaram House

[Pichavaram House](https://sites.google.com/student.onlinedegree.iitm.ac.in/pichavaramhouse/home?authuser=0) is one of the 12 Official Houses of [IIT Madras BS Degree](https://study.iitm.ac.in/ds/).

Being the Web Administrator of Pichavaram House for 2023-24, I have created this bot.

## How to use

The bot is mainly used in #verify-here channel of Pichavaram House Discord server only.

### Application Commands

#### `/verify <email id>`

-   This command is used to verify the user.
-   It asks for the email id of the user.
-   And if it's a valid email id, it sends an OTP to the email id.

#### `/code <otp>`

-   This command is used to verify the OTP sent to the email id.
-   It asks for the OTP sent and checks if it's correct.
-   If it's correct, it gives the user the role of a verified user.
-   And other required roles such as:
-   -   If the user is of Pichavaram house, it gives the role of Pichavaram house and their respective group no.
-   -   If not, it gives Other House member role.
-   -   Apart from the above roles, it also gives their branch role (DS/ES). [DS - Data Science, ES - Electronic Systems] and their respective group no. role with the Group Leader role if they are.

#### `/reset`

-   This command is used to reset the verification.
-   If user entered wrong email id, or there's some typo and not able to receive the OTP, they can use this command to reset the verification process.
-   After reseting, they can verify again using the [`/verify`](#verify-email-id) command.

> It also logs each activity of the verification process in a log file as well as in a log channel.

### How it works

-   First it takes the email id of the user using the [`/verify`](#verify-email-id) command.
-   Then it parses the email id according to the format required.
-   If It's parses correctly, it sends an OTP to the email id.
-   If it's not, it asks to again enter the email id.
-   Then it asks for the OTP sent to the email id using the [`/code`](#code-otp) command.
-   If the OTP is correct, it gives the required roles to the user. Else it asks to enter the OTP again.
-   If the user wants to reset the verification process, they can use the [`/reset`](#reset) command.
-   It also logs each activity of the verification process in a log file and in a log channel.
-   For the multi-users verifying at same time, it handles the synchronization of the data as well.

### Requirements:

All the requirements are mentioned in the [`requirements.txt`](./requirements.txt) file.

-   `Python 3.10.12` or above
-   `discord.py 2.3.2`
-   `python-dotenv 1.0.0`

### How to run

-   Clone the repository
-   Install the requirements using `pip install -r requirements.txt`
    > Make sure you have created the virtual environment and activated it before installing the requirements.
-   Create a `.env` file in the root directory of the project.
-   Add the following variables in the `.env` file:

```
DISCORD_TOKEN=<your discord bot token>
ACC_EMAIL=<your email id to send emails>
ACC_PSWD=<your google acc app password to send emails>
```

> Discord bot token can be obtained from [Discord Developer Portal](https://discord.com/developers/applications).
>
> Make sure to on the **Privileged Gateway Intents** and provide required permissions to the bot. Also, don't forget to add the bot in server 😂
>
> Google account passkey can be obtained from [Google Account App passwords](https://myaccount.google.com/apppasswords).

-   Create `ids.json` file which contains the ids of the roles and channels used in the bot.
-   Create `data.csv` file which contains the data of respective house users.
    > **Note**: You need to change the variables in [`bot.py`](./bot.py) file accordingly.
    > All the ids can be obtained from `IDs` class.
-   Run the bot using:

```bash
python3 main.py
```

Or better to create a docker image and run the bot in it.

```bash
sudo docker build -t . dc-verification-bot
sudo docker run -it dc-verification-bot
```

-   You can keep track of the actions done with bot in [`discord-bot.log`](./discord-bot.log) file.

### File Structure

```bash
.
├── .gitignore
├── .env
├── ids.json
├── data.csv
├── README.md
├── main.py
├── bot.py
├── utils.py
├── discord-bot.log     // created automatically
└── requirements.txt
```

-   [`main.py`](./main.py) - Main file to run the bot.
-   [`bot.py`](./bot.py) - Contains the bot commands and other functions.
-   [`utils.py`](./utils.py) - Contains the utility functions such as parsing email id, sending email, generating otp etc...

## Checklist

A checklist of all the tasks and features to be done.

-   [x] Start bot
-   [x] Add data
-   [x] Bot can msg
-   [x] Application commands
-   [x] Parse email
-   [x] Able to Verify
-   [x] fetch details
-   [x] Email OTP
-   [x] Verify OTP
-   [x] Synchronize multi-user at a time
-   [x] Status added
-   [x] Log data in a channel and in a file
-   -   [x] Details when joined with user id and email id in a file.
-   -   [x] Log details in a channel
-   -   [x] Above details with username, role assigned in channel
-   [x] Add Embedded msgs rather than text messages
-   [x] Change Roles
-   [x] Host the bot

## Want to contribute?

-   You can contribute to this project by adding new features, fixing bugs, improving the code, etc...

### How to contribute?

-   Fork the repository
-   Clone the repository
-   Create a new branch
-   Make changes in the code
-   Commit the changes
-   Push the changes to your forked repository

> Please contact me at my [email id](mailto:rubercuber.30@gmail.com) while contributing.

### Contributors
-   [Parampreet Singh](https://github.com/Param302)
-   [Yash Mehrotra](https://github.com/ReDxDaGer)
