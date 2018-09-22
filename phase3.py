    def phase3(self):
        prompt = pg.font.SysFont(None,48).render("Match Each Person to Answer", False, (173,255,47))
        promptRect = prompt.get_rect()
        promptRect.centerx = WINDOW_WIDTH/2
        promptRect.centery = 50
        self.screen.blit(prompt, promptRect)
        for i in range(len(self.players)):
            self.playerRect[i].draw(self.screen)
            self.answerRect[i].draw(self.screen)
       
class DisplayInputs():
    def __init__(self, write, x, y, activeCol, inactiveCol):
        self.content = write
        self.x = x
        self.y = y
        self.actCol = activeCol
        self.inactCol = inactiveCol
        self.color = inactiveCol
        self.clicked = False
        
        
    def draw(self, screen):
        basicfont = pg.font.SysFont(None, 48)
        self.printContent = basicfont.render(self.content, False, self.color,(0,0,0))
        self.textrect = self.printContent.get_rect()
        
        self.textrect.centerx = self.x
        self.textrect.centery = self.y
        screen.blit(self.printContent, self.textrect)
        
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.textrect.collidepoint(event.pos):
            if self.color == self.actCol:
                self.color = self.inactCol
                self.clicked = not self.clicked
            else:
                self.color = self.actCol
                self.clicked = not self.clicked
        return self.clicked
