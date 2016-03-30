AnkiHub
=======

Anki addon for connecting to AnkiHub

Table of Contents
-----------------

* [Installation](#installation)
* [A User Story](#a-user-story)
* What AnkiHub Doesn't Support (TODO)
* [Development](#development)
* [The Inner Workings of Anki](#the-inner-workings-of-anki)

Installation
------------

Copy everything from the `src` folder into the `addons` folder of your local
Anki installation.

A User Story
------------

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

Development
-----------

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

The Inner Workings of Anki
--------------------------

Official documentation is on Anki's [website][Anki Docs]

Anki structures cards that allows for a lot of customization but which complicates AnkiHub.
There are 4 concepts: notes, note types, templates, and card types.

**Notes** are the actual pieces information you want to learn. We colloquially call these "cards."
For example, in a simple deck of English vocabulary, each vocab-definition pair would be a
separate note.

**Note types** are Anki's way of modularizing note data. Each note type contains **fields**
which define and standardize the information that each note contains. Fields are particularly
useful for styling purposes (stay tuned). In the "Basic" (default) note type, there are two
fields: "Front" and "Back". Likewise, continuing our example of an English vocab deck, we would
define a note _type_ called "Eng Vocab (Simple)" with two fields:"Word" and "Definition". Or,
perhpas, we decide we also want to add the part of speech. We could then define a new note type
(e.g. "Eng Vocab (Complex)") with 3 fields: "Word", "Part of Speech", "Definition".

Note that each field is guaranteed to be a string, but they may refer to multimedia files
such as images or audio.

**Templates** use HTML to define _where_ each field will be placed on the card.

**Card types** are essentially wrappers for templates and styling. Each card type contains
one template for the front and one for the back of the card. It also contains CSS styling
shared by both templates. Each note type can contain multiple card types (e.g. for
studying both recall and recognition).

### A Real Life Example
These screenshots are from a deck that uses a custom note type with multiple fields and 3 card
types ("Recall", "Recognition", and "Comprehension"). As always, each card type contains 2
templates and CSS styling.

![Fields of custom note type](/img/fields_example.png?raw=true)

![Card types for custom note type](/img/card_types_example.png?raw=true)

[Anki Docs]: http://ankisrs.net/docs/manual.html
