init python:

################################################################################
## Persistent Data
################################################################################
    
    game_resetattr = {"multiplier":1, "multiplier_price":10, "prize":1, "prize_price":100, "money":0 }
    if persistent.game_attributes is None:
            persistent.game_attributes = game_resetattr

################################################################################
## Regular Python Import
################################################################################

    import glob, json, os.path, base64, os, requests
    from math import sqrt

################################################################################
## Python Classes
################################################################################

    class base_class(renpy.python.RevertableObject):

        def __getstate__(self):
            return vars(self).copy()
        
        def __setstate__(self,new_dict):
            self.__dict__.update(new_dict)


    class game_core(base_class):
        '''Define Base core Class of Game
        '''
        def __init__(self):
            """ Init Game Core Class                
            """
            self.video_path = "{}/{}".format(config.gamedir,"videos/levels")
            self.all_videos = glob.glob("{}/*".format(self.video_path))
            self.game_attributes = persistent.game_attributes
            self.music_list = []
            self.video_choices = []
            self.current_video = 0
            self.multiplier = 1
            self.load_videos()
            self.create_videos()

        def credit_money(self, credit):
            self.game_attributes["money"] += credit
            self.save_attributes()

        def debit_money(self, debit):
            if (self.game_attributes["money"] - debit) > 0:
                self.game_attributes["money"] -= debit
                self.save_attributes()
                return True
            else:
                renpy.notify(message="Not enouth Money to debit {} dindin!!".format(debit))
                return False
        
        def get_attribute(self, attr):
            return self.game_attributes[attr]

        def save_attributes(self):
            persistent.game_attributes = self.game_attributes
            renpy.save_persistent()

        def game_reset(self):
            persistent.game_attributes = game_resetattr
            self.game_attributes = persistent.game_attributes
            renpy.save_persistent()

        def shop(self, music_name):
            data_file = "{}/{}/data.json".format(self.video_path.replace("\\","/"), music_name)            
            for idx, music_item in enumerate(self.music_list):
                if music_item["name"] == music_name:
                    if self.debit_money(music_item["price"]):
                        with open(data_file, "r") as json_file:
                            json_data = json.load(json_file)
                            json_data["status"] = 1
                        with open(data_file, "w") as json_file:                            
                            json.dump(json_data, json_file)
                            self.music_list[idx]["status"] = 1
                        json_file.close()
            self.video_choices = []
            for idx, video in enumerate(self.music_list):                
                if video["status"]:
                    idx_value = idx
                else:
                    idx_value = None
                self.video_choices.append((video["name"], idx_value))

        def upgrade(self, upgrade_type=""):
            price = fib(self.game_attributes[upgrade_type])*self.game_attributes["{}_price".format(upgrade_type)]
            if self.debit_money(price):
                self.game_attributes[upgrade_type] += 1
                self.save_attributes()

        def load_videos(self):
            for video in self.all_videos:
                data_file = "{}/data.json".format(video)
                if os.path.exists(data_file):
                    with open(data_file) as json_file:
                        self.music_list.append(json.load(json_file))
        
        def create_videos(self):
            for idx, video in enumerate(self.music_list):                
                renpy.image(video["name"], Movie(play="{}/{}/{}".format(self.video_path.replace("\\","/"),video["name"],video["filename"]), pos=(0, 0), anchor=(0, 0), size=(1280, 720), channel='movie',) )
                renpy.image("{}_cover".format(video["name"]), "{}/{}/{}".format(self.video_path.replace("\\","/"),video["name"],video["cover"]))
                if video["status"]:
                    idx_value = idx
                else:
                    idx_value = None
                self.video_choices.append((video["name"], idx_value))

        def ping_api(self):
            url = 'http://localhost/tanixapi/services/services.php?action=test_api'
            response = requests.get(url)
            return response

################################################################################
## Functions
################################################################################

    def step_action(key):
        global status, score_value, score, check_score, key_value
        if check_score and score > 0 and key_value == key:
            status = ref_status[score]
            score_value += 1*score
            renpy.play("audio/plin.ogg",channel="sound")
            score = 0
            check_score = False            
        else:
            score_value -= 1
            renpy.play("audio/falha.ogg",channel="sound")            

    def fib(n):
        return int(((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5)))
    
    def step_handler(trans, st, at):
        global position, ref_speed, zigzag, ref_pos

        if position == 0:
            trans.xpos = ref_xpos[ref_direction1]             

        position += ref_speed
        
        if position <= 550:
            trans.ypos = position            
            if (ref_direction1 in zigzag):
                trans.xpos = zigzag[ref_direction1] - int(position*0.61999)                 
            return 0
        else:
            trans.ypos = 550
            position = 0            
            return None
    
    def step_handler2(trans, st, at):
        global position2, ref_speed, zigzag, ref_pos

        if position2 == 0:
            trans.xpos = ref_xpos[ref_direction2]

        position2 += ref_speed
        
        if position2 <= 550:
            trans.ypos = position            
            if (ref_direction1 in zigzag):
                trans.xpos = zigzag[ref_direction1] - int(position*0.61999)                 
            return 0
        else:
            trans.ypos = 550
            position2 = 0            
            return None
            

################################################################################
## System Vars
################################################################################

    #Developer Mode
    config.developer = True

################################################################################
## Game Objects
################################################################################

    current_game = game_core()

    score_value = 0
    position = 0
    position2 = 0
    ref_pos = 550
    ref_speed = 0    
    ref_direction1 = ""
    ref_xpos = {"left_step":400, "shaking_left":400 , "rotate_left":400, "up_step":520, "rotate_leftup":520, "rotate_rightdown":630, "down_step":630, "right_step":750, "rotate_right":750, "shaking_right":750}
    ref_key = {"left_step":"K_LEFT", "shaking_left":"K_LEFT", "rotate_left":"K_LEFT", "up_step":"K_UP", "down_step":"K_DOWN", "right_step":"K_RIGHT", "rotate_right": "K_RIGHT", "shaking_right": "K_RIGHT", "rotate_leftup": "K_UP", "rotate_rightdown": "K_DOWN"}
    ref_status = ["","GREAT","PERFECT"]
    current_time = 0.0
    blink = False
    score = 0
    status = ""
    check_score = False
    key_value = ""

    tutorial_steps = [[10, 1, None, "Mensagem de Texto"], [5, 3, None, "Mensagem de Texto2"], [5, 3, None, "Mensagem de Texto3"],[30, 2, None, ""] ]


################################################################################
## IMAGES
################################################################################

image left_step:
    "esquerda"
    xpos 400
    ypos -20
    linear ref_speed ypos 550

image up_step:
    "cima"
    xpos 520
    ypos -20
    linear ref_speed ypos 550

image down_step:
    "baixo"
    xpos 630
    ypos -20
    linear ref_speed ypos 550

image right_step:
    "direita"
    xpos 750
    ypos -20
    linear ref_speed ypos 550

image rotate_right:
    "esquerda v"
    xpos 374
    ypos -20
    rotate 0
    alpha 1.0
    linear ref_speed*0.5 ypos 225
    ease ref_speed*0.3 ypos 450 xpos 724 rotate 180
    linear ref_speed*0.2 ypos 524

image rotate_rightdown:
    "direita v"
    xpos 724
    ypos -20
    rotate 0
    alpha 1.0
    linear ref_speed*0.5 ypos 225
    ease ref_speed*0.3 ypos 450 xpos 614 rotate 90
    linear ref_speed*0.2 ypos 524

image rotate_leftup:
    "esquerda v"
    xpos 374
    ypos -20
    rotate 0
    alpha 1.0
    linear ref_speed*0.5 ypos 225
    ease ref_speed*0.3 ypos 450 xpos 496 rotate 90
    linear ref_speed*0.2 ypos 524

image rotate_left:
    "direita v"
    xpos 724
    ypos -20
    rotate 0
    alpha 1.0
    linear ref_speed*0.5 ypos 225
    ease ref_speed*0.3 ypos 450 xpos 374 rotate 180
    linear ref_speed*0.2 ypos 524

image shaking_left:
    "esquerda zig"
    xpos 400
    ypos -20    
    linear ref_speed*0.5 ypos 510
    linear ref_speed*0.3 ypos 470
    linear ref_speed*0.2 ypos 550

image shaking_right:
    "direita zig"
    xpos 750
    ypos -20    
    linear ref_speed*0.5 ypos 510
    linear ref_speed*0.3 ypos 470
    linear ref_speed*0.2 ypos 550

image inter1:
    "black"
    alpha 0.7
    size(320,100)
    on hide:
        linear 1.0 xpos -500

image inter2:
    "preto1"
    alpha 0.2
    size(1000,100)
    xpos 320
    on hide:
        linear 1.0 xpos -1000

image select_loja2:
    "shop 2"
    zoom 0.5
    xpos 480
    ypos 60
    ease 1.1 ypos 90
    ease 1.1 ypos 60
    repeat

image select_loja3:
    "shop 3"
    zoom 0.6
    xpos 920
    ypos 20
    ease 1.0 ypos 50
    ease 1.0 ypos 20
    repeat

image tutorial_background = Movie(play="tutorial/video.webm", pos=(0, 0), anchor=(0, 0), size=(1280, 720), channel='movie')
image launch2 = Movie(play="videos/oa4_launch.webm", pos=(0, 0), anchor=(0, 0), size=(1280, 720), channel='movie')

################################################################################
## TRANSFORM
################################################################################

transform step_blink:
    linear 0.3 zoom 1.1
    linear 0.3 zoom 1.1

transform step_speed:
    ypos -20  
    function step_handler

transform step_speed2:
    ypos -20  
    function step_handler2

#To Refactor

define config.mouse = {"default":[ ("gui/gggg.png", 0, 0) ] }
#LiveComposite ou Composite
image ola = Composite(
    (1280, 720),
    (0, 0), "set1",
    (0, 0), "set4"
    )#HBox("set1", "set4")
image enzo = Crop((200, 200, 300, 300), "erer")

transform sobedesce:
    zoom 0.5
    ypos 150
    xpos 150
    ease 2.0 ypos 120
    ease 2.0 ypos 150
    repeat

transform escolhas:
    zoom 1.5
    alpha 0.0
    ease 0.3 zoom 0.85 alpha 1.0
    ease 0.3 zoom 1.05
    ease 0.3 zoom 1.0
transform umi1:
    xpos 400
    ypos 550
    linear 0.3 xpos 390 ypos 540 zoom 1.05
    linear 0.3 xpos 750 ypos 550 zoom 1.05
transform umi2:
    xpos 520
    ypos 550
    linear 0.3 xpos 510 ypos 540 zoom 1.05
    linear 0.3 xpos 750 ypos 550 zoom 1.05
transform umi3:
    xpos 630
    ypos 550
    linear 0.3 xpos 640 ypos 540 zoom 1.05
    linear 0.3 xpos 750 ypos 550 zoom 1.05
transform umi4:
    xpos 750
    ypos 550
    linear 0.3 xpos 760 ypos 540 zoom 1.05
    linear 0.3 xpos 750 ypos 550 zoom 1.05
transform video:
    alpha 0.6
transform ajud:
    xpos -1280
    ease 0.5 xpos 250
transform ajud1:
    xpos -1280
    ease 0.5 xpos 30
transform zonu:
    ease 1.0 zoom 1.04 rotate -3
    ease 1.0 zoom 1.0 rotate 3
    repeat
transform zonu1:
    ease 0.7 zoom 1.07 rotate -2
    ease 0.7 zoom 1.0 rotate 2
    repeat
transform zonu2:
    ease 0.7 zoom 1.07 rotate 1
    ease 0.7 zoom 1.0 rotate -1
    repeat
transform alpa:
    on show:
        alpha 0.0
        ease 0.5 alpha 1.0
    on hide:
        ease 0.5 alpha 0.0 
init python:
    config.keymap["game_menu"] = [ 'K_MENU', 'mouseup_3', 'K_p']
    config.keymap["hide_windows"] = []
    pref = False
    ajuda = False
    selecionado = False
    
    
    
    
