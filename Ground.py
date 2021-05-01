
class Ground:
    VEL = 5

    def __init__(self, y, ground_img):
        self.img = ground_img
        self.width = self.img.get_width()
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.width < -10:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < -10:
            self.x2 = self.x1 + self.width

    def draw(self, window):
        window.blit(self.img, (self.x1, self.y))
        window.blit(self.img, (self.x2, self.y))
