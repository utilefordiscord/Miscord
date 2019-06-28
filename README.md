<img align="center" src="https://ialex11.github.io/assets/miscord-logo.png" />
<h3 align="center">The revolutionary music bot for Discord is here</h1>
<div align="center">

![projectVersion](https://img.shields.io/badge/-v1.0-9cf.svg?link=https://utileForDiscord.github.io/miscord/latest) ![discordPyVersion](https://img.shields.io/badge/discord.py-1.2.2-9EA6F9.svg?logo=discord&logoColor=white&link=https://github.com/Rapptz/discord.py&link=https://utileForDiscord.github.io/miscord/docs/libs#discord)

</div>

<br>

## Why Miscord?
Miscord is a project by the [Utile Developers Team](https://github.com/orgs/utilefordiscord/teams/developers/members) for the **Discord Hack Week**, which lasted from June 24 to June 28, 2019.

It is a Discord bot made in Python which allows you to create songs using `discord.py`'s internal voice support and a custom implementation of the Github NoopsChallenge's Drumbot API, play songs from the internet, display the lyrics and information of the song (Genius) and more fun and entertaining things like a leveling system for your server.

## Get Started
Using **Miscord** is a really straight-forward process.

Invite Miscord from [this link](https://utileForDiscord.github,io/miscord/invite).<br>
Once done that, the owner of the server will receive a guide from Miscord that will show how to set up it for the server.

To get a full detailed list of all the Miscord commands, go [here](https://utileForDiscord.github.io/miscord/commands).

## Team
The awesome **Utile Developers Team** is formed by:

- **Tilda** | <a href="https://github.com/tilda" rel="some text"><img href="example.com" src="https://ialex11.github.io/assets/github.svg" width="16" height="16" title="500px" alt="500px"></a> <a href="https://www.reddit.com/u/RShotZz" rel="some text"><img href="example.com" src="https://ialex11.github.io/assets/reddit.svg" width="16" height="16" title="500px" alt="500px"></a>

- **Semiak** | <a href="https://github.com/iAlex11" rel="some text"><img href="example.com" src="https://ialex11.github.io/assets/github.svg" width="16" height="16" title="500px" alt="500px"></a> <a href="https://www.reddit.com/u/iAlex11" rel="some text"><img href="example.com" src="https://ialex11.github.io/assets/reddit.svg" width="16" height="16" title="500px" alt="500px"></a> <a href="https://twitter.com/semiak_" rel="some text"><img href="example.com" src="https://ialex11.github.io/assets/twitter.svg" width="16" height="16" title="500px" alt="500px"></a>

- **Blue** | <a href="https://github.com/bluecification" rel="some text"><img href="example.com" src="https://ialex11.github.io/assets/github.svg" width="16" height="16" title="500px" alt="500px"></a> <a href="https://www.reddit.com/u/an516" rel="some text"><img href="example.com" src="https://ialex11.github.io/assets/reddit.svg" width="16" height="16" title="500px" alt="500px"></a> <a href="https://twitter.com/bluecantcode" rel="some text"><img href="example.com" src="https://ialex11.github.io/assets/twitter.svg" width="16" height="16" title="500px" alt="500px"></a>

- **SemiColon** | <a href="https://github.com/semiicolon" rel="some text"><img href="example.com" src="https://ialex11.github.io/assets/github.svg" width="16" height="16" title="500px" alt="500px"></a>

## Contributing
In the nature of open-source, all types of suggestions are accepted and fully appreciated, just make a pull request or send us a message in the [Support Server](discord.gg/supportserverlinkgoeshere) and we'll try to review it.

To report a bug go to the [Miscord Public Bug Tracker](bugs.semiak.dev) or make a [new issue](https://github.com/utileForDiscord/miscord/issues).

Alternatively, you can use **Miscord**'s `m!feedback` command.

#### Installing source
If you want to run your own development version of Miscord, you can achieve that easily.

##### Requirements
1. Have both **npm** and **Node.js** installed (for discord-leveling API).
2. Python 3.6 or newer.
3. Have discord.py 1.2.2 or higher.

##### Getting Started
Run the following commands:
```bash
git clone --recursive https://github.com/utilefordiscord/miscord.git #clones repo and its submodules
cd Miscord && pip install -r dependencies.txt #accesses folder and installs the dependencies required for Miscord to run
```

All the Miscord discord.py code is found at the `/src` directory.
Do all the changes you want, and then use the following command to run it:
```
npm start
```

This will try to parse an instance.json file containing the tokens for the bot to run.
If there's no file, it'll ask you for the discord bot token and Genius token and then will proceed to generate the file so you don't need to do this again.

## Disclaimer
Both Utile and Miscord are made by the [Utile Developers Team](https://github.com/orgs/utilefordiscord/teams/developers/members).      

Do not distribute or modify this software without permission.

<div align="center"><sup>Copyright @ 2019 <a href="https://github.com/orgs/utilefordiscord/teams/developers/members">Utile Developers Team</a>.</sup></div>
