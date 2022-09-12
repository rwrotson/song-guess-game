## Install

In order to play audiofiles inside the game you need `ffmpeg`. Install [it](https://ffmpeg.org/download.html).

On MacOS, via Homebrew:
```
brew install ffmpeg
```

On Linux:
```
sudo apt update
sudo apt install ffmpeg
```

On Windows, via Chocolatey:
```
choco install ffmpeg
```

Then create a build of the game by:
```
pip install .
```

## Start

After install, run the game by executing:
```
song-guess-game
```
Then you will see main menu, where you can configure the game, see current configuration or start the game. Before launching the game, configure it via built-in questionnaire: specify game settings, players number, players' names and paths to music libraries. 

Game supports mp3-, flac- and wav-files as sources of audio.
We recommend to start your first game with ```sample duration = 1.0```.

## Rules

Each round one or more players guess one randomly selected song from their musical libraries by its short sample. One player guesses after another. Guessing the name of the song gives the player a full point, while guessing the album on which the song appears gives the player a half point. You can also independently agree on the conditions for receiving 1, 0.5 or 0 points, if the standard rules do not suit you.

Each round each sample can be repeated a certain amount of times, which are specified when setting up the game. For infinite repeats configure the game with ```repeats = 0```.

The clue allows you to listen to another random fragment of the same song. You can use multiple clues per round, but each time a new fragment will be issued. The clue cannot be repeated, be careful! The number of clues is the same for all rounds of the game and is determined when setting it up.

For more 
