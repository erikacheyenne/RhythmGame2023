label start:
    "Welcome to the Ren'Py Rhythm Game! Ready for a challenge?"
    window hide
    $ quick_menu = False

    # avoid rolling back and losing chess game state
    $ renpy.block_rollback()

    $ rhythm_game_displayable = game_core.load_song("Isolation")
    call screen rhythm_game(rhythm_game_displayable)

    # avoid rolling back and entering the chess game again
    $ renpy.block_rollback()

    # restore rollback from this point on
    $ renpy.checkpoint()

    $ quick_menu = True
    window show

    return