
<pre>
 ._.  __      __.__                   __  .__                       ._. 
 | | /  \    /  \  |__   ____ _____ _/  |_|  |   ____ ___.__.       | | 
 |_| \   \/\/   /  |  \_/ __ \\__  \\   __\  | _/ __ <   |  |       |_| 
 |-|  \        /|   Y  \  ___/ / __ \|  | |  |_\  ___/\___  |       |-| 
 | |   \__/\  / |___|  /\___  >____  /__| |____/\___  > ____|       | | 
 |_|        \/       \/     \/     \/               \/\/            |_| 
 ._.    _____                .__          __                 __     ._. 
 | |   /  _  \   ______ _____|__| _______/  |______    _____/  |_   | | 
 |_|  /  /_\  \ /  ___//  ___/  |/  ___/\   __\__  \  /    \   __\  |_| 
 |-| /    |    \\___ \ \___ \|  |\___ \  |  |  / __ \|   |  \  |    |-| 
 | | \____|__  /____  >____  >__/____  > |__| (____  /___|  /__|    | | 
 |_|         \/     \/     \/        \/            \/     \/        |_| 
              ⠀⠀⡀⠀⠀⠀⣀⣠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
              ⠀⠘⢿⣝⠛⠋⠉⠉⠉⣉⠩⠍⠉⣿⠿⡭⠉⠛⠃⠲⣞⣉⡙⠿⣇⠀⠀⠀
              ⠀⠀⠈⠻⣷⣄⡠⢶⡟⢁⣀⢠⣴⡏⣀⡀⠀⠀⣠⡾⠋⢉⣈⣸⣿⡀⠀⠀
              ⠀⠀⠀⠀⠙⠋⣼⣿⡜⠃⠉⠀⡎⠉⠉⢺⢱⢢⣿⠃⠘⠈⠛⢹⣿⡇⠀⠀
              ⠀⠀⠀⢀⡞⣠⡟⠁⠀⠀⣀⡰⣀⠀⠀⡸⠀⠑⢵⡄⠀⠀⠀⠀⠉⠀⣧⡀
              ⠀⠀⠀⠌⣰⠃⠁⣠⣖⣡⣄⣀⣀⣈⣑⣔⠂⠀⠠⣿⡄⠀⠀⠀⠀⠠⣾⣷
              ⠀⠀⢸⢠⡇⠀⣰⣿⣿⡿⣡⡾⠿⣿⣿⣜⣇⠀⠀⠘⣿⠀⠀⠀⠀⢸⡀⢸
              ⠀⠀⡆⢸⡀⠀⣿⣿⡇⣾⡿⠁⠀⠀⣹⣿⢸⠀⠀⠀⣿⡆⠀⠀⠀⣸⣤⣼
              ⠀⠀⢳⢸⡧⢦⢿⣿⡏⣿⣿⣦⣀⣴⣻⡿⣱⠀⠀⠀⣻⠁⠀⠀⠀⢹⠛⢻
              ⠀⠀⠈⡄⢷⠘⠞⢿⠻⠶⠾⠿⣿⣿⣭⡾⠃⠀⠀⢀⡟⠀⠀⠀⠀⣹⠀⡆
              ⠀⠀⠀⠰⣘⢧⣀⠀⠙⠢⢤⠠⠤⠄⠊⠀⠀⠀⣠⠟⠀⠀⠀⠀⠀⢧⣿⠃
              ⠀⣀⣤⣿⣇⠻⣟⣄⡀⠀⠘⣤⣣⠀⠀⠀⣀⢼⠟⠀⠀⠀⠀⠀⠄⣿⠟⠀
              ⠿⠏⠭⠟⣤⣴⣬⣨⠙⠲⢦⣧⡤⣔⠲⠝⠚⣷⠀⠀⠀⢀⣴⣷⡠⠃⠀⠀
              ⠀⠀⠀⠀⠀⠉⠉⠉⠛⠻⢛⣿⣶⣶⡽⢤⡄⢛⢃⣒⢠⣿⣿⠟⠀⠀⠀⠀
              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠁⠀⠁⠀⠀⠀⠀⠀
</pre>

## Summary
Using selenium, the application connects to [character.ai](https://www.character.ai) and launches the desired chat 
(in this case, being Wheatley's, though I plan on making a more customizable version for this project eventually). 
It calls the character, and that's how you have conversation. This uses KoljaB's RealTimeSST to capture the user's sentences
and run appropriate pre-written commands associated with them.

# Setting up
1. [Clone the repository](https://github.com/vorkutavorkutlag/wheatley-assistant.git)
2. [Install Python](https://www.python.org/downloads/) if needed, then run `{path to python executable} pip install requirements.txt` inside the folder of the cloned repoistory.
3. [Download Firefox](https://www.mozilla.org/en-US/firefox/new/)
4. [Get the cookie.txt extension](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)
5. Open [character.ai](https://www.character.ai) and log in. Click the extensions icone -> cookie.txt -> current site. This will download a cookie.txt file.
6. Drag the file to the `config` folder of the cloned repository.
7. Run main.py

## Commands 
The application contains a set of prewritten voice commands in `voice_commands.py`
They include and are limited to:
1. Terminate Application -> Closes the application, and by extension its browsers.
2. On YouTube Play [text] -> Searches up [text] on youtube and plays the first result.
3. Let's Play A Random Game -> Launches random game from your steam library.
4. Let's Play Isaac -> Launches The Binding Of Isaac, if you have it ;3
5. Shut Up -> Interrupts the character, if they are currently talking, allowing you to speak.
6. Please Google [Text] -> Opens up google and googles [text]
7. Terminate Google -> Closes down the web browser (same one as YouTube!)

More to come...

## Technical Nuances
1. Start speaking only if you either see the character, hear a beep sound, or see your microphone being used by the app. It will not receive any speech prior to that.
2. The character doesn't hear you whenever they are talking, you have to interrupt them first (say `Shut Up`)
3. In order to reset the memory of the bot, delete the `BIRTH` file in the `config` folder. This will make it create a new chat next time it's launched (It takes a bit to create a new chat, so beware!) If you wish to return to a previous chat/memory set, make sure you have a `BIRTH` file (they are empty, 0B), go to character.ai, and select the chat you want to continue in. Next time you launch the application it will automatically continue in that chat.
4. In order to add extensions, such as adblock, drag and drop the `.crx` file of the extension to the `extensions` folder.
