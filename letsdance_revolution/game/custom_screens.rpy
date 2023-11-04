################################################################################
## STEP GAME System Screens
################################################################################

#Add Step to Screen
screen add_step(img):
    if len(img) != 2:
        #image At(img, step_speed)
        image At(img)
    else:
        #image At(img[0], step_speed)
        #image At(img[1], step_speed2)
        image At(img[0])
        image At(img[1])


screen select_music():
    frame:
        xsize 500
        ysize 400

        vbox:
            text "Music List" xpos 100 size 40
            for i in movies_list:
                button:
                    yalign 100
                    xalign 100 
                    action Return(i)                    
                    text i size 20

screen tutorial:    
    $renpy.movie_stop(clear=True)
    image "tutorial_background"
    default tutorial_header = "Ola seja bem vindo ao Tutorial{p}preciso te informar sobre algumas {outlinecolor=#00ff00}mecanicas{/outlinecolor} desse jogo de ritmo {image=esquerda.png}"
    vbox:
        xalign 0.5
        text "[tutorial_header]":
            #color "#008080"
            slow_cps 21
            outlines [ (absolute(1), "#008080", absolute(1), absolute(2)) ]
            #italic True

    key "mouseup_3" action Return()
    
    image "left_step":
        alpha 0.5
        ypos 550
        if blink and ref_xpos[ref_direction1] == 400:
            at step_blink
    image "up_step":
        alpha 0.5
        ypos 550
        if blink and ref_xpos[ref_direction1] == 520:
            at step_blink
    image "down_step":
        alpha 0.5
        ypos 550
        if blink and ref_xpos[ref_direction1] == 630:
            at step_blink
    image "right_step":
        alpha 0.5
        ypos 550
        if blink and ref_xpos[ref_direction1] == 750:
            at step_blink

    $count = 0
    for i in tutorial_steps:
        $count += 1        
        $current_time += i[0] 
        timer current_time action SetScreenVariable("tutorial_header", i[3])
        if i[2]:
            timer current_time action SetVariable("ref_speed", 1.0/i[1]), SetVariable("ref_direction1", i[2]), Show("add_step",img=i[2]), SetVariable("key_value", ref_key[i[2]]), SetVariable("check_score", True)
            $current_time += 1.0/i[1]
            timer current_time*0.90 action SetVariable("score", 1)
            timer current_time*0.95 action SetVariable("score", 2)
            timer current_time action Hide("add_step"), SetVariable("blink", True)
            timer current_time+0.2 action Hide("add_step"), SetVariable("blink", False)
            timer current_time+0.4 action SetVariable("status", "")
            

        if len(tutorial_steps) == count:
            timer current_time+0.5 action Hide("tutorial"), Show("result")
    
#Play a Music
screen play_music():
    $target = current_game.music_list[current_game.current_video]["target"]     
    image current_game.music_list[current_game.current_video]["name"]
    image "inter1"
    image "inter2"    
    text "{size=40}{b}Voce precisa de [target] pontos para vencer{/b}":
        xalign 0.9
        ypos 25
    text "{size=50}{b}Pontos [score_value]{/b}{/size}":
        ypos 17
        xpos 20

    key "mouseup_3" action Return()
    
    image "left_step":
        alpha 0.5
        ypos 550
        if blink and ref_xpos[ref_direction1] == 400:
            at step_blink
    image "up_step":
        alpha 0.5
        ypos 550
        if blink and ref_xpos[ref_direction1] == 520:
            at step_blink
    image "down_step":
        alpha 0.5
        ypos 550
        if blink and ref_xpos[ref_direction1] == 630:
            at step_blink
    image "right_step":
        alpha 0.5
        ypos 550
        if blink and ref_xpos[ref_direction1] == 750:
            at step_blink


    text "{size=50}{b}[status]{/b}{/size}":
        ypos 300
        xpos 300
    
    #os tempos da musica
    $count = 0
    $music_steps = current_game.music_list[current_game.current_video]["music_steps"] 
    for i in music_steps:
        $count += 1        
        $current_time += i[0] 
        if len(i[2]) != 2:
            #timer current_time action SetVariable("ref_speed", int(550.0/60.0*i[1])+1), SetVariable("ref_direction1", i[2]), Show("add_step",img=i[2])
            timer current_time action SetVariable("ref_speed", 1.0/i[1]), SetVariable("ref_direction1", i[2]), Show("add_step",img=i[2]), SetVariable("key_value", ref_key[i[2]]), SetVariable("check_score", True)
        else:
            timer current_time action SetVariable("ref_speed", int(550.0/60.0*i[1])+1), SetVariable("ref_direction1", i[2][0]), SetVariable("ref_direction2", i[2][1]), Show("add_step",img=i[2])
        $current_time += 1.0/i[1]
        timer current_time*0.90 action SetVariable("score", 1)
        timer current_time*0.95 action SetVariable("score", 2)
        timer current_time action Hide("add_step"), SetVariable("blink", True)
        timer current_time+0.2 action Hide("add_step"), SetVariable("blink", False)
        timer current_time+0.4 action SetVariable("status", "")
        if len(music_steps) == count:
            timer current_time+0.5 action Hide("play_music"), Show("result")

    key "K_LEFT" action Function(step_action, key="K_LEFT")
    key "K_UP" action Function(step_action, key="K_UP")
    key "K_DOWN" action Function(step_action, key="K_DOWN")
    key "K_RIGHT" action Function(step_action, key="K_RIGHT")

screen result:
    image "black" alpha 0.7
    $target = current_game.music_list[current_game.current_video]["target"]
    vbox:
        xalign 0.5
        text "{size=35}{b}GREAT JOB!{/size}"
        text ""
        text "{size=50}{b}TOTAL SCORE [score_value]{/size}"        
        text "{size=50}{b}TARGET [target]{/size}"
        text ""
        if score_value >= target:
            text "{size=60}CONGRATULATIONS TARGET WAS REACH AND BONUS APPLY{/size}"

    textbutton "{size=35}{b}{i}Sair{/size}":
        xalign 0.5
        yalign 0.97
        action Hide("result"), Return()

screen main_background:
    $money = current_game.game_attributes["money"]
    image current_game.music_list[current_game.current_video]["name"]
    image "{}_cover".format(current_game.music_list[current_game.current_video]["name"]):
        at sobedesce
    image "blue":
        alpha 0.4#35
    image "menu do menu":
        alpha 0.9
    text current_game.music_list[current_game.current_video]["name"]:
        outlines [ (absolute(2), "#888888", absolute(1), absolute(1)) ]
        bold True
        size 40
        xpos 180
        ypos 12
    image "black":
        ypos 14
        xpos 890
        alpha 0.5
        size (400, 40)
    text "{color=D2691E}${/color} [money]":
        bold True
        size 30
        xpos 900
        ypos 15
    $ tooltip = GetTooltip()
    if tooltip:
        text "[tooltip]":
            xalign 0.4
            yalign 0.7
    textbutton "{b}{size=50}Tutorial{/size}{/b}":
        tooltip "Inicie Por Aqui!"
        xpos 550
        ypos 430
        action  Hide("main_background"), SetVariable("score_value", 0), Show("tutorial")
    textbutton "{b}{size=50}Start{/size}{/b}":
        tooltip "Boa sorte"
        xpos 400
        ypos 500
        action  SetVariable("score_value", 0), Show("play_music")
    textbutton "{b}{size=38}Shoping{/b}":
        xpos 490
        ypos 570
        action Jump("loja")
    if config.developer:
        textbutton "{b}{size=38}Developer Menu{/b}":
            xpos 550
            ypos 630
            action Jump("developer_menu")

screen developer_screen:
    modal True
    image "black" alpha 0.7
    vbox:
        textbutton "Game Reset":
            action Function(current_game.game_reset)
        textbutton "Credit Money 10000":
            action Function(current_game.credit_money, credit=10000)

    hbox:
        xalign 0.2
        yalign 0.2
        text "Attributes:"
        for attr, attr_value in current_game.game_attributes.items():
            text "    [attr] - [attr_value]    "


    textbutton "{size=35}{b}{i}Sair{/size}":
        xalign 0.5
        yalign 0.97
        action Return()
    
screen mercado:
    modal True
    default store = 0
    default upgrade = None
    image "black" alpha 0.7
    
    imagebutton:
        idle "select_loja2"
        hover "select_loja2" 
        action SetScreenVariable("store",1)

    imagebutton idle "select_loja3" action SetScreenVariable("store",2)
    textbutton "{size=35}{b}{i}Sair{/size}":
        xalign 0.5
        yalign 0.97
        action Return()

    textbutton "upgrade": 
        xalign 0.3
        yalign 0.8
        action Hide("shop_music"), Show("upgrades")

    textbutton "shop_music":
        xalign 0.3
        yalign 0.85
        action Hide("upgrades"), Show("shop_music")

screen upgrades:
    $multiplier = current_game.get_attribute("multiplier")
    $prize = current_game.get_attribute("prize")

    $multiplier_price = fib(multiplier)*current_game.game_attributes["multiplier_price"]

    textbutton "Multipy Factor - NOW in [multiplier] - PRICE $ [multiplier_price]":
        action Function(current_game.upgrade,upgrade_type="multiplier")        
    textbutton "Prize factor - NOW in [prize]":
        action Function(current_game.upgrade,upgrade_type="prize")
        yalign 0.05

screen shop_music:
    for idx, music_item in enumerate(current_game.music_list):        
        if music_item["status"]==0:
            $music_name = music_item["name"]
            $music_price = music_item["price"]            
            textbutton "id[idx] [music_name] - Price [music_price]":
                action Function(current_game.shop,music_name=music_name)
                yalign 0.05*idx 

