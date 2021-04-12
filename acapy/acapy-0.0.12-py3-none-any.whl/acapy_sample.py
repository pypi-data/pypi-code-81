import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image
import sys
import time

import acapy
from acapy import graphicsbox

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)

        self.master.title("AcaPy(AcapLib2 Python wrapper) Sample")     # ウィンドウタイトル
        self.master.geometry("600x400")                 # ウィンドウサイズ(幅x高さ)

        # ウィンドウ画面の生成
        self.initialize_component()

         #AcaPyの初期化
        self.init_acapy()  

        self.last_disp_image = np.array([])

    def __del__(self):
        # AcaPyの解放
        del(self.capture)

    def initialize_component(self):
        '''ウィンドウ画面の生成'''

        # メニューの追加
        self.menubar = tk.Menu(self)
        self.menubar.add_command(label= "BoadName")
        self.menubar.add_command(label= "Snap",         command = self.snap_click)
        self.menubar.add_command(label= "Grab",         command = self.grab_click)
        self.menubar.add_command(label= "Image Save",   command = self.save_click)
        self.master.config(menu = self.menubar)

        # ステータスバー
        frame_statusbar = tk.Frame(self.master, relief = tk.SUNKEN, bd = 2)
        self.label_framerate = tk.StringVar(value = "--ms/--fps")
        label = tk.Label(frame_statusbar, textvariable = self.label_framerate)
        label.pack(side = tk.RIGHT)
        frame_statusbar.pack(side = tk.BOTTOM, fill = tk.X)

        # GraphicsBoxの追加(オプション設定はtkinterのCanvasクラスと同じ)
        self.graphics = graphicsbox.GraphicsBox(self.master, bg = "dark cyan")
        self.graphics.pack(expand = True, fill = tk.BOTH)
        self.graphics.profile_enabled = True # プロファイル表示を有効にする（初期値は無効）

    def init_acapy(self):
        ''' AcaPyの初期化'''

        # AcaPyのインスタンス
        self.capture = acapy.AcaPy()

        if self.capture.is_opened == False:
            # キャプチャボードが見つからないときは終了
            print("Cannot open board")
            del(self.capture)
            sys.exit(0)

        print(f"Handle = {self.capture.handle}")
        print(f"BoardName = {self.capture.board_name}")
        print(f"BoardID = {self.capture.board_id}")
        print(f"Ch = {self.capture.ch}")

        # メニューにボード名の表示
        self.menubar.entryconfigure(1, label = f"{self.capture.board_name.decode('utf-8')} Ch{self.capture.ch}")

        # iniファイルの読込
        inifilename = filedialog.askopenfilename(
		    title = "Open initial file",
		    filetypes = [("initial file", ".ini")], # ファイルフィルタ
		    initialdir = "./" # 自分自身のディレクトリ
		    )

        if len(inifilename) == 0:
            print("Open inifile error")
            return

        # イニシャルファイルの読込
        self.capture.load_inifile(inifilename)

        # リングバッファの面数を指定（プログラムで変更する場合、イニシャルファイルにも設定がある）
        #self.capture.mem_num = 4
        
    def snap_click(self):
        '''Snap:1画面取込(連続取込をする場合はGrabを使用のこと)'''

        ret, frame = self.capture.snap() # カラーのときはBGR（OpenCVのMat互換）

        # カラーの場合、BGRをRGBに変換される
        frame = self.capture.bgr2rgb(frame)

        self.graphics.draw_image(frame)
        self.last_disp_image = frame

        self.graphics.focus()

    def grab(self, update_time):
        # 前回のフレーム番号の次から、現在のフレーム番号までの画像を取得する
        ret, frames, count, frame_no = self.capture.read_frames() # カラーのときはBGR

        # フレームレート計測
        if (frame_no % 10 == 0):
            current_time = time.perf_counter() # 現在の経過時間
            fps = (frame_no - self.last_time_frame) / (current_time - self.last_time)
            self.label_framerate.set(f"Frame count:{frame_no} / {1000.0/fps:.2f}ms / {fps:.2f}fps")
            self.last_time = current_time
            self.last_time_frame = frame_no

        # 前回のフレーム番号から今回のフレーム番号までの差がmem_num以上の場合は、全ての画像の処理ができない
        # iniファイルのUSER_MEMORY_NUMの値を大きくするかupdate_timeを小さくすること
        if ret != acapy.AcaPy.OK:
            print("Frame dropped")
            #self.last_frame_no = frame - 1

        image = None

        # 前回のフレーム番号の次から、現在のフレーム番号までを処理する
        for i in range(count):
            image = frames[i] # 画像データ(ndarray、OpenCVのMatと同等)
            # カラーの場合、BGRをRGBに変換される
            image = self.capture.bgr2rgb(image)

            ###########################################
            # 画像処理する場合はここで、imageを処理する
            ###########################################


        # 最後に取得した画像の描画
        self.graphics.draw_image(image)
        self.last_disp_image = image

        # grabメソッドの繰り返し
        self.grab_id = self.master.after(update_time, self.grab, update_time)

    def grab_click(self):
        '''Grab:連続画面取込'''

        if (self.capture.is_grab == False):
            # Grab中ではないとき

            # 画像取込開始
            self.capture.grab_start()

            # 連続画像取込
            self.last_frame_no = 0
            self.last_time = 0          # フレームレート計算用
            self.last_time_frame = 0    # フレームレート計算用

            # メニューの文字を変更
            self.menubar.entryconfigure(3, label = "Stop")
            # メニューを無効にする
            self.menubar.entryconfigure(2, state="disabled")
            self.menubar.entryconfigure(4, state="disabled")

            # Grabの開始（10msec間隔でフレーム画像を確認する、時間を短くするとGUIが遅くなる）
            self.grab(10)
        else:
            # Grab中のとき
            self.master.after_cancel(self.grab_id)

            # 画像取込停止
            self.capture.grab_stop()
            # メニューの文字を変更
            self.menubar.entryconfigure(3, label = "Grab")
            # メニューを有効にする
            self.menubar.entryconfigure(2, state="normal")
            self.menubar.entryconfigure(4, state="normal")

    def save_click(self):
        '''名前を付けて最後に表示した画像を保存'''
        if self.last_disp_image.size == 0:
            return

        filename = filedialog.asksaveasfilename(
            title = "画像ファイルを開く",
            filetypes = [("Bitmap", ".bmp"), ("PNG", ".png"), ("JPEG", ".jpg"), ("Tiff", ".tif") ], # ファイルフィルタ
            initialdir = "./", # 初期に開かれるディレクトリ（自分自身のディレクトリ）
            defaultextension = "bmp"
            )
        # ファイル名の指定が無いとき
        if len(filename) == 0:
            return
        # ndarrayをPILに変換して保存
        Image.fromarray(self.last_disp_image).save(filename)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()




