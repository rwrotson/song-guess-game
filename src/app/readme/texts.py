_RULES_TEXT = (
    """Each round one or more players guesses one song
    from their musical libraries by its short sample,
    one player guess after another.

    The game supports .mp3, .flac and .wav audiofiles.
        Ensure that files have correct meta and tags.

    Each round each player can REPEAT the sample some few times.
        Also, if CLUES enabled, player can get another sample(s) from this song.
            The number of repeats is uniform for repeats of 
            the original sample and of clue samples.

    When a player is ready to answer, he presses ANSWER 
        and can write down his suggestion about the song 
        or tell it aloud to the audience.
    Then he should press the REVEAL button to show info about the song.

    The AUDIENCE decide whether the answer was correct, incomplete, incorrect or absent.
    Due to this a player gets points. You can configure the points system, however,
    the default one is:
        CORRECT        : +1
        INCOMPLETE     : +0.5 
        INCORRECT      : 0
        ABSENT         : 0

    Then turn goes to the next player and game repeats.

    After the end of the game, 
        the results are summed up
        and winners are being revealed.
    """
)

_SETTINGS_TEXT = (
    """Before play you need to configure the game. 
    
    You can do it in two ways:
    -- by interactive questionnaries
    -- by editing the config yaml file
    
    Main settings include: 
        -- players_number   : number of players in game 
                              (>= 1) 
        -- players_names    : nicknames of players
        -- players_folders  : paths to musical folder 
                              of player's respectively
        -- sample_duration  : duration of a sample from 
                              a song in seconds 
                              (0.25-5.0, 1.0 recommended)
        -- repeats_number   : number of allowed repeats in
                              one round (0 for infinite)
        -- clues_number     : number of additional samples
                              from the same song (9 max)
                              (note that clues counter
                              is uniform across rounds)
        -- rounds_number    : number of songs each player tries 
                              to guess, number of rounds of the game
                              (can't be less than the number of songs
                              in the smallest player's library)"""
)

_ADVANCED_SETTINGS_TEXT = (
    """
    Advanced
    """
)

_AUTHORS = (
    """
    Game was created by:
    -- igor lashkov <rwrotson@yandex.ru>
    
    If you want to contribute, write email or get in touch with me on github.
    
    github.com/rwrotson/song-guess-game
    """
)


README_TEXTS = {
    "rules": _RULES_TEXT,
    "settings": _SETTINGS_TEXT,
    "advanced settings": _ADVANCED_SETTINGS_TEXT,
    "authors": _AUTHORS,
}
