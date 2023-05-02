import pyxel


class App:
    def __init__(self):
        pyxel.init(160,120)
        pyxel.load("m.pyxres")
        self.x = 50
        self.y = 96
        self.vx = 0
        self.vy = 0
        self.ay = 0
        self.canjump = True
        self.map_x = 0
        self.map_y = 0
        
    def run(self):
        pyxel.run(self.update,self.draw)
        
    def update(self):
        #入力を受け入れる
        if pyxel.btnp(pyxel.KEY_A):
            self.vx -= 2
            self.map_x = 1
        elif pyxel.btnp(pyxel.KEY_D):
            self.vx += 2
            self.map_x = 0
        elif pyxel.btnp(pyxel.KEY_SPACE):
            if self.canjump == True:
                self.vy = -6
                self.ay = 0.5
                self.canjump = False
        if pyxel.btnr(pyxel.KEY_A) or pyxel.btnr(pyxel.KEY_D):
        
            self.vx = 0
        
        #当たり判定
        if self.x < 8:
            self.x = 8
        if self.x > 136:
            self.x = 136
        if self.y < 8:
            self.y = 8
        if self.y > 96:
            self.y = 96
            self.ay = 0
            self.vy = 0
            self.canjump = True
        #移動処理
        self.x += self.vx
        self.y += self.vy
        self.vy += self.ay
        #マリオの動き設定
        if self.canjump == True:
            if self.vx != 0:
                self.map_y = pyxel.frame_count%3
            
        elif self.canjump == False:
            self.map_y = 3
        
    
        
        
        
    def draw(self):
        pyxel.bltm(0,0,0,0,0,160,120,2)
        pyxel.blt(self.x,self.y,0,16*self.map_x,16*(self.map_y),16,16,0)
    
app= App()
app.run()
        