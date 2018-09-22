import pygame as pg

pg.init()

COLOR_INACTIVE = pg.Color("white")
COLOR_ACTIVE = (173,255,47)
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 700

class InputBox:
    # constructor for input box
    def __init__(self, xpos, ypos, w, h, is_c, mx, my, text=''):
        self.text = text
        self.input_box = pg.Rect(xpos, ypos, w, h)
        self.is_chat_box = is_c 
        self.xpos_message = mx
        self.ypos_message = my
        self.color = COLOR_INACTIVE
        self.txt_surface = pg.font.Font(None, 32).render(text, True, self.color) # first 20 char of chat message
        self.txt_surface2 = pg.font.Font(None, 32).render(text, True, self.color) # next 20 char of chat message
        self.is_active = False
        self.log = list() # chat log
        self.max_msg = 1
        if self.is_chat_box:
            self.max_msg = 27

    # handles mouse click
    def handle_event(self, event):
        # if the user clicked on the input box, input box is active
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.is_active = not self.is_active
            else:
                self.is_active = False
            self.color = COLOR_ACTIVE if self.is_active else COLOR_INACTIVE
            
        # checks if key is pushed
        if event.type == pg.KEYDOWN:
            if self.is_active:
                if event.key == pg.K_RETURN:
                    if len(self.text) != 0:
                        self.log.append(self.text) # adds to chat log
                        if len(self.log) > self.max_msg:
                            self.log.pop(0)
                        self.text = ''
                        return self.log[len(self.log) - 1]
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 60:
                    self.text += event.unicode
        return 0

    # edits the text entered into two lines
    def update(self):
        self.txt_surface = pg.font.Font(None, 32).render(self.text[0:30], True, (173,255,47))
        self.txt_surface2 = pg.font.Font(None, 32).render(self.text[30:60], True, (173,255,47))

    # draws chat box
    def draw(self, screen):
        self.input_box.w = WINDOW_WIDTH / 2
        screen.blit(self.txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        screen.blit(self.txt_surface2, (self.input_box.x + 5, self.input_box.y + 37))
        if self.xpos_message >= 0 and self.ypos_message >= 0:
            y = self.ypos_message
            for msg in self.log:
                self.update()
                screen.blit(msg_surface, (self.xpos_message, y))
                if len(msg) > 20:
                    y += 20
                screen.blit(msg_surface2, (self.xpos_message, y))
                y += 20
        pg.draw.rect(screen, self.color, self.input_box, 2)

class HackBox():
    def __init__(self):
        self.state = 0
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption("Hackbox")
        self.clock = pg.time.Clock()
        self.chat_box = InputBox(0, WINDOW_HEIGHT - 64, WINDOW_WIDTH / 2, 64, True, 5, 30)
        self.question_input = InputBox(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 64, WINDOW_WIDTH / 2, 64, False, -1, -1)
        self.username_input = InputBox(WINDOW_WIDTH / 4 + 20, WINDOW_HEIGHT / 3 + 100, WINDOW_WIDTH / 2, 64, False, -1, -1)
        self.input_boxes = [self.chat_box, self.question_input]
        self.username = ''

    def introScreen(self):
        title = pg.font.SysFont("Times New Roman", 80).render("HackBox", 1, (173,255,47))
        self.screen.blit(title, (WINDOW_WIDTH / 3 + 120, 100))
        description = pg.font.SysFont("Times New Roman", 30).render("Answer coding questions! Play Against Your Friends!", 1, (173,255,47))
        self.screen.blit(description, (425, 180))
        label = pg.font.SysFont("Times New Roman", 32).render("Please enter a username below:", 1, (173,255,47))
        self.screen.blit(label, (WINDOW_WIDTH / 3 + 75, WINDOW_HEIGHT / 3 + 75))

    def phase1(self):
        pass
    def phase2(self):
        pass
    def phase3(self):
        pass
    def phase4(self):
        #Very similar to phase2. Maybe just copy paste most of it
        pass
    def phase5(self):
        pass

    def waitingScreen(self):
        pg.draw.rect(self.screen, 0, (50, 50, 100, 100), 0)
        loading = pg.font.SysFont("Times New Roman", 30).render("Loading...", 1, (255, 255, 255))
        self.screen.blit(loading, (WINDOW_WIDTH / 2, 0))

    def update(self):
        self.clock.tick(60)
        
        self.screen.fill((0,0,0))

        if self.state == 0:
            hb.introScreen()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                self.username = self.username_input.handle_event(event)
                if self.username != 0:
                    self.state += 1
            self.username_input.update()
            self.username_input.draw(self.screen)

        elif self.state == 1:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                answer = self.question_input.handle_event(event)
                self.chat_box.handle_event(event)
                if answer != 0:
                    self.state += 1

            self.chat_box.update()
            self.question_input.update()

            if pg.mouse.get_pressed()[0]:
                mouse_pos = pg.mouse.get_pos()
                pg.draw.rect(self.screen, (173,255,47), (mouse_pos[0] - 5, mouse_pos[1] - 5, 10, 10), 0)
            
            pg.draw.rect(self.screen, (0, 0, 225), (WINDOW_WIDTH / 2 - 5, 0, 10, WINDOW_HEIGHT), 0)
            chat_label = pg.font.SysFont("Times New Roman", 30).render("Chat:", 1, (173,255,47))
            self.screen.blit(chat_label, (5, 5))
            chat_message = pg.font.SysFont("Times New Roman", 30).render("Type Message Below:", 1, (173,255,47))
            self.screen.blit(chat_message, (10, 610))
            self.question_input.draw(self.screen)
            self.chat_box.draw(self.screen)
            
        elif self.state == 2:
            self.state += 1

        elif self.state == 3:
            self.phase3()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.state += 1

        elif self.state == 4:
            self.state += 1

        elif self.state == 5:
            self.state = 1
            
        pg.display.flip()


hb = HackBox()
while 1:
    hb.update()
