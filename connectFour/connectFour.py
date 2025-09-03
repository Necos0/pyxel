import pyxel

COLS = 7
ROWS = 6
CELL = 20
MARGIN = 10
WINDOW_W = 160
WiNDOW_H = 256
BOARD_W = CELL * COLS
BOARD_H = CELL * ROWS
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2
IN_A_ROW = 4

#リセットボタン
BTN_W = 60
BTN_H = 14
BTN_X = 2 * MARGIN
BTN_Y = 4 * MARGIN + BOARD_H


class App:
    def __init__(self):
        pyxel.init(WINDOW_W, WiNDOW_H)
        pyxel.mouse(True)
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = PLAYER1
        self.message = ""
        self.is_playing = True
        print(self.board)
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.is_playing:
            for i in range(COLS):
                    if pyxel.btnp(pyxel.KEY_1 + i):
                        self.place_piece(i)

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):

                if self.is_inside_board( pyxel.mouse_x, pyxel.mouse_y):
                    col = self.screen_to_col(pyxel.mouse_x)
                    self.place_piece(col)
        
        # Rキーならどこでも即リセット
        if pyxel.btnp(pyxel.KEY_R):
            self.reset()
            return

        # 左クリック時の処理
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            if self.is_inside_reset(mx, my):
                self.reset()


    def draw(self):
        pyxel.cls(0)
        self.draw_board()
        self.draw_pieces()
        self.draw_reset_button()
        pyxel.text(4 * MARGIN ,  2 * MARGIN + BOARD_H, self.message, 7)

#描画
    def draw_board(self):
        for col in range(COLS + 1):
            x = col * CELL + MARGIN
            y0 = MARGIN
            y1 = MARGIN + BOARD_H
            pyxel.line(x,y0,x,y1,1)

        for row in range(ROWS + 1):
            x0 = MARGIN
            x1 = MARGIN + BOARD_W
            y = row * CELL + MARGIN
            pyxel.line(x0,y,x1,y,1)
    def draw_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                x0 = col * CELL + MARGIN
                y0 = row * CELL + MARGIN
                x = x0 + CELL // 2
                y = y0 + CELL // 2
                if self.board[row][col] == EMPTY:
                    continue
                elif self.board[row][col] == PLAYER1:
                    pyxel.circ(x,y,5,8)
                elif self.board[row][col] == PLAYER2:
                    pyxel.circ(x,y,5,5)
    def draw_reset_button(self):
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        hover = self.is_inside_reset(mx, my)
        fill = 11 if hover else 6  # ホバーで少し明るく
        pyxel.rect(BTN_X, BTN_Y, BTN_W, BTN_H, fill)
        pyxel.rectb(BTN_X, BTN_Y, BTN_W, BTN_H, 7)
        label = "RESET"
        tx = BTN_X + (BTN_W - len(label) * 4) // 2
        ty = BTN_Y + (BTN_H - 6) // 2
        pyxel.text(tx, ty, label, 0)

#コマ配置
    def place_piece(self, col):

        if col < 0 or col >= COLS:
            return

        for row in reversed(range(ROWS)):  # 下から上に向かってチェック
            if self.board[row][col] == EMPTY:
                #コマを配置
                self.board[row][col] = self.current_player
                #勝利判定
                if self.is_connect4(row,col,self.current_player):
                    self.message = f"PLAYER{self.current_player} WIN!!"
                    self.is_playing = False
                elif self.is_board_full():
                    self.message = "Game was even..."
                    self.is_playing = False
                break
         # プレイヤー交代
        self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1
        
#リセット
    def reset(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = PLAYER1
        self.is_playing = True
        self.message = ""
    def is_inside_reset(self, x: int, y: int) -> bool:
            return (BTN_X <= x < BTN_X + BTN_W) and (BTN_Y <= y < BTN_Y + BTN_H)
#勝利判定
    def is_connect4(self, r: int, c: int, player: int) -> bool:
        # 4方向（横・縦・斜め2種）でチェック
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
            total = self.count_line(r, c, dr, dc, player) + self.count_line(r, c, -dr, -dc, player) - 1
            if total >= IN_A_ROW:
                return True
        return False
    def count_line(self, r: int, c: int, dr: int, dc: int, player: int) -> int:
        """(r,c) を起点に (dr,dc) 方向へ同じ駒が続く数を数える（起点を含む）。"""
        cnt = 0
        rr, cc = r, c
        while 0 <= rr < ROWS and 0 <= cc < COLS and self.board[rr][cc] == player:
            cnt += 1
            rr += dr
            cc += dc
        return cnt
    
      # ------------ 引き分け判定 ------------
    def is_board_full(self) -> bool:
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] == EMPTY:
                    return False
        return True
#クリック判定
    def is_inside_board(self, x: int, y: int) -> bool:
     return (MARGIN <= x < MARGIN + BOARD_W) and (MARGIN <= y < MARGIN + BOARD_H)
    def screen_to_col(self, x: int) -> int:
        return (x - MARGIN) // CELL

        
App()