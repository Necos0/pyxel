import pyxel
import random


class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y  
        self.my = 16

class Food:
    def __init__(self):
        self.fx = random.randint(0,7)
        self.fy = random.randint(0,7)
    def change(self):
        self.fx = random.randint(0,7)
        self.fy = random.randint(0,7)
        
class App:
    def __init__(self):
        pyxel.init(128,128,capture_scale=8,fps=20)
        pyxel.load("e.pyxres")
        self.player = Player(16,16)
        self.food = Food()
        self.dis = pyxel.sqrt(((self.player.x) - (self.food.fx))**2 + ((self.player.y )- (self.food.fy)**2))
        self.score = 0
        
    def run(self):
        pyxel.run(self.update,self.draw)
        
    def update(self):
        self.dis = pyxel.sqrt(((self.player.x+4) - 16*self.food.fx)**2 + ((self.player.y+4)- 16*self.food.fy)**2)
        if self.dis < 7:
            self.food.change()
            self.score += 1000
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.player.x -= 16
            self.player.my = 32
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.player.x += 16
            self.player.my = 16
        elif pyxel.btnp(pyxel.KEY_UP):
            self.player.y -= 16
            self.player.my = 48
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.player.y += 16
            self.player.my = 64
        
        if self.player.x >112:
            self.player.x = 112
        if self.player.x <0:
            self.player.x = 0
        if self.player.y >112:
            self.player.y = 112
        if self.player.y<0:
            self.player.y = 0
        
            
            
    
    def draw(self):
        pyxel.cls(0)
        pyxel.blt(self.player.x,self.player.y,0,16*(pyxel.frame_count%2),self.player.my,16,16,0)
        pyxel.blt(16*self.food.fx,16*self.food.fy,0,32,16,16,16,0)
        pyxel.text(0,0,f"score:{self.score}",2)
app= App()
app.run()