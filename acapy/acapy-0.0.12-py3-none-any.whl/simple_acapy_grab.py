import sys

import cv2
import acapy

# AcaPyクラスのインスタンス
capture = acapy.AcaPy()

if capture.is_opened == False:
    # キャプチャボードが見つからないときは終了
    del(capture)
    sys.exit(0)

# iniファイル（カメラ設定ファイル）の読込
#capture.load_inifile("./AreaSensor_color.ini")
capture.load_inifile("./AreaSensor_mono.ini")

# grab(連続画像取込)の開始
capture.grab_start()

while(True):
    
    # 前回のフレームの次から今回のフレームまでを取得
    ret, frames, count, frame_no = capture.read_frames()# カラーのときはBGR(OpenCVのMatと互換)
    if ret != acapy.AcaPy.OK:
        # リングバッファが上書きされたとき
        print("Frame dropped")
    # 最後に取得した画像を表示
    cv2.imshow ("Image", frames[count - 1] )

    if cv2.waitKey(1) > 0:
        # キー入力待ち
        break

# grab(連続画像取込)の停止
capture.grab_stop()

cv2.destroyAllWindows()