import pygame as pg
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Hackbox")
sheet3 = sheet.worksheet('sheet3')
questions = sheet.worksheet('questions')
row = 0

#Convert a guess to a dictionary
def guess_to_dict():
    pass


#Based on answers, return a dictionary with correct answers
def get_correct_answer(s):
    values = s.get_all_values
    solution = {
        values[1][1]: values[1][4],
        values[2][1]: values[2][4],
        values[3][1]: values[3][4],
        values[4][1]: values[4][4]
    }
    return solution

#Reset the sheet for a new game
def reset(s):
    for r in range(1, 5):
        for c in range(1, 6):
            s.update_cell(r, c, "0")

#Clear the answers
def clear_answers(s):
    for r in range(1, 5):
        s.update_cell(r, 4, "0")

#Clear the guesses
def clear_guesses(s):
    for r in range(1, 5):
        s.update_cell(r, 5, "0")

#Update your score
def update_score(s, inc):
    global row
    score = int(s.cell(row, 2).value)
    s.update_cell(row, 2, score + inc)

#Send a chat message
def send_msg(s, msg):
    global row
    s.update_cell(row, 3, msg)

#Send an answer
def send_answer(s, ans):
    global row
    s.update_cell(row, 4, ans)

#Send a guess
def send_guess(s, guess):
    global row
    s.update_cell(row, 5, guess)

#Read col
def read_col(s, col):
    return s.col_values(col)

#Check value at a cell
def check_cell(s, row, col, val):
    return s.cell(row, col).value == val

#Check col for zeroes
def check_col(s, col, v):
    vals = s.col_values(col)
    for val in vals:
        if(val == v):
            return False
    return True


pg.init()

COLOR_INACTIVE = pg.Color("white")
COLOR_ACTIVE = (173, 255, 47)
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
        self.txt_surface = pg.font.Font(None, 32).render(text, True, self.color)  # first 20 char of chat message
        self.txt_surface2 = pg.font.Font(None, 32).render(text, True, self.color)  # next 20 char of chat message
        self.is_active = False
        self.log = list()  # chat log
        self.max_msg = 1
        if self.is_chat_box:
            self.max_msg = 20

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
                elif len(self.text) < 60:
                    self.text += event.unicode
        return 0

    # edits the text entered into two lines
    def update(self):
        self.txt_surface = pg.font.Font(None, 32).render(self.text[0:30], True, (173, 255, 47))
        self.txt_surface2 = pg.font.Font(None, 32).render(self.text[30:60], True, (173, 255, 47))

    # draws chat box
    def draw(self, screen):
        self.input_box.w = WINDOW_WIDTH / 2
        screen.blit(self.txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        screen.blit(self.txt_surface2, (self.input_box.x + 5, self.input_box.y + 37))
        if self.xpos_message >= 0 and self.ypos_message >= 0:
            y = self.ypos_message
            for msg in self.log:
                msg_surface = pg.font.Font(None, 32).render(msg[0:30], True, (173, 255, 47))
                msg_surface2 = pg.font.Font(None, 32).render(msg[30:60], True, (173, 255, 47))
                screen.blit(msg_surface, (self.xpos_message, y))
                if len(msg) > 20:
                    y += 25
                screen.blit(msg_surface2, (self.xpos_message, y))
                y += 25
        pg.draw.rect(screen, self.color, self.input_box, 2)


class HackBox():
    def __init__(self):
        global sheet3
        self.state = 0
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption("Hackbox")
        self.clock = pg.time.Clock()
        self.chat_box = InputBox(0, WINDOW_HEIGHT - 64, WINDOW_WIDTH / 2, 64, True, 5, 30)
        self.question_input = InputBox(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 64, WINDOW_WIDTH / 2, 64, False, -1, -1)
        self.username_input = InputBox(WINDOW_WIDTH / 4 + 20, WINDOW_HEIGHT / 3 + 100, WINDOW_WIDTH / 2, 64, False, -1,
                                       -1)
        self.input_boxes = [self.chat_box, self.question_input]
        self.username = ''
        self.dots = 0
        reset(sheet3)

    def introScreen(self):
        title = pg.font.SysFont("Times New Roman", 80).render("HackBox", 1, (173, 255, 47))
        self.screen.blit(title, (WINDOW_WIDTH / 3 + 120, 100))
        description = pg.font.SysFont("Times New Roman", 30).render(
            "Answer coding questions! Play Against Your (Imaginary) Friends!", 1, (173, 255, 47))
        self.screen.blit(description, (425, 180))
        label = pg.font.SysFont("Times New Roman", 32).render("Please enter a username below:", 1, (173, 255, 47))
        self.screen.blit(label, (WINDOW_WIDTH / 3 + 75, WINDOW_HEIGHT / 3 + 75))

    def phase1(self):
        pass

    def phase2(self):
        pass

    def phase3(self):
        pass

    def phase4(self):
        # Very similar to phase2. Maybe just copy paste most of it
        pass

    def phase5(self):
        pass

    def waitingScreen(self):
        code_image = pg.image.load("code_image.png")
        self.screen.blit(code_image, (60, 0))
        dotstring = ""
        for dot in range(0, self.dots):
            dotstring += "."
        self.dots = (self.dots + 1) % 4
        loading = pg.font.SysFont("Times New Roman", 30).render("Loading" + dotstring, 1, (173, 255, 47))
        self.screen.blit(loading, (WINDOW_WIDTH / 2 - 45, WINDOW_HEIGHT / 2))

    def update(self):
        global sheet3, questions, row
        self.clock.tick(60)

        self.screen.fill((0, 0, 0))

        if self.state == 0:
            hb.introScreen()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                self.username = self.username_input.handle_event(event)
                if self.username != 0:
                    self.state += 1
                    players = read_col(sheet3, 1)
                    for i in range(0, 4):
                        if players[i] == "0":
                            row = i + 1
                            sheet3.update_cell(row, 1, self.username)
                            break

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
                pg.draw.circle(self.screen, (173, 255, 47), (mouse_pos[0], mouse_pos[1]), 5, 0)

            pg.draw.rect(self.screen, (0, 0, 225), (WINDOW_WIDTH / 2 - 5, 0, 10, WINDOW_HEIGHT), 0)
            chat_label = pg.font.SysFont("Times New Roman", 30).render("Chat:", 1, (173, 255, 47))
            self.screen.blit(chat_label, (5, 5))
            chat_message = pg.font.SysFont("Times New Roman", 30).render("Type Message Below:", 1, (173, 255, 47))
            self.screen.blit(chat_message, (10, 610))
            self.question_input.draw(self.screen)
            self.chat_box.draw(self.screen)

        elif self.state == 2:
            self.waitingScreen()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
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
