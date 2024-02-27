# About Hiddify Manager Bot

This bot currently only works with API version 1.

And this bot is for testing purposes.

# Installation Steps:

<b>1. Update and upgrade system packages:</b>

`apt update && apt upgrade -y`

<b>2. Install Python 3 and pip:</b>

`apt install python3 && apt install python3-pip`

<b>3. Clone the bot repository:</b>

`apt install git -y`

`git clone https://github.com/Hiddify-Return/Hiddify-Manager-Bot.git`

<b>4. Navigate to the cloned directory:</b>

`cd Hiddify-Manager-Bot`

<b>5. Install required Python packages:</b>

`pip install -r requirement.txt`

# Configuration:

<b>1. Open `api.py` with an editor like nano:</b>

`nano api.py`

<b>2. Edit the following lines according to your configuration:</b>

```python
ALLOWED_USER_IDS = [11111111] # get it from https://t.me/userinfobot
ADMIN_UUID = "Admin-UUID"
ADMIN_URLAPI = "https://Admin-UURL"
SUBLINK_URL = "https://subscription_URL"
TELEGRAM_TOKEN = "BOT-TOKEN"
```
Replace the placeholders with your actual values.

# Running the Bot:

<b>1.Run the bot temporarily:</b>

`python3 telegram_bot.py`

# Creating a systemd Service (Optional):
<b>1. Create a systemd service file:</b>

`nano /etc/systemd/system/telegram_bot.service`

<b>2. Paste the following content into the file:</b>

```
[Unit]
Description=HiddifyBOT Service
After=network.target

[Service]
WorkingDirectory=/root/Hiddify-Manager-Bot/
ExecStart=/usr/bin/python telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
``` 
<b>3. Reload systemd and enable/start the service:</b>

`sudo systemctl daemon-reload`

`sudo systemctl enable telegram_bot`

`sudo systemctl start telegram_bot`

Now, your Hiddify Manager Bot should be set up and running as a systemd service, ready to serve its purpose. Make sure to replace placeholder values with your actual configuration details.
