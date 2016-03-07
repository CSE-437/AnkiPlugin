# AnkiHub
Python plugin for connecting to AnkiHub

## Installation
To install AnkiHub as a plugin, copy everything from the `src` folder into
the `addons` folder of your local Anki installation.

## Development
### windowsAnkiRestart - Automated Anki Restarting
This script restarts Anki automatically for you every time you save the plugin.

#### Running the Script
You will need a file called `ankiRestartPaths.txt` in the same directory as
windowsAnkiRestart. This file should specify the paths to the Anki executable,
the plugin file, and the Anki addons folder. The last line should be the
command to kill the Anki process. Below is an example:

```
C:\Program Files (x86)\Anki\anki.exe
C:\Users\Tyler\Documents\WashU 2015-2016\CSE 437\AnkiPlugin\src\ankiPlugin.py
C:\Users\Tyler\Documents\Anki\addons
TASKKILL /F /IM anki.exe
```

To run it, enter `python windowsAnkiRestart.py` on the command line from the same directory.
Ctrl-C will stop it.

#### How Does It Work?
Every second, windowsAnkiRestart examines the timestamp of the "Date Modified" field for
the file you specified. If that value is different from the timestamp it cached earlier,
windowsAnkiRestart copies the file to the addons directory specified in aniRestartPaths.txt.
Then, it executes the supplied kill command and then opens Anki using the supplied path
to the Anki executable.
