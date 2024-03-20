# About Hiddify Manager Bot

Hello , and welcome to the [Hiddify Manager](https://github.com/hiddify/Hiddify-Manager) Bot GitHub page. I'm currently developing a bot for managing the Hiddify panel, and I'd be delighted if you could assist me in testing and refining the bot through trial and error. Additionally, if you have any ideas, I'd love to hear them. Thank you!

> [!IMPORTANT]
> This bot currently only works with API version 1.0 and this bot is for testing purposes.

# How to Automatic Installation ?
To use the bot , you will need the following information:
1. **Chat ID:** You need to obtain this from the [@chatIDrobot](https://t.me/chatIDrobot).
2. **Bot Token:** You need to obtain this from the [@botfather](https://t.me/BotFather).
3. **Admin uuid:** Enter your admin uuid.
4. **Admin url:** Enter your panel url.
5. **Admin sublink:** Enter your panel sublink.


### install command :
```
cd / && rm -f returninstall.sh* || true && wget https://raw.githubusercontent.com/H-Return/Hiddify-Manager-Bot/main/returninstall.sh && chmod +x returninstall.sh && ./returninstall.sh
```

> [!NOTE]
> With this method, you enter only the required information.

### restart command :
```
cd / && rm -f returnrestart.sh* || true && wget https://raw.githubusercontent.com/H-Return/Hiddify-Manager-Bot/main/returnrestart.sh && chmod +x returnrestart.sh && ./returnrestart.sh
```

<details>
  <summary><b>How to Manuel Installation ?</b></summary>
  <p><b>1. Update and upgrade system packages:</b></p>
  <pre><code>apt update && apt upgrade -y</code></pre>

  <p><b>2. Install Python 3 and pip:</b></p>
  <pre><code>apt install python3 && apt install python3-pip</code></pre>

  <p><b>3. Clone the bot repository:</b></p>
  <pre><code>apt install git -y</code></pre>
  <pre><code>git clone https://github.com/Hiddify-Return/Hiddify-Manager-Bot.git</code></pre>

  <p><b>4. Navigate to the cloned directory:</b></p>
  <pre><code>cd Hiddify-Manager-Bot</code></pre>

  <p><b>5. Install required Python packages:</b></p>
  <pre><code>pip install -r requirement.txt</code></pre>

  <h2>Configuration:</h2>

  <p><b>1. Open or create <code>.env</code> with an editor like nano:</b></p>
  <pre><code>nano .env</code></pre>

  <p><b>2. Add the following lines according to your configuration:</b></p>
  <pre><code>
  ALLOWED_USER_IDS=11111111
  ADMIN_UUID=Admin-UUID
  ADMIN_URLAPI=https://Admin-URL
  SUBLINK_URL=https://subscription_URL
  TELEGRAM_TOKEN=BOT-TOKEN
  </code></pre>
  <p>Replace the placeholders with your actual values.</p>

  <h2>Running the Bot:</h2>

  <p><b>1. Run the bot temporarily:</b></p>
  <pre><code>python3 telegram_bot.py</code></pre>
</details>

# Creating a systemd Service (Optional):
<b>1. Create a systemd service file:</b>

```
nano /etc/systemd/system/telegram_bot.service
```

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

```
sudo systemctl daemon-reload
```

```
sudo systemctl enable telegram_bot
```

```
sudo systemctl start telegram_bot
```

Now, your Hiddify Manager Bot should be set up and running as a systemd service, ready to serve its purpose. Make sure to replace placeholder values with your actual configuration details.
