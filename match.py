class Match():
    def __init__(self, id1, id2, con1, con2, gun1, gun2):
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0

        self.hp1 = 100
        self.hp2 = 100

        self.gun1 = gun1
        self.gun2 = gun2

        self.id1 = id1
        self.id2 = id2

        self.con1 = con1
        self.con2 = con2

    def update(self, newx, newy, pn):
        if pn == 0:
            self.x2 = newx
            self.y2 = newy
        if pn == 1:
            self.x1 = newx
            self.x2 = newy

    def list(self):
        return [self.con1, self.con2]

    def grab(self, pn):
        if pn == 1:
            return self.con1
        if pn == 0:
            return self.con2

    def hit(self, pn, dmg):
        if pn == 0:
            self.hp1 -= dmg
            if self.hp1 <= 0:
                return True
            else:
                return False
        if pn == 1:
            self.hp2 -= dmg
            if self.hp2 <= 0:
                return True
            else:
                return False

    def check(self, pid):
        if pid == self.id1 or pid == self.id2:
            return True
        else:
            return False

    def oth(self, pid):
        if pid == self.id1:
            return self.con2
        else:
            return self.con1
