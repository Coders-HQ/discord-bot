CHQ_WELCOME_MESSAGE = """
Hello and welcome fellow Wizard! 🧙‍♂️ This is a contributor only server where active contributors of CHQ work on different parts of the platform in teams.

Structure of the Channels:

•    Teams - represents all the roles (aka teams) we have on the server. Roles will be assigned manually by management team. 

•    Projects - represents all currently active projects CodersHQ Wizards  man_mage   are working on, and each project may have multiple teams working on them (e.g. ui and python-dev).

To find more about the avaliable tasks and projects we are working on, please go through <#947073435895468063> channel, or check the pinned messages on the channels which are usually the tasks that a specific team are working on.

Have a look around and spend some time at each channel to get familiar with the teams. Also, If you find something you like to help with you can ask the team directly and they will happily help you out. 

If you are still unsure then ask on <#947073932719190086> we will help guide you to a task that you will enjoy the most. Have fun!
"""

GUILD_ID = 934517768898883605

LOG_CHANNELID = 949725775374995576

MEMBERCOUNT_CHANNELID = 934517769343471707

MODERATION_CHANNELID = 951213425164427325

BOT_COLOR = 0x00afb1

USER_COMMANDS = {'!chq':"Command is used to provide information and details on coders(hq) and it's initiatives.",
                 '!count':"View current member count of server",
                 '!resources':"Command coders regardless of their experience can use to find quality resources on a list of languages",
                 '!serverage':"Time since the user has joined the server"}
ADMIN_COMMANDS = {'!kick':"Command is used to kick a user",
                  '!ban':"Command used to ban a user from the server",
                  '!unban':"Command used to unban a user from the server",
                  '!mute':"Command used to mute a user from the server",
                  '!unmute':"Command used to unmute a user from the server",
                  '!purge':"Command used to purge n number of messages from the channel in the server"}
ALL_COMMANDS = {}
ALL_COMMANDS.update(USER_COMMANDS),ALL_COMMANDS.update(ADMIN_COMMANDS)