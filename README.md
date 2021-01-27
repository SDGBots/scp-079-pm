# SCP-079-PM

Everyone can have their own Telegram private chat bot.

This project provides python code of a Telegram private chat forwarding bot.

## How to use

- See [this article](https://scp-079.org/pm/) to build a bot by yourself
- [README](https://github.com/scp-079/scp-079-readme) of the SCP-079 Project
- Discuss [group](https://t.me/SCP_079_CHAT)

## Requirements

- Python 3.6 or higher
- pip: `pip install -r requirements.txt` or `pip install -U APScheduler pyAesCrypt pyrogram[fast]`

## Files

- plugins
    - functions
        - `channel.py` : Functions about channel
        - `deliver.py` : I am a delivery boy
        - `etc.py` : Miscellaneous
        - `file.py` : Save files
        - `filters.py` : Some filters
        - `ids.py` : Modify id lists
        - `receive.py` : Receive data from exchange channel
        - `telegram.py` : Some telegram functions
        - `timers.py` : Timer functions
        - `user.py` : Functions about user
    - handlers
        - `callback.py` : Handle callbacks
        - `command.py` : Handle commands
        - `message.py` : Handle messages
    - `glovar.py` : Global variables
- `.gitignore` : Ignore
- `config.ini.example` -> `config.ini` : Configuration
- `LICENSE` : GPLv3
- `main.py` : Start here
- `README.md` : This file
- `requirements.txt` : Managed by pip

## Contribute

Welcome to make this project even better. You can submit merge requests, or report issues.

## Credit
This is a fork (forked on 1/26/2021 PST) of the repo from scp-079 (https://github.com/scp-079) project.

## License

Licensed under the terms of the [GNU General Public License v3](LICENSE).
