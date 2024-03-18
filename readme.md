# songs-roulette

*A terminal game to play with friends, lovers and music geeks! Who knows own music library better?
Do you really can tell the difference between "Hey Jude" and "Strawberry Fields Forever" by 1-sec sample? 
Between "And I Love Her" and "PS I Love You"?
Then how about 0.5 seconds? 
Need a clue?..
Roll the roulette!*

Try to guess random songs from your music library. You can repeat question sample or listen .
Broadly configurable game params: random algorithms, rules, mechanics and appearance in the terminal. 

All you need to start game is a directory with music files inside for every player.
Game supports `mp3-`, `flac-` and `wav-`files as sources of audio.

# Install

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
poetry install .
```

# Start

After install, run the game by executing:
```
poetry run start
```
Then you will see main menu, where you can configure the game, see current configuration and libraries and eventually start the game.

![Screenshot of a main menu screen.](/readme/main-menu.png)

Before launching the game, configure it via built-in questionnaire: specify game settings, players number, players' names and paths to music libraries.

![Screenshot of a settings navigation screen.](/readme/all-settings.png)
![Screenshot of a game settings screen.](/readme/game-settings.png)
![Screenshot of a player's settings screen.](/readme/player-settings.png)

Your imputs will be validated and saved. 

You can check 

We recommend to start your first game with ```sample duration = 1.0```, then adjust it too your taste.

# Rules

Each round one or more players guess one randomly selected song from their musical libraries by its short sample. One player guesses after another. Guessing the name of the song gives the player a full point, while guessing the album on which the song appears gives the player a half point. You can also independently agree on the conditions for receiving 1, 0.5 or 0 points, if the standard rules do not suit you.

Each round each sample can be repeated a certain amount of times, which are specified when setting up the main settings of the game.

The clue allows you to listen to another random fragment of the same song. You can use multiple clues per round, but each time a new fragment will be issued. The clue cannot be repeated, be careful! The number of clues is the same for all rounds of the game and is determined when setting it up.

For more detailed rules and help visit help menu within app.

# Customization

You can further customize game conditions with Advanced Settings section.

![Screenshot of an advanced settings screen.](/readme/advanced-settings.png)

It may be tedious to edit a lot of settings with internal questionnaires. In such cases you can edit config file directly in your terminal's text editor. Also note that if you've gone too far, you can always reset everything to default.

You can explore customization options in the reference right below.

# Settings Reference

### MAIN_SETTINGS:
- **players_number** : number of players in the game (*>=1*, default: **2**)
- **sample_duration** : duration of a sample from a song in seconds (*>=0.1*, default: **1.0**)
- **infinite_repeats** : if True, player can repeat the sample infinite times (default: **False**)
- **repeats_number** : number of allowed repeats in one round (*>=1*, default: **5**)
- **clues_number** : number of clue samples (*>=0*, default: **10**)
- **clues_strategy** : method of how next clue sample for the same song will be chosen (*random_next|new_next*, default: **new_next**)
- **rounds_number** : number of songs each player tries to guess, number of rounds of the game *(can't be less than the number of songs in the smallest player's library)* (*>=1*, default: **10**)

### PLAYERS_SETTINGS:
- **name** : nickname of player
- **path** : path to library directory with all the audiofiles of a player

### DISPLAY_SETTINGS:
- **color_enabled** : are color tags for text enabled in terminal (default: **True**)
- **typing_enabled** : is text being typed letter by letter (True), or is is being typed instantly (False) (default: **True**)
- **min_delay** : minimum delay between two letters being typed in seconds, if typing is enabled (*>=0.0, <=0.5*, default: **0.001**)
- **max_delay** : maximum delay between two letters being typed in seconds, if typing is enabled (*>=0.0, <=0.5*, default: **0.05**)

### SELECTION_SETTINGS:
- **strategy** : how the songs are being chosen from player library (default: **naive**)
  - *naive*: select songs randomely from all audiofiles
  - *normalized_by_folder*: select songs evenly from each folder inside players library 
  - *normalized_by_album*: select songs evenly from each album inside players library

### SAMPLING_SETTINGS:
- **from_** : from what second of the song the sample will be taken (*>=0.0*, default: **0.0**)
- **to_finish** : from what second till the end of the song the sample will be taken (*>=0.0*, default: **3.0**)
- **distance** : minimal distance between two samples from the same song in seconds (*>=1.0*, default: **5.0**)
- **clues_quantity** : number of clue samples for the song (*>=1, <=10*, default: **3**)
- **strategy** : method of how next clue sample for the same song will be chosen 
  - *naive*: select next clue randomely from all clue samples
  - *normalized*: select next clue from all clue samples sequentially (default: normalized)

### PLAYBACK_BAR_SETTINGS:
- **empty_char** : character that represents empty space in playback bar (default: **░**)
- **full_char** : character that represents filled space in playback bar (default: **█**)
- **space_char** : character that represents space between playback bar and time display (default: " ")
- **bar_lenght** : length of playback bar in characters (*>=20, <=100*, default: **50**)
- **update_frequency** : frequency of playback bar update in seconds (*>=0.5, <=1.0*, default: **0.1**)
- **enable_flashing** : if True, playback bar will flash and blink (default: **False**)
- **enable_question_mark** : show question sample mark in the progress bar (default: **True**)
- **enable_clue_marks** : show clue samples marks in the progress bar (default: **True**)

### EVALUATION_SETTINGS:
- **full_answer** : points for full correct answer (*>=0.0*, default: **1.0**)
- **half_answer** : points for half correct answer (*>=0.0*, default: **0.5**)
- **no_answer** : points for no answer (*>=0.0*, default: **0.0**)
- **wrong_answer** : points for wrong answer (*>=0.0*, default: **0.0**)
- **clue_discount** : discount for points for each clue use (*>=0.0, <=1.0*, default: **0.1**)

### SERVICE_PATHS_SETTINGS:
- **config_path** : path to config file, where set settings are stored (default: **config.yaml**)
- **game_pickle_path** : path to pickle file, where unfinished game state is stored (default: **game.pickle**)
- **history_log_path** : path to history log file (default: **history.log**)
