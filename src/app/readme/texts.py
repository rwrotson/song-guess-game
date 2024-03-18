from app.cli.formatters import TemplateString, Text
from app.readme.representations import SETTINGS_DICT, represent_setting


_RULES_TEXT = TemplateString(
    """\
    Each round one or more players guess a
        randomely selected songs from their musical libraries 
        by short samples taken from these songs. 
    
    Within one round you can REPEAT the sample a few times 
        and get additional CLUE samples from the same song.
        The number of repeats is being reset every round,
        while clue counter is uniform across rounds.

    When a player is ready to answer, he presses ANSWER 
        and then writes down his suggestion about the song 
        or tells it aloud to the audience.

    After the correct answer is being revealed, 
        the AUDIENCE decide whether the answer was correct, 
        incomplete, incorrect or absent. 
    Due to this evaluation a player gets points. 
    
    Then turn goes to the next player and game repeats.
    
    You can configure the points system, however, defaults are these:
        CORRECT        : +1
        HALF-CORRECT   : +0.5 
        WRONG          : 0
        ABSENT         : 0
        
    Also note that every clue use reduces the points for evaluated song,
        by default by 10%. You can also configure this number in 
        advanced evaluation settings or disable discount by setting it to 0.

    After the end of the game, 
        the results are summed up
        and winners are being revealed.
        
    The game supports .mp3, .flac and .wav audiofiles.
        Ensure that files have correct meta and tags.
    """
)


_SETTINGS_TEXT = f"""\
    Before play you need to configure main game params and set up players. 
    
    You can do it in two ways:
    --$i by interactive questionnaries to each settings section $r
    --$i by directly editing the config file with yaml syntax $r
    
    {represent_setting("MAIN_SETTINGS")}
    {represent_setting("PLAYERS_SETTINGS")}
"""


_ADVANCED_SETTINGS_TEXT = f"""\
    Advanced settings are options to further customise game experience.
           
    {represent_setting("DISPLAY_SETTINGS")}
    {represent_setting("SELECTION_SETTINGS")}
    {represent_setting("SAMPLING_SETTINGS")}
    {represent_setting("PLAYBACK_BAR_SETTINGS")}
    {represent_setting("EVALUATION_SETTINGS")}
    {represent_setting("SERVICE_PATHS_SETTINGS")}
"""


_AUTHORS = """\
    Game was created by:
        -- igor lashkov ${i}<rwrotson@yandex.ru>${r}
    
    If you want to contribute, write email or get in touch with me on github.
    
        ${b}github.com/rwrotson/songs-roulette${r}
"""


README_TEXTS: dict[str, Text] = {
    "rules": _RULES_TEXT,
    "settings": TemplateString(_SETTINGS_TEXT),
    "advanced_settings": TemplateString(_ADVANCED_SETTINGS_TEXT),
    "authors": TemplateString(_AUTHORS),
}


# TODO: add strategies code representation
