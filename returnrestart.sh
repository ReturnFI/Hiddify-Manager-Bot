#!/bin/bash
HOME=/
pkill -f telegram_bot.py 
cd /telegram_bot
source returnbot/bin/activate
chmod +x telegram_bot.py
nohup python3 telegram_bot.py & disown
clear && echo -e "\n\nBot is restarted!\n\n" && sleep 1
