# AnkiHub
Python plugin for connecting to AnkiHub

## Installation
To install AnkiHub as a plugin, copy everything from the `src` folder into
the `addons` folder of your local Anki installation.

## A User Story
Bob wants to study from Alice's Anki deck called DeckA. Alice logs onto the AnkiHub plugin
and uploads DeckA. Then, Bob logs onto the AnkiHub website and searches for DeckA. He
subscribes to the deck and then opens his local installation of Anki (henceforth called
"vanilla Anki"). He enters his AnkiHub credentials on the plugin login window.

After the plugin verifies his credentials, the backend of the plugin receives a list of his
subscriptions from the server. Since one of these decks, DeckA, does not exist locally,
the plugin imports DeckA using JSON data from the server. In addition, the plugin updates
any subscribed decks that already exists locally.

At this point, the plugin finishes loading the deck viewer window, which shows every local
and subscribed deck (including DeckA). Next to subscribed decks (which includes uploaded
decks that Bob owns) is a "Disconnect" button; it forks the deck if Bob is subscribed to it
but does not own it, and it no longer sends updates if Bob is the deck originator.
Next to local decks that have not been uploaded, there is an "Upload" button. If Bob pushes
the "Uplaod" button for one of his decks, the button then changes to a "Disconnect" button.

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
