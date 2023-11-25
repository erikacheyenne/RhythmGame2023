label start:

    scene black

    "WELLCOME TO CHART TEST"

    "Lets test Begins TEST"

    show image game_core.chars["Aria"]["Neutral"] at left

    game_core.chars["Aria"]["char"] Neutral "Hi I'm Aria Nocturne"

    game_core.chars["Aria"]["char"] Neutral "But Call me Aria"

    hide image game_core.chars["Aria"]["Neutral"]

    show image game_core.chars["Aria"]["Anxious"] at left

    game_core.chars["Aria"]["char"] Anxious "Sorry I'm a little Anxious because it's my first time"

    game_core.chars["Aria"]["char"] Anxious "So go easy on me please"

    hide image game_core.chars["Aria"]["Anxious"]

    show image game_core.chars["Aria"]["Happy"] at right with dissolve

    game_core.chars["Aria"]["char"] Happy "But anyway lets be friends, OK?"

    game_core.chars["Aria"]["char"] Happy "Errr... is it too fast?"

    hide image game_core.chars["Aria"]["Happy"]

    show image game_core.chars["Aria"]["Shocked"] at right with dissolve

    game_core.chars["Aria"]["char"] Shocked "Sorry, I think I overreact a bit"

    game_core.chars["Aria"]["char"] Shocked "Errr... I dont even let you talk Yet"

    hide image game_core.chars["Aria"]["Shocked"]

    show image game_core.chars["Aria"]["Stressed"] at right with dissolve

    game_core.chars["Aria"]["char"] Stressed "Damm sorry I did again... Forgive this my Bad habit"

    game_core.chars["Aria"]["char"] Stressed "It still a Monologue"

    "Welcome to the Tanix Core Rhythm Game! Ready for a challenge?"
    #Init Rith Game
    window hide
    $ quick_menu = False
    $ renpy.block_rollback()
    #Use Music definition on refdata.json
    $ rhythm_game_displayable = game_core.load_song("Isolation")
    call screen rhythm_game(rhythm_game_displayable)

    $ renpy.block_rollback()
    $ renpy.checkpoint()
    $ quick_menu = True
    window show

    return