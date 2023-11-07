label start:
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