# scores for Good and Perfect hits
define SCORE_GOOD = 60
define SCORE_PERFECT = 100

screen select_song_screen(songs):

    modal True

    frame:
        xalign 0.5
        yalign 0.5
        xpadding 30
        ypadding 30

        vbox:
            spacing 20

            label 'Click on a song to play' xalign 0.5

            vbox spacing 10:
                hbox spacing 160:
                    label 'Song Name'
                    label 'Highest Score'
                    label '% Perfect Hits'

                grid 3 len(songs):
                    xspacing 100
                    for song in songs:
                        textbutton song.name action [
                        Return(song)
                        ]
                        $ highest_score, highest_percent = persistent.rhythm_game_high_scores[song.name]
                        text str(highest_score)
                        text '([highest_percent]%)'

            textbutton _("Exit"):
                xalign 0.5
                action Return(None)

screen rhythm_game(rhythm_game_displayable):

    zorder 100
    key 'K_LEFT' action NullAction()
    key 'K_UP' action NullAction()
    key 'K_DOWN' action NullAction()
    key 'K_RIGHT' action NullAction()

    #background
    add "skyyyy.png"
    add rhythm_game_displayable

    vbox:
        xpos 50
        ypos 50
        spacing 20

        textbutton 'Quit' action [
        Confirm('Would you like to quit the rhythm game?',
            yes=[
            Stop(CHANNEL_RHYTHM_GAME), # stop the music on this channel
            Return(rhythm_game_displayable.score)
            ])]:
            # force the button text to be white when hovered
            text_hover_color '#fff'

        # can also use has_music_started so this won't show during the silence
        showif rhythm_game_displayable.has_game_started:
            text 'Score: ' + str(rhythm_game_displayable.score):
                color '#fff'
                size 40

    # use has_music_started, do not use has_game_started, b/c we are still in silence
    showif rhythm_game_displayable.has_music_started:
        bar:
            xalign 0.5
            ypos 20
            xsize 740
            value AudioPositionValue(channel=CHANNEL_RHYTHM_GAME)

    # return the number of hits and total number of notes to the main game
    if rhythm_game_displayable.has_ended:
        # use a timer so the player can see the screen before it returns
        timer 2.0 action Return(rhythm_game_displayable.score)
