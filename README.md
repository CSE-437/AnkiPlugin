# AnkiHub
Python plugin for connecting to AnkiHub

## Installation
To install AnkiHub as a plugin, copy everything from the `src` folder into
the `addons` folder of your local Anki installation.

## Development
The script windowsAnkiRestart provides a streamlined way to develop on Windows
(it hasn't been run on Unix). To run it, enter `python windowsAnkiRestart.py`
on the command line from the same directory. Ctrl-C will stop it.

You will need to have a file called `ankiRestartPaths.txt` in the same directory
which specifies on different lines the paths of the Anki executable, the plugin
file, the Anki addons folder, and the command to kill the Anki process.
Below is an example:

```
C:\Program Files (x86)\Anki\anki.exe
C:\Users\Tyler\Documents\WashU 2015-2016\CSE 437\AnkiPlugin\src\ankiPlugin.py
C:\Users\Tyler\Documents\Anki\addons
TASKKILL /F /IM anki.exe
```

Upon changes to the plugin file, the script will copy the file to the Anki addons
folder and restart Anki.
