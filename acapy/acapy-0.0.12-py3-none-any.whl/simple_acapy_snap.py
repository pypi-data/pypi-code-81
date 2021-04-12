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
capture.load_inifile("./AreaSensor_color.ini")
#capture.load_inifile("./AreaSensor_mono.ini")

while(True):
    # 画像を１枚取得
    ret, frame = capture.snap() # カラーのときはBGR(OpenCVのMatと互換)
    # 画像の表示
    cv2.imshow ("Image", frame )

    if cv2.waitKey(1) > 0:
        # キー入力待ち
        break

cv2.destroyAllWindows()

