# Warwick's Quiz Runner
Hey, it's me, Warwick! I got bored standing by my stable in Avalon watching you save the spiral, so I thought I would help out!
<p align="center">
 <img width="467" height="248" alt="Image" src="https://github.com/user-attachments/assets/5c0e49c1-804f-4ec2-b9aa-99f88d65c207" />
</p>

## What is Warwick's Quiz Runner?
Warwick's Quiz Runner is a python application designed to automatically complete 10 quizzes on the Wizard101 trivia page and earn 100 crowns daily.

## Will this get me banned?
This program is against the Wizard101 ToS, however I have not heard of anyone getting banned because of it, so use at your own risk.

## How do I download & use?
NOTE: REQUIRES CHROMIUM BROWSER (Ideally Google Chrome)

Download the latest release [here](https://github.com/Doggyshot/WarwicksQuizRunner/releases).

If you only plan to use one account, I would recommend the lite version.

From my testing I've never triggered the Captcha running just one account per day, which makes the captcha-solving lite version much more convenient.

## This program requires my Wizard101 username and password, should I be concerned?
No, your login credentials are only stored locally in the Config.json file so you do not have to reinput them every time. Your login is only used to log into the wizard101 webpage before running the quizzes. 

If you are still conerned, I encourage you to read through the source code (It's not very long, I promise) and compile the program yourself with the following command:

```python -m PyInstaller QuizRunner.py --onedir --icon="ICON_PATH_HERE\bin\Warwick32x32.ico" --windowed```

Replace the icon argument with your path, or omit the argument entirely if you don't care.

## I want to contact you regarding a question or bug, how can I do that?
Shoot me a message on Discord (@doggyshot), X/Twitter (@NasusOTP), or open an issue on Github. I try to respond when I'm available. 

## Future Plans/Updates
- Long Term test Captcha Solver (In theory it should work fine but needs more extensive testing)
- Linux Support (Not that hard just lazy)
- Individually track quiz timers instead of just the last quiz completed
- Individually track crowns based on the account used

### Credits to [Zeyu2001](https://github.com/zeyu2001) for the inspiration and quiz answers :^)
