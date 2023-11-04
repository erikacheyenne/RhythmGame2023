#ENGINE!!! essa é a parte que controla as setinhas do jogo

screen espera:
    timer 1.0 action Return()








########################################################################################################################
########################################################################################################################
image legenda:
    "efeito"
    xalign 0.5
    yalign 0.5
    size (1280, 0)
    ease 0.4 size (1280, 251)
    1.0
    ease 1.0 alpha 0.0
    
    

screen pausa:
    image "legenda"
    timer 2.4 action Return()
########################################################################################################################
########################################################################################################################
    







#ESSAS SÃO AS SETAS COMUNS

    
    
########################################################################################################################
image set1:
    "esquerda"
    xpos 400
    ypos -20
    linear 1.0 ypos 550
########################################################################################################################
screen esq: #SETA ESQUERDA
    #modal True
    image "set1"
    #ANOTÇÂO SUPER MEGA HIPER IMPORTANTE!!!
    #key "keydown_l" action SetVariable("pontos", pontos+1)
    #key "keyup_l" action SetVariable("pontos", pontos-1)
    #key "repeat_9" action SetVariable("pontos", pontos+1)
    #key "9" action SetVariable("pontos", pontos-3)
    if b1 == True:
        key "K_LEFT" action SetVariable("pontos", pontos+3), SetVariable("b1", False), Play("sound", "audio/plin.ogg")
    timer 0.7 action SetVariable("b1", True)
    timer 1.0 action SetVariable("b1", False), Return()    




########################################################################################################################
image set4:
    "direita"
    xpos 750
    ypos -20
    linear 1.0 ypos 550
########################################################################################################################
screen dir: #SETA DIREITA
    image "set4"
    if b4 == True:
        key "K_RIGHT" action SetVariable("pontos", pontos+3), SetVariable("b4", False), Play("sound", "audio/plin.ogg")
    timer 0.7 action SetVariable("b4", True)
    timer 1.0 action SetVariable("b4", False), Return()




########################################################################################################################
image set2:
    "cima"
    xpos 520
    ypos -20
    linear 1.0 ypos 550
########################################################################################################################
screen sup: #SETA SUPERIOR
    image "set2"
    if b2 == True:
        key "K_UP" action SetVariable("pontos", pontos+3), SetVariable("b2", False), Play("sound", "audio/plin.ogg")
    timer 0.7 action SetVariable("b2", True)
    timer 1.0 action SetVariable("b2", False), Return()
    
    
    
    
########################################################################################################################
image set3:
    "baixo"
    xpos 630
    ypos -20
    linear 1.0 ypos 550
########################################################################################################################
screen inf: #SETA INFERIOR
    image "set3"
    if b3 == True:
        key "K_DOWN" action SetVariable("pontos", pontos+3), SetVariable("b3", False), Play("sound", "audio/plin.ogg")
    timer 0.7 action SetVariable("b3", True)
    timer 1.0 action SetVariable("b3", False), Return()




########################################################################################################################
########################################################################################################################