import pyxel
from enum import Enum
#状態の設定
class flag(Enum):
    title  = 0
    ground = 1
    air    = 2

class App:
    #初期化
    def __init__(self):
        pyxel.init(240, 120)
        pyxel.load("k.pyxres")
        self.state = flag.title
        self.player_x = 30
        self.player_y = 88
        self.player_dx = 0
        self.player_dy = 0
        self.player_g  =0
        self.player_mx = 0
        self.player_my = 0
        self.scroll_x = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        #タイトルイベント取得
        if self.state == flag.title:
            if pyxel.btn(pyxel.KEY_SPACE):
                self.state = flag.ground
        #プレイイベント取得        
        elif self.state == flag.ground or flag.air:
            if pyxel.btn(pyxel.KEY_D):
                self.player_dx = 1.3
                self.player_mx = 0
            elif pyxel.btn(pyxel.KEY_A):
                self.player_dx = -1.3
                self.player_mx = 1
            if pyxel.btnr(pyxel.KEY_D) or pyxel.btnr(pyxel.KEY_A):
                self.player_dx = 0
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.player_dy = -2
                self.player_g =0.2
                self.state = flag.air
        #移動計算
        self.player_x += self.player_dx
        self.player_y += self.player_dy
        self.player_dy += self.player_g
        if self.player_dy > 1:
            self.player_dy = 1
            self.player_g = 0
        if self.state == flag.air and self.player_y > 88:
            self.player_y = 88
            self.player_dy = 0
            self.state = flag.ground
    def draw(self):
        pyxel.cls(0)
        #タイトル画面
        if self.state == flag.title:
            pyxel.bltm(0,0,1,0,0,240,120,8)
            if pyxel.frame_count%30 < 15:
                pyxel.text(90,80,"Space to start",7)
        #プレイ画面
        elif self.state == flag.ground or self.state == flag.air:
            pyxel.bltm(0,0,2,self.scroll_x,0,240,120,0)
        #地面時
            if self.state == flag.ground:
                if self.player_dx != 0:
                    if 0 <=pyxel.frame_count%15 <5:
                        self.player_my = 0
                    elif 5 <=pyxel.frame_count%15 <10:
                        self.player_my = 1
                    elif 10 <=pyxel.frame_count%15 <15:
                        self.player_my = 2
                else:
                    self.player_my = 0
                pyxel.blt(self.player_x,self.player_y,0,16*(self.player_mx),16*(self.player_my),16,16,7)
        #空中時
            elif self.state == flag.air:
                self.player_my = 3
                pyxel.blt(self.player_x,self.player_y,0,24*(self.player_mx),16*(self.player_my),24,24,7)
            
App()