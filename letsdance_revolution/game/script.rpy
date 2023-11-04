label start:
    jump jogando

label jogando:
    show screen main_background

    $current_game.current_video = menu(current_game.video_choices)

    jump jogando

label loja:
    call screen mercado
    jump jogando

label developer_menu:
    call screen developer_screen
    jump jogando


