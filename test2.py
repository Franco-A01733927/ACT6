import sys, random, os, time
import pygame

pygame.init()
pygame.mixer.init()
FPS = 60
size=width, height=450, 650
screen_w = width
screen_h = height
half_w = screen_w/2
pygame.display.set_caption("Actividad #6")
difficulty = 2
score = 0
tmp = 0
hscore = 0
rows = 4
row_w = screen_w / rows
row_h = screen_h
tile_w = row_w - 2
half_t_w = tile_w/2
tile_h = tile_w*2
y = 10
ledtime = 0.5
pygame.mixer.music.load("super-electronicas-mario-bros-mix-2018.mp3")


  
class rgb:
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    WHITE2 = (254,254,254)
    RED = (255,0,0)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
def font(font_name,size):
    return pygame.font.SysFont(font_name, int(size))
def label(font_name,size,text,rgb,pos,center=False):
    global screen
    lbl = font(font_name,size).render(text, 1, rgb)
    if center == False:
        screen.blit(lbl, pos)
    else:
        screen.blit(lbl, lbl.get_rect(center=center))
def add_tile():
    global tiles, rows, row_w
    row = random.randint(int(0),int(rows-1))
    color = rgb.BLACK
    def getY():
        global tile_h
        n = -random.randint(int(tile_h),int(1000))
        for t in tiles:
            if n == t[2]-tile_h-1 and n != t[2]:
                return n
        try:
            return getY()
        except:
            return t[2]-tile_h-1
    y = getY()
    tiles.append([color,2+row_w*row,y])
def play(filename_with_sound):
    Effect = pygame.mixer.Sound(open("Sounds/%s"%(filename_with_sound),"rb"))
    Effect.play()
def start_game():
    global game, hscore_msg, tiles
    game = True
    play("begin.ogg")
    hscore_msg = False
    tiles = [[rgb.BLACK, 2, -tile_h*2],[rgb.BLACK, 2+row_w*1, -tile_h*2]]
    [add_tile() for x in range(0,7)]
def end_game():
    global game, score, hscore, hscore_msg, tiles
    play("end.ogg")
    game = False
    highscore("SAVE")
    score = 0
def highscore(method):
    global score, hscore, hscore_msg
    if method == "SAVE":
        if score > hscore:
            hscore = score
            hscore_msg = True
    elif method == "BGCOLOR":
        if score < hscore or score == 0:
            return rgb.WHITE
        else:
            return rgb.WHITE
    elif method == "FGCOLOR":
        if score < hscore or score == 0:
            return rgb.BLACK
        else:
            return rgb.BLACK
def click_tile():
    global mouse_position, tiles, score, tile_w, tile_h
    x, y = mouse_position
    i = 0
    click_on_tile = False
    for t in tiles:
        if x > t[1] and x < t[1] + tile_w and y > t[2] and y < t[2] + tile_h:
            click_on_tile = True
            del tiles[i]
            play("click.ogg")
            add_tile()
            score += 1
        i += 1
    if click_on_tile == False:
        pygame.mixer.music.pause()
        end_game()
def handle_title_tile_click(select_from):
    global mouse_position, score, tile_w, tile_h, rows
    x, y = mouse_position
    i = 0
    z = 0
    click_on_tile = False
    for t in select_from:
        if rows != 2 or t[0] in [rgb.RED, rgb.GREEN]:
            cur_row = z
            if x > 2+row_w*cur_row and x < 2+row_w*cur_row + tile_w and y > t[1] and y < t[1] + tile_h:
                click_on_tile = True
                play("click.ogg")
                return select_from[i]
            z += 1
        i += 1
    if click_on_tile == False:
        play("end.ogg")
def screens_click():
    global screens, cur_screen, difficulty, rows, row_w, row_h, screen_w, screen_h, half_t_w, tile_w, tile_h,tmp,ledtime
    selection = handle_title_tile_click(screens[cur_screen])
    selected_long = selection
    if selection == None:
        return None
    selection = selection[0]
    if cur_screen == 0:
        if selection == rgb.BLACK:
            pygame.mixer.music.play()
            tmp = 0
            start_game()
        elif selection == rgb.WHITE2:
            cur_screen += 1
    elif cur_screen == 1:
        cur_screen -= 1
        if str(selected_long[4]) == "FACIL":
            difficulty = 2
            pygame.mixer.music.load("super-electronicas-mario-bros-mix-2018.mp3")
            ledtime = 0.5
        elif str(selected_long[4]) == "MEDIO":
            difficulty = 3
            pygame.mixer.music.load("Superx10.mp3")
            ledtime = 0.4
        elif str(selected_long[4]) == "DIFICIL":
            difficulty = 4
            pygame.mixer.music.load("Superx20.mp3")
            ledtime = 0.3
        elif str(selected_long[4]) == "LEGENDARIO":
            difficulty = 5
            pygame.mixer.music.load("Superx30.mp3")
            ledtime = 0.2
        f2=open('prueba2.txt','w')
        lt = str(ledtime)
        f2.write(lt)
        f2.close()

def draw_vertical_lines():
    global rows, screen, row_w, row_h
    for x in range(0,rows+1):
        pygame.draw.line(screen, highscore("FGCOLOR"), (row_w*x, 0), (row_w*x, row_h), 2)
tiles = []
title_screen = [[rgb.BLACK,300,tile_w,tile_h, "J    U   G",15],[rgb.BLACK,300,tile_w,tile_h,"A  R   !",35],[rgb.WHITE2, 300, tile_w, tile_h, "D I F I C",30],[rgb.WHITE2,300,tile_w,tile_h,"U L T A D",15]]

difficulty_screen = [[rgb.BLACK, 250, tile_w, tile_h,"FACIL",100],[rgb.BLACK,300,tile_w,tile_h,"MEDIO",100],[rgb.BLACK,250,tile_w,tile_h,"DIFICIL",100],[rgb.BLACK,300,tile_w,tile_h,"LEGENDARIO",100]]
screens = [title_screen,difficulty_screen]
cur_screen = 0
game = False
hscore_msg = False
while True:
    """

    """
    screen.fill(highscore("BGCOLOR"))
    draw_vertical_lines()
    if game == True:
        for t in tiles:
            pygame.draw.rect(screen, t[0], [t[1], t[2], tile_w, tile_h], 0)
            if t[2] < row_h and t[2] + tile_h != row_h:
                t[2] = t[2]+difficulty
            else:
                pygame.mixer.music.pause()
                end_game()
        label("monospace",100,str(score),highscore("FGCOLOR"),(row_w/3.25, screen_h-100))
        if score != tmp:
            f=open('prueba.txt','w')
            s = str(score)
            f.write(s)
            f.close()
            tmp +=1
            

    else:
        i = 0
        for t in screens[cur_screen]:
            if rows != 2 or t[0] in [rgb.RED, rgb.GREEN]:
                cur_row = i
                pygame.draw.rect(screen, t[0], [2+row_w*cur_row, t[1], tile_w, tile_h], 0)
                #Defines the properties of the label
                label("monospace",tile_w/len(t[4])+5,t[4],rgb.RED,(),center=(tile_w*cur_row+half_t_w+cur_row*2.5,t[1]+tile_h/2))
                i += 1
        if hscore_msg == False:
            label("monospace",100,"Tiles",rgb.BLACK,(),center=(half_w, 100))
            label("monospace", 15,"High Score:" + str(hscore),rgb.BLACK,(),center=(half_w, screen_h-20))
        else:
            label("monospace",65,"High Score!",rgb.BLACK,(),center=(half_w, 100))
            label("monospace",100,str(hscore),rgb.BLACK,(),center=(half_w, 200))
    #Registers the Mouse clicking
    for event in pygame.event.get():
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game == True:
                click_tile()
            else:
                screens_click()
                
    pygame.display.flip()
    clock.tick(FPS)
