CHQ_WELCOME_MESSAGE = """
Hello and welcome fellow Wizard! 🧙‍♂️ This is a contributor only server where active contributors of CHQ work on different parts of the platform in teams.

Structure of the Channels:

•    Teams - represents all the roles (aka teams) we have on the server. Roles will be assigned manually by management team. 

•    Projects - represents all currently active projects CodersHQ Wizards  man_mage   are working on, and each project may have multiple teams working on them (e.g. ui and python-dev).

To find more about the avaliable tasks and projects we are working on, please go through <#947073435895468063> channel, or check the pinned messages on the channels which are usually the tasks that a specific team are working on.

Have a look around and spend some time at each channel to get familiar with the teams. Also, If you find something you like to help with you can ask the team directly and they will happily help you out. 

If you are still unsure then ask on <#947073932719190086> we will help guide you to a task that you will enjoy the most. Have fun!
"""

MEMBERCOUNT_CHANNEL = 0
LOG_CHANNEL = 0
MODERATION_CHANNEL = 0
BOT_COLOR = 0x00AFB1

USER_COMMANDS = {
    "chq": "Command is used to provide information and details on coders(hq) and it's initiatives.",
    "count": "View current member count of server",
    "resources": "Command coders can use to find quality resources on a list of languages",
    "help": "Command to show all the existing command based on user heirarchy",
    "age": "Time since the user has joined the server",
    "features": "Command used to gain descriptions on certain features of the coders(hq) platform",
    "ping": "Ping the bot to see if it gives any response back or is online",
    "self-role": "Command used to assign role to the user",
    "remove-role": "Command used to remove the self role from the user",
}

ADMIN_COMMANDS = {
    "kick": "Command is used to kick a user",
    "ban": "Command used to ban a user from the server",
    "unban": "Command used to unban a user from the server",
    "mute": "Command used to mute a user from the server",
    "unmute": "Command used to unmute a user from the server",
    "purge": "Command used to purge 'n' number of messages from a channel in the server",
    "softban": "Command used to apply softban to user for 60 seconds",
    "timeout": "Command used to apply timeout to a user for given minutes",
    "lockdown": "Command used to put the channel into slowmode of given seconds",
    "table-create": "Command used to create the table incase it got deleted",
    "reconnect-db": "Command used to attempt a reconnection to the database",
}

ISSUES_COMMANDS = {
    "list": "Command used to list all the issues in the repo",
    "get": "Command used to get the issue with given id",
    "create": "Command used to create an issue with given options",
    "update": "Command used to update the existing issue with given options",
    "close": "Command used to close the issue with given id",
}

ALL_COMMANDS = ADMIN_COMMANDS | ISSUES_COMMANDS

URL_THUMBNAIL = "https://www.arsal.xyz/CHQAssets/CHQLogo.png"

CHQ_WHO = {
    "title": "Who We Are?",
    "description": "Coders HQ is a community for all coders in the UAE to come and empower their skills and mindset with the power of code.",
    "color": BOT_COLOR,
    "image": {"url": URL_THUMBNAIL},
    "fields": [
        {
            "name": "To Know More:",
            "value": "/chq [command]\n\n*Available commands are listed below:*",
        },
        {
            "name": "Command - Description",
            "value": "what - What We Do\nevents - Events\ninvolve - Get Involved",
        },
    ],
}

CHQ_EVENTS = {
    "title": "Events",
    "description": "**1.** Upskilling workshops offered by coders HQ, in different coding-related verticals.\n\n**2.** Meeting and Networking with like-minded individuals in your field.\n\n**3.** Prior registration opportunity for new announcements by the coders HQ.\n\n**4.** Different engagement opportunities with representatives of different companies.\n\n**5.** Having the ability to place suggestions of new activities that are coding-related.\n\n**6.** Articles of interest published and shared by the community.",
    "color": BOT_COLOR,
    "image": {"url": URL_THUMBNAIL},
}

CHQ_WHAT = {
    "title": "What We Do?",
    "description": "**1. HQ Learn:** Upskilling hands-on workshops, provided by the coders HQ network.\n**2. HQ Assessment:** Assess yourself in different coding skills  that are demanded by the industry.\n**3. HQ Meetups:** Join a user group meetup.\n**4. HQ Challenges:** Try resolving a challenge, create impact and get rewarded with a prize.\n**5. HQ Hackathons:** Be part of the upcoming hackathon.\n**6. HQ Conferences:** Be part of the world biggest coding-related conferences.\n**7. HQ Get Inspired:** Listen to those who might inspire you.\n**8. HQ Internships:** Take an internship at the coders HQ or with its partners.",
    "color": BOT_COLOR,
    "image": {"url": URL_THUMBNAIL},
}

CHQ_INVOLVE = {
    "title": "Get Involved",
    "description": "We would love to have you involved in any one of our projects, have a look at our [Github](https://github.com/Coders-HQ/CodersHQ) to learn more!",
    "color": BOT_COLOR,
    "image": {"url": URL_THUMBNAIL},
}

SELF_ROLES = {
    "Open Source": "👥",
    "Robotics": "🤖",
    "DevOps": "👁‍🗨",
    "Embedded Systems": "📻",
    "Ethical Hacking": "🕵️‍♂️",
    "Virtual Reality": "🥽",
    "Blockchain": "🪙",
    "App Development": "📱",
    "Artificial Intelligence": "👾",
    "Retail Analytics": "🛒",
    "Web Development": "🕸️",
}
