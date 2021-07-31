import tkinter as tk
import math
import random
from tkinter import messagebox

canvas = None
cells = []
open_cells = []
Flag = "★"
BOM = -1
bom = 2


SQUARE_LENGTH = 30
RADIUS = SQUARE_LENGTH / 2 - 5
POSITION = {"x": 8, "y": 8}
BORDER_WIDTH = 2
NUMBER = 5
LENGTH = SQUARE_LENGTH * NUMBER + BORDER_WIDTH * NUMBER
#四角の盤
def set_field():
  global cells
  global open_cells
  canvas.create_rectangle(POSITION["x"], POSITION["y"], LENGTH + POSITION["x"], LENGTH + POSITION["y"], fill='#aaa', width=BORDER_WIDTH)
  #マス目と線
  for i in range(NUMBER - 1):
    x = POSITION["x"] + SQUARE_LENGTH * (i + 1) + BORDER_WIDTH * i + BORDER_WIDTH
    y = POSITION["y"] + SQUARE_LENGTH * (i + 1) + BORDER_WIDTH * i + BORDER_WIDTH
    canvas.create_line(x, POSITION["y"], x, LENGTH + POSITION["y"], width=BORDER_WIDTH)
    canvas.create_line(POSITION["x"], y, LENGTH + POSITION["x"], y, width=BORDER_WIDTH)
  cells = [[0] * NUMBER for i in range(NUMBER)] 
  open_cells = [[0] * NUMBER for i in range(NUMBER)]

#地雷、旗、数字の描画
def set_item(kind, x, y):
  center_x = POSITION["x"] + BORDER_WIDTH * x + BORDER_WIDTH / 2 + SQUARE_LENGTH * x + SQUARE_LENGTH / 2
  center_y = POSITION["y"] + BORDER_WIDTH * y + BORDER_WIDTH / 2 + SQUARE_LENGTH * y + SQUARE_LENGTH / 2

  canvas.create_rectangle(center_x - SQUARE_LENGTH / 2, center_y - SQUARE_LENGTH / 2, center_x + SQUARE_LENGTH / 2, center_y + SQUARE_LENGTH / 2, fill="#fff", width=0)

  if cells[x][y] == BOM:
      canvas.create_oval(center_x - RADIUS, center_y - RADIUS, center_x + RADIUS, center_y + RADIUS, fill="#f00", width=0)
  elif cells[x][y] != 0:
      canvas.create_text(center_x, center_y, text=cells[x][y], justify="center", font=("", 25), tag="count_text")
  if kind == Flag:
    canvas.create_rectangle(center_x - SQUARE_LENGTH / 2, center_y - SQUARE_LENGTH / 2, center_x + SQUARE_LENGTH / 2, center_y + SQUARE_LENGTH / 2, fill="#984ea3", width=0)
    cells[x][y] = "★"
    canvas.create_text(center_x, center_y, text=kind,justify="center", font=("", 25), tag="F")
  #開示されたマス
  open_cells[x][y] = 1

# すべてのマスを開く
def all_open(x,y):
  center_x = POSITION["x"] + BORDER_WIDTH * x + BORDER_WIDTH / 2 + SQUARE_LENGTH * x + SQUARE_LENGTH / 2
  center_y = POSITION["y"] + BORDER_WIDTH * y + BORDER_WIDTH / 2 + SQUARE_LENGTH * y + SQUARE_LENGTH / 2

  canvas.create_rectangle(center_x - SQUARE_LENGTH / 2, center_y - SQUARE_LENGTH / 2, center_x + SQUARE_LENGTH / 2, center_y + SQUARE_LENGTH / 2, fill="#fff", width=0)

  if cells[x][y] == BOM:
    canvas.create_oval(center_x - RADIUS, center_y - RADIUS, center_x + RADIUS, center_y + RADIUS, fill="#f00", width=0)
  elif cells[x][y] != 0:
    canvas.create_text(center_x, center_y, text=cells[x][y], justify="center", font=("", 25), tag="count_text")
  if cells[x][y] == "F":
    canvas.create_rectangle(center_x - SQUARE_LENGTH / 2, center_y - SQUARE_LENGTH / 2, center_x + SQUARE_LENGTH / 2, center_y + SQUARE_LENGTH / 2, fill="#fff", width=0)
    canvas.create_oval(center_x - RADIUS, center_y - RADIUS, center_x + RADIUS, center_y + RADIUS, fill="#f00", width=0)
# 地雷を設置
def bom_set():
  count = 0
  while True:
    x = random.randint(0, NUMBER - 1)
    y = random.randint(0, NUMBER - 1)

    if cells[x][y] != BOM:
      cells[x][y] = BOM
      count += 1
    
    if count == bom:
      break

#クリックされた場所に地雷があるかどうか判定する
def is_item(x,y):
  if cells[x][y] == BOM:
    return True 
  else:
    return False

#ゲーム終了時のメッセージ
def game_over():
  messagebox.showinfo('Game Over', '爆弾を選択したのでゲーム終了です。')

#ゲームクリア時のメッセージ
def game_clear():
  messagebox.showinfo('Game Clear', '地雷をすべて当てました。\nゲーム終了です。')

#地雷が20x20のマス目に地雷が残っているかを確認する
def is_item_right():
  bomFlag = False
  for i in cells:
    if -1 in i:
      bomFlag = True
  return bomFlag
#中心座標を求める
def point_to_numbers(event_x, event_y):
    x = math.floor((event_x - POSITION["x"]) / (SQUARE_LENGTH + BORDER_WIDTH))
    y = math.floor((event_y - POSITION["y"]) / (SQUARE_LENGTH + BORDER_WIDTH))
    return x, y
#キャンバスを作る
def create_canvas():
  root = tk.Tk()
  root.geometry(f"""{LENGTH + POSITION["x"] * 2}x{LENGTH + POSITION["y"] * 2}""")
  root.title("マインスイーパー")
  canvas = tk.Canvas(root, width=(LENGTH + POSITION["x"]), height=(LENGTH + POSITION["y"]))
  canvas.place(x=0, y=0)

  return root, canvas
#右クリック
def right_click(event):
  x, y = point_to_numbers(event.x, event.y)
  set_item(Flag, x, y)
  bom_flag = is_item_right()

  if not bom_flag:
    for x in range(NUMBER):
      for y in range(NUMBER):
        all_open(x, y)
    game_clear()
    
# 左クリック
def left_click(event):
  x, y = point_to_numbers(event.x, event.y)
  if not open_cells[x][y] == 1:
    set_item(None, x, y)
    bom_flag = is_item(x, y)

    if bom_flag:
      for i in range(NUMBER):
        for j in range(NUMBER):
          all_open(i, j)
      game_over()
    # 周りも開けられるかどうか
    if cells[x][y] == 0:
      open_neighbor(x - 1, y - 1)
      open_neighbor(x, y - 1)
      open_neighbor(x + 1, y - 1)
      open_neighbor(x - 1, y)
      open_neighbor(x + 1, y)
      open_neighbor(x - 1, y + 1)
      open_neighbor(x, y + 1)
      open_neighbor(x + 1, y + 1)

# 周りに地雷が何個あるかセット
def neighboring_boms_num():
  for j in range(NUMBER):
    for i in range(NUMBER):
      if cells[j][i] == BOM:
        continue
      count = 0

      #８方向の地雷をカウント
      for y in range(-1,2):
        for x in range(-1,2):
          if y != 0 or x != 0:
            bomFlag = is_bom(i + x, j + y)

            if bomFlag:
              count += 1
      cells[j][i] = count
#地雷があるかどうか判断
def is_bom(i,j):
  #ボード内座標チェック
  if j >= 0 and i >= 0 and j < NUMBER and i < NUMBER:
    if cells[j][i] == BOM:
      #座標に爆弾があればTrue
      return True
  else:
    #ボード外もしくは地雷でない場合はFalse
    return False

def open_neighbor(i,j):
  if not (j >= 0 and i >= 0 and j < NUMBER and i < NUMBER):
    return
  if cells[i][j] == BOM:
    return
  if open_cells[i][j] == 1:
    return
  set_item(None, i, j)
  
  if cells[i][j] == 0:
    open_neighbor(i - 1, j - 1)
    open_neighbor(i, j - 1)
    open_neighbor(i + 1, j - 1)
    open_neighbor(i - 1, j)
    open_neighbor(i + 1, j)
    open_neighbor(i - 1, j + 1)
    open_neighbor(i, j + 1)
    open_neighbor(i + 1, j + 1)

def play():
  global canvas
  root, canvas = create_canvas()
  set_field()
  bom_set()
  neighboring_boms_num()
  canvas.bind("<Button-1>", lambda event: left_click(event)) #左クリック
  canvas.bind("<Button-2>", lambda event: right_click(event)) #右クリック
  root.mainloop()

play()

