import random
import copy
import math
from tkinter import *

# Space押したら新しく生成
# 常時描画するもの 枠
# 更新時変わるもの　数字
# 

class Window(Frame):
    def __init__(self):
        self.win = Tk()
        self.win.title("Sudoku Generator")
        self.win.geometry("300x300")
        self.win.resizable(width=False, height=False)
        self.win.configure(bg="white")
        super().__init__(self.win)
        self.canvas = Canvas(self.win, bg="white", height = 300, width = 300)
        self.labels = [[Label(background="white",font=("MSゴシック", "10", "bold")) for i in range(9)] for j in range(9)]
        for i in range(9):
            for j in range(9):
                self.labels[i][j].place(x=27+30*j,y=17+30*i)
        self.generate()
        self.update()

    def update(self):
        self.draw()
        self.win.after(50,self.update)

    def draw(self):
        for i in range(10):
            self.canvas.create_line(20,10+30*i,290,10+30*i,fill='black')
            self.canvas.create_line(20+i*30,10,20+i*30,280,fill='black')
        self.canvas.pack()
        for i in range(9):
            for j in range(9):
                if self.ge.gearr[i][j] != 0:
                    self.labels[i][j]["text"] = str(self.ge.gearr[i][j])

    def delete(self):
        pass

    def generate(self):
        self.ge = Generate(55)
        self.ge.print_gearr()
        # self.ge.gearrに数独が生成された

class Sudoku():

    def __init__(self,arr):
        # 枠の大きさ.固定しているが2*2などサイズを変えたい時用
        self.n = 9
        self.arr = arr

    def solve(self,x,y): # x,yは0を入れる
        if y > self.n-1:
            return True
        elif x > self.n-1:
            if self.solve(0,y+1):
                return True
            else:
                return False
        elif self.arr[y][x] != 0:
            if self.solve(x+1,y): # x > 8は上で弾いているのでこの形でスキップ
                return True
            else:
                return False
        else:
            l = [i for  i in range(1,10)]
            random.shuffle(l) # こうすることで全ての組合せを作ることができる
            for i in l:
            #for i in range(1,self.n+1):
                if self.check_v(x,i) and self.check_h(y,i) and self.check_s(x,y,i):
                    self.arr[y][x] = i
                    if self.solve(x+1,y):
                        return True
        self.arr[y][x] = 0 # 上のfor文で誤ったものを訂正
        return False

    def check_v(self,x,n): # 縦に同じ数字がないか調べる
        for i in range(self.n):
            if self.arr[i][x] == n:
                return False
        return True
    
    def check_h(self,y,n): # 横に同じ数字がないか調べる
        for i in range(self.n):
            if self.arr[y][i] == n:
                return False
        return True

    def check_s(self,x,y,n): # 正方形に同じ数字がないか調べる
        ms = int(math.sqrt(self.n))
        for i in range(ms):
            for j in range(ms):
                if self.arr[(y//ms)*ms+i][(x//ms)*ms+j] == n:
                    return False
        return True

    def print_arr(self): # 数独を埋め表示する
        self.solve(0,0)
        for i in range(self.n):
            print(self.arr[i])

# こちらは計算時間を考慮して3×3マスしか対応していない
class Generate(Sudoku):
    
    def __init__(self,diff):
        self.gearr = [[0 for i in range(9)] for j in range(9)]
        self.diff = diff # 60以上は重いので60以下推奨
    
    # 上三行を埋める安易な関数
    def per(self):
        a = [] # 1つめのブロック
        b = [] # 2つめのブロック
        c = [] # 3つめのブロック
        num = [i for i in range(1,10)]
        random.shuffle(num)
        for i in range(9):
            self.gearr[0][i] = num[i]
            if i < 3:
                a.append(num[i])
            elif i < 6:
                b.append(num[i])
            else:
                c.append(num[i])
        random.shuffle(num)
        for i in range(3):
            for j in range(3,9):
                if num[i] in a and not(num[j] in a):
                    num[i],num[j] = num[j],num[i]
        for i in range(3,6):
            for j in range(9):
                if j <= 5 and j >= 3:
                    continue
                if num[i] in b and not(num[j] in b):
                    num[i],num[j] = num[j],num[i]
        for i in range(6,9):
            for j in range(6):
                if num[i] in c and not(num[j] in c):
                    num[i],num[j] = num[j],num[i]
        for i in range(9):
            self.gearr[1][i] = num[i]
            if i < 3:
                a.append(num[i])
            elif i < 6:
                b.append(num[i])
            else:
                c.append(num[i])
        random.shuffle(num)
        for i in range(9):
            if not(num[i] in a) and len(a) < 9:
                a.append(num[i])
            elif not(num[i] in b) and len(b) < 9:
                b.append(num[i])
            else:
                c.append(num[i])
        for i in range(3):
            self.gearr[2][i] = a[6+i]
        for i in range(3):
            self.gearr[2][3+i] = b[6+i]
        for i in range(3):
            self.gearr[2][6+i] = c[6+i]

    # 数字を消す関数
    def del_num(self):
        list_num = [i for i in range(81)]
        random.shuffle(list_num)
        for i in range(55): # ここの数字で難易度を調整
            tmp = copy.deepcopy(self.gearr) # 多次元リストの場合deepcopyで値受け渡し
            flag = True
            for j in range(1,10):
                if j == tmp[list_num[i]//9][list_num[i]%9]:
                    continue
                self.gearr[list_num[i]//9][list_num[i]%9] = 0
                super().__init__(self.gearr)
                if super().check_h(list_num[i]//9,j) and super().check_v(list_num[i]%9,j) and super().check_s(list_num[i]%9,list_num[i]//9,j):
                    self.gearr[list_num[i]//9][list_num[i]%9] = j
                    if super().solve(0,0): # Trueなら下の数字以外を挿入しても大丈夫なので0にしてしまうと一意性を保証できない
                        flag = False
                self.gearr = copy.deepcopy(tmp)
            if flag:
                self.gearr[list_num[i]//9][list_num[i]%9] = 0

    def print_gearr(self):
        self.per()
        super().__init__(self.gearr)
        super().solve(0,0)
        self.del_num()
        """for i in range(9):
            print(self.gearr[i])
        """

if __name__ == "__main__":
    app = Window()
    app.win.mainloop()