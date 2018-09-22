import pygame as pg
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
from utility import *
from box import InputBox
from displayinput import DisplayInputs
import random

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Hackbox")
sheet3 = sheet.worksheet('sheet3')
row = 0

pg.init()

COLOR_INACTIVE = pg.Color("white")
COLOR_ACTIVE = (173, 255, 47)
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 700


class HackBox():
    def __init__(self):
        global sheet3, sheet
        self.state = 0
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption("Hackbox")
        self.clock = pg.time.Clock()
        self.question_input = InputBox(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 3, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3, 64, -1, -1,
                                       100)
        self.username_input = InputBox(WINDOW_WIDTH / 4 + 20, WINDOW_HEIGHT / 3 + 100, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3, 64, -1, -1, 30)
        self.username = ''
        self.dots = 0
        self.question = 0
        self.score = 0
        self.players = list()
        self.questions = sheet.worksheet('questions').get_all_values()
        self.clicked = False
        self.answers = list()
        self.playerRect = list()
        self.answerRect = list()
        self.selectedPlayer = 0
        self.selectedAnswer = 0
        self.guess = {}
        reset(sheet3)

    def introScreen(self):
        title = pg.font.SysFont("None", 80).render("HackBox", 1, (173, 255, 47))
        self.screen.blit(title, (WINDOW_WIDTH / 3 + 120, 100))
        description = pg.font.SysFont("None", 30).render(
            "Answer coding questions! Play Against Your (Imaginary) Friends!", 1, (173, 255, 47))
        self.screen.blit(description, (425, 180))
        label = pg.font.SysFont("None", 32).render("Please enter a username below:", 1, (173, 255, 47))
        self.screen.blit(label, (WINDOW_WIDTH / 3 + 75, WINDOW_HEIGHT / 3 + 75))

    def phase1(self):
        the_question = self.questions[self.question][0]
        basicfont = pg.font.SysFont(None, 48)
        score_message = pg.font.SysFont(None, 30).render(f"Score: {self.score}", 1, (173, 255, 47))
        self.screen.blit(score_message, (5, 5))

        text = basicfont.render(the_question, False, (173, 255, 47), (0, 0, 0))
        textrect = text.get_rect()
        textrect.centerx = WINDOW_WIDTH / 2
        textrect.centery = 150
        self.screen.blit(text, textrect)
        self.question_input.draw(self.screen)

    def phase3(self):
        #Display the 4 players and mixed answers
        score_message = pg.font.SysFont(None, 30).render(f"Score: {self.score}", 1, (173, 255, 47))
        self.screen.blit(score_message, (5, 5))
        prompt = pg.font.SysFont(None, 48).render("Match Each Person to Answer", False, (173, 255, 47))
        promptRect = prompt.get_rect()
        promptRect.centerx = WINDOW_WIDTH / 2
        promptRect.centery = 50
        self.screen.blit(prompt, promptRect)
        for i in range(len(self.playerRect)):
            self.playerRect[i].draw(self.screen)
            self.answerRect[i].draw(self.screen)

    def phase5(self):
        #Display the 4 answers and who thought who answered what
        score_message = pg.font.SysFont(None, 30).render(f"Score: {self.score}", 1, (173, 255, 47))
        self.screen.blit(score_message, (5, 5))
        for i in range(2):
            for k in range(2):
                x = 0
                y = 0
                w = WINDOW_WIDTH / 3 + 50
                h = WINDOW_HEIGHT / 6
                if k == 0:
                    x = WINDOW_WIDTH / 8
                else:
                    x = 5 * WINDOW_WIDTH / 8
                if i == 0:
                    y = WINDOW_HEIGHT / 8
                else:
                    y = 5 * WINDOW_HEIGHT / 8
                pg.draw.rect(self.screen, (0, 0, 255),
                             (x, y, w, h), 0)
                who = self.answers[2 * i + k]
                description = pg.font.SysFont("None", 30).render(who[0:50], 1, (173, 255, 47))
                description2 = pg.font.SysFont("None", 30).render(who[50:100], 1, (173, 255, 47))
                self.screen.blit(description, (x, y + 5))
                self.screen.blit(description2, (x, y + 35))

                correct = self.players[2 * i + k]
                label = pg.font.SysFont(None, 32).render(correct, 1, (173, 255, 47))
                self.screen.blit(label, (x, y + 95))

    def phase7(self):
        scores = read_col(sheet3, 2)
        y = 5
        for i in range (0, 4):
            score_message = pg.font.SysFont(None, 50).render(f"{self.players[i]}: {scores[i]}", 1, (173, 255, 47))
            self.screen.blit(score_message, (WINDOW_WIDTH / 3, y))
            y += 50

    def waitingScreen(self):
        code_image = pg.image.load("code_image.png")
        self.screen.blit(code_image, (60, 0))
        dotstring = ""
        for dot in range(0, self.dots):
            dotstring += "."
        self.dots = (self.dots + 1) % 4
        loading = pg.font.SysFont("None", 30).render("Loading" + dotstring, 1, (173, 255, 47))
        self.screen.blit(loading, (WINDOW_WIDTH / 2 - 45, WINDOW_HEIGHT / 2))
        score_message = pg.font.SysFont(None, 30).render(f"Score: {self.score}", 1, (173, 255, 47))
        self.screen.blit(score_message, (5, 5))

    def update_score(self):
        inc = 0
        values = sheet3.get_all_values()
        solutions = get_correct_answer(sheet3)
        guess_dict = guess_to_dict(values[row - 1][4], self.players)
        for player in solutions:
            if solutions[player] == guess_dict[player]:
                inc += 100
        self.score += inc

    def update(self):
        global sheet3, row
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
            self.waitingScreen()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
            time.sleep(1)
            if check_col(sheet3, 1, "0"):
                ps = read_col(sheet3, 1)
                for p in ps:
                    self.players.append(p)
                    self.guess[p] = "0"
                self.state += 1

        elif self.state == 2:
            self.phase1()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.KEYDOWN:
                    answer = self.question_input.handle_event(event)
                    if answer != 0:
                        send_answer(sheet3, answer, row)
                        self.state += 1
                        self.question += 1

            self.question_input.update()
            self.question_input.draw(self.screen)

        elif self.state == 3:
            self.waitingScreen()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
            time.sleep(1)
            if check_col(sheet3, 4, "0"):
                if len(self.answers) == 0:
                    self.answers = read_col(sheet3, 4)
                a = random.sample(range(0, 4), 4)
                for i in range(4):
                    usernames = DisplayInputs(self.players[i], WINDOW_WIDTH / 8, 150 + i * 125, (173, 255, 47),
                                              (255, 255, 255))
                    answers = DisplayInputs(self.answers[i], WINDOW_WIDTH * 3 / 4, 150 + a[i] * 125, (173, 255, 47),
                                            (255, 255, 255))
                    self.playerRect.append(usernames)
                    self.answerRect.append(answers)
                self.state += 1

        elif self.state == 4:
            self.phase3()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                for p in self.playerRect:
                    handled = p.handle_event(event)
                    if handled != 0:
                        self.selectedPlayer = handled
                for a in self.answerRect:
                    handled = a.handle_event(event)
                    if handled != 0:
                        self.selectedAnswer = handled
                        self.guess[self.selectedPlayer.content] = self.selectedAnswer.content
                        self.playerRect.remove(self.selectedPlayer)
                        self.answerRect.remove(self.selectedAnswer)
                        self.selectedPlayer = 0
                        self.selectedAnswer = 0
            if len(self.playerRect) == 0:
                g = ''
                for key in self.guess:
                    g += self.guess[key] + ","
                g = g[0:len(g) - 1]
                send_guess(sheet3, g, row)
                self.state += 1


        elif self.state == 5:
            self.waitingScreen()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
            time.sleep(1)
            if check_col(sheet3, 5, "0"):
                self.state += 1

        elif self.state == 6:
            self.phase5()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.clicked = True
            if self.clicked:
                if row == 1:
                    self.update_score()
                    clear_answers(sheet3)
                    clear_guesses(sheet3)
                    self.state = 2
                else:
                    time.sleep(1)
                    if check_col(sheet3, 5, "0"):
                        self.update_score()
                        self.state = 2
                if self.question == len(self.questions):
                    update_score(sheet3, self.score, row)
                    self.state = 7
                self.clicked = False
                self.answers = list()
        elif self.state == 7:
            #Display leaderboard
            self.phase7()

            #Let them out
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

        pg.display.flip()


hb = HackBox()
while 1:
    hb.update()
