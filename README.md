<div align="center">
    <a href='https://ai.gov.ae/codershq/'>
        <picture>
            <source media="(prefers-color-scheme: dark)" srcset="https://www.arsal.xyz/CHQAssets/CHQLogo.png">
            <img alt="White CHQ logo in dark mode and dark CHQ logo in light mode" src="https://www.arsal.xyz/CHQAssets/CHQLogoYellow.png" width="500">
        </picture>
    </a>
    <h1>CodersHQ Discord Bot</h1>
    <a href="/LICENSE.md" style="text-underline:none">
      <img height="19" src="https://img.shields.io/badge/License-MIT-red.svg">
    </a>
    <a href="https://dsc.gg/codershq">
        <img height="19" src="https://discordapp.com/api/guilds/910100464496963584/widget.png">
    </a>
    <a>
        <img src="https://img.shields.io/github/all-contributors/Coders-HQ/discord-bot?color=ee8449&style=flat-square)">
    </a>
</div>

<h2 id="toc">📝 Table of Contents</h2>
<ol>
    <li><a href="#intro">Introduction</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#dependencies">Dependencies</a></li>
    <li><a href="#setup">Setup</a></li>
    <ul>
        <li><a href="#bot-creation">Discord bot creation</a></li>
        <li><a href="#github-settings">GitHub settings</a></li>
        <li><a href="#env">Setup environment variables</a></li>
        <li><a href="#run-direct">Running the files directly</a></li>
        <li><a href="#run-docker">Getting up and running locally with Docker</a></li>
    </ul>
    <li><a href="#contributors">Contributors</a></li>
</ol>

<h2 id="intro">🤖 Introduction</h2>
    <p>
        The CodersHQ Discord Bot is a general-purpose bot designed to communicate with the CodersHQ platform to announce events, moderate, and gamify servers.
    </p>

<div align="right">
    <a href='#toc'>Back to top ↥</a>
</div>

<h2 id="features">🧠 Features</h2>
    <p>The CHQ Discord Bot comes with these features:
    <ul>
        <li>Logging</li>
            <ul>
                <li>Member messages that are profane</li>
                <li>Member join/leave</li>
                <li>Member message edits</li>
                <li>Member message deletes</li>
                <li>Member updates</li>
            </ul>
        <li>Commands to interact with the bot</li>
        <li>Moderation</li>
            <ul>
                <li>Kick members</li>
                <li>Ban/Unban members</li>
                <li>Mute/Unmute members</li>
                <li>Purge messages</li>
                <li>Softban members</li>
                <li>Timeout members</li>
                <li>Lockdown channels</li>
            </ul>
        <li>Manage GitHub Issues within discord server</li>
            <ul>
                <li>Create/Edit GitHub issues</li>
                <li>Fetch all/specific GitHub issues</li>
                <li>Close GitHub issues</li>
            </ul>
    </ul>

<div align="right">
    <a href='#toc'>Back to top ↥</a>
</div>

<h2 id="dependencies">🛠️ Dependencies</h2>
    <p>There are requirements to run the bot, namely:</p>
    <ul>
        <li>Python 3.10+</li>
        <li>Postgres server (only if the <code>/mute</code> command is used)</li>
        <li>GitHub PAT (only if the <code>/issue</code> commands are used)</li>
        <li>Docker (optional for containerized deployment)</li>
        <li>Libraries in <code><a href="/requirements.txt">requirements.txt</a></code></li>
        <li><code>.env</code> file to hold environment variables (same format from <code><a href="sample.env">sample.env</a></code>)</li>
        <li>Discord server requirements:</li>
        <ul>
            <li>Bot must have all the moderation and read permissions</li>
            <li>"Muted" role in server</li>
            <li>"moderation" and "micro-logs" channels in server</li>
        </ul>
    </ul>

<p>We recommend installing these dependencies in a <a href="https://medium.com/python-environments/learn-python-venv-in-under-5-minutes-42205842cabd">Python Virtual Environment</a> to keep management easy. To install all the libraries inside <code><a href="/requirements.txt">requirements.txt</a></code> quickly, run this command in the root folder: <code>python -m pip install -r requirements.txt</code></p>

<div align="right">
    <a href='#toc'>Back to top ↥</a>
</div>

<h2 id="setup">⚙️ Setup</h2>
<p>
    There are some steps that needs to be followed in order for the bot to connect with Discord API as well as for the proper functioning of all the <a href="#features">bot features </a> mentioned above.
</p>
<h3 id="bot-creation">⭐ Discord Bot Creation</h3>
<p>
    To begin inviting and running a Discord bot onto your server, first of all, you need to head over to <a href="https://discord.com/developers">Discord Developers Portal</a> and create your bot there. After that, you need to retrieve your <a href="https://www.writebots.com/discord-bot-token/">bot token</a> and create a <a href="https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks">webhook URL (ignore the "Quick Example" section)</a>, both of which you need to save for later. Finally, you need to make some changes in the server:
    <ul>
        <li>
            Create a "Muted" role in your server (only if you want the <code>/muted</code> command to work)
        </li>
        <li>
            Create "moderation" and "micro-logs" channels in your server for the moderation panel and in-server logs to show up
        </li>
        <li>
            <a href="https://www.writebots.com/discord-bot-token#5-add-your-bot-to-a-discord-server">
                Invite your bot to the required server
            </a>
        </li>
    </ul>
</p>

<div align="right">
    <a href='#toc'>Back to top ↥</a>
</div>

<h3 id="github-settings">🐙 GitHub Settings</h3>
<p>
    Once the Discord bot is created and installed to the server, the next step is to connect the code with the bot we just added to the server. Start by <a href="https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository">cloning the repository</a> to get access to the code. You will also need a PAT from GitHub (explained <a href="https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token">here</a> on how to get). The PAT is only needed if you wish to manage issues for a repository within the discord server.
</p>

<div align="right">
    <a href='#toc'>Back to top ↥</a>
</div>

<h3 id="env">🍀 Setup Environment Variables</h3>
<p>
    To run the Discord bot, you need to setup environment variables. This can be done by adding a <code>.env</code> file to the root directory of your clone*. The <a href="/sample.env"><code>sample.env</code></a> file contains required variables to be defined. All these variables <strong>MUST</strong> be present, even if the value is empty.<br>
    Note that the field with the values are the ones that are expected by the docker container and not what is expected if the bot runs directly. Also note that if you don't have the value for an environment variable, leave it blank, do not delete the entire field instead.
    Here's what each field represents:
</p>
<ul>
    <li>
        <code>TOKEN</code> field should contain your Discord bot token that you generated earlier.
    </li>
    <li>
        <code>WEBHOOK_URL</code> field should contain your webhook URL from the webhook that you created earlier.
    </li>
    <li>
        <code>DB_HOST</code> field should contain the host in which your postgres server is running (usually <code>localhost</code> but <code>micro_postgres</code> (name of the postgres service inside <code><a href='/docker-compose.yml'>docker-compose.yml</a></code>), if you are using Docker)
    </li>
    <li>
        <code>DB_USER</code> field should contain the user to connect to in the server (usually <code>postgres</code>)
    </li>
    <li>
        <code>DB_PASS</code> field should contain the password of the user to connect to the server (usually <code>root</code>)
    </li>
    <li>
        <code>DB_PORT</code> field should contain the port where the postgres service is running (usually <code>5432</code>)
    </li>
    <li>
        <code>DB_DATABASE</code> field should contain the database to connect to (usually <code>postgres</code>, but <code>micro</code> is kept default for docker.)
    </li>
    <li>
        <code>PGADMIN_MAIL</code> field should contain the mail (any) to connect to pgadmin for viewing (only required if running via docker)
    </li>
    <li>
        <code>GITHUB_TOKEN</code> field should contain a <a href="https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token">PAT (Personal Access Token)</a> generated from your account.
    </li>
    <li>
        <code>GITHUB_REPO</code> field should contain your repository in the format <code>username/repository_name</code>
    </li>
</ul>
Do <strong>NOT</strong> upload your <code>.env</code> file to your GitHub repository as it contains sensitive information that shouldn't be published online.
</p>

<div align="right">
    <a href='#toc'>Back to top ↥</a>
</div>

<h3 id="run-direct">🧑‍💻 Run the files directly</h3>
<p>
    It's finally time! Once you're done with steps above, run this command once you have switched directory to <code>micro</code> folder: <code>python main.py</code>. 
    Your Discord bot should now be online on your server as long as the code is running.
</p>

<div align="right">
    <a href='#toc'>Back to top ↥</a>
</div>

<h3 id="run-docker">🐋 Run the containarized Discord bot with Docker (Alternative)</h3>
<p>
This step is optional, and you may skip it if you wish to run the discord bot via local python files. The root folder contains a <code><a href="docker-compose.yml">docker-compose.yml</a></code> file and a <code><a href="Dockerfile">Dockerfile</a></code>, which are used for creating the services and container image respectively.

To build the stack, execute this command:

```
docker-compose -f docker-compose.yml build
```

Then, to run the stack, execute this command:

```
docker-compose -f docker-compose.yml up
```

To run it in detached (background) mode, use:

```
docker-compose -f docker-compose.yml up -d
```

You can use this command to stop the stack whenever you wish:

```
docker-compose -f docker-compose.yml down
```

but keep in mind that the volumes containing the database will still be intact. To delete those, you can check the volume names that are currently attached to your container by executing this command: <code>docker volume ls</code>, and then executing this command individually on each volume that you want to delete to get a fresh start:

```
docker volume rm <name_of_volume>
```

</p>

<div align="right">
    <a href='#toc'>Back to top ↥</a>
</div>

## 🖥️ Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/arsxl"><img src="https://avatars.githubusercontent.com/u/69077626?v=4?s=100" width="100px;" alt="Muhammad Arsalan Nawazish"/><br /><sub><b>Muhammad Arsalan Nawazish</b></sub></a><br /><a href="https://github.com/Coders-HQ/discord-bot/commits?author=arsxl" title="Code">💻</a> <a href="#maintenance-arsxl" title="Maintenance">🚧</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nihaalnz"><img src="https://avatars.githubusercontent.com/u/110490083?v=4?s=100" width="100px;" alt="Nihaal Nz"/><br /><sub><b>Nihaal Nz</b></sub></a><br /><a href="https://github.com/Coders-HQ/discord-bot/commits?author=nihaalnz" title="Code">💻</a> <a href="#maintenance-nihaalnz" title="Maintenance">🚧</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

<div align="right">
    <a href='#toc'>Back to top ↥</a>
</div>

<h2>✨ Want to contribute?</h2>
<p>
If you wish to contribute, create a fork and put up a PR explaining the changes you have made. You can also get more information or help by joining the discord server (linked at the top).
</p>

<br>

<h6>*This same file will be used to supply environment variables to the docker container as well</h6>

<div align="right">
    <a href='#toc'>Back to top ↥</a>
</div>

