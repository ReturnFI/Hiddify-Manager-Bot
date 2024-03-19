#!/bin/bash

clear && echo -e "\n\nStart installing the bot!\n\n" && sleep 1

apt update && apt upgrade -y || { echo -e "\n\nFailed to update and upgrade packages. Exiting...\n\n"; exit 1; }
apt install python3 python3-pip git python3-dev python3-venv -y || { echo -e "\n\nFailed to install required packages. Exiting...\n\n"; exit 1; }


if pgrep -f "python3 telegram_bot.py" &> /dev/null; then
    pkill -f "python3 telegram_bot.py"
fi

if [ -d "/Hiddify-Manager-Bot" ]; then
    rm -rf /Hiddify-Manager-Bot
fi

git clone -b main https://github.com/Hiddify-Return/Hiddify-Manager-Bot.git /Hiddify-Manager-Bot && \
cd /Hiddify-Manager-Bot && \
python3 -m venv returnbot && \
source returnbot/bin/activate && \
pip install -r requirement.txt || { echo -e "\n\nFailed to install the bot. Exiting...\n\n"; exit 1; }

clear && echo -e "\n\nEverything is ok!\n\n" && sleep 1

read -p "Please enter your Telegram chat ID: " ALLOWED_USER_IDS
read -p "Please enter your Telegram bot token: " TELEGRAM_TOKEN
read -p "Please enter your admin UUID: " ADMIN_UUID
read -p "Please enter your admin URL API: " ADMIN_URLAPI
read -p "Please enter your sublink URL: " SUBLINK_URL

echo -e "ALLOWED_USER_IDS=$ALLOWED_USER_IDS
ADMIN_UUID=$ADMIN_UUID
ADMIN_URLAPI=$ADMIN_URLAPI
SUBLINK_URL=$SUBLINK_URL
TELEGRAM_TOKEN=$TELEGRAM_TOKEN" > .env

chmod +x telegram_bot.py && nohup python3 telegram_bot.py > bot.log 2> bot_error.log & disown

if pgrep -f "python3 telegram_bot.py" &> /dev/null; then
    sleep 1 && echo -e "\n\nHiddify-Manager-Bot is now running!\n\n"
else
    sleep 1 && echo -e "\n\nThere is a problem!\n\n"
fi

chmod +x returninstall.sh
cronjob="@reboot sleep 20 && /bin/bash /Hiddify-Manager-Bot/returninstall.sh"
if ! crontab -l | grep -Fq "$cronjob"; then
  (crontab -l 2>/dev/null; echo "$cronjob") | crontab -
fi
