# Web Scraper Bot
This is my web scraper / bot that can perform tasks automatically on the web. This bot bypasses cloudflare and also most websites that have their own bot protections. It also runs using sim cards in iPhones as proxies, and i found out that this is extremely cost efficient since proxies are often expensive that work.

Everytime you toggle airplane mode on an iPhone, it gets a new ip adress, which in turn makes it harder for websites to detect botting.


## Features
- **Cost effective:** Since we use iPhones with simcards rather than proxies, we reduce the cost significantly. I bought unlimited sim data cheap and i am using this with this bot.


- **Randomized Fingerprints:** It changes all the 'Fingerprints' the browser produces, so it essentially bypasses WebGL fingerprinting, audio, canvas etc.

- **Undetected Chromedriver:** It uses undetected chromedriver to also trick chrome into not being in remote control mode. This runs along with selenium

- **Humanized functions:** It has humanized functions like for example it can write text like a human by randomizing delay between keystrokes

- **Very reliable:** It runs with a watchdog, which essentially checks if the program works correctly and if not it resets it. We use this because there are so many errors to account for.

## Installation
To actually run this code, you would need to program what it should bot. I created and did tasks on a website, but i removed the code for that in kmbot.py and instead added comments where you should add your code

## Usage

1. Run the bot:
   ```bash
   python kmrun.py
   ```
2. Dont forget to connect an iPhone with the shortcut script activated! The shortcut script is in the repository.

## License

You can only use this for educational purposes.