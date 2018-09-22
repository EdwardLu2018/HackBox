import pygame as pg

COLOR_INACTIVE = pg.Color("white")
COLOR_ACTIVE = (173, 255, 47)
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 700

class InputBox:
    # constructor for input box
    def __init__(self, xpos, ypos, w, h, is_c, mx, my, max_len, text=''):
        self.text = text
        self.input_box = pg.Rect(xpos, ypos, w, h)
        self.is_chat_box = is_c
        self.xpos_message = mx
        self.ypos_message = my
        self.color = COLOR_INACTIVE
        self.txt_surface = pg.font.Font(None, 32).render(text, True, self.color)  # first 20 char of chat message
        self.txt_surface2 = pg.font.Font(None, 32).render(text, True, self.color)  # next 20 char of chat message
        self.is_active = False
        self.log = list()  # chat log
        self.max_msg = max_len

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
                        self.log.append(self.text)  # adds to chat log
                        if len(self.log) > self.max_msg:
                            self.log.pop(0)
                        self.text = ''
                        return self.log[len(self.log) - 1]
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < self.max_msg:
                    self.text += event.unicode
        return 0

    # edits the text entered into two lines
    def update(self):
        self.txt_surface = pg.font.Font(None, 32).render(self.text[0:int(self.max_msg/2)], True, (173, 255, 47))
        self.txt_surface2 = pg.font.Font(None, 32).render(self.text[int(self.max_msg/2):int(self.max_msg)], True, (173, 255, 47))

    # draws chat box
    def draw(self, screen):
        self.input_box.w = WINDOW_WIDTH / 2
        screen.blit(self.txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        screen.blit(self.txt_surface2, (self.input_box.x + 5, self.input_box.y + 37))
        pg.draw.rect(screen, self.color, self.input_box, 2)
