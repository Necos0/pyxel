import pyxel
from enum import Enum
#状態の設定
class flag(Enum):
    title  = 0
    ground = 1
    air    = 2 
    vacuum = 3


class App:
    #初期化
    def __init__(self):
        pyxel.init(240, 120)
        pyxel.load("k.pyxres")
        self.state = flag.title
        self.player_x = 35
        self.player_y = 88
        self.player_dx = 0
        self.player_dy = 0
        self.player_g  =0
        self.player_dir = 1
        self.player_my = 0
        self.scroll_x = 0
        self.time = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        #タイトルイベント取得
        if self.state == flag.title:
            if pyxel.btn(pyxel.KEY_SPACE):
                self.state = flag.ground
        #プレイイベント取得        
        elif self.state == flag.ground or self.state == flag.air:
            if pyxel.btnp(pyxel.KEY_W):
                self.state = flag.vacuum
            if pyxel.btn(pyxel.KEY_A):
                if self.player_dx > -1.5:
                    self.player_dx -= 0.3
                self.player_dir = -1
            if pyxel.btn(pyxel.KEY_D):
                if self.player_dx < 1.5:
                    self.player_dx += 0.3
                self.player_dir = 1
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.player_dy = -2
                self.player_g =0.2
                self.time = pyxel.frame_count
                self.state = flag.air
            if pyxel.btnr(pyxel.KEY_D) or pyxel.btnr(pyxel.KEY_A):
                self.player_dx = 0
        elif self.state==flag.vacuum:
            self.player_dx = self.player_dx*0.7
            if pyxel.btnr(pyxel.KEY_W):
                if self.player_dy == 0:
                    self.state = flag.ground
                else:
                    self.state = flag.air
        #移動計算
        self.player_x += self.player_dx
        self.player_y += self.player_dy
        self.player_dy += self.player_g
        if self.player_dy > 1.3:
            self.player_dy = 1.3
            self.player_g = 0
        #当たり判定
        if self.player_x < 0:
            self.player_x = 0
        if self.player_y < 0:
            self.player_y = 0
        if (self.state == flag.air or self.state == flag.vacuum) and self.player_y > 88:
            self.player_y = 88
            self.player_dy = 0
            if self.state == flag.air:
                self.state = flag.ground
        #スクロール判定
        if self.player_x > self.scroll_x + 120:
            self.scroll_x = self.player_x -120
        if self.player_x < self.scroll_x + 20:
            self.scroll_x = self.player_x -20
        if self.scroll_x < 0:
            self.scroll_x = 0
    def draw(self):
        pyxel.cls(0)
        #タイトル画面
        if self.state == flag.title:
            pyxel.bltm(0,0,1,0,0,240,120)
            if pyxel.frame_count%30 < 15:
                pyxel.text(90,80,"Space to start",7)
        #プレイ画面
        else:
            pyxel.camera(self.scroll_x,0)
            pyxel.bltm(self.scroll_x,0,2,(self.scroll_x)%240,0,240,120)
            
        #地面時
            if self.state == flag.ground:
                if abs(self.player_dx - 0)>0.01:
                    if 0 <=pyxel.frame_count%15 <5:
                        self.player_my = 0
                    elif 5 <=pyxel.frame_count%15 <10:
                        self.player_my = 1
                    elif 10 <=pyxel.frame_count%15 <15:
                        self.player_my = 2
                else:
                    self.player_my = 0
                pyxel.blt(self.player_x,self.player_y,0,0,16*(self.player_my),16*self.player_dir,16,7)
        #空中時
            elif self.state == flag.air:
                if self.time + 5 > pyxel.frame_count:
                    self.player_my = 4.5
                else:
                    self.player_my = 3
                pyxel.blt(self.player_x,self.player_y,0,0,16*(self.player_my),24*self.player_dir,24,7)
        #吸い込み時
            elif self.state == flag.vacuum:
                self.player_my = 6
                pyxel.blt(self.player_x,self.player_y-8,0,0,16*(self.player_my),16*self.player_dir,24,7)
App()