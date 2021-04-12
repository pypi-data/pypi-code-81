# ************************************************************************************************
#
#   Image Capture Library   ---  Avaldata Capture Library 2
#
#
#   Copyright (c) 2008-2014 AVAL DATA Corporation All Right Reserved.
#
# ************************************************************************************************

# AcapLib2のPython用定義ファイル
# C言語用ヘッダファイル(AcapLib2.h)からの置き換え

# pylint: disable=W0311
# pylint: disable=W0614

import numpy as np
from ctypes import *
import ctypes
import platform

__version__ = "0.0.12"

'''
////////////////////////////////////////////////////////////
//  Ver.0.0.12  (2021.04.12) 
////////////////////////////////////////////////////////////
●プレリリース版
'''

_os_name = platform.system()

if _os_name == 'Windows':
	_acap = ctypes.WinDLL('AcapLib2')	# Windows
elif _os_name == 'Linux':
	_acap = np.ctypeslib.load_library('libAcap2.so','/usr/lib')		# Linux
else:
	#_acap = None
	raise NotImplementedError()

def to_string_buffer(string):
	if string is None:
		return None
	if _os_name == 'Windows':
		enc_str = string.encode('cp932')	# Windows
	elif _os_name == 'Linux':
		enc_str = string.encode('utf-8')	# Linux
	else:
		return ACL_INITIALIZE_ERROR

	return ctypes.create_string_buffer(enc_str)

def bgr2rgb(bgr_image):
	'''カラー画のとき、データの順番をBGRからRGBへ変更する'''
	if len(bgr_image.shape) >= 3:
		# カラーの場合、BGRをRGBに変換する
		rgb_image = bgr_image[...,::-1] # RGBへ変換
		return rgb_image
	else:
		return bgr_image

# ******************************************************************
# 	定数定義
# ******************************************************************
INVALID_HANDLE_VALUE		= -1

MAX_BOARD					= 8					# ボードの最大数
MAX_BOARD_256				= 256				# ボードの最大数拡張
MAX_BOARD_NAME				= 16

ACL_INT_GRABSTART			= 0x00000001		# 画像入力開始割り込み
ACL_INT_FRAMEEND			= 0x00000002		# フレーム確定割り込み
ACL_INT_GRABEND				= 0x00000004		# 画像入力終了割り込み
#ACL_INT_GPIO_1			= 0x00000040		# GPIO割り込み 1
#ACL_INT_GPIO_2			= 0x00000080		# GPIO割り込み 2
ACL_INT_GPIN				= 0x00000100		# GPIN割り込み (Ver 4.0.0新規)
ACL_INT_OVERFLOW			= 0x00000400		# バッファオーバーフロー
ACL_INT_TIMEOUT				= 0x00000800		# タイムアウト
ACL_INT_ABORT				= 0x00008000		# イベント待ち、強制解除

#pragma deprecated(ACL_INT_CXP_LINK_DETECT)
ACL_INT_CXP_LINK_DETECT		= 0x00010000		# Ch=1でIN-1のリンク検出
#pragma deprecated(ACL_INT_CXP_LINK_UNDETECT)
ACL_INT_CXP_LINK_UNDETECT	= 0x00020000		# Ch=1でIN-1のリンクロスト
#pragma deprecated(ACL_INT_CXP_POWER_ERR)
ACL_INT_CXP_POWER_ERR		= 0x00100000		# 電源エラー割込(IN-1とIN-2一緒)
#pragma deprecated(ACL_INT_CXP_FIFO_ERR)
ACL_INT_CXP_FIFO_ERR		= 0x00001000		# FIFOエラー発生割込

ACL_FILE_READ				= (0)
ACL_FILE_WRITE				= (1)

# 新・外部トリガ設定用定義 (Ver 4.0.0)
ACL_EXTRG_DISABLE			= (0)
ACL_EXTRG_TTL_1				= (1 <<  0)
ACL_EXTRG_TTL_2				= (1 <<  1)
ACL_EXTRG_TTL_3				= (1 <<  2)
ACL_EXTRG_TTL_4				= (1 <<  3)
ACL_EXTRG_RS422_1			= (1 <<  4)
ACL_EXTRG_RS422_2			= (1 <<  5)
ACL_EXTRG_RS422_3			= (1 <<  6)
ACL_EXTRG_RS422_4			= (1 <<  7)
ACL_EXTRG_OPT_1				= (1 <<  8)
ACL_EXTRG_OPT_2				= (1 <<  9)
ACL_EXTRG_OPT_3				= (1 << 10)
ACL_EXTRG_OPT_4				= (1 << 11)
ACL_EXTRG_MASK				= (0xFFF)

# 新・外部トリガ設定用定義追加 (Ver 6.8.0)
ACL_EXTRG_TTL_5				= (1 << 12)
ACL_EXTRG_TTL_6				= (1 << 13)
ACL_EXTRG_TTL_7				= (1 << 14)
ACL_EXTRG_TTL_8				= (1 << 15)
ACL_EXTRG_RS422_5			= (1 << 16)
ACL_EXTRG_RS422_6			= (1 << 17)
ACL_EXTRG_RS422_7			= (1 << 18)
ACL_EXTRG_RS422_8			= (1 << 19)
ACL_EXTRG_OPT_5				= (1 << 20)
ACL_EXTRG_OPT_6				= (1 << 21)
ACL_EXTRG_OPT_7				= (1 << 22)
ACL_EXTRG_OPT_8				= (1 << 23)
ACL_EXTRG_MASK_EX			= (0xFFFFFF)

ACL_EXT_EN_TTL				= (1)
ACL_EXT_EN_RS422			= (2)
ACL_EXT_EN_DIFF				= (3)
ACL_EXT_EN_OPT				= (4)
ACL_EXT_EN_MULTI			= (5)

ACL_BAYER_DISABLE			= (0)
ACL_BAYER_SOFTWARE			= (1)
ACL_BAYER_HARDWARE			= (2)

ACL_BAYERGRID_BG_GR			= (0)
ACL_BAYERGRID_RG_GB			= (1)
ACL_BAYERGRID_GB_RG			= (2)
ACL_BAYERGRID_GR_BG			= (3)

ACL_BAYER_EDIT_STOP			= (0)
ACL_BAYER_EDIT_R			= (1)
ACL_BAYER_EDIT_G			= (2)
ACL_BAYER_EDIT_B			= (3)

ACL_POWER_ERR_ON				= (1 <<  0)
ACL_POWER_ERR_OFF				= (1 <<  1)

ACL_POWER_ERR_NO_CLK			= (1 <<  4)
ACL_POWER_ERR_LOST_CLK			= (1 <<  5)
ACL_POWER_ERR_CONNECT			= (1 <<  6)
ACL_POWER_ERR_POCL				= (1 <<  7)


# コールバック関数
#typedef void (CALLBACK* EVENT_FUNC)(int,DWORD,int,int);
#typedef void (CALLBACK* EVENT_FUNC_EX)(int,DWORD,int,int,void*);

# ボード種別・枚数構造体
#typedef struct {
#	int nBoardNum;
#	struct {
#		char	pBoardName[MAX_BOARD_NAME];
#		int		nBoardID;
#	}BORADINDEX[MAX_BOARD], BOARDINDEX[MAX_BOARD];
#} ACAPBOARDINFO, *PACAPBOARDINFO;
class BORADINDEX_(Structure):
	_fields_ = [
		("pBoardName",	c_char * MAX_BOARD_NAME ),
		("nBoardID",	c_int)
		]
class ACAPBOARDINFO(Structure):
	_fields_ = [
		("nBoardNum",	c_int),
		("boardIndex",	BORADINDEX_ * MAX_BOARD)
		]

# ボード種別・枚数構造体(Ver.6.2.0)
#typedef struct {
#	int nBoardNum;
#	struct {
#		char	pBoardName[MAX_BOARD_NAME];
#		int		nBoardID;
#		int		nDevice;
#		int		nCustom;
#		int		nChannelNum;
#		int		nFpgaVer;
#		INT64	nSerialNo;
#	}BOARDINDEX[MAX_BOARD];
#} ACAPBOARDINFOEX, *PACAPBOARDINFOEX;
class BORADINDEX(Structure):
	_fields_ = [
		("pBoardName",	c_char * MAX_BOARD_NAME ),
		("nBoardID",	c_int),
		("nDevice",		c_int),
		("nCustom",		c_int),
		("nChannelNum", c_int),
		("nFpgaVer",	c_int),
		("nSerialNo",	c_ulonglong)
		]
class ACAPBOARDINFOEX(Structure):
	_fields_ = [
		("nBoardNum",	c_int),
		("boardIndex",	BORADINDEX * MAX_BOARD)
		]

# ボード種別・枚数構造体(Ver.6.6.0)
#typedef struct {
#	int nBoardNum;
#	struct {
#		char	pBoardName[MAX_BOARD_NAME];
#		int		nBoardID;
#		int		nDevice;
#		int		nCustom;
#		int		nChannelNum;
#		int		nFpgaVer;
#		INT64	nSerialNo;
#	}BOARDINDEX[MAX_BOARD_256];
#} ACAPBOARDINFOEX_256, *PACAPBOARDINFOEX_256;
class ACAPBOARDINFOEX_256(Structure):
	_fields_ = [
		("nBoardNum",	c_int),
		("boardIndex",	BORADINDEX * MAX_BOARD_256)
		]

# エラー情報構造体
#typedef struct {
#	int		nChannel;
#	DWORD	dwCommonErrorCode;
#	DWORD	dwBoardErrorCode;
#	DWORD	dwExtendErrorCode;
#} ACAPERRORINFO, *PACAPERRORINFO;
class ACAPERRORINFO(Structure):
	_fields_ = [
		("nChannel",			c_int),
		("dwCommonErrorCode",	c_ulong),
		("dwBoardErrorCode",	c_ulong),
		("dwExtendErrorCode",	c_ulong)
		]

ACL_MAX_BUFF				= 256

# DMA方法 設定構造体
#typedef struct {
#	void*	pUserBuff[ACL_MAX_BUFF];
#	int		nXSize;
#	int		nYSize;
#	int		nBit;
#	int		nXDivide;
#} ACAPDMAINFO, *PACAPDMAINFO;
class ACAPDMAINFO(Structure):
	_fields_ = [
		("pUserBuff",	c_void_p),
		("nXSize",		c_int),
		("nYSize",		c_int),
		("nBit",		c_int),
		("nXDivide",	c_int)
		]

# カメラリンク設定構造体
#typedef struct {
#	int nArrangeMode;
#	int nCameraBit;
#	int	nBitShift;
#	int nTapNum;
#	int	nHighClip;
#	int nTotalXSize;
#	int nTapDirection[8];
#	int nLineReverse;
#	int nDataMaskLower;
#	int nDataMaskUpper;
#	int nReserve[15];
#} BITASSIGNINFO, *PBITASSIGNINFO;
class BITASSIGNINFO(Structure):
	_fields_ = [
		("nArrangeMode",	c_void_p),
		("nCameraBit",		c_int),
		("nBitShift",		c_int),
		("nTapNum",			c_int),
		("nHighClip",		c_int),
		("nTotalXSize",		c_int),
		("nTapDirection",	c_int * 8),
		("nLineReverse",	c_int),
		("nDataMaskLower",	c_int),
		("nDataMaskUpper",	c_int),
		("nReserve",		c_int * 15)
		]

#typedef struct{
#	void*	pSrcBuff[ACL_MAX_BUFF];
#	int		nDivideNum;
#	int		nSrcX;
#	int		nSrcY;
#	int		nSrcBit;
#} ACAPSRCIMAGE, *PACAPSRCIMAGE;
class ACAPSRCIMAGE(Structure):
	_fields_ = [
		("pSrcBuff",	c_void_p * ACL_MAX_BUFF),
		("nDivideNum",	c_int),
		("nSrcX",		c_int),
		("nSrcY",		c_int),
		("nSrcBit",		c_int)
		]

#typedef struct{
#	void*	pDstBuff[ACL_MAX_BUFF];
#	int		npDstX;
#	int		npDstY;
#	int		npDstBit;
#	int		npDstNum;
#} ACAPDSTIMAGE, *PACAPDSTIMAGE;
class ACAPDSTIMAGE(Structure):
	_fields_ = [
		("pDstBuff",	c_void_p * ACL_MAX_BUFF),
		("npDstX",		c_int),
		("npDstY",		c_int),
		("npDstBit",	c_int),
		("npDstNum",	c_int)
		]

#typedef struct{
#	void*	pBuffer;
#	int		nWidth;
#	int		nHeight;
#	int		nBitWidth;
#	int		nShiftFlag;
#	int		nShift;
#	struct {
#		int		nOffsetX;
#		int		nOffsetY;
#		int		nRoiX;
#		int		nRoiY;
#	} ROIIMAGE;
#} ACAPROIIMAGE, *PACAPROIIMAGE;
class ROIIMAGE(Structure):
	_fields_ = [
		("nOffsetX",	c_int),
		("nOffsetY",	c_int),
		("nRoiX",		c_int),
		("nRoiY",		c_int)
		]
class ACAPROIIMAGE(Structure):
	_fields_ = [
		("pBuffer",		c_void_p),
		("nWidth",		c_int),
		("nHeight",		c_int),
		("nBitWidth",	c_int),
		("nShiftFlag",	c_int),
		("nShift",		c_int),
		("rotimage",	ROIIMAGE)
		]

#-------------------------------------
# 非線形DMA構造体 (Ver 4.0.0)
#-------------------------------------
ACL_DMATYPE_NORMAL				= (0)
ACL_DMATYPE_YREVERSE			= (1 <<  0)
ACL_DMATYPE_VERT_REMAP			= (1 <<  1)

ACL_BUFFTYPE_INTERNAL			= (0)
ACL_BUFFTYPE_EXTERNAL			= (1)
ACL_BUFFTYPE_KERNEL				= (2)  # Ver 5.2.0
ACL_BUFFTYPE_KERNEL_EX			= (3)  # Ver 5.2.0

#typedef struct _ACL_BUFF_INFO_RESIZE {
#	DWORD SizeOf;
#	DWORD TransferXSize;
#	DWORD TransferYSize;
#	DWORD BitWidth;
#	DWORD DmaType;
#	void* pBuffer;
#}ACL_BUFF_INFO_RESIZE, *PACL_BUFF_INFO_RESIZE;
class ACL_BUFF_INFO_RESIZE(Structure):
	_fields_ = [
		("SizeOf",			c_ulong),
		("TransferXSize",	c_ulong),
		("TransferYSize",	c_ulong),
		("BitWidth",		c_ulong),
		("DmaType",			c_ulong),
		("pBuffer",			c_void_p)
		]

#typedef struct _ACL_BUFF_INFO_ROI {
#	DWORD SizeOf;
#	DWORD TransferXSize;
#	DWORD TransferYSize;
#	DWORD BitWidth;
#	DWORD DmaType;
#	DWORD BufferXSize;
#	DWORD BufferYSize;
#	DWORD XOffset;
#	DWORD YOffset;
#	void* pBuffer;
#}ACL_BUFF_INFO_ROI, *PACL_BUFF_INFO_ROI;
class ACL_BUFF_INFO_ROI(Structure):
	_fields_ = [
		("SizeOf",			c_ulong),
		("TransferXSize",	c_ulong),
		("TransferYSize",	c_ulong),
		("BitWidth",		c_ulong),
		("DmaType",			c_ulong),
		("BufferXSize",		c_ulong),
		("BufferYSize",		c_ulong),
		("XOffset",			c_ulong),
		("YOffset",			c_ulong),
		("pBuffer",			c_void_p)
		]

#typedef struct _ACL_REGION {
#	DWORD XSize;
#	DWORD YSize;
#	DWORD XOffset;
#	DWORD YOffset;
#	DWORD Size;
#	DWORD DmaType;
#	void* pBuffer;
#} ACL_REGION, *PACL_REGION;
class ACL_REGION(Structure):
	_fields_ = [
		("XSize",	c_ulong),
		("YSize",	c_ulong),
		("XOffset",	c_ulong),
		("YOffset",	c_ulong),
		("Size",	c_ulong),
		("DmaType",	c_ulong),
		("pBuffer",	c_void_p)
		]

#typedef struct _ACL_BUFF_INFO_DIVIDE {
#	DWORD SizeOf;
#	DWORD TransferXSize;
#	DWORD TransferYSize;
#	DWORD BitWidth;
#	DWORD DmaType;
#	DWORD NumOfRegions;
#	ACL_REGION Region[1];
#} ACL_BUFF_INFO_DIVIDE, *PACL_BUFF_INFO_DIVIDE;
class ACL_BUFF_INFO_DIVIDE(Structure):
	_fields_ = [
		("SizeOf",	c_ulong),
		("TransferXSize",	c_ulong),
		("TransferYSize",	c_ulong),
		("BitWidth",	c_ulong),
		("DmaType",	c_ulong),
		("NumOfRegions",	c_ulong),
		("Region",	ACL_REGION * 1)
		]
	
# シリアル定義
ACL_SERIAL_STX				= "02"
ACL_SERIAL_ETX				= "03"
ACL_SERIAL_CR				= "0D"
ACL_SERIAL_LF				= "0A"

# ****************************************************************************************
# 	コード定義
#		0x1XXX : 共通
#		0x3XXX : APX-3312 固有
# ****************************************************************************************
# 共通  ----------------------------------------------------------------------------------
ACL_X_SIZE						= 0x1001	# Xサイズ(横)
ACL_Y_SIZE						= 0x1002	# Yサイズ(縦)
ACL_X_DELAY						= 0x1003	# Xディレイ
ACL_Y_DELAY						= 0x1004	# Yディレイ
ACL_Y_TOTAL						= 0x1005	# YTotalサイズ
ACL_CAM_BIT						= 0x1006	# カメラ入力ビット幅(8/10/12/14/16/24/32)
ACL_BOARD_BIT					= 0x1007	# ボード入力ビット幅(8/16/32)
ACL_PIX_SHIFT					= 0x1008	# シフト回数
ACL_TIME_OUT					= 0x1009	# タイムアウト時間
ACL_MEM_NUM						= 0x100A	# メモリ確保数
ACL_EXP_UNIT					= 0x100B	# 露光幅の単位
ACL_EXP_POL						= 0x100C	# 露光信号出力論理(1:正論理/0:負論理)
ACL_EXP_CYCLE					= 0x100D	# 露光周期
ACL_EXPOSURE					= 0x100E	# 露光時間
ACL_EXP_CC_OUT					= 0x100F	# 露光信号出力CC
ACL_ROLLING_SHUTTER				= 0x1010	# ローリングシャッタ 有効/無効
ACL_EXT_EN						= 0x1011	# 外部トリガ有効・無効(0:無効/1:有効[TTL]/2:有効[RS-422])
ACL_EXT_MODE					= 0x1012	# 外部トリガモード(0:連続トリガ/1:単発トリガ)
ACL_EXT_CHATTER					= 0x1013	# 外部トリガ、無効期間
ACL_EXT_DELAY					= 0x1014	# 外部トリガ、出力遅延時間
ACL_ENC_EN						= 0x1015	# エンコーダ 有効/無効
ACL_ENC_START					= 0x1016	# エンコーダ用外部トリガ、起動方法(0:CPU/1:起動信号/2:一致信号)
ACL_ENC_MODE					= 0x1017	# モード(1:エンコーダスキャン/2:エンコーダライン選択)
ACL_ENC_PHASE					= 0x1018	# A/AB相
ACL_ENC_DIRECTION				= 0x1019	# CW/CCW
ACL_ENC_ZPHASE_EN				= 0x101A	# Z相 有効/無効
ACL_ENC_COMPARE_1				= 0x101B	# 比較レジスタ1
ACL_ENC_COMPARE_2				= 0x101C	# 比較レジスタ2
ACL_STROBE_EN					= 0x101D	# ストロボ 有効/無効
ACL_STROBE_DELAY				= 0x101E	# 発生遅延時間
ACL_STROBE_TIME					= 0x101F	# 発生時間
ACL_CC1_LEVEL					= 0x1020	# CC1レベル(位相)
ACL_CC2_LEVEL					= 0x1021	# CC2レベル(位相)
ACL_CC3_LEVEL					= 0x1022	# CC3レベル(位相)
ACL_CC4_LEVEL					= 0x1023	# CC4レベル(位相)
ACL_SCAN_SYSTEM					= 0x1024	# カメラ方式(0:エリア/1:ライン)
ACL_REVERSE_DMA					= 0x1025	# リバースDMA 有効/無効
ACL_DVAL_EN						= 0x1026	# DVAL 有効/無効
ACL_TAP_NUM						= 0x1027	# タップ数
ACL_TAP_ARRANGE					= 0x1028	# タップ並び替え(0:なし/1:→→/2:←←/3:→←/4:←→)
ACL_SYNC_LT						= 0x1029	# SyncLT 有効/無効
ACL_GPOUT_SEL					= 0x102A	# GPOUT選択
ACL_GPOUT_POL					= 0x102B	# GPOUT論理
ACL_INTR_LINE					= 0x102C	# ライン割り込み行数
#pragma deprecated(ACL_SERIAL_CHANNEL)
_ACL_SERIAL_CHANNEL				= 0x102D	# シリアルチャンネル設定
#pragma deprecated(ACL_SERIAL_PORT)
_ACL_SERIAL_PORT					= 0x102E	# シリアルポート設定
ACL_EXP_EN						= 0x102F	# 露光信号(CC)出力 有効/無効
ACL_ENC_ABS_START				= 0x1030	# 絶対位置エンコーダ 開始/停止 (絶対位置エンコーダ使用時)
ACL_ENC_ABS_COUNT				= 0x1031	# 現在のカウント値 (絶対位置エンコーダ使用時)
ACL_DATA_MASK_LOWER				= 0x1032	# カメラリンクデータマスク 下位32bit
ACL_DATA_MASK_UPPER				= 0x1033	# カメラリンクデータマスク 上位32bit
ACL_ENC_RLT_COUNT				= 0x1034	# 現在のエンコーダカウント値 (相対位置エンコーダ使用時)
ACL_ENC_RLT_ALL_COUNT			= 0x1035	# 総エンコーダカウント値 (相対位置エンコーダ使用時)
ACL_ENC_AGR_COUNT				= 0x1036	# 一致パルス数 (相対位置エンコーダ使用時)
ACL_EXT_CHATTER_SEPARATE		= 0x1037	# 外部トリガ、無効期間(High/Low個別設定)
ACL_EXT_PIN_SEL					= 0x1038	# 外部トリガピンの選択
ACL_GPIN_PIN_SEL				= 0x1039	# GPIN割り込みピンの選択
ACL_SYNC_CH						= 0x103A	# 同期取込設定
#pragma deprecated(ACL_BAYER_SETUP)
_ACL_BAYER_SETUP					= 0x103B	# Bayerの設定(現在、何もせずに成功)
ACL_BAYER_GRID					= 0x103C	# 開始位置パターンの設定
ACL_BAYER_LUT_EDIT				= 0x103D	# BayerLUTの編集開始・停止
ACL_BAYER_LUT_DATA				= 0x103E	# BayerLUTのデータ設定
ACL_POWER_SUPPLY				= 0x103F	# カメラ電源ON/OFF制御
ACL_POWER_STATE					= 0x1040	# カメラ電源エラーフラグクリア/エラー発生確認
ACL_STROBE_POL					= 0x1041	# ストロボ極性設定
ACL_VERTICAL_REMAP				= 0x1042	# VerticalRemap (0=無効, 1=Vertical, 2=DualLine) Ver.6.7.0
ACL_CC_DELAY					= 0x1043	# CC遅延設定
#Ver.4.0.0
ACL_HIGH_CLIP					= 0x1044	# ハイクリップ
ACL_EXPRESS_LINK				= 0x1045	# PCIEリンク幅
ACL_FPGA_VERSION				= 0x1046	# FPGAバージョン
ACL_TAP_DIRECTION				= 0x1047	# タップ方向
ACL_ARRANGE_XSIZE				= 0x1048	# 並び替え総XSize
ACL_LVAL_DELAY					= 0x1049	# LVALディレイ
ACL_LINE_REVERSE				= 0x104A	# ラインリバース
ACL_CAMERA_STATE				= 0x104B	# カメラ状態確認
ACL_GPIN_POL					= 0x104C	# GPINレベル確認
ACL_BOARD_ERROR					= 0x104D	# ボードエラー
#Ver.4.1.0
ACL_START_FRAME_NO				= 0x104E	# 入力開始フレーム番号
#Ver.5.0.0
ACL_CANCEL_INITIALIZE			= 0x104F	# 初期化と内部バッファ確保のキャンセル
#Ver.5.2.0
ACL_EXP_CYCLE_EX				= 0x1050	# CC出力周期(x100ns)
ACL_EXPOSURE_EX					= 0x1051	# CC出力幅(x100ns)
#Ver.6.3.0
ACL_DRIVER_NAME					= 0x1052	# ドライバ名の取得
ACL_HW_PROTECT					= 0x1053	# HWプロテクトの取得
ACL_BAYER_ENABLE				= 0x1054	# Bayer処理の有効/無効
ACL_BAYER_INPUT_BIT				= 0x1055	# Bayer処理の入力ビット幅
ACL_BAYER_OUTPUT_BIT			= 0x1056	# Bayer処理の出力ビット幅
ACL_BUFFER_ZERO_FILL			= 0x1057	# バッファのゼロクリア
#Ver.6.4.1
ACL_CC_STOP						= 0x1058	# CC出力の停止

#Ver.4.0.0
ACL_IMAGE_PTR					= 0x10A0	# 画像バッファの先頭アドレス
#Ver.5.0.0
#pragma deprecated(ACL_CXP_STATE)
_ACL_CXP_STATE					= 0x1101	# Cxp関連のエラーを取得・クリア
#pragma deprecated(ACL_CAMSCAN_MODE)
_ACL_CAMSCAN_MODE				= 0x1102	# Progressive/Interlace

#Ver.6.8.0
ACL_CXP_LINK_RESET				= 0x1110	# カメラに対し、ディスカバリ処理を再実行します。
#pragma deprecated(ACL_CXP_LINK_SPEED)
_ACL_CXP_LINK_SPEED				= 0x1111	# ビットレートを設定/取得
ACL_CXP_ACQ_START_ADR			= 0x1112	# Acqusition Startのアドレス 
ACL_CXP_PIX_FORMAT_ADR			= 0x1113	# Pixel Formatのアドレス
#Ver.7.1.8
ACL_CXP_ACQ_START_VALUE			= 0x1114	# Acqusition Startへ書き込む値
ACL_CXP_ACQ_STOP_ADR			= 0x1115	# Acqusition Stopのアドレス
ACL_CXP_ACQ_STOP_VALUE			= 0x1116	# Acqusition Stopへ書き込む値
ACL_CXP_PIX_FORMAT				= 0x1117	# Pixel Formatへ書き込む値

ACL_OPT_LINK_RESET				= 0x1120	# Opt-C Linkリセット

#Ver.7.1.11
ACL_CXP_BITRATE					= 0x1111	# ビットレートを設定/取得

#Ver.6.5.1
ACL_LVDS_CCLK_SEL				= 0x1201	# LVDSカメラ駆動クロック
ACL_LVDS_PHASE_SEL				= 0x1202	# LVDS位相反転
ACL_LVDS_SYNCLT_SEL				= 0x1203	# LVDSSYNCLT入力

#Ver.6.7.0
ACL_COUNT_RESET					= 0x1210	# EXTTRIG/CC/FVAL/LVAL回数リセット
ACL_COUNT_CC					= 0x1211	# CC出力回数
ACL_COUNT_FVAL					= 0x1212	# FVAL回数
ACL_COUNT_LVAL					= 0x1213	# LVAL回数
ACL_COUNT_EXTTRIG				= 0x1214	# 外部トリガ回数
ACL_INTERVAL_EXTTRIG_1			= 0x1215	# 外部トリガ間隔１
ACL_INTERVAL_EXTTRIG_2			= 0x1216	# 外部トリガ間隔２
ACL_INTERVAL_EXTTRIG_3			= 0x1217	# 外部トリガ間隔３
ACL_INTERVAL_EXTTRIG_4			= 0x1218	# 外部トリガ間隔４
ACL_VIRTUAL_COMPORT				= 0x1219	# 仮想COM番号

#Ver.7.0.0
ACL_ENC_ABS_MODE				= 0x1220	# 絶対位置エンコーダモード(シングルポイント/マルチポイント)
ACL_ENC_ABS_MP_COUNT			= 0x1221	# 絶対位置エンコーダマルチポイント カウント値
ACL_POCL_LITE_ENABLE			= 0x1222	# PoCL-Lite有効/無効

#Ver.7.1.0
ACL_RGB_SWAP_ENABLE				= 0x1223	# RGB変換(RGB⇒BGR)

#Ver.7.2.0
ACL_NARROW10BIT_ENABLE			= 0x1224	# 10⇒16/30⇒32 ビット変換
ACL_CAPTURE_FLAG				= 0x1225	# 入力フラグ

#Ver.7.1.0
ACL_A_CW_CCW					= 0x1A01	# A相の回転方向 (0:CW)
ACL_B_CW_CCW					= 0x1A02	# B相の回転方向 (0:CW)
ACL_FREQ_A						= 0x1A03	# A相の周波数  (Hz単位)
ACL_FREQ_B						= 0x1A04	# B相の周波数  (Hz単位) 
ACL_FREQ_Z						= 0x1A05	# Z相の周波数  (Hz単位)
ACL_FREQ_LVAL					= 0x1A06	# LVALの周波数 (KHz単位)
ACL_FREQ_FVAL					= 0x1A07	# FVALの周波数 (Hz単位)
ACL_FREQ_TTL1					= 0x1A08	# TTL1の周波数 (Hz単位)
ACL_FREQ_TTL2					= 0x1A09	# TTL2の周波数 (Hz単位)
ACL_FREQ_TTL3					= 0x1A0A	# TTL3の周波数 (Hz単位)
ACL_FREQ_TTL4					= 0x1A0B	# TTL4の周波数 (Hz単位)
ACL_FREQ_TTL5					= 0x1A0C	# TTL5の周波数 (Hz単位)
ACL_FREQ_TTL6					= 0x1A0D	# TTL6の周波数 (Hz単位)
ACL_FREQ_TTL7					= 0x1A0E	# TTL7の周波数 (Hz単位)
ACL_FREQ_TTL8					= 0x1A0F	# TTL8の周波数 (Hz単位)
ACL_FREQ_OPT1					= 0x1A10	# OPT1の周波数 (Hz単位)
ACL_FREQ_OPT2					= 0x1A11	# OPT2の周波数 (Hz単位)
ACL_FREQ_OPT3					= 0x1A12	# OPT3の周波数 (Hz単位)
ACL_FREQ_OPT4					= 0x1A13	# OPT4の周波数 (Hz単位)
ACL_FREQ_OPT5					= 0x1A14	# OPT5の周波数 (Hz単位)
ACL_FREQ_OPT6					= 0x1A15	# OPT6の周波数 (Hz単位)
ACL_FREQ_OPT7					= 0x1A16	# OPT7の周波数 (Hz単位)
ACL_FREQ_OPT8					= 0x1A17	# OPT8の周波数 (Hz単位)
ACL_FREQ_D						= 0x1A18	# D相の周波数  (Hz単位)
ACL_FIFO_FULL					= 0x1A19	# FIFO Fullステータス

# Ver.7.1.10
ACL_BOARD_TEMP					= 0x1A1A	# 基板温度情報
ACL_FPGA_TEMP					= 0x1A1B	# FPGA温度情報

# APX-3312  ----------------------------------------------------------------------------------
ACL_3312_CAMERA_STATE			= 0x3001	# カメラの状態確認(Setで確認/Getで状態読み出し)
ACL_3312_STATUS_REG				= 0x3002	# カメラの状態確認(SetでReset/Getで状態読み出し)
ACL_3312_ENCODER_REG			= 0x3003	# カメラの状態確認(SetでReset/Getで状態読み出し)
ACL_3312_BOARD_RECONFIG			= 0x3004	# ボードリコンフィグ
ACL_3312_MEMORY_RESET			= 0x3005	# ボードメモリリセット
#pragma deprecated(ACL_3312_EXPRESS_LINK)
_ACL_3312_EXPRESS_LINK			= 0x3006	# Expressリンク
#pragma deprecated(ACL_3312_FPGA_VERSION)
_ACL_3312_FPGA_VERSION			= 0x3007	# APX-3312 FPGAバージョン

ACL_3312_LUT_EN					= 0x3008	# LUT 有効/無効
ACL_3312_LUT_VALUE				= 0x3009	# LUT設定値

#pragma deprecated(ACL_3312_IMAGE_PTR)	
_ACL_3312_IMAGE_PTR				= 0x3020	# 画像バッファの先頭アドレス


# APX-3313  ----------------------------------------------------------------------------------
#pragma deprecated(ACL_3313_EXPRESS_LINK)
_ACL_3313_EXPRESS_LINK			= 0x4001	# Expressリンク
#pragma deprecated(ACL_3313_FPGA_VERSION)
_ACL_3313_FPGA_VERSION			= 0x4002	# APX-3313 FPGAバージョン
ACL_3313_HIGH_CLIP				= 0x4003	# ハイクリップ (0=無効/1=10bit/2=12bit)
ACL_3313_TAP_ARRANGE			= 0x4004	# タップ間並び替え
ACL_3313_TAP_DIRECTION			= 0x4005	# データ出力方向
ACL_3313_ARRANGE_XSIZE			= 0x4006	# 並び替え 総Xサイズ
ACL_3313_LVAL_DELAY				= 0x4007	# LVALディレイ
ACL_3313_LINE_REVERSE			= 0x4008	# ライン反転
ACL_3313_CAMERA_STATE			= 0x4009	# カメラ接続状態
ACL_3313_STATUS_REG				= 0x400A	# カメラの状態確認(SetでReset/Getで状態読み出し) /* Ver3.2.0 */
ACL_3313_ENCODER_REG			= 0x400B	# エンコーダの状態確認(SetでReset/Getで状態読み出し) /* Ver3.2.0 */

#pragma deprecated(ACL_3313_IMAGE_PTR)
_ACL_3313_IMAGE_PTR				= 0x4020	# 画像バッファの先頭アドレス


# APX-3318  ----------------------------------------------------------------------------------
#pragma deprecated(ACL_3318_EXPRESS_LINK)
_ACL_3318_EXPRESS_LINK			= 0x5001	# Expressリンク
#pragma deprecated(ACL_3318_FPGA_VERSION)
_ACL_3318_FPGA_VERSION			= 0x5002	# APX-3318 FPGAバージョン
ACL_3318_HIGH_CLIP				= 0x5003	# ハイクリップ (0=無効/1=10bit/2=12bit)
ACL_3318_TAP_ARRANGE			= 0x5004	# タップ間並び替え
ACL_3318_TAP_DIRECTION			= 0x5005	# データ出力方向
ACL_3318_ARRANGE_XSIZE			= 0x5006	# 並び替え 総Xサイズ
ACL_3318_LVAL_DELAY				= 0x5007	# LVALディレイ
ACL_3318_LINE_REVERSE			= 0x5008	# ライン反転
ACL_3318_CAMERA_STATE			= 0x5009	# カメラ接続状態 
ACL_3318_STATUS_REG				= 0x500A	# カメラの状態確認(SetでReset/Getで状態読み出し) /* Ver3.2.0 */
ACL_3318_ENCODER_REG			= 0x500B	# エンコーダの状態確認(SetでReset/Getで状態読み出し) /* Ver3.2.0 */

#pragma deprecated(ACL_3318_IMAGE_PTR)
_ACL_3318_IMAGE_PTR				= 0x5020	# 画像バッファの先頭アドレス

# APX-3311
#pragma deprecated(ACL_3311_IMAGE_PTR)
_ACL_3311_IMAGE_PTR				= 0x6020	# 画像バッファの先頭アドレス


setting_code_dict ={
	"ACL_X_SIZE"					: 0x1001,	# Xサイズ(横)
	"ACL_Y_SIZE"					: 0x1002,	# Yサイズ(縦)
	"ACL_X_DELAY"					: 0x1003,	# Xディレイ
	"ACL_Y_DELAY"					: 0x1004,	# Yディレイ
	"ACL_Y_TOTAL"					: 0x1005,	# YTotalサイズ
	"ACL_CAM_BIT"					: 0x1006,	# カメラ入力ビット幅(8/10/12/14/16/24/32)
	"ACL_BOARD_BIT"					: 0x1007,	# ボード入力ビット幅(8/16/32)
	"ACL_PIX_SHIFT"					: 0x1008,	# シフト回数
	"ACL_TIME_OUT"					: 0x1009,	# タイムアウト時間
	"ACL_MEM_NUM"					: 0x100A,	# メモリ確保数
	"ACL_EXP_UNIT"					: 0x100B,	# 露光幅の単位
	"ACL_EXP_POL"					: 0x100C,	# 露光信号出力論理(1:正論理/0:負論理)
	"ACL_EXP_CYCLE"					: 0x100D,	# 露光周期
	"ACL_EXPOSURE"					: 0x100E,	# 露光時間
	"ACL_EXP_CC_OUT"				: 0x100F,	# 露光信号出力CC
	"ACL_ROLLING_SHUTTER"			: 0x1010,	# ローリングシャッタ 有効/無効
	"ACL_EXT_EN"					: 0x1011,	# 外部トリガ有効・無効(0:無効/1:有効[TTL]/2:有効[RS-422])
	"ACL_EXT_MODE"					: 0x1012,	# 外部トリガモード(0:連続トリガ/1:単発トリガ)
	"ACL_EXT_CHATTER"				: 0x1013,	# 外部トリガ、無効期間
	"ACL_EXT_DELAY"					: 0x1014,	# 外部トリガ、出力遅延時間
	"ACL_ENC_EN"					: 0x1015,	# エンコーダ 有効/無効
	"ACL_ENC_START"					: 0x1016,	# エンコーダ用外部トリガ、起動方法(0:CPU/1:起動信号/2:一致信号)
	"ACL_ENC_MODE"					: 0x1017,	# モード(1:エンコーダスキャン/2:エンコーダライン選択)
	"ACL_ENC_PHASE"					: 0x1018,	# A/AB相
	"ACL_ENC_DIRECTION"				: 0x1019,	# CW/CCW
	"ACL_ENC_ZPHASE_EN"				: 0x101A,	# Z相 有効/無効
	"ACL_ENC_COMPARE_1"				: 0x101B,	# 比較レジスタ1
	"ACL_ENC_COMPARE_2"				: 0x101C,	# 比較レジスタ2
	"ACL_STROBE_EN"					: 0x101D,	# ストロボ 有効/無効
	"ACL_STROBE_DELAY"				: 0x101E,	# 発生遅延時間
	"ACL_STROBE_TIME"				: 0x101F,	# 発生時間
	"ACL_CC1_LEVEL"					: 0x1020,	# CC1レベル(位相)
	"ACL_CC2_LEVEL"					: 0x1021,	# CC2レベル(位相)
	"ACL_CC3_LEVEL"					: 0x1022,	# CC3レベル(位相)
	"ACL_CC4_LEVEL"					: 0x1023,	# CC4レベル(位相)
	"ACL_SCAN_SYSTEM"				: 0x1024,	# カメラ方式(0:エリア/1:ライン)
	"ACL_REVERSE_DMA"				: 0x1025,	# リバースDMA 有効/無効
	"ACL_DVAL_EN"					: 0x1026,	# DVAL 有効/無効
	ACL_TAP_NUM						: 0x1027,	# タップ数
	ACL_TAP_ARRANGE					: 0x1028,	# タップ並び替え(0:なし/1:→→/2:←←/3:→←/4:←→)
	ACL_SYNC_LT						: 0x1029,	# SyncLT 有効/無効
	ACL_GPOUT_SEL					: 0x102A,	# GPOUT選択
	ACL_GPOUT_POL					: 0x102B,	# GPOUT論理
	ACL_INTR_LINE					: 0x102C,	# ライン割り込み行数
	#pragma deprecated(ACL_SERIAL_CHANNEL)
	"_ACL_SERIAL_CHANNEL"			: 0x102D,	# シリアルチャンネル設定
	#pragma deprecated(ACL_SERIAL_PORT)
	"_ACL_SERIAL_PORT"				: 0x102E,	# シリアルポート設定
	"ACL_EXP_EN"					: 0x102F,	# 露光信号(CC)出力 有効/無効
	"ACL_ENC_ABS_START"				: 0x1030,	# 絶対位置エンコーダ 開始/停止 (絶対位置エンコーダ使用時)
	"ACL_ENC_ABS_COUNT"				: 0x1031,	# 現在のカウント値 (絶対位置エンコーダ使用時)
	"ACL_DATA_MASK_LOWER"			: 0x1032,	# カメラリンクデータマスク 下位32bit
	"ACL_DATA_MASK_UPPER"			: 0x1033,	# カメラリンクデータマスク 上位32bit
	"ACL_ENC_RLT_COUNT"				: 0x1034,	# 現在のエンコーダカウント値 (相対位置エンコーダ使用時)
	"ACL_ENC_RLT_ALL_COUNT"			: 0x1035,	# 総エンコーダカウント値 (相対位置エンコーダ使用時)
	"ACL_ENC_AGR_COUNT"				: 0x1036,	# 一致パルス数 (相対位置エンコーダ使用時)
	"ACL_EXT_CHATTER_SEPARATE"		: 0x1037,	# 外部トリガ、無効期間(High/Low個別設定)
	"ACL_EXT_PIN_SEL"				: 0x1038,	# 外部トリガピンの選択
	"ACL_GPIN_PIN_SEL"				: 0x1039,	# GPIN割り込みピンの選択
	ACL_SYNC_CH						: 0x103A,	# 同期取込設定
	#pragma deprecated(ACL_BAYER_SETUP)
	"_ACL_BAYER_SETUP"				: 0x103B,	# Bayerの設定(現在、何もせずに成功)
	"ACL_BAYER_GRID"				: 0x103C,	# 開始位置パターンの設定
	"ACL_BAYER_LUT_EDIT"			: 0x103D,	# BayerLUTの編集開始・停止
	"ACL_BAYER_LUT_DATA"			: 0x103E,	# BayerLUTのデータ設定
	"ACL_POWER_SUPPLY"				: 0x103F,	# カメラ電源ON/OFF制御
	"ACL_POWER_STATE"				: 0x1040,	# カメラ電源エラーフラグクリア/エラー発生確認
	"ACL_STROBE_POL"				: 0x1041,	# ストロボ極性設定
	"ACL_VERTICAL_REMAP"				: 0x1042,	# VerticalRemap (0=無効, 1=Vertical, 2=DualLine) Ver.6.7.0
	"ACL_CC_DELAY"					: 0x1043,	# CC遅延設定
	#Ver.4.0.0
	"ACL_HIGH_CLIP"					: 0x1044,	# ハイクリップ
	"ACL_EXPRESS_LINK"				: 0x1045,	# PCIEリンク幅
	"ACL_FPGA_VERSION"				: 0x1046,	# FPGAバージョン
	"ACL_TAP_DIRECTION"				: 0x1047,	# タップ方向
	"ACL_ARRANGE_XSIZE"				: 0x1048,	# 並び替え総XSize
	"ACL_LVAL_DELAY"				: 0x1049,	# LVALディレイ
	"ACL_LINE_REVERSE"				: 0x104A,	# ラインリバース
	"ACL_CAMERA_STATE"				: 0x104B,	# カメラ状態確認
	"ACL_GPIN_POL"					: 0x104C,	# GPINレベル確認
	"ACL_BOARD_ERROR"				: 0x104D,	# ボードエラー
	#Ver.4.1.0
	"ACL_START_FRAME_NO"			: 0x104E,	# 入力開始フレーム番号
	#Ver.5.0.0
	"ACL_CANCEL_INITIALIZE"			: 0x104F,	# 初期化と内部バッファ確保のキャンセル
	#Ver.5.2.0
	"ACL_EXP_CYCLE_EX"				: 0x1050,	# CC出力周期(x100ns)
	"ACL_EXPOSURE_EX"				: 0x1051,	# CC出力幅(x100ns)
	#Ver.6.3.0
	"ACL_DRIVER_NAME"				: 0x1052,	# ドライバ名の取得
	"ACL_HW_PROTECT"				: 0x1053,	# HWプロテクトの取得
	"ACL_BAYER_ENABLE"				: 0x1054,	# Bayer処理の有効/無効
	"ACL_BAYER_INPUT_BIT"			: 0x1055,	# Bayer処理の入力ビット幅
	"ACL_BAYER_OUTPUT_BIT"			: 0x1056,	# Bayer処理の出力ビット幅
	"ACL_BUFFER_ZERO_FILL"			: 0x1057,	# バッファのゼロクリア
	#Ver.6.4.1
	"ACL_CC_STOP"					: 0x1058,	# CC出力の停止

	#Ver.4.0.0
	"ACL_IMAGE_PTR"					: 0x10A0,	# 画像バッファの先頭アドレス
	#Ver.5.0.0
	#pragma deprecated(ACL_CXP_STATE)
	"_ACL_CXP_STATE"				: 0x1101,	# Cxp関連のエラーを取得・クリア
	#pragma deprecated(ACL_CAMSCAN_MODE)
	"_ACL_CAMSCAN_MODE"				: 0x1102,	# Progressive/Interlace

	#Ver.6.8.0
	"ACL_CXP_LINK_RESET"			: 0x1110,	# カメラに対し、ディスカバリ処理を再実行します。
	#pragma deprecated(ACL_CXP_LINK_SPEED)
	"_ACL_CXP_LINK_SPEED"			: 0x1111,	# ビットレートを設定/取得
	"ACL_CXP_ACQ_START_ADR"			: 0x1112,	# Acqusition Startのアドレス 
	"ACL_CXP_PIX_FORMAT_ADR"		: 0x1113,	# Pixel Formatのアドレス
	#Ver.7.1.8
	"ACL_CXP_ACQ_START_VALUE"		: 0x1114,	# Acqusition Startへ書き込む値
	"ACL_CXP_ACQ_STOP_ADR"			: 0x1115,	# Acqusition Stopのアドレス
	"ACL_CXP_ACQ_STOP_VALUE"		: 0x1116,	# Acqusition Stopへ書き込む値
	"ACL_CXP_PIX_FORMAT"			: 0x1117,	# Pixel Formatへ書き込む値

	"ACL_OPT_LINK_RESET"			: 0x1120,	# Opt-C Linkリセット

	#Ver.7.1.11
	"ACL_CXP_BITRATE"				: 0x1111,	# ビットレートを設定/取得

	#Ver.6.5.1
	"ACL_LVDS_CCLK_SEL"				: 0x1201,	# LVDSカメラ駆動クロック
	"ACL_LVDS_PHASE_SEL"			: 0x1202,	# LVDS位相反転
	"ACL_LVDS_SYNCLT_SEL"			: 0x1203,	# LVDSSYNCLT入力

	#Ver.6.7.0
	"ACL_COUNT_RESET"				: 0x1210,	# EXTTRIG/CC/FVAL/LVAL回数リセット
	"ACL_COUNT_CC"					: 0x1211,	# CC出力回数
	"ACL_COUNT_FVAL"				: 0x1212,	# FVAL回数
	"ACL_COUNT_LVAL"				: 0x1213,	# LVAL回数
	"ACL_COUNT_EXTTRIG"				: 0x1214,	# 外部トリガ回数
	"ACL_INTERVAL_EXTTRIG_1"		: 0x1215,	# 外部トリガ間隔１
	"ACL_INTERVAL_EXTTRIG_2"		: 0x1216,	# 外部トリガ間隔２
	"ACL_INTERVAL_EXTTRIG_3"		: 0x1217,	# 外部トリガ間隔３
	"ACL_INTERVAL_EXTTRIG_4"		: 0x1218,	# 外部トリガ間隔４
	"ACL_VIRTUAL_COMPORT"			: 0x1219,	# 仮想COM番号

	#Ver.7.0.0
	"ACL_ENC_ABS_MODE"				: 0x1220,	# 絶対位置エンコーダモード(シングルポイント/マルチポイント)
	"ACL_ENC_ABS_MP_COUNT"			: 0x1221,	# 絶対位置エンコーダマルチポイント カウント値
	"ACL_POCL_LITE_ENABLE"			: 0x1222,	# PoCL-Lite有効/無効

	#Ver.7.1.0
	"ACL_RGB_SWAP_ENABLE"			: 0x1223,	# RGB変換(RGB⇒BGR)

	#Ver.7.2.0
	"ACL_NARROW10BIT_ENABLE"		: 0x1224,	# 10⇒16/30⇒32 ビット変換
	"ACL_CAPTURE_FLAG"				: 0x1225,	# 入力フラグ

	#Ver.7.1.0
	"ACL_A_CW_CCW"					: 0x1A01,	# A相の回転方向 (0:CW)
	"ACL_B_CW_CCW"					: 0x1A02,	# B相の回転方向 (0:CW)
	"ACL_FREQ_A"					: 0x1A03,	# A相の周波数  (Hz単位)
	"ACL_FREQ_B"					: 0x1A04,	# B相の周波数  (Hz単位) 
	"ACL_FREQ_Z"					: 0x1A05,	# Z相の周波数  (Hz単位)
	"ACL_FREQ_LVAL"					: 0x1A06,	# LVALの周波数 (KHz単位)
	"ACL_FREQ_FVAL"					: 0x1A07,	# FVALの周波数 (Hz単位)
	"ACL_FREQ_TTL1"					: 0x1A08,	# TTL1の周波数 (Hz単位)
	"ACL_FREQ_TTL2"					: 0x1A09,	# TTL2の周波数 (Hz単位)
	"ACL_FREQ_TTL3"					: 0x1A0A,	# TTL3の周波数 (Hz単位)
	"ACL_FREQ_TTL4"					: 0x1A0B,	# TTL4の周波数 (Hz単位)
	"ACL_FREQ_TTL5"					: 0x1A0C,	# TTL5の周波数 (Hz単位)
	"ACL_FREQ_TTL6"					: 0x1A0D,	# TTL6の周波数 (Hz単位)
	"ACL_FREQ_TTL7"					: 0x1A0E,	# TTL7の周波数 (Hz単位)
	"ACL_FREQ_TTL8"					: 0x1A0F,	# TTL8の周波数 (Hz単位)
	"ACL_FREQ_OPT1"					: 0x1A10,	# OPT1の周波数 (Hz単位)
	"ACL_FREQ_OPT2"					: 0x1A11,	# OPT2の周波数 (Hz単位)
	"ACL_FREQ_OPT3"					: 0x1A12,	# OPT3の周波数 (Hz単位)
	"ACL_FREQ_OPT4"					: 0x1A13,	# OPT4の周波数 (Hz単位)
	"ACL_FREQ_OPT5"					: 0x1A14,	# OPT5の周波数 (Hz単位)
	"ACL_FREQ_OPT6"					: 0x1A15,	# OPT6の周波数 (Hz単位)
	"ACL_FREQ_OPT7"					: 0x1A16,	# OPT7の周波数 (Hz単位)
	"ACL_FREQ_OPT8"					: 0x1A17,	# OPT8の周波数 (Hz単位)
	"ACL_FREQ_D"					: 0x1A18,	# D相の周波数  (Hz単位)
	"ACL_FIFO_FULL"					: 0x1A19,	# FIFO Fullステータス

	# Ver.7.1.10
	"ACL_BOARD_TEMP"				: 0x1A1A,	# 基板温度情報
	"ACL_FPGA_TEMP"					: 0x1A1B,	# FPGA温度情報

	# APX-3312  ----------------------------------------------------------------------------------
	"ACL_3312_CAMERA_STATE"			: 0x3001,	# カメラの状態確認(Setで確認/Getで状態読み出し)
	"ACL_3312_STATUS_REG"			: 0x3002,	# カメラの状態確認(SetでReset/Getで状態読み出し)
	"ACL_3312_ENCODER_REG"			: 0x3003,	# カメラの状態確認(SetでReset/Getで状態読み出し)
	"ACL_3312_BOARD_RECONFIG"		: 0x3004,	# ボードリコンフィグ
	"ACL_3312_MEMORY_RESET"			: 0x3005,	# ボードメモリリセット
	#pragma deprecated(ACL_3312_EXPRESS_LINK)
	"_ACL_3312_EXPRESS_LINK"		: 0x3006,	# Expressリンク
	#pragma deprecated(ACL_3312_FPGA_VERSION)
	"_ACL_3312_FPGA_VERSION"		: 0x3007,	# APX-3312 FPGAバージョン

	"ACL_3312_LUT_EN"				: 0x3008,	# LUT 有効/無効
	"ACL_3312_LUT_VALUE"			: 0x3009,	# LUT設定値

	#pragma deprecated(ACL_3312_IMAGE_PTR)	
	"_ACL_3312_IMAGE_PTR"			: 0x3020,	# 画像バッファの先頭アドレス


	# APX-3313  ----------------------------------------------------------------------------------
	#pragma deprecated(ACL_3313_EXPRESS_LINK)
	"_ACL_3313_EXPRESS_LINK"		: 0x4001,	# Expressリンク
	#pragma deprecated(ACL_3313_FPGA_VERSION)
	"_ACL_3313_FPGA_VERSION"		: 0x4002,	# APX-3313 FPGAバージョン
	"ACL_3313_HIGH_CLIP"			: 0x4003,	# ハイクリップ (0=無効/1=10bit/2=12bit)
	"ACL_3313_TAP_ARRANGE"			: 0x4004,	# タップ間並び替え
	"ACL_3313_TAP_DIRECTION"		: 0x4005,	# データ出力方向
	"ACL_3313_ARRANGE_XSIZE"		: 0x4006,	# 並び替え 総Xサイズ
	"ACL_3313_LVAL_DELAY"			: 0x4007,	# LVALディレイ
	"ACL_3313_LINE_REVERSE"			: 0x4008,	# ライン反転
	"ACL_3313_CAMERA_STATE"			: 0x4009,	# カメラ接続状態
	"ACL_3313_STATUS_REG"			: 0x400A,	# カメラの状態確認(SetでReset/Getで状態読み出し) /* Ver3.2.0 */
	"ACL_3313_ENCODER_REG"			: 0x400B,	# エンコーダの状態確認(SetでReset/Getで状態読み出し) /* Ver3.2.0 */

	#pragma deprecated(ACL_3313_IMAGE_PTR)
	"_ACL_3313_IMAGE_PTR"				: 0x4020,	# 画像バッファの先頭アドレス


	# APX-3318  ----------------------------------------------------------------------------------
	#pragma deprecated(ACL_3318_EXPRESS_LINK)
	"_ACL_3318_EXPRESS_LINK"		: 0x5001,	# Expressリンク
	#pragma deprecated(ACL_3318_FPGA_VERSION)
	"_ACL_3318_FPGA_VERSION"		: 0x5002,	# APX-3318 FPGAバージョン
	"ACL_3318_HIGH_CLIP"			: 0x5003,	# ハイクリップ (0=無効/1=10bit/2=12bit)
	"ACL_3318_TAP_ARRANGE"			: 0x5004,	# タップ間並び替え
	"ACL_3318_TAP_DIRECTION"		: 0x5005,	# データ出力方向
	"ACL_3318_ARRANGE_XSIZE"		: 0x5006,	# 並び替え 総Xサイズ
	"ACL_3318_LVAL_DELAY"			: 0x5007,	# LVALディレイ
	"ACL_3318_LINE_REVERSE"			: 0x5008,	# ライン反転
	"ACL_3318_CAMERA_STATE"			: 0x5009,	# カメラ接続状態 
	"ACL_3318_STATUS_REG"			: 0x500A,	# カメラの状態確認(SetでReset/Getで状態読み出し) /* Ver3.2.0 */
	"ACL_3318_ENCODER_REG"			: 0x500B,	# エンコーダの状態確認(SetでReset/Getで状態読み出し) /* Ver3.2.0 */

	#pragma deprecated(ACL_3318_IMAGE_PTR)
	"_ACL_3318_IMAGE_PTR"			: 0x5020,	# 画像バッファの先頭アドレス

	# APX-3311
	#pragma deprecated(ACL_3311_IMAGE_PTR)
	"_ACL_3311_IMAGE_PTR"			: 0x6020	# 画像バッファの先頭アドレス
	}

def get_setting_value(setting_key):
    return setting_code_dict[setting_key]

def get_setting_name(setting_value):
    return [k for k, v in setting_code_dict.items() if v == setting_value][0]


# ******************************************************************
# 	DLLプロトタイプ定義
# ******************************************************************
# ボード情報の取得

#AVALCAPLIB2DLL int WINAPI AcapGetBoardInfo( PACAPBOARDINFO pAcapBoardInfo );
_acap.AcapGetBoardInfo.argtypes = [POINTER(ACAPBOARDINFO)]
_acap.AcapGetBoardInfo.restype = c_int
def AcapGetBoardInfo():
	"""
	Get board information
	returns[0]: int	:			Succeed:1  Fail:0
	returns[1]: ACAPBOARDINFO :	Structure which stores board information
	"""
	bdInfo = ACAPBOARDINFOEX()
	ret = _acap.AcapGetBoardInfoEx(byref(bdInfo))
	
	return ret, bdInfo

#AVALCAPLIB2DLL int WINAPI AcapGetBoardInfoEx( PACAPBOARDINFOEX pAcapBoardInfoEx );
_acap.AcapGetBoardInfoEx.argtypes = [POINTER(ACAPBOARDINFOEX)]
_acap.AcapGetBoardInfoEx.restype = c_int
def AcapGetBoardInfoEx():
	"""
	Get board information (extend)
	returns[0]: int	:				Succeed:1  Fail:0
	returns[1]: ACAPBOARDINFOEX :	Structure which stores board information
	"""
	bdInfo = ACAPBOARDINFOEX()
	ret = _acap.AcapGetBoardInfoEx(byref(bdInfo))

	return ret, bdInfo

#AVALCAPLIB2DLL int WINAPI AcapGetBoardInfoEx256( PACAPBOARDINFOEX_256 pAcapBoardInfoEx256 );
_acap.AcapGetBoardInfoEx256.argtypes = [POINTER(ACAPBOARDINFOEX_256)]
_acap.AcapGetBoardInfoEx256.restype = c_int
def AcapGetBoardInfoEx256():
	"""
	Get board information (extend)
	returns[0]: int	:					Succeed:1  Fail:0
	returns[1]: ACAPBOARDINFOEX_256 :	Structure which stores board information
	"""
	bdInfo = ACAPBOARDINFOEX_256()
	ret = _acap.AcapGetBoardInfoEx256(byref(bdInfo))
	
	return ret, bdInfo

# デバイスオープン
#AVALCAPLIB2DLL HANDLE WINAPI AcapOpen( char* lpBoardName, int nBoardNo, int nCh );
_acap.AcapOpen.argtypes = [c_char_p, c_int, c_int]
_acap.AcapOpen.restype = c_int
def AcapOpen(lpBoardName, nBoardNo, nCh):
	"""
	Open device
	param boardName:	bytes	:Specify the board name you are going to use
	param nBoardNo:		int		:Specify board number which is set up
	param nCh:			int		:1:CH1 / 2:CH2 / 3:CH3 / 4:CH4, 0: All channel (APX-3312/3302/3324/3326)
	returns: int				:Succeeded : Library handle, Failed : INVALID_HANDLE_VALUE (-1)
	"""
	if (type(lpBoardName) is str):
		lpBoardName = to_string_buffer(lpBoardName)

	return _acap.AcapOpen(lpBoardName, nBoardNo, nCh)

# デバイスクローズ
#AVALCAPLIB2DLL int WINAPI AcapClose( HANDLE hDev, int nCh );
_acap.AcapClose.argtypes = [c_int, c_int]
_acap.AcapClose.restype = c_int
def AcapClose(hDev, nCh):
	"""
	Close device
	param hDev:	int	:Library handle
	param nCh:	int	:The channel to close  1:CH1 / 2:CH2 / 3:CH3 / 4:CH4, 0: All channel (APX-3312/3302/3324/3326)
	returns: int	:Succeeded : 1, Failed : 0
	"""
	return _acap.AcapClose(hDev, nCh)

# 画像情報設定
#AVALCAPLIB2DLL int WINAPI AcapSetInfo( HANDLE hDev, int nCh, ULONG ulType, int nMemNum, int nValue );
_acap.AcapSetInfo.argtypes = [c_int, c_int, c_ulong, c_int, c_int]
_acap.AcapSetInfo.restype = c_int
def AcapSetInfo( hDev, nCh, ulType, nMemNum, nValue):
	return _acap.AcapSetInfo(hDev, nCh, ulType, nMemNum, nValue)
# 画像情報取得
#AVALCAPLIB2DLL int WINAPI AcapGetInfo( HANDLE hDev, int nCh, ULONG ulType, int nMemNum, int* npValue );
_acap.AcapGetInfo.argtypes = [c_int, c_int, c_ulong, c_int, POINTER(c_int)]
_acap.AcapGetInfo.restype = c_int
def AcapGetInfo( hDev, nCh, ulType, nMemNum = 0):
	nValue = c_int()
	ret = _acap.AcapGetInfo(hDev, nCh, ulType, nMemNum, byref(nValue))
	return ret, nValue.value

# 画像バッファアドレス設定
#AVALCAPLIB2DLL int WINAPI AcapSetBufferAddress( HANDLE hDev, int nCh, ULONG ulType, int nMemNum, void* pAddress );
_acap.AcapSetBufferAddress.argtypes = [c_int, c_int, c_ulong, c_int, c_void_p]
_acap.AcapSetBufferAddress.restype = c_int
def AcapSetBufferAddress( hDev, nCh, ulType, nMemNum, pAddress):
	return _acap.AcapSetBufferAddress(hDev, nCh, ulType, nMemNum, pAddress)

# 画像バッファアドレス取得
#AVALCAPLIB2DLL int WINAPI AcapGetBufferAddress( HANDLE hDev, int nCh, ULONG ulType, int nMemNum, void* pAddress );
_acap.AcapGetBufferAddress.argtypes = [c_int, c_int, c_ulong, c_int, c_void_p]
_acap.AcapGetBufferAddress.restype = c_int
def AcapGetBufferAddress( hDev, nCh, ulType, nMemNum):
	pAddress = c_void_p()
	ret = _acap.AcapGetBufferAddress(hDev, nCh, ulType, nMemNum, byref(pAddress))
	return ret, pAddress
# 設定値の反映
#AVALCAPLIB2DLL int WINAPI AcapReflectParam( HANDLE hDev, int nCh );
_acap.AcapReflectParam.argtypes = [c_int, c_int]
_acap.AcapReflectParam.restype = c_int
def AcapReflectParam( hDev, nCh):
	ret = _acap.AcapReflectParam(hDev, nCh)
	return ret
# 画像入力開始
#AVALCAPLIB2DLL int WINAPI AcapGrabStart( HANDLE hDev, int nCh, int nInputNum );
_acap.AcapGrabStart.argtypes = [c_int, c_int, c_int]
_acap.AcapGrabStart.restype = c_int
def AcapGrabStart( hDev, nCh, nInputNum):
	return _acap.AcapGrabStart(hDev, nCh, nInputNum)

#画像入力停止
#AVALCAPLIB2DLL int WINAPI AcapGrabStop( HANDLE hDev, int nCh );
_acap.AcapGrabStop.argtypes = [c_int, c_int]
_acap.AcapGrabStop.restype = c_int
def AcapGrabStop( hDev, nCh):
	return _acap.AcapGrabStop(hDev, nCh)
#画像入力強制停止
#AVALCAPLIB2DLL int WINAPI AcapGrabAbort( HANDLE hDev, int nCh );
_acap.AcapGrabAbort.argtypes = [c_int, c_int]
_acap.AcapGrabAbort.restype = c_int
def AcapGrabAbort( hDev, nCh):
	return _acap.AcapGrabAbort(hDev, nCh)

# iniファイルの編集
#AVALCAPLIB2DLL int WINAPI AcapSelectFile( HANDLE hDev, int nCh, char* lpFileName, int nReadWriteFlag );
_acap.AcapSelectFile.argtypes = [c_int, c_int, c_char_p, c_int]
_acap.AcapSelectFile.restype = c_int
def AcapSelectFile( hDev, nCh, lpFileName, nReadWriteFlag = 0):
	return _acap.AcapSelectFile(hDev, nCh, to_string_buffer(lpFileName), nReadWriteFlag)

# DMA方法の設定
#AVALCAPLIB2DLL int WINAPI AcapSetDmaOption( HANDLE hDev, int nCh, int nDmaMemNum, PACAPDMAINFO pAcapDmaInfo );
_acap.AcapSetDmaOption.argtypes = [c_int, c_int, c_int, POINTER(ACAPDMAINFO)]
_acap.AcapSetDmaOption.restype = c_int
def AcapSetDmaOption( hDev, nCh, nDmaMemNum, pAcapDmaInfo):
	return _acap.AcapSetDmaOption(hDev, nCh, nDmaMemNum, pAcapDmaInfo)

# DMA方法の取得
#AVALCAPLIB2DLL int WINAPI AcapGetDmaOption( HANDLE hDev, int nCh, int nDmaMemIndex, PACAPDMAINFO pAcapDmaInfo );
_acap.AcapGetDmaOption.argtypes = [c_int, c_int, c_int, POINTER(ACAPDMAINFO)]
_acap.AcapGetDmaOption.restype = c_int
def AcapGetDmaOption( hDev, nCh, nDmaMemNum):
	pAcapDmaInfo = ACAPDMAINFO()
	ret = _acap.AcapSetDmaOption(hDev, nCh, nDmaMemNum, byref(pAcapDmaInfo))
	return ret, pAcapDmaInfo


# トリガシャッタ設定
#AVALCAPLIB2DLL int WINAPI AcapSetShutterTrigger( HANDLE hDev, int nCh, ULONG ulExpCycle, ULONG ulExposure,
#															int nExpPol, int nExpUnit, int nCCSel );
_acap.AcapSetShutterTrigger.argtypes = [c_int, c_int, c_ulong, c_ulong, c_int, c_int, c_int]
_acap.AcapSetShutterTrigger.restype = c_int
def AcapSetShutterTrigger( hDev, nCh, ulExpCycle, ulExposure, nExpPol, nExpUnit, nCCSel):
	return _acap.AcapSetShutterTrigger(hDev, nCh, ulExpCycle, ulExposure, nExpPol, nExpUnit, nCCSel)

# トリガシャッタ取得
#AVALCAPLIB2DLL int WINAPI AcapGetShutterTrigger( HANDLE hDev, int nCh, ULONG* ulpExpCycle, ULONG* ulpExposure,
#															int* npExpPol, int* npExpUnit, int* npCCSel );
_acap.AcapGetShutterTrigger.argtypes = [c_int, c_int, POINTER(c_ulong), POINTER(c_ulong), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
_acap.AcapGetShutterTrigger.restype = c_int
def AcapGetShutterTrigger( hDev, nCh):
	ulExpCycle = c_ulong()
	ulExposure = c_ulong()
	nExpPol = c_int()
	nExpUnit = c_int()
	nCCSel = c_int()
	ret = _acap.AcapGetShutterTrigger(hDev, nCh, byref(ulExpCycle), byref(ulExposure), byref(nExpPol), byref(nExpUnit), byref(nCCSel))
	return ret, ulExpCycle.value, ulExposure.value, nExpPol.value, nExpUnit.value, nCCSel.value

# ライントリガ設定
#AVALCAPLIB2DLL int WINAPI AcapSetLineTrigger( HANDLE hDev, int nCh, ULONG ulExpCycle, ULONG ulExposure, int nExpPol );
_acap.AcapSetLineTrigger.argtypes = [c_int, c_int, c_ulong, c_ulong, c_int]
_acap.AcapSetLineTrigger.restype = c_int
def AcapSetLineTrigger( hDev, nCh, ulExpCycle, ulExposure, nExpPol):
	return _acap.AcapSetLineTrigger(hDev, nCh, ulExpCycle, ulExposure, nExpPol)

# ライントリガ取得
#AVALCAPLIB2DLL int WINAPI AcapGetLineTrigger( HANDLE hDev, int nCh, ULONG* ulpExpCycle, ULONG* ulpExposure, int* npExpPol );
_acap.AcapGetLineTrigger.argtypes = [c_int, c_int, POINTER(c_ulong), POINTER(c_ulong), POINTER(c_int)]
_acap.AcapGetLineTrigger.restype = c_int
def AcapGetLineTrigger( hDev, nCh):
	ulExpCycle = c_ulong()
	ulExposure = c_ulong()
	nExpPol = c_int()
	ret = _acap.AcapGetLineTrigger(hDev, nCh, byref(ulExpCycle), byref(ulExposure), byref(nExpPol))
	return ret, ulExpCycle.value, ulExposure.value, nExpPol.value


# 外部トリガ設定
#AVALCAPLIB2DLL int WINAPI AcapSetExternalTrigger( HANDLE hDev, int nCh, int nExtTrgEn,
#														int nExtTrgMode, int nExtTrgDly, int nExtTrgChatter, ULONG ulTimeout );
_acap.AcapSetExternalTrigger.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_ulong]
_acap.AcapSetExternalTrigger.restype = c_int
def AcapSetExternalTrigger( hDev, nCh, nExtTrgEn, nExtTrgMode, nExtTrgDly, nExtTrgChatter, ulTimeout):
	return _acap.AcapSetExternalTrigger(hDev, nCh, nExtTrgEn, nExtTrgMode, nExtTrgDly, nExtTrgChatter, ulTimeout)

# 外部トリガ取得
#AVALCAPLIB2DLL int WINAPI AcapGetExternalTrigger( HANDLE hDev, int nCh, int* npExtTrgEn,
#														int* npExtTrgMode, int* npExtTrgDly, int* npExtTrgChatter, ULONG* ulpTimeout );
_acap.AcapGetExternalTrigger.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_ulong)]
_acap.AcapGetExternalTrigger.restype = c_int
def AcapGetExternalTrigger( hDev, nCh):
	npExtTrgEn = c_int()
	npExtTrgMode = c_int()
	npExtTrgDly = c_int()
	npExtTrgChatter = c_int()
	ulpTimeout = c_ulong()
	ret = _acap.AcapGetExternalTrigger(hDev, nCh, byref(npExtTrgEn), byref(npExtTrgMode), byref(npExtTrgDly), byref(npExtTrgChatter), byref(ulpTimeout))
	return ret, npExtTrgEn.value, npExtTrgMode.value, npExtTrgDly.value, npExtTrgChatter.value, ulpTimeout.value

# ストロボ設定
#AVALCAPLIB2DLL int WINAPI AcapSetStrobe( HANDLE hDev, int nCh, int nStrobeEn, WORD wStrobeDelay, WORD wStrobeTime );
_acap.AcapSetStrobe.argtypes = [c_int, c_int, c_int, c_ushort, c_ushort]
_acap.AcapSetStrobe.restype = c_int
def AcapSetStrobe( hDev, nCh, nStrobeEn, wStrobeDelay, wStrobeTime):
	return _acap.AcapSetStrobe(hDev, nCh, nStrobeEn, wStrobeDelay, wStrobeTime)

# ストロボ取得
#AVALCAPLIB2DLL int WINAPI AcapGetStrobe( HANDLE hDev, int nCh, int* npStrobeEn, WORD* wpStrobeDelay, WORD* wpStrobeTime );
_acap.AcapGetStrobe.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_ushort), POINTER(c_ushort)]
_acap.AcapGetStrobe.restype = c_int
def AcapGetStrobe( hDev, nCh):
	npStrobeEn = c_int()
	wpStrobeDelay = c_ushort()
	wpStrobeTime = c_ushort()
	ret = _acap.AcapGetStrobe(hDev, nCh, byref(npStrobeEn), byref(wpStrobeDelay), byref(wpStrobeTime))
	return ret, npStrobeEn.value, wpStrobeDelay.value, wpStrobeTime.value

# 汎用入出力(GPIO)設定
#AVALCAPLIB2DLL int WINAPI AcapSetGPIO( HANDLE hDev, int nCh, int nInOut, int nMode, int nLevel );
_acap.AcapSetGPIO.argtypes = [c_int, c_int, c_int, c_int, c_int]
_acap.AcapSetGPIO.restype = c_int
def AcapSetGPIO( hDev, nCh, nInOut, nMode, nLevel):
	return _acap.AcapSetGPIO(hDev, nCh, nInOut, nMode, nLevel)

# エンコーダ設定
#AVALCAPLIB2DLL int WINAPI AcapSetEncoder( HANDLE hDev, int nCh, int nEncEnable, int nEncMode, int nEncStart, int nEncPhase,
#												int nEncDirection, int nZPhaseEnable, ULONG ulCompare1, ULONG ulCompare2 );
_acap.AcapSetEncoder.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_ulong, c_ulong]
_acap.AcapSetEncoder.restype = c_int
def AcapSetEncoder( hDev, nCh, nEncEnable, nEncMode, nEncStart, nEncPhase, nEncDirection, nZPhaseEnable, ulCompare1, ulCompare2):
	return _acap.AcapSetEncoder(hDev, nCh, nEncEnable, nEncMode, nEncStart, nEncPhase, nEncDirection, nZPhaseEnable, ulCompare1, ulCompare2)


# エンコーダ取得
#AVALCAPLIB2DLL int WINAPI AcapGetEncoder( HANDLE hDev, int nCh, int* npEncEnable, int* npEncMode, int* npEncStart, int* npEncPhase,
#												int* npEncDirection, int* npZPhaseEnable, ULONG* ulpCompare1, ULONG* ulpCompare2, ULONG* ulpComp2Count );
_acap.AcapGetEncoder.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_ulong), POINTER(c_ulong), POINTER(c_ulong)]
_acap.AcapGetEncoder.restype = c_int
def AcapGetEncoder( hDev, nCh):
	npEncEnable = c_int()
	npEncMode = c_int()
	npEncStart = c_int()
	npEncPhase = c_int()
	npEncDirection = c_int()
	npZPhaseEnable = c_int()
	ulpCompare1 = c_ulong()
	ulpCompare2 = c_ulong()
	ulpComp2Count = c_ulong()
	ret = _acap.AcapGetEncoder(hDev, nCh, byref(npEncEnable), byref(npEncMode), byref(npEncStart), byref(npEncPhase), byref(npEncDirection), byref(npZPhaseEnable), byref(ulpCompare1), byref(ulpCompare2), byref(ulpComp2Count))
	return ret, npEncEnable.value, npEncMode.value, npEncStart.value, npEncPhase.value, npEncDirection.value, npZPhaseEnable.value, ulpCompare1.value, ulpCompare2.value, ulpComp2Count.value
# 画像ビット変換
#AVALCAPLIB2DLL int WINAPI AcapImageConvert( HANDLE hDev, int nCh, ACAPSRCIMAGE AcapSrcImage, int nDivUni, int nMode, PACAPDSTIMAGE pAcapDstImage );
_acap.AcapImageConvert.argtypes = [c_int, c_int, ACAPSRCIMAGE, c_int, c_int, POINTER(ACAPDSTIMAGE)]
_acap.AcapImageConvert.restype = c_int
def AcapImageConvert( hDev, nCh, AcapSrcImage, nDivUni, nMode):
	pAcapDstImage = ACAPDSTIMAGE()
	ret = _acap.AcapImageConvert(hDev, nCh, AcapSrcImage, nDivUni, nMode, byref(pAcapDstImage))
	return ret, pAcapDstImage.value

# 画像ビット変換 (ROI)
#AVALCAPLIB2DLL int WINAPI AcapRoiConvert( HANDLE hDev, int nCh, ACAPROIIMAGE AcapSrcRoiImage, ACAPROIIMAGE AcapDstRoiImage );
_acap.AcapRoiConvert.argtypes = [c_int, c_int, ACAPROIIMAGE, ACAPROIIMAGE]
_acap.AcapRoiConvert.restype = c_int
def AcapRoiConvert( hDev, nCh, AcapSrcRoiImage, AcapDstRoiImage):
	return _acap.AcapRoiConvert(hDev, nCh, AcapSrcRoiImage, AcapDstRoiImage)

# カメラリンク設定
#AVALCAPLIB2DLL int WINAPI AcapSetBitAssign( HANDLE hDev, int nCh, int nCameraBit, int nBitShift, int nTapNum, int nTapDir, int nCLMask  )
#_acap.AcapSetBitAssign.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_int]
#_acap.AcapSetBitAssign.restype = c_int
#def AcapSetBitAssign( hDev, nCh, nCameraBit, nBitShift, nTapNum, nTapDir, nCLMask):
#	return _acap.AcapSetBitAssign(hDev, nCh, nCameraBit, nBitShift, nTapNum, nTapDir, nCLMask)

# カメラリンク取得
#AVALCAPLIB2DLL int WINAPI AcapGetBitAssign( HANDLE hDev, int nCh, int* npCameraBit, int* npBitShift,
#																		int* npTapNum, int* npTapDir, int* npCLMask  );
_acap.AcapGetBitAssign.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
_acap.AcapGetBitAssign.restype = c_int
def AcapGetBitAssign( hDev, nCh):
	npCameraBit = c_int()
	npBitShift = c_int()
	npTapNum = c_int()
	npTapDir = c_int()
	npCLMask = c_int()
	ret = _acap.AcapGetBitAssign(hDev, nCh, byref(npCameraBit), byref(npBitShift), byref(npTapNum), byref(npTapDir), byref(npCLMask))
	return ret, npCameraBit.value, npBitShift.value, npTapNum.value, npTapDir.value, npCLMask.value

# カメラリンク設定(拡張)
#AVALCAPLIB2DLL int WINAPI AcapSetBitAssignEx( HANDLE hDev, int nCh, PBITASSIGNINFO pBitAssignInfo );
_acap.AcapSetBitAssignEx.argtypes = [c_int, c_int, POINTER(BITASSIGNINFO)]
_acap.AcapSetBitAssignEx.restype = c_int
def AcapSetBitAssignEx( hDev, nCh, pBitAssignInfo):
	return _acap.AcapSetBitAssign(hDev, nCh, pBitAssignInfo)

# カメラリンク取得(拡張)
#AVALCAPLIB2DLL int WINAPI AcapGetBitAssignEx( HANDLE hDev, int nCh, PBITASSIGNINFO pBitAssignInfo );
_acap.AcapGetBitAssignEx.argtypes = [c_int, c_int, POINTER(BITASSIGNINFO)]
_acap.AcapGetBitAssignEx.restype = c_int
def AcapGetBitAssignEx( hDev, nCh):
	pBitAssignInfo = BITASSIGNINFO()
	ret = _acap.AcapGetBitAssignEx(hDev, nCh, byref(pBitAssignInfo))
	return ret, pBitAssignInfo

# フレーム番号の取得
#AVALCAPLIB2DLL int WINAPI AcapGetFrameNo( HANDLE hDev, int nCh, int* npFramet, int* npLine, int* npIndex );
_acap.AcapGetFrameNo.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int)]
_acap.AcapGetFrameNo.restype = c_int
def AcapGetFrameNo( hDev, nCh):
	npFramet = c_int()
	npLine = c_int()
	npIndex = c_int()
	ret = _acap.AcapGetFrameNo(hDev, nCh, byref(npFramet), byref(npLine), byref(npIndex))
	return ret, npFramet.value, npLine.value, npIndex.value
# イベントの登録
#AVALCAPLIB2DLL int WINAPI AcapSetEvent( HANDLE hDev, int nCh, DWORD dwEvent, BOOL bEventEnable );
_acap.AcapSetEvent.argtypes = [c_int, c_int, c_ulong, c_bool]
_acap.AcapSetEvent.restype = c_int
def AcapSetEvent( hDev, nCh, dwEvent, bEventEnable):
	return _acap.AcapSetEvent(hDev, nCh, dwEvent, bEventEnable)
# イベントの待機
#AVALCAPLIB2DLL int WINAPI AcapWaitEvent( HANDLE hDev, int nCh, DWORD dwEvent, DWORD dwTimeout );
_acap.AcapWaitEvent.argtypes = [c_int, c_int, c_ulong, c_ulong]
_acap.AcapWaitEvent.restype = c_int
def AcapWaitEvent( hDev, nCh, dwEvent, dwTimeout):
	return _acap.AcapWaitEvent(hDev, nCh, dwEvent, dwTimeout)
# コールバック関数の登録
#AVALCAPLIB2DLL int WINAPI AcapRegistCallback( HANDLE hDev, int nCh, DWORD dwEvent, EVENT_FUNC fEventFunc );

# コールバック関数の登録(拡張)
#AVALCAPLIB2DLL int WINAPI AcapRegistCallbackEx( HANDLE hDev, int nCh, DWORD dwEvent, EVENT_FUNC_EX fEventFuncEx, void* pParam );

# シリアルオープン
#AVALCAPLIB2DLL int WINAPI AcapSerialOpen( HANDLE hDev, int nCh );
_acap.AcapSerialOpen.argtypes = [c_int, c_int]
_acap.AcapSerialOpen.restype = c_int
def AcapSerialOpen( hDev, nCh):
	return _acap.AcapSerialOpen(hDev, nCh)

# シリアルクローズ
#AVALCAPLIB2DLL int WINAPI AcapSerialClose( HANDLE hDev, int nCh );
_acap.AcapSerialClose.argtypes = [c_int, c_int]
_acap.AcapSerialClose.restype = c_int
def AcapSerialClose( hDev, nCh):
	return _acap.AcapSerialClose(hDev, nCh)

# シリアルライト(送信[ボード→カメラ])
#AVALCAPLIB2DLL int WINAPI AcapSerialWrite( HANDLE hDev, int nCh, BOOL bAscii, 
#												char* cpWriteCommand, char* cpStartStr, char* cpEndStr );
_acap.AcapSerialWrite.argtypes = [c_int, c_int, c_bool, c_char_p, c_char_p, c_char_p]
_acap.AcapSerialWrite.restype = c_int
def AcapSerialWrite( hDev, nCh, bAscii, cpWriteCommand, cpStartStr, cpEndStr):
	cpWriteCommand = to_string_buffer(cpWriteCommand)
	cpStartStr = to_string_buffer(cpStartStr)
	cpEndStr = to_string_buffer(cpEndStr)
	return _acap.AcapSerialWrite(hDev, nCh, bAscii, cpWriteCommand, cpStartStr, cpEndStr)

# シリアルリード(受信[カメラ→ボード])
#AVALCAPLIB2DLL int WINAPI AcapSerialRead( HANDLE hDev, int nCh, BOOL bAscii, ULONG ulTimeout, int nBufferSize,
#												char* cpEndStr, char* cpReadCommand, int* npByte );
_acap.AcapSerialRead.argtypes = [c_int, c_int, c_bool, c_ulong, c_int, c_char_p, c_char_p, POINTER(c_int)]
_acap.AcapSerialRead.restype = c_int
def AcapSerialRead( hDev, nCh, bAscii, ulTimeout, nBufferSize, cpEndStr):
	#cpReadCommand = c_char() * ACL_MAX_BUFF
	cpReadCommand = create_string_buffer(nBufferSize)
	npByte = c_int()
	ret = _acap.AcapSerialRead(hDev, nCh, bAscii, ulTimeout, nBufferSize, to_string_buffer(cpEndStr), cpReadCommand, byref(npByte))
	return ret, cpReadCommand.value.decode(), npByte.value





#AVALCAPLIB2DLL int WINAPI AcapSerialSetParameter( HANDLE hDev, int nCh, int nBaudRate, int nDataBit,
#												  int nParity, int nStopBit, int nFlow );
_acap.AcapSerialSetParameter.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_int]
_acap.AcapSerialSetParameter.restype = c_int
def AcapSerialSetParameter( hDev, nCh, nBaudRate, nDataBit, nParity, nStopBit, nFlow):
	return _acap.AcapSerialSetParameter(hDev, nCh, nBaudRate, nDataBit, nParity, nStopBit, nFlow)

#AVALCAPLIB2DLL int WINAPI AcapSerialGetParameter( HANDLE hDev, int nCh, int* npBaudRate, int* npDataBit,
#												  int* npParity, int* npStopBit, int* npFlow );
_acap.AcapSerialGetParameter.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
_acap.AcapSerialGetParameter.restype = c_int
def AcapSerialGetParameter( hDev, nCh):
	npBaudRate = c_int()
	npDataBit = c_int()
	npParity = c_int()
	npStopBit = c_int()
	npFlow = c_int()

	ret = _acap.AcapSerialGetParameter(hDev, nCh, byref(npBaudRate), byref(npDataBit), byref(npParity), byref(npStopBit), byref(npFlow))
	return ret, npBaudRate.value, npDataBit.value, npParity.value, npStopBit.value, npFlow.value

# ファイルバージョンの取得
#AVALCAPLIB2DLL int WINAPI AcapGetFileVersion( char* cpFileName, char* pVerRev );
_acap.AcapGetFileVersion.argtypes = [ c_char_p, c_char_p]
_acap.AcapGetFileVersion.restype = c_int
def AcapGetFileVersion( lpFileName):
	pVerRev = create_string_buffer(ACL_MAX_BUFF)
	ret = _acap.AcapGetFileVersion(to_string_buffer(lpFileName), pVerRev)
	return ret, pVerRev.value.decode()

# エラーコード
#AVALCAPLIB2DLL void WINAPI AcapGetLastErrorCode( PACAPERRORINFO pAcapErrInfo, BOOL bErrReset );
_acap.AcapGetLastErrorCode.argtypes = [POINTER(ACAPERRORINFO), c_bool]
def AcapGetLastErrorCode(bErrReset) -> (int, ACAPERRORINFO):
	pAcapErrInfo = ACAPERRORINFO()
	ret = _acap.AcapGetLastErrorCode(byref(pAcapErrInfo), bErrReset)
	return ret, pAcapErrInfo

# レジスタへ値を設定
#AVALCAPLIB2DLL int WINAPI AcapSetReg( HANDLE hDev, int nCh, int nRegType, DWORD dwAddress, DWORD dwValue );
_acap.AcapSetReg.argtypes = [c_int, c_int, c_int, c_ulong, c_ulong]
_acap.AcapSetReg.restype = c_int
def AcapSetReg( hDev, nCh, nRegType, dwAddress, dwValue):
	return _acap.AcapSetReg(hDev, nCh, nRegType, dwAddress, dwValue)

# レジスタから値の取得
#AVALCAPLIB2DLL int WINAPI AcapGetReg( HANDLE hDev, int nCh, int nRegType, DWORD dwAddress, DWORD* dwpValue );
_acap.AcapGetReg.argtypes = [c_int, c_int, c_int, c_ulong, POINTER(c_ulong)]
_acap.AcapGetReg.restype = c_int
def AcapGetReg( hDev, nCh, nRegType, dwAddress, dwValue):
	dwpValue = c_ulong()
	ret = _acap.AcapGetReg(hDev, nCh, nRegType, dwAddress, byref(dwValue))
	return ret, dwpValue

# 非線形DMA設定 (Ver 4.0.0)
#AVALCAPLIB2DLL int WINAPI AcapSetDmaOptionEx(HANDLE hDev, int nCh, int nMemNum, void* pAclBuffInfo);
_acap.AcapSetDmaOptionEx.argtypes = [c_int, c_int, c_int, c_void_p]
_acap.AcapSetDmaOptionEx.restype = c_int
def AcapSetDmaOptionEx( hDev, nCh, nMemNum, pAclBuffInfo):
	return _acap.AcapSetDmaOptionEx(hDev, nCh, nMemNum, pAclBuffInfo)

#AVALCAPLIB2DLL int WINAPI AcapGetDmaOptionEx(HANDLE hDev, int nCh, int nMemNum, DWORD* dwpBuffInfoSize, void* pAclBuffInfo);
_acap.AcapGetDmaOptionEx.argtypes = [c_int, c_int, c_int, POINTER(c_ulong), c_void_p]
_acap.AcapGetDmaOptionEx.restype = c_int
def AcapGetDmaOptionEx( hDev, nCh, nMemNum):
	dwpBuffInfoSize = c_ulong()
	pAclBuffInfo = c_ulong()
	ret = _acap.AcapGetDmaOptionEx(hDev, nCh, nMemNum, byref(dwpBuffInfoSize), byref(pAclBuffInfo))
	return ret, dwpBuffInfoSize.value, pAclBuffInfo.value


# GPOUT制御関数 (Ver 4.0.0)
#AVALCAPLIB2DLL int WINAPI AcapSetGPOut(HANDLE hDev, int nCh, DWORD dwOutputLevel);
_acap.AcapSetGPOut.argtypes = [c_int, c_int, c_ulong]
_acap.AcapSetGPOut.restype = c_int
def AcapSetGPOut( hDev, nCh, dwOutputLevel):
	return _acap.AcapSetGPOut(hDev, nCh, dwOutputLevel)

#AVALCAPLIB2DLL int WINAPI AcapGetGPOut(HANDLE hDev, int nCh, DWORD* dwpOutputLevel);
_acap.AcapGetGPOut.argtypes = [c_int, c_int, POINTER(c_ulong)]
_acap.AcapGetGPOut.restype = c_int
def AcapGetGPOut( hDev, nCh):
	dwOutputLevel = c_ulong()
	ret = _acap.AcapGetGPOut(hDev, nCh, byref(dwOutputLevel))
	return ret, dwOutputLevel

#AVALCAPLIB2DLL int WINAPI AcapGetBufferInfo(HANDLE hDev, int nCh, DWORD* pBufferSize, DWORD* pNumOfBuffers,
#											DWORD* pNumOfInternal, DWORD* pNumOfExternal);
_acap.AcapGetBufferInfo.argtypes = [c_int, c_int, POINTER(c_ulong), POINTER(c_ulong), POINTER(c_ulong), POINTER(c_ulong)]
_acap.AcapGetBufferInfo.restype = c_int
def AcapGetBufferInfo( hDev, nCh):
	pBufferSize = c_ulong()
	pNumOfBuffers = c_ulong()
	pNumOfInternal = c_ulong()
	pNumOfExternal = c_ulong()
	ret = _acap.AcapGetBufferInfo(hDev, nCh, byref(pBufferSize), byref(pNumOfBuffers), byref(pNumOfInternal), byref(pNumOfExternal))
	return ret, pBufferSize.value, pNumOfBuffers.value, pNumOfInternal.value, pNumOfExternal.value

#AVALCAPLIB2DLL int WINAPI AcapFileoutDebugInfo(HANDLE hDev, int nCh, char* FileName);
_acap.AcapFileoutDebugInfo.argtypes = [c_int, c_int, c_char_p]
_acap.AcapFileoutDebugInfo.restype = c_int
def AcapFileoutDebugInfo( hDev, nCh, FileName):
	return _acap.AcapFileoutDebugInfo(hDev, nCh, to_string_buffer(FileName))

#AVALCAPLIB2DLL int WINAPI AcapFileoutDebugReg(HANDLE hDev, int nCh, char* FileName);
_acap.AcapFileoutDebugReg.argtypes = [c_int, c_int, c_char_p]
_acap.AcapFileoutDebugReg.restype = c_int
def AcapFileoutDebugReg( hDev, nCh, FileName):
	return _acap.AcapFileoutDebugReg(hDev, nCh, to_string_buffer(FileName))


#未実装
#AVALCAPLIB2DLL int WINAPI AcapSetExternalTriggerEx(HANDLE hDev, int nCh, DWORD SignalSel, DWORD ExTrgDelay,
#												   DWORD ExTrgChatterHigh, DWORD ExTrgChatterLow, DWORD TimeOut);
# ****************************************************************************************

def CreateRingBuf( hDev, nCh, memNum):
	'''リングバッファの確保(30bitカラーは非対応)'''
	# , dtype = np.uint8

	# サイズ情報取得
	_, width = AcapGetInfo(hDev, nCh, ACL_X_SIZE)
	_, height = AcapGetInfo(hDev, nCh, ACL_Y_SIZE)
	#_, camera_bit = AcapGetInfo(hDev, nCh, ACL_CAM_BIT)
	_, board_bit = AcapGetInfo(hDev, nCh, ACL_BOARD_BIT)

	if board_bit == 16:
		return [ np.zeros((height, width), dtype = np.uint16) ] * memNum
	elif board_bit == 8:
		return [ np.zeros((height, width), dtype = np.uint8) ] * memNum
	else:
		return [ np.zeros((height, width, board_bit // 8), dtype = np.uint8) ] * memNum

def GetRingBufPointer( ringBuf, width, height, index):

	if len(ringBuf[index].shape) == 2:
		# モノクロのとき
		if ringBuf[index].dtype == np.uint16:
			return ringBuf[index].ctypes.data_as(POINTER((c_ushort * width) * height)).contents
		else:
			return ringBuf[index].ctypes.data_as(POINTER((c_uint8 * width) * height)).contents
	else:
		# カラーのとき
		return ringBuf[index].ctypes.data_as(POINTER((c_uint8 * ringBuf[index].shape[2] * width) * height) ).contents
	

# ****************************************************************************************



# ****************************************************************************************
# 	エラーコード
#		0xF1XX : 共通
#		0xF3XX : APX-3312 固有
# ****************************************************************************************
# 共通  ----------------------------------------------------------------------------------
ACL_RTN_OK									= 1		# エラーなし
ACL_RTN_ERROR							    = 0		# エラーあり

ACL_NO_ERROR								= 0		# エラーなし

ACL_BOARD_NOT_FOUND_ERROR					= 0xF101	# (61697L) ボードが見つからない
ACL_BOARD_NAME_ERROR						= 0xF102	# (61698L) ボード名が間違っている
ACL_BOARD_NUMBER_ERROR						= 0xF103	# (61699L) 指定したボード番号は無い　
ACL_SAME_BOARDNO_ERROR						= 0xF104	# (61700L) 同じボード番号が複数存在する
ACL_INVALID_HANDLE_ERROR					= 0xF105	# (61701L) ハンドルが不正
ACL_SELECT_CHANNEL_ERROR					= 0xF106	# (61702L) 指定したチャンネルが不正
ACL_MEM_ALLOCATE_ERROR						= 0xF107	# (61703L) メモリ確保に失敗した
ACL_INVALID_MUTEX_ERROR						= 0xF108	# (61704L) 排他用ハンドルが不正
ACL_MUTEX_LOCKED_ERROR						= 0xF109	# (61705L) 関数が排他状態になっている
ACL_FILE_NOT_FOUND_ERROR					= 0xF10A	# (61706L) 指定したファイルが見つからない
ACL_EVENT_TIMEOUT_ERROR						= 0xF10B	# (61707L) イベント待ちでタイムアウト
ACL_OPEN_ERROR								= 0xF10C	# (61708L) デバイスオープンに失敗した
ACL_CLOSE_ERROR							    = 0xF10D	# (61709L) デバイスクローズに失敗した
ACL_INITIALIZE_ERROR						= 0xF10E	# (61710L) ボードの初期化に失敗した
ACL_REFLECT_PARAM_ERROR						= 0xF10F	# (61711L) 設定値の反映に失敗した
ACL_SNAP_ERROR							    = 0xF110	# (61712L) 一画面入力に失敗した
ACL_SNAP_WAIT_ERROR							= 0xF111	# (61713L) 一画面入力待ちに失敗した
ACL_GRAB_START_ERROR						= 0xF112	# (61714L) 連続入力に失敗した
ACL_GRAB_STOP_ERROR							= 0xF113	# (61715L) 連続入力停止に失敗した
ACL_GRAB_ABORT_ERROR						= 0xF114	# (61716L) 強制停止処理に失敗した
ACL_GET_FRAMENO_ERROR						= 0xF115	# (61717L) フレーム数の取得に失敗した
ACL_SET_EVENT_ERROR							= 0xF116	# (61718L) イベント登録に失敗した
ACL_WAIT_EVENT_ERROR						= 0xF117	# (61719L) イベント待機に失敗した
ACL_REGIST_CALLBACK_ERROR					= 0xF118	# (61710L) コールバック関数登録に失敗した
ACL_SET_ENCODER_ERROR						= 0xF119	# (61721L) エンコーダの設定に失敗した
ACL_GET_ENCODER_ERROR						= 0xF11A	# (61722L) エンコーダの取得に失敗した
ACL_SET_SHUTTER_TRIGGER_ERROR				= 0xF11B	# (61723L) トリガの設定に失敗した
ACL_SET_LINE_TRIGGER_ERROR					= 0xF11C	# (61724L) ライントリガの設定に失敗した
ACL_SET_EXTERNAL_TRIGGER_ERROR				= 0xF11D	# (61725L) 外部トリガの設定に失敗した
ACL_ABORT_EXTERNAL_WAIT						= 0xF11E	# (61726L) 外部トリガ待ちを中止した
ACL_SET_STROBE_ERROR						= 0xF11F	# (61727L) ストロボの設定に失敗した
ACL_SET_GPIO_ERROR							= 0xF120	# (61728L) GPIOの設定に失敗した
ACL_IMAGE_CONVERT_ERROR						= 0xF121	# (61729L) 画像ビット変換に失敗した
ACL_SET_CAMERALINK_ERROR					= 0xF122	# (61730L) カメラリンク設定に失敗した
ACL_SET_DMA_ERROR							= 0xF123	# (61731L) DMA設定に失敗した
ACL_SERIAL_OPEN_ERROR						= 0xF124	# (61732L) シリアルオープンに失敗した
ACL_SERIAL_CLOSE_ERROR						= 0xF125	# (61733L) シリアルクローズに失敗した
ACL_SERIAL_WRITE_ERROR						= 0xF126	# (61734L) シリアル送信(書き込み)に失敗した
ACL_SERIAL_READ_ERROR						= 0xF127	# (61735L) シリアル受信(読み込み)に失敗した
ACL_SERIAL_SET_PARAM_ERROR					= 0xF128	# (61736L) シリアルパラメータの設定に失敗した
ACL_SERIAL_GET_PARAM_ERROR					= 0xF129	# (61737L) シリアルパラメータの取得に失敗した
ACL_SERIAL_HANDLE_ERROR						= 0xF12A	# (61738L) シリアルハンドルが不正
ACL_SERIAL_SELECT_PORT_ERROR				= 0xF12B	# (61739L) 指定されたポートは使用できない
ACL_SET_BUFFER_ADRS_ERROR					= 0xF12C	# (61740L) バッファアドレスの設定に失敗した
ACL_GET_BUFFER_ADRS_ERROR					= 0xF12D	# (61741L) バッファアドレスの取得に失敗した
ACL_SET_CAMERALINK_EX_ERROR					= 0xF12E	# (61742L) カメラリンク設定(拡張)に失敗した
ACL_ABORT_EVENT_WAIT						= 0xF12F	# (61743L) イベント待ちを中止した
ACL_GET_BOARDINFO_ERROR						= 0xF130	# (61744L) ボード情報の取得に失敗した
ACL_SET_INFO_ERROR							= 0xF131	# (61745L) 値の設定に失敗した
ACL_GET_INFO_ERROR							= 0xF132	# (61746L) 値の取得に失敗した
ACL_SELECT_FILE_ERROR						= 0xF133	# (61747L) イニシャルファイルの読み書きに失敗した
ACL_GET_FILE_VERSION_ERROR					= 0xF134	# (61748L) ファイルバージョンの取得に失敗した
ACL_REGIST_CALLBACK_EX_ERROR				= 0xF135	# (61749L) コールバック関数登録(拡張)に失敗した
ACL_ROI_CONVERT_ERROR						= 0xF136	# (61750L) ROI画像変換に失敗した
ACL_GET_CAMERALINK_ERROR					= 0xF137	# (61751L) カメラリンク設定の取得に失敗した
ACL_GET_DMA_ERROR							= 0xF138	# (61752L) DMA設定の取得に失敗した
ACL_GET_LINE_TRIGGER_ERROR					= 0xF139	# (61753L) ライントリガの取得に失敗した
ACL_SET_EXTERNAL_TRIGGER2_ERROR				= 0xF13A	# (61754L) 外部トリガの設定に失敗した (Ver 4.0.0)
ACL_SET_DMA_OPTION_EX_ERROR					= 0xF13B	# (61755L) 非線形DMAの設定に失敗した (Ver 4.0.0)
ACL_GET_DMA_OPTION_EX_ERROR					= 0xF13C	# (61756L) 非線形DMAの設定取得に失敗した (Ver 4.0.0)
ACL_GET_GPOUT_ERROR							= 0xF13D	# (61757L) GPOUT状態取得に失敗した (Ver 4.0.0)
ACL_GET_CAMERALINK_EX_ERROR					= 0xF13E	# (61742L) カメラリンク取得(拡張)に失敗した

ACL_PARAM_1_ERROR							= 0xF201	# (61953L) パラメータエラー (第1引数)
ACL_PARAM_2_ERROR							= 0xF202	# (61954L) パラメータエラー (第2引数)
ACL_PARAM_3_ERROR							= 0xF203	# (61955L) パラメータエラー (第3引数)
ACL_PARAM_4_ERROR							= 0xF204	# (61956L) パラメータエラー (第4引数)
ACL_PARAM_5_ERROR							= 0xF205	# (61957L) パラメータエラー (第5引数)
ACL_PARAM_6_ERROR							= 0xF206	# (61958L) パラメータエラー (第6引数)
ACL_PARAM_7_ERROR							= 0xF207	# (61959L) パラメータエラー (第7引数)
ACL_PARAM_8_ERROR							= 0xF208	# (61960L) パラメータエラー (第8引数)
ACL_PARAM_9_ERROR							= 0xF209	# (61961L) パラメータエラー (第9引数)
ACL_PARAM_10_ERROR							= 0xF20A	# (61962L) パラメータエラー (第10引数)
ACL_PARAM_11_ERROR							= 0xF20B	# (61963L) パラメータエラー (第11引数)


# APX-3312  -------------------------------------------------------------------------
ACL_3312_NO_ERROR							= 0		# エラーなし

ACL_3312_DRIVER_ERROR						= 0xF301	# (62209L) ドライバエラー
ACL_3312_INVALID_PARAM						= 0xF302	# (62210L) パラメータが不正
ACL_3312_NO_DEVICE							= 0xF303	# (62211L) デバイスが見つからない
ACL_3312_EVENT_ERROR						= 0xF304	# (62212L) イベントが登録エラー
ACL_3312_INVALID_HANDLE						= 0xF305	# (62213L) ハンドルが不正
ACL_3312_INVALID_CAPTURE					= 0xF306	# (62214L) 取り込みが不正
ACL_3312_CAPTURE_RUNNING					= 0xF307	# (62215L) 取り込み中
ACL_3312_TIME_OUT							= 0xF308	# (62216L) タイムアウト
ACL_3312_INSUFFICIENT_CONFIG				= 0xF309	# (62217L) 設定が不足している
ACL_3312_NOT_CONNECTED_CAMERA				= 0xF30A	# (62218L) カメラが接続されていない
ACL_3312_NULL_POINTER_ERROR					= 0xF30B	# (62219L) 指定されたポインタがNULLです
ACL_3312_X_SIZE_ERROR						= 0xF30C	# (62220L) 不正なXサイズが設定された
ACL_3312_Y_SIZE_ERROR						= 0xF30D	# (62221L) 不正なYサイズが設定された
ACL_3312_SET_BUFFER_ERROR					= 0xF30E	# (62222L) バッファの登録に失敗した
ACL_3312_CAMERA_KIND_ERROR					= 0xF30F	# (62223L) カメラ種別(エリア・ライン)が間違っている
ACL_3312_GRAB_ABORT							= 0xF310	# (62224L) 入力を強制停止した
ACL_3312_CH_NOT_OPENED						= 0xF311	# (61725L) 設定されたチャンネルはオープンされていない
ACL_3312_FIFO_ERROR							= 0xF312	# (61726L) FIFOエラーが発生した
ACL_3312_DMA_ERROR							= 0xF313	# (61727L) DMAエラーが発生した
ACL_3312_GET_REGISTRY_KEY_ERROR				= 0xF314	# (62228L) レジストリキーの取得に失敗
ACL_3312_NOT_CONNECTED_CAM1					= 0xF315	# (62229L) CAM1のカメラが接続されていない
ACL_3312_NOT_CONNECTED_CAM2					= 0xF316	# (62230L) CAM2のカメラが接続されていない
ACL_3312_POCL_STATUS_ERROR					= 0xF317	# (62231L) PoCLが異常状態
ACL_3312_DLL_DRIVER_ERROR					= 0xF318	# (62232L) DLLエラー
ACL_3312_INTERNAL_LIBRARY_ERROR				= 0xF319	# (62233L) ライブラリエラー
ACL_3312_UNKNOWN_ERROR						= 0xF31A	# (62234L) 不明なエラー
ACL_3312_NOT_USED_64BITOS					= 0xF31B	# (62235L) 64bitOSでは使用できない
ACL_3312_NOT_SUPPORT						= 0xF3FF	# (62463L) サポートされていない


# APX-3313  -------------------------------------------------------------------------
ACL_3313_NO_ERROR							= 0		# エラーなし

ACL_3313_DRIVER_ERROR						= 0xF401	# (62465L) ドライバエラー
ACL_3313_INVALID_PARAM						= 0xF402	# (62466L) パラメータが不正
ACL_3313_NO_DEVICE							= 0xF403	# (62467L) デバイスが見つからない
ACL_3313_EVENT_ERROR						= 0xF404	# (62468L) イベントが登録エラー
ACL_3313_INVALID_HANDLE						= 0xF405	# (62469L) ハンドルが不正
ACL_3313_INVALID_CAPTURE					= 0xF406	# (62470L) 取り込みが不正
ACL_3313_CAPTURE_RUNNING					= 0xF407	# (62471L) 取り込み中
ACL_3313_TIME_OUT							= 0xF408	# (62472L) タイムアウト
ACL_3313_INSUFFICIENT_CONFIG				= 0xF409	# (62473L) 設定が不足している
ACL_3313_NOT_CONNECTED_CAMERA				= 0xF40A	# (62474L) カメラが接続されていない
ACL_3313_NULL_POINTER_ERROR					= 0xF40B	# (62475L) 指定されたポインタがNULLです
ACL_3313_X_SIZE_ERROR						= 0xF40C	# (62476L) 不正なXサイズが設定された
ACL_3313_Y_SIZE_ERROR						= 0xF40D	# (62477L) 不正なYサイズが設定された
ACL_3313_BITSHIFT_ERROR						= 0xF40E	# (62478L) 不正なビットシフト設定された
ACL_3313_TAPNUM_ERROR						= 0xF40F	# (62479L) 不正なタップ数が設定された
ACL_3313_SET_BUFFER_ERROR					= 0xF410	# (62480L) バッファの登録に失敗した
ACL_3313_CAMERA_KIND_ERROR					= 0xF411	# (62481L) カメラ種別(エリア・ライン)が間違っている
ACL_3313_GRAB_ABORT							= 0xF412	# (62482L) 入力を強制停止した
ACL_3313_CH_NOT_OPENED						= 0xF413	# (62483L) 設定されたチャンネルはオープンされていない
ACL_3313_FIFO_ERROR							= 0xF414	# (62484L) FIFOエラーが発生した
ACL_3313_DMA_ERROR							= 0xF415	# (62485L) DMAエラーが発生した
ACL_3313_GET_REGISTRY_KEY_ERROR				= 0xF416	# (62486L) レジストリキーの取得に失敗
ACL_3313_DLL_DRIVER_ERROR					= 0xF417	# (62487L) DLLエラー
ACL_3313_INTERNAL_LIBRARY_ERROR				= 0xF418	# (62488L) ライブラリエラー
ACL_3313_UNKNOWN_ERROR						= 0xF419	# (62489L) 不明なエラー
ACL_3313_NOT_USED_64BITOS					= 0xF41A	# (62490L) 64bitOSでは使用できない
ACL_3313_NOT_SUPPORT						= 0xF4FF	# (62719L) サポートされていない


# APX-3318  -------------------------------------------------------------------------
ACL_3318_NO_ERROR							= 0		# エラーなし

ACL_3318_DRIVER_ERROR						= 0xF501	# (62465L) ドライバエラー
ACL_3318_INVALID_PARAM						= 0xF502	# (62466L) パラメータが不正
ACL_3318_NO_DEVICE							= 0xF503	# (62467L) デバイスが見つからない
ACL_3318_EVENT_ERROR						= 0xF504	# (62468L) イベントが登録エラー
ACL_3318_INVALID_HANDLE						= 0xF505	# (62469L) ハンドルが不正
ACL_3318_INVALID_CAPTURE					= 0xF506	# (62470L) 取り込みが不正
ACL_3318_CAPTURE_RUNNING					= 0xF507	# (62471L) 取り込み中
ACL_3318_TIME_OUT							= 0xF508	# (62472L) タイムアウト
ACL_3318_INSUFFICIENT_CONFIG				= 0xF509	# (62473L) 設定が不足している
ACL_3318_NOT_CONNECTED_CAMERA				= 0xF50A	# (62474L) カメラが接続されていない
ACL_3318_NULL_POINTER_ERROR					= 0xF50B	# (62475L) 指定されたポインタがNULLです
ACL_3318_X_SIZE_ERROR						= 0xF50C	# (62476L) 不正なXサイズが設定された
ACL_3318_Y_SIZE_ERROR						= 0xF50D	# (62477L) 不正なYサイズが設定された
ACL_3318_BITSHIFT_ERROR						= 0xF50E	# (62478L) 不正なビットシフト設定された
ACL_3318_TAPNUM_ERROR						= 0xF50F	# (62479L) 不正なタップ数が設定された
ACL_3318_SET_BUFFER_ERROR					= 0xF510	# (62480L) バッファの登録に失敗した
ACL_3318_CAMERA_KIND_ERROR					= 0xF511	# (62481L) カメラ種別(エリア・ライン)が間違っている
ACL_3318_GRAB_ABORT							= 0xF512	# (62482L) 入力を強制停止した
ACL_3318_CH_NOT_OPENED						= 0xF513	# (62483L) 設定されたチャンネルはオープンされていない
ACL_3318_FIFO_ERROR							= 0xF514	# (62484L) FIFOエラーが発生した
ACL_3318_DMA_ERROR							= 0xF515	# (62485L) DMAエラーが発生した
ACL_3318_GET_REGISTRY_KEY_ERROR				= 0xF516	# (62486L) レジストリキーの取得に失敗
ACL_3318_DLL_DRIVER_ERROR					= 0xF517	# (62487L) DLLエラー
ACL_3318_INTERNAL_LIBRARY_ERROR				= 0xF518	# (62488L) ライブラリエラー
ACL_3318_UNKNOWN_ERROR						= 0xF519	# (62489L) 不明なエラー
ACL_3318_NOT_USED_64BITOS					= 0xF51A	# (62490L) 64bitOSでは使用できない
ACL_3318_NOT_SUPPORT						= 0xF5FF	# (62719L) サポートされていない

# APX-3311 (Ver 4.0.0) --------------------------------------------------------------
ACL_3311_DRIVER_ERROR						= 0xF601	# (62977L) ドライバエラー
ACL_3311_INVALID_PARAM						= 0xF602	# (62978L) パラメータが不正
ACL_3311_NO_DEVICE							= 0xF603	# (62979L) デバイスが見つからない
ACL_3311_CAPTURE_RUNNING					= 0xF607	# (62983L) 取り込み中
ACL_3311_TIME_OUT							= 0xF608	# (62984L) タイムアウト
ACL_3311_NOT_CONNECTED_CAMERA				= 0xF60A	# (62986L) カメラが接続されていない
ACL_3311_NULL_POINTER_ERROR					= 0xF60B	# (62987L) 指定されたポインタがNULLです
ACL_3311_X_SIZE_ERROR						= 0xF60C	# (62988L) 不正なXサイズが設定された
ACL_3311_Y_SIZE_ERROR						= 0xF60D	# (62989L) 不正なYサイズが設定された
ACL_3311_SET_BUFFER_ERROR					= 0xF60E	# (62990L) バッファの登録に失敗した
ACL_3311_GRAB_ABORT							= 0xF610	# (62992L) 入力を強制停止した
ACL_3311_CAMERA_KIND_ERROR					= 0xF611	# (62993L) カメラ種別(エリア・ライン)が間違っている
ACL_3311_INTERNAL_LIBRARY_ERROR				= 0xF618	# (63000L) ライブラリエラー
ACL_3311_UNKNOWN_ERROR						= 0xF619	# (63001L) 不明なエラー
ACL_3311_INVALID_CAMBIT						= 0xF620	# (63008L) カメラ入力ビットが不正 
ACL_3311_OPEN_ALREADY						= 0xF621	# (63009L) 他のプロセスが開いている
ACL_3311_CREATE_THREAD						= 0xF622	# (63010L) スレッドの生成に失敗した
ACL_3311_KILL_THREAD						= 0xF623	# (63011L) スレッドの削除に失敗した
ACL_3311_INVALID_EVENT						= 0xF624	# (63012L) イベントが不正
ACL_3311_SETEVENT_ALREADY					= 0xF625	# (63013L) 既にイベントが登録されている
ACL_3311_CREATEEVENT_FAILED					= 0xF626	# (63014L) CreateEventに失敗
ACL_3311_WAITEVENT_ALREADY					= 0xF627	# (63015L) 既に待機状態もしくはABORT処理中
ACL_3311_EVENT_NOT_IDLE						= 0xF628	# (63016L) 待機中のため、解除できません
ACL_3311_CALLBACK_ALREADY					= 0xF629	# (63017L) 既にコールバックが登録されている
ACL_3311_INVALID_CC							= 0xF62A	# (63018L) CC周期や幅の関係が不正
ACL_3311_INVALID_BUFFER						= 0xF62B	# (63019L) バッファが不正
ACL_3311_INVALID_XDELAY						= 0xF62C	# (63020L) XDelayが不正
ACL_3311_INVALID_YDELAY						= 0xF62D	# (63021L) YDelayが不正
ACL_3311_INVALID_POWER_STATE				= 0xF62E	# (63022L) カメラ電源状態が異常
ACL_3311_POWER_STATE_ERROR					= 0xF62F	# (63023L) カメラ電源状態エラー
ACL_3311_POWER_ON_TIMEOUT					= 0xF630	# (63024L) カメラ電源をONしたが指定時間内にカメラクロックを検出できなかった
ACL_3311_POWER_OFF_TIMEOUT					= 0xF631	# (63025L) カメラ電源をOFFしたが指定時間経過後もカメラクロックを検出した
ACL_3311_LUT_NOT_EDIT						= 0xF632	# (63026L) BayerLUTを編集できる状態ではない
ACL_3311_LUT_EDIT_ALREADY					= 0xF633	# (63027L) 既にBayerLUTを編集中なので編集できない
ACL_3311_NOT_SUPPORT						= 0xF6FF	# (63231L) サポートされていない


# APX-3662  -------------------------------------------------------------------------
#pragma deprecated(ACL_3662_NO_ERROR)
_ACL_3662_NO_ERROR							= 0		# エラーなし

#pragma deprecated(ACL_3662_DRIVER_ERROR)
_ACL_3662_DRIVER_ERROR						= 0xF801	# (63489L) ドライバエラー
#pragma deprecated(ACL_3662_INVALID_PARAM)
_ACL_3662_INVALID_PARAM						= 0xF802	# (63490L) パラメータが不正
#pragma deprecated(ACL_3662_NO_DEVICE)
_ACL_3662_NO_DEVICE							= 0xF803	# (63491L) デバイスが見つからない
#pragma deprecated(ACL_3662_EVENT_ERROR)
_ACL_3662_EVENT_ERROR						= 0xF804	# (63492L) イベントが登録エラー
#pragma deprecated(ACL_3662_INVALID_HANDLE)
_ACL_3662_INVALID_HANDLE					= 0xF805	# (63493L) ハンドルが不正
#pragma deprecated(ACL_3662_INVALID_CAPTURE)
_ACL_3662_INVALID_CAPTURE					= 0xF806	# (63494L) 取り込みが不正
#pragma deprecated(ACL_3662_CAPTURE_RUNNING)
_ACL_3662_CAPTURE_RUNNING					= 0xF807	# (63495L) 取り込み中
#pragma deprecated(ACL_3662_TIME_OUT)
_ACL_3662_TIME_OUT							= 0xF808	# (63496L) タイムアウト
#pragma deprecated(ACL_3662_INSUFFICIENT_CONFIG)
_ACL_3662_INSUFFICIENT_CONFIG				= 0xF809	# (63497L) 設定が不足している
#pragma deprecated(ACL_3662_NOT_CONNECTED_CAMERA)
_ACL_3662_NOT_CONNECTED_CAMERA				= 0xF80A	# (63498L) カメラが接続されていない
#pragma deprecated(ACL_3662_NULL_POINTER_ERROR)
_ACL_3662_NULL_POINTER_ERROR				= 0xF80B	# (63499L) 指定されたポインタがNULLです
#pragma deprecated(ACL_3662_X_SIZE_ERROR)
_ACL_3662_X_SIZE_ERROR						= 0xF80C	# (63500L) 不正なXサイズが設定された
#pragma deprecated(ACL_3662_Y_SIZE_ERROR)
_ACL_3662_Y_SIZE_ERROR						= 0xF80D	# (63501L) 不正なYサイズが設定された
#pragma deprecated(ACL_3662_BITSHIFT_ERROR)
_ACL_3662_BITSHIFT_ERROR					= 0xF80E	# (63502L) 不正なビットシフト設定された
#pragma deprecated(ACL_3662_TAPNUM_ERROR)
_ACL_3662_TAPNUM_ERROR						= 0xF80F	# (63503L) 不正なタップ数が設定された
#pragma deprecated(ACL_3662_SET_BUFFER_ERROR)
_ACL_3662_SET_BUFFER_ERROR					= 0xF810	# (63504L) バッファの登録に失敗した
#pragma deprecated(ACL_3662_CAMERA_KIND_ERROR)
_ACL_3662_CAMERA_KIND_ERROR					= 0xF811	# (63505L) カメラ種別(エリア・ライン)が間違っている
#pragma deprecated(ACL_3662_GRAB_ABORT)
_ACL_3662_GRAB_ABORT						= 0xF812	# (63506L) 入力を強制停止した
#pragma deprecated(ACL_3662_CH_NOT_OPENED)
_ACL_3662_CH_NOT_OPENED						= 0xF813	# (63507L) 設定されたチャンネルはオープンされていない
#pragma deprecated(ACL_3662_FIFO_ERROR)
_ACL_3662_FIFO_ERROR						= 0xF814	# (63508L) FIFOエラーが発生した
#pragma deprecated(ACL_3662_DMA_ERROR)
_ACL_3662_DMA_ERROR							= 0xF815	# (63509L) DMAエラーが発生した
#pragma deprecated(ACL_3662_GET_REGISTRY_KEY_ERROR)
_ACL_3662_GET_REGISTRY_KEY_ERROR			= 0xF816	# (63510L) レジストリキーの取得に失敗
#pragma deprecated(ACL_3662_DLL_DRIVER_ERROR)
_ACL_3662_DLL_DRIVER_ERROR					= 0xF817	# (63511L) DLLエラー
#pragma deprecated(ACL_3662_INTERNAL_LIBRARY_ERROR)
_ACL_3662_INTERNAL_LIBRARY_ERROR			= 0xF818	# (63512L) ライブラリエラー
#pragma deprecated(ACL_3662_UNKNOWN_ERROR)
_ACL_3662_UNKNOWN_ERROR						= 0xF819	# (63513L) 不明なエラー
#pragma deprecated(ACL_3662_INVALID_CAMBIT)
_ACL_3662_INVALID_CAMBIT					= 0xF820	# (63520L) カメラ入力ビットが不正 
#pragma deprecated(ACL_3662_OPEN_ALREADY)
_ACL_3662_OPEN_ALREADY						= 0xF821	# (63521L) 他のプロセスが開いている
#pragma deprecated(ACL_3662_INVALID_EVENT)
_ACL_3662_INVALID_EVENT						= 0xF824	# (63524L) イベントが不正
#pragma deprecated(ACL_3662_SETEVENT_ALREADY)
_ACL_3662_SETEVENT_ALREADY					= 0xF825	# (63525L) 既にイベントが登録されている
#pragma deprecated(ACL_3662_CREATEEVENT_FAILED)
_ACL_3662_CREATEEVENT_FAILED				= 0xF826	# (63526L) CreateEventに失敗
#pragma deprecated(ACL_3662_WAITEVENT_ALREADY)
_ACL_3662_WAITEVENT_ALREADY					= 0xF827	# (63527L) 既に待機状態もしくはABORT処理中
#pragma deprecated(ACL_3662_EVENT_NOT_IDLE)
_ACL_3662_EVENT_NOT_IDLE					= 0xF828	# (63528L) 待機中のため、解除できません
#pragma deprecated(ACL_3662_CALLBACK_ALREADY)
_ACL_3662_CALLBACK_ALREADY					= 0xF829	# (63529L) 既にコールバックが登録されている
#pragma deprecated(ACL_3662_INVALID_CC)
_ACL_3662_INVALID_CC						= 0xF82A	# (63530L) CC周期や幅の関係が不正
#pragma deprecated(ACL_3662_INVALID_BUFFER)
_ACL_3662_INVALID_BUFFER					= 0xF82B	# (63531L) バッファが不正
#pragma deprecated(ACL_3662_INVALID_XDELAY)
_ACL_3662_INVALID_XDELAY					= 0xF82C	# (63532L) XDelayが不正
#pragma deprecated(ACL_3662_INVALID_YDELAY)
_ACL_3662_INVALID_YDELAY					= 0xF82D	# (63533L) YDelayが不正
#pragma deprecated(ACL_3662_POWER_ON_TIMEOUT)
_ACL_3662_POWER_ON_TIMEOUT					= 0xF830	# (63536L) 
#pragma deprecated(ACL_3662_NOT_SUPPORT)
_ACL_3662_NOT_SUPPORT						= 0xF8FF	# (63743L) サポートされていない

#Ver.6.3.0
#ボードのエラーコードを共通化
#非対象機種：APX-3311/3312/3313/3318
ACL_3662_ERROR_ID							= 0xF800	# Ver.7.1.10
ACL_3302_ERROR_ID							= 0xF900	# Ver.7.1.10
ACL_3323_ERROR_ID							= 0xFA00	# Ver.7.1.10
ACL_3324_ERROR_ID							= 0xFB00	# Ver.7.1.10
ACL_3326_ERROR_ID							= 0xFC00	# Ver.7.1.10
ACL_3800_ERROR_ID							= 0xFD00	# Ver.6.8.0 Ver.7.1.10
ACL_3841_ERROR_ID							= 0xFE00	# Ver.6.8.0 Ver.7.1.10
ACL_3881_ERROR_ID							= 0xFF00	# Ver.7.1.10
ACL_3634_ERROR_ID							= 0x0100	# Ver.7.1.10
ACL_3636_ERROR_ID							= 0x0200	# Ver.7.1.10
ACL_3664_ERROR_ID							= 0x0300	# Ver.7.1.10
ACL_3661_ERROR_ID							= 0x0400	# Ver.7.1.10
ACL_3334_ERROR_ID							= 0x0500	# Ver.7.1.10

ACL_3300_DRIVER_ERROR						= 0x0001	# ドライバエラー
ACL_3300_INVALID_PARAM						= 0x0002	# パラメータが不正
ACL_3300_NO_DEVICE							= 0x0003	# デバイスが見つからない
ACL_3300_EVENT_ERROR						= 0x0004	# イベントが登録エラー
ACL_3300_INVALID_HANDLE						= 0x0005	# ハンドルが不正
ACL_3300_INVALID_CAPTURE					= 0x0006	# 取り込みが不正
ACL_3300_CAPTURE_RUNNING					= 0x0007	# 取り込み中
ACL_3300_TIME_OUT							= 0x0008	# タイムアウト
ACL_3300_INSUFFICIENT_CONFIG				= 0x0009	# 設定が不足している
ACL_3300_NOT_CONNECTED_CAMERA				= 0x000A	# カメラが接続されていない
ACL_3300_NULL_POINTER_ERROR					= 0x000B	# 指定されたポインタがNULLです
ACL_3300_X_SIZE_ERROR						= 0x000C	# 不正なXサイズが設定された
ACL_3300_Y_SIZE_ERROR						= 0x000D	# 不正なYサイズが設定された
ACL_3300_BITSHIFT_ERROR						= 0x000E	# 不正なビットシフト設定された
ACL_3300_TAPNUM_ERROR						= 0x000F	# 不正なタップ数が設定された
ACL_3300_SET_BUFFER_ERROR					= 0x0010	# バッファの登録に失敗した
ACL_3300_CAMERA_KIND_ERROR					= 0x0011	# カメラ種別(エリア・ライン)が間違っている
ACL_3300_GRAB_ABORT							= 0x0012	# 入力を強制停止した
ACL_3300_CH_NOT_OPENED						= 0x0013	# 設定されたチャンネルはオープンされていない
ACL_3300_FIFO_ERROR							= 0x0014	# FIFOエラーが発生した
ACL_3300_DMA_ERROR							= 0x0015	# DMAエラーが発生した
ACL_3300_GET_REGISTRY_KEY_ERROR				= 0x0016	# レジストリキーの取得に失敗
ACL_3300_DLL_DRIVER_ERROR					= 0x0017	# DLLエラー
ACL_3300_INTERNAL_LIBRARY_ERROR				= 0x0018	# ライブラリエラー
ACL_3300_UNKNOWN_ERROR						= 0x0019	# 不明なエラー
ACL_3300_INVALID_CAMBIT						= 0x0020	# カメラ入力ビットが不正 
ACL_3300_OPEN_ALREADY						= 0x0021	# 他のプロセスが開いている
ACL_3300_INVALID_EVENT						= 0x0024	# イベントが不正
ACL_3300_SETEVENT_ALREADY					= 0x0025	# 既にイベントが登録されている
ACL_3300_CREATEEVENT_FAILED					= 0x0026	# CreateEventに失敗
ACL_3300_WAITEVENT_ALREADY					= 0x0027	# 既に待機状態もしくはABORT処理中
ACL_3300_EVENT_NOT_IDLE						= 0x0028	# 待機中のため、解除できません
ACL_3300_CALLBACK_ALREADY					= 0x0029	# 既にコールバックが登録されている
ACL_3300_INVALID_CC							= 0x002A	# CC周期や幅の関係が不正
ACL_3300_INVALID_BUFFER						= 0x002B	# バッファが不正
ACL_3300_INVALID_XDELAY						= 0x002C	# XDelayが不正
ACL_3300_INVALID_YDELAY						= 0x002D	# YDelayが不正
ACL_3300_INVALID_POWER_STATE				= 0x002E	# カメラ電源状態が異常
ACL_3300_POWER_STATE_ERROR					= 0x002F	# カメラ電源状態エラー
ACL_3300_POWER_ON_TIMEOUT					= 0x0030	# カメラ電源をONしたが指定時間内にカメラクロックを検出できなかった
ACL_3300_POWER_OFF_TIMEOUT					= 0x0031	# カメラ電源をOFFしたが指定時間経過後もカメラクロックを検出した
ACL_3300_TAP_SEL_ERROR						= 0x0032	# Tap/Bit/Arrangeの関係が不正
ACL_3300_ARRANGE_X_ERROR					= 0x0033	# ArrangeXSizeが不正
ACL_3300_CXP_ACK_ERROR						= 0x0040	# ACKエラー
ACL_3300_CXP_EMPTY_ERROR					= 0x0041	# Emptyエラー
ACL_3300_OPT_RD_REQ_ERROR					= 0x0050	# リードリクエスト

ACL_3300_NOT_SUPPORT						= 0x00FF	# (63743L) サポートされていない



# 拡張エラー バッファ制御関連 (Ver 4.0.0) -------------------------------------------
ACL_BUFFINFO_SUCCESS						= (0)
ACL_BUFFINFO_ERR_NUMOFMEM					= (-1)
ACL_BUFFINFO_ERR_ALLOCATE					= (-2)
ACL_BUFFINFO_ERR_EXIST						= (-3)
ACL_BUFFINFO_ERR_XSIZE						= (-4)
ACL_BUFFINFO_ERR_YSIZE						= (-5)
ACL_BUFFINFO_ERR_BITWIDTH					= (-6)
ACL_BUFFINFO_ERR_PTRNULL					= (-7)
ACL_BUFFINFO_ERR_NO_BUFFER					= (-8)
ACL_BUFFINFO_ERR_REGION_SIZE				= (-9)
ACL_BUFFINFO_ERR_REGION_PTRNULL				= (-10)
ACL_BUFFINFO_ERR_REGION_NUM					= (-11)
ACL_BUFFINFO_ERR_INITDMA					= (-12)
ACL_BUFFINFO_ERR_SETBUFFER					= (-13)
ACL_BUFFINFO_ERR_SIZEOF						= (-14)
ACL_BUFFINFO_ERR_MUTEX						= (-15)
ACL_BUFFINFO_ERR_INCREASE_WORKINGSETSIZE	= (-16)
ACL_BUFFINFO_ERR_DECREASE_WORKINGSETSIZE	= (-17)
ACL_BUFFINFO_ERR_VIRTUAL_LOCK				= (-18)
ACL_BUFFINFO_ERR_ALLOCATE_KNLBUFF			= (-19)


error_code_dict ={
    "NO_ERROR"                                  :0,
        
    "ACL_BOARD_NOT_FOUND_ERROR"					: 0xF101,	# (61697L) ボードが見つからない
    "ACL_BOARD_NAME_ERROR"						: 0xF102,	# (61698L) ボード名が間違っている
    "ACL_BOARD_NUMBER_ERROR"					: 0xF103,	# (61699L) 指定したボード番号は無い　
    "ACL_SAME_BOARDNO_ERROR"					: 0xF104,	# (61700L) 同じボード番号が複数存在する
    "ACL_INVALID_HANDLE_ERROR"					: 0xF105,	# (61701L) ハンドルが不正
    "ACL_SELECT_CHANNEL_ERROR"					: 0xF106,	# (61702L) 指定したチャンネルが不正
    "ACL_MEM_ALLOCATE_ERROR"					: 0xF107,	# (61703L) メモリ確保に失敗した
    "ACL_INVALID_MUTEX_ERROR"					: 0xF108,	# (61704L) 排他用ハンドルが不正
    "ACL_MUTEX_LOCKED_ERROR"					: 0xF109,	# (61705L) 関数が排他状態になっている
    "ACL_FILE_NOT_FOUND_ERROR"					: 0xF10A,	# (61706L) 指定したファイルが見つからない
    "ACL_EVENT_TIMEOUT_ERROR"					: 0xF10B,	# (61707L) イベント待ちでタイムアウト
    "ACL_OPEN_ERROR"							: 0xF10C,	# (61708L) デバイスオープンに失敗した
    "ACL_CLOSE_ERROR"							: 0xF10D,	# (61709L) デバイスクローズに失敗した
    "ACL_INITIALIZE_ERROR"						: 0xF10E,	# (61710L) ボードの初期化に失敗した
    "ACL_REFLECT_PARAM_ERROR"					: 0xF10F,	# (61711L) 設定値の反映に失敗した
    "ACL_SNAP_ERROR"							: 0xF110,	# (61712L) 一画面入力に失敗した
    "ACL_SNAP_WAIT_ERROR"					    : 0xF111,	# (61713L) 一画面入力待ちに失敗した
    "ACL_GRAB_START_ERROR"						: 0xF112,	# (61714L) 連続入力に失敗した
    "ACL_GRAB_STOP_ERROR"						: 0xF113,	# (61715L) 連続入力停止に失敗した
    "ACL_GRAB_ABORT_ERROR"						: 0xF114,	# (61716L) 強制停止処理に失敗した
    "ACL_GET_FRAMENO_ERROR"						: 0xF115,	# (61717L) フレーム数の取得に失敗した
    "ACL_SET_EVENT_ERROR"						: 0xF116,	# (61718L) イベント登録に失敗した
    "ACL_WAIT_EVENT_ERROR"						: 0xF117,	# (61719L) イベント待機に失敗した
    "ACL_REGIST_CALLBACK_ERROR"					: 0xF118,	# (61710L) コールバック関数登録に失敗した
    "ACL_SET_ENCODER_ERROR"						: 0xF119,	# (61721L) エンコーダの設定に失敗した
    "ACL_GET_ENCODER_ERROR"						: 0xF11A,	# (61722L) エンコーダの取得に失敗した
    "ACL_SET_SHUTTER_TRIGGER_ERROR"				: 0xF11B,	# (61723L) トリガの設定に失敗した
    "ACL_SET_LINE_TRIGGER_ERROR"				: 0xF11C,	# (61724L) ライントリガの設定に失敗した
    "ACL_SET_EXTERNAL_TRIGGER_ERROR"			: 0xF11D,	# (61725L) 外部トリガの設定に失敗した
    "ACL_ABORT_EXTERNAL_WAIT"					: 0xF11E,	# (61726L) 外部トリガ待ちを中止した
    "ACL_SET_STROBE_ERROR"						: 0xF11F,	# (61727L) ストロボの設定に失敗した
    "ACL_SET_GPIO_ERROR"						: 0xF120,	# (61728L) GPIOの設定に失敗した
    "ACL_IMAGE_CONVERT_ERROR"					: 0xF121,	# (61729L) 画像ビット変換に失敗した
    "ACL_SET_CAMERALINK_ERROR"					: 0xF122,	# (61730L) カメラリンク設定に失敗した
    "ACL_SET_DMA_ERROR"							: 0xF123,	# (61731L) DMA設定に失敗した
    "ACL_SERIAL_OPEN_ERROR"						: 0xF124,	# (61732L) シリアルオープンに失敗した
    "ACL_SERIAL_CLOSE_ERROR"					: 0xF125,	# (61733L) シリアルクローズに失敗した
    "ACL_SERIAL_WRITE_ERROR"					: 0xF126,	# (61734L) シリアル送信(書き込み)に失敗した
    "ACL_SERIAL_READ_ERROR"						: 0xF127,	# (61735L) シリアル受信(読み込み)に失敗した
    "ACL_SERIAL_SET_PARAM_ERROR"				: 0xF128,	# (61736L) シリアルパラメータの設定に失敗した
    "ACL_SERIAL_GET_PARAM_ERROR"				: 0xF129,	# (61737L) シリアルパラメータの取得に失敗した
    "ACL_SERIAL_HANDLE_ERROR"					: 0xF12A,	# (61738L) シリアルハンドルが不正
    "ACL_SERIAL_SELECT_PORT_ERROR"				: 0xF12B,	# (61739L) 指定されたポートは使用できない
    "ACL_SET_BUFFER_ADRS_ERROR"					: 0xF12C,	# (61740L) バッファアドレスの設定に失敗した
    "ACL_GET_BUFFER_ADRS_ERROR"					: 0xF12D,	# (61741L) バッファアドレスの取得に失敗した
    "ACL_SET_CAMERALINK_EX_ERROR"				: 0xF12E,	# (61742L) カメラリンク設定(拡張)に失敗した
    "ACL_ABORT_EVENT_WAIT"						: 0xF12F,	# (61743L) イベント待ちを中止した
    "ACL_GET_BOARDINFO_ERROR"					: 0xF130,	# (61744L) ボード情報の取得に失敗した
    "ACL_SET_INFO_ERROR"						: 0xF131,	# (61745L) 値の設定に失敗した
    "ACL_GET_INFO_ERROR"						: 0xF132,	# (61746L) 値の取得に失敗した
    "ACL_SELECT_FILE_ERROR"						: 0xF133,	# (61747L) イニシャルファイルの読み書きに失敗した
    "ACL_GET_FILE_VERSION_ERROR"				: 0xF134,	# (61748L) ファイルバージョンの取得に失敗した
    "ACL_REGIST_CALLBACK_EX_ERROR"				: 0xF135,	# (61749L) コールバック関数登録(拡張)に失敗した
    "ACL_ROI_CONVERT_ERROR"						: 0xF136,	# (61750L) ROI画像変換に失敗した
    "ACL_GET_CAMERALINK_ERROR"					: 0xF137,	# (61751L) カメラリンク設定の取得に失敗した
    "ACL_GET_DMA_ERROR"							: 0xF138,	# (61752L) DMA設定の取得に失敗した
    "ACL_GET_LINE_TRIGGER_ERROR"				: 0xF139,	# (61753L) ライントリガの取得に失敗した
    "ACL_SET_EXTERNAL_TRIGGER2_ERROR"			: 0xF13A,	# (61754L) 外部トリガの設定に失敗した (Ver 4.0.0)
    "ACL_SET_DMA_OPTION_EX_ERROR"				: 0xF13B,	# (61755L) 非線形DMAの設定に失敗した (Ver 4.0.0)
    "ACL_GET_DMA_OPTION_EX_ERROR"				: 0xF13C,	# (61756L) 非線形DMAの設定取得に失敗した (Ver 4.0.0)
    "ACL_GET_GPOUT_ERROR"						: 0xF13D,	# (61757L) GPOUT状態取得に失敗した (Ver 4.0.0)
    "ACL_GET_CAMERALINK_EX_ERROR"				: 0xF13E,	# (61742L) カメラリンク取得(拡張)に失敗した

    "ACL_PARAM_1_ERROR"							: 0xF201,	# (61953L) パラメータエラー (第1引数)
    "ACL_PARAM_2_ERROR"							: 0xF202,	# (61954L) パラメータエラー (第2引数)
    "ACL_PARAM_3_ERROR"							: 0xF203,	# (61955L) パラメータエラー (第3引数)
    "ACL_PARAM_4_ERROR"							: 0xF204,	# (61956L) パラメータエラー (第4引数)
    "ACL_PARAM_5_ERROR"							: 0xF205,	# (61957L) パラメータエラー (第5引数)
    "ACL_PARAM_6_ERROR"							: 0xF206,	# (61958L) パラメータエラー (第6引数)
    "ACL_PARAM_7_ERROR"							: 0xF207,	# (61959L) パラメータエラー (第7引数)
    "ACL_PARAM_8_ERROR"							: 0xF208,	# (61960L) パラメータエラー (第8引数)
    "ACL_PARAM_9_ERROR"							: 0xF209,	# (61961L) パラメータエラー (第9引数)
    "ACL_PARAM_10_ERROR"						: 0xF20A,	# (61962L) パラメータエラー (第10引数)
    "ACL_PARAM_11_ERROR"						: 0xF20B,	# (61963L) パラメータエラー (第11引数)


    # APX-3312  -------------------------------------------------------------------------
    #ACL_3312_NO_ERROR							: 0		# エラーなし

    "ACL_3312_DRIVER_ERROR"						: 0xF301,	# (62209L) ドライバエラー
    "ACL_3312_INVALID_PARAM"					: 0xF302,	# (62210L) パラメータが不正
    "ACL_3312_NO_DEVICE"						: 0xF303,	# (62211L) デバイスが見つからない
    "ACL_3312_EVENT_ERROR"						: 0xF304,	# (62212L) イベントが登録エラー
    "ACL_3312_INVALID_HANDLE"					: 0xF305,	# (62213L) ハンドルが不正
    "ACL_3312_INVALID_CAPTURE"					: 0xF306,	# (62214L) 取り込みが不正
    "ACL_3312_CAPTURE_RUNNING"					: 0xF307,	# (62215L) 取り込み中
    "ACL_3312_TIME_OUT"							: 0xF308,	# (62216L) タイムアウト
    "ACL_3312_INSUFFICIENT_CONFIG"				: 0xF309,	# (62217L) 設定が不足している
    "ACL_3312_NOT_CONNECTED_CAMERA"				: 0xF30A,	# (62218L) カメラが接続されていない
    "ACL_3312_NULL_POINTER_ERROR"				: 0xF30B,	# (62219L) 指定されたポインタがNULLです
    "ACL_3312_X_SIZE_ERROR"						: 0xF30C,	# (62220L) 不正なXサイズが設定された
    "ACL_3312_Y_SIZE_ERROR"						: 0xF30D,	# (62221L) 不正なYサイズが設定された
    "ACL_3312_SET_BUFFER_ERROR"					: 0xF30E,	# (62222L) バッファの登録に失敗した
    "ACL_3312_CAMERA_KIND_ERROR"				: 0xF30F,	# (62223L) カメラ種別(エリア・ライン)が間違っている
    "ACL_3312_GRAB_ABORT"						: 0xF310,	# (62224L) 入力を強制停止した
    "ACL_3312_CH_NOT_OPENED"					: 0xF311,	# (61725L) 設定されたチャンネルはオープンされていない
    "ACL_3312_FIFO_ERROR"						: 0xF312,	# (61726L) FIFOエラーが発生した
    "ACL_3312_DMA_ERROR"						: 0xF313,	# (61727L) DMAエラーが発生した
    "ACL_3312_GET_REGISTRY_KEY_ERROR"			: 0xF314,	# (62228L) レジストリキーの取得に失敗
    "ACL_3312_NOT_CONNECTED_CAM1"				: 0xF315,	# (62229L) CAM1のカメラが接続されていない
    "ACL_3312_NOT_CONNECTED_CAM2"				: 0xF316,	# (62230L) CAM2のカメラが接続されていない
    "ACL_3312_POCL_STATUS_ERROR"				: 0xF317,	# (62231L) PoCLが異常状態
    "ACL_3312_DLL_DRIVER_ERROR"					: 0xF318,	# (62232L) DLLエラー
    "ACL_3312_INTERNAL_LIBRARY_ERROR"			: 0xF319,	# (62233L) ライブラリエラー
    "ACL_3312_UNKNOWN_ERROR"					: 0xF31A,	# (62234L) 不明なエラー
    "ACL_3312_NOT_USED_64BITOS"					: 0xF31B,	# (62235L) 64bitOSでは使用できない
    "ACL_3312_NOT_SUPPORT"						: 0xF3FF,	# (62463L) サポートされていない

    # APX-3313  -------------------------------------------------------------------------
    #ACL_3313_NO_ERROR							: 0		# エラーなし

    "ACL_3313_DRIVER_ERROR"						: 0xF401,	# (62465L) ドライバエラー
    "ACL_3313_INVALID_PARAM"					: 0xF402,	# (62466L) パラメータが不正
    "ACL_3313_NO_DEVICE"						: 0xF403,	# (62467L) デバイスが見つからない
    "ACL_3313_EVENT_ERROR"						: 0xF404,	# (62468L) イベントが登録エラー
    "ACL_3313_INVALID_HANDLE"					: 0xF405,	# (62469L) ハンドルが不正
    "ACL_3313_INVALID_CAPTURE"					: 0xF406,	# (62470L) 取り込みが不正
    "ACL_3313_CAPTURE_RUNNING"					: 0xF407,	# (62471L) 取り込み中
    "ACL_3313_TIME_OUT"							: 0xF408,	# (62472L) タイムアウト
    "ACL_3313_INSUFFICIENT_CONFIG"				: 0xF409,	# (62473L) 設定が不足している
    "ACL_3313_NOT_CONNECTED_CAMERA"				: 0xF40A,	# (62474L) カメラが接続されていない
    "ACL_3313_NULL_POINTER_ERROR"				: 0xF40B,	# (62475L) 指定されたポインタがNULLです
    "ACL_3313_X_SIZE_ERROR"						: 0xF40C,	# (62476L) 不正なXサイズが設定された
    "ACL_3313_Y_SIZE_ERROR"						: 0xF40D,	# (62477L) 不正なYサイズが設定された
    "ACL_3313_BITSHIFT_ERROR"					: 0xF40E,	# (62478L) 不正なビットシフト設定された
    "ACL_3313_TAPNUM_ERROR"						: 0xF40F,	# (62479L) 不正なタップ数が設定された
    "ACL_3313_SET_BUFFER_ERROR"					: 0xF410,	# (62480L) バッファの登録に失敗した
    "ACL_3313_CAMERA_KIND_ERROR"				: 0xF411,	# (62481L) カメラ種別(エリア・ライン)が間違っている
    "ACL_3313_GRAB_ABORT"						: 0xF412,	# (62482L) 入力を強制停止した
    "ACL_3313_CH_NOT_OPENED"					: 0xF413,	# (62483L) 設定されたチャンネルはオープンされていない
    "ACL_3313_FIFO_ERROR"						: 0xF414,	# (62484L) FIFOエラーが発生した
    "ACL_3313_DMA_ERROR"						: 0xF415,	# (62485L) DMAエラーが発生した
    "ACL_3313_GET_REGISTRY_KEY_ERROR"			: 0xF416,	# (62486L) レジストリキーの取得に失敗
    "ACL_3313_DLL_DRIVER_ERROR"					: 0xF417,	# (62487L) DLLエラー
    "ACL_3313_INTERNAL_LIBRARY_ERROR"			: 0xF418,	# (62488L) ライブラリエラー
    "ACL_3313_UNKNOWN_ERROR"					: 0xF419,	# (62489L) 不明なエラー
    "ACL_3313_NOT_USED_64BITOS"					: 0xF41A,	# (62490L) 64bitOSでは使用できない
    "ACL_3313_NOT_SUPPORT"						: 0xF4FF,	# (62719L) サポートされていない


    # APX-3318  -------------------------------------------------------------------------
    #ACL_3318_NO_ERROR							: 0		# エラーなし

    "ACL_3318_DRIVER_ERROR"						: 0xF501,	# (62465L) ドライバエラー
    "ACL_3318_INVALID_PARAM"					: 0xF502,	# (62466L) パラメータが不正
    "ACL_3318_NO_DEVICE"						: 0xF503,	# (62467L) デバイスが見つからない
    "ACL_3318_EVENT_ERROR"						: 0xF504,	# (62468L) イベントが登録エラー
    "ACL_3318_INVALID_HANDLE"					: 0xF505,	# (62469L) ハンドルが不正
    "ACL_3318_INVALID_CAPTURE"					: 0xF506,	# (62470L) 取り込みが不正
    "ACL_3318_CAPTURE_RUNNING"					: 0xF507,	# (62471L) 取り込み中
    "ACL_3318_TIME_OUT"							: 0xF508,	# (62472L) タイムアウト
    "ACL_3318_INSUFFICIENT_CONFIG"				: 0xF509,	# (62473L) 設定が不足している
    "ACL_3318_NOT_CONNECTED_CAMERA"				: 0xF50A,	# (62474L) カメラが接続されていない
    "ACL_3318_NULL_POINTER_ERROR"				: 0xF50B,	# (62475L) 指定されたポインタがNULLです
    "ACL_3318_X_SIZE_ERROR"						: 0xF50C,	# (62476L) 不正なXサイズが設定された
    "ACL_3318_Y_SIZE_ERROR"						: 0xF50D,	# (62477L) 不正なYサイズが設定された
    "ACL_3318_BITSHIFT_ERROR"					: 0xF50E,	# (62478L) 不正なビットシフト設定された
    "ACL_3318_TAPNUM_ERROR"						: 0xF50F,	# (62479L) 不正なタップ数が設定された
    "ACL_3318_SET_BUFFER_ERROR"					: 0xF510,	# (62480L) バッファの登録に失敗した
    "ACL_3318_CAMERA_KIND_ERROR"				: 0xF511,	# (62481L) カメラ種別(エリア・ライン)が間違っている
    "ACL_3318_GRAB_ABORT"						: 0xF512,	# (62482L) 入力を強制停止した
    "ACL_3318_CH_NOT_OPENED"					: 0xF513,	# (62483L) 設定されたチャンネルはオープンされていない
    "ACL_3318_FIFO_ERROR"						: 0xF514,	# (62484L) FIFOエラーが発生した
    "ACL_3318_DMA_ERROR"						: 0xF515,	# (62485L) DMAエラーが発生した
    "ACL_3318_GET_REGISTRY_KEY_ERROR"			: 0xF516,	# (62486L) レジストリキーの取得に失敗
    "ACL_3318_DLL_DRIVER_ERROR"					: 0xF517,	# (62487L) DLLエラー
    "ACL_3318_INTERNAL_LIBRARY_ERROR"			: 0xF518,	# (62488L) ライブラリエラー
    "ACL_3318_UNKNOWN_ERROR"					: 0xF519,	# (62489L) 不明なエラー
    "ACL_3318_NOT_USED_64BITOS"					: 0xF51A,	# (62490L) 64bitOSでは使用できない
    "ACL_3318_NOT_SUPPORT"						: 0xF5FF,	# (62719L) サポートされていない

    # APX-3311 (Ver 4.0.0) --------------------------------------------------------------
    "ACL_3311_DRIVER_ERROR"						: 0xF601,	# (62977L) ドライバエラー
    "ACL_3311_INVALID_PARAM"					: 0xF602,	# (62978L) パラメータが不正
    "ACL_3311_NO_DEVICE"						: 0xF603,	# (62979L) デバイスが見つからない
    "ACL_3311_CAPTURE_RUNNING"					: 0xF607,	# (62983L) 取り込み中
    "ACL_3311_TIME_OUT"							: 0xF608,	# (62984L) タイムアウト
    "ACL_3311_NOT_CONNECTED_CAMERA"				: 0xF60A,	# (62986L) カメラが接続されていない
    "ACL_3311_NULL_POINTER_ERROR"				: 0xF60B,	# (62987L) 指定されたポインタがNULLです
    "ACL_3311_X_SIZE_ERROR"						: 0xF60C,	# (62988L) 不正なXサイズが設定された
    "ACL_3311_Y_SIZE_ERROR"						: 0xF60D,	# (62989L) 不正なYサイズが設定された
    "ACL_3311_SET_BUFFER_ERROR"					: 0xF60E,	# (62990L) バッファの登録に失敗した
    "ACL_3311_GRAB_ABORT"						: 0xF610,	# (62992L) 入力を強制停止した
    "ACL_3311_CAMERA_KIND_ERROR"				: 0xF611,	# (62993L) カメラ種別(エリア・ライン)が間違っている
    "ACL_3311_INTERNAL_LIBRARY_ERROR"			: 0xF618,	# (63000L) ライブラリエラー
    "ACL_3311_UNKNOWN_ERROR"					: 0xF619,	# (63001L) 不明なエラー
    "ACL_3311_INVALID_CAMBIT"					: 0xF620,	# (63008L) カメラ入力ビットが不正 
    "ACL_3311_OPEN_ALREADY"						: 0xF621,	# (63009L) 他のプロセスが開いている
    "ACL_3311_CREATE_THREAD"					: 0xF622,	# (63010L) スレッドの生成に失敗した
    "ACL_3311_KILL_THREAD"						: 0xF623,	# (63011L) スレッドの削除に失敗した
    "ACL_3311_INVALID_EVENT"					: 0xF624,	# (63012L) イベントが不正
    "ACL_3311_SETEVENT_ALREADY"					: 0xF625,	# (63013L) 既にイベントが登録されている
    "ACL_3311_CREATEEVENT_FAILED"				: 0xF626,	# (63014L) CreateEventに失敗
    "ACL_3311_WAITEVENT_ALREADY"				: 0xF627,	# (63015L) 既に待機状態もしくはABORT処理中
    "ACL_3311_EVENT_NOT_IDLE"					: 0xF628,	# (63016L) 待機中のため、解除できません
    "ACL_3311_CALLBACK_ALREADY"					: 0xF629,	# (63017L) 既にコールバックが登録されている
    "ACL_3311_INVALID_CC"						: 0xF62A,	# (63018L) CC周期や幅の関係が不正
    "ACL_3311_INVALID_BUFFER"					: 0xF62B,	# (63019L) バッファが不正
    "ACL_3311_INVALID_XDELAY"					: 0xF62C,	# (63020L) XDelayが不正
    "ACL_3311_INVALID_YDELAY"					: 0xF62D,	# (63021L) YDelayが不正
    "ACL_3311_INVALID_POWER_STATE"				: 0xF62E,	# (63022L) カメラ電源状態が異常
    "ACL_3311_POWER_STATE_ERROR"				: 0xF62F,	# (63023L) カメラ電源状態エラー
    "ACL_3311_POWER_ON_TIMEOUT"					: 0xF630,	# (63024L) カメラ電源をONしたが指定時間内にカメラクロックを検出できなかった
    "ACL_3311_POWER_OFF_TIMEOUT"				: 0xF631,	# (63025L) カメラ電源をOFFしたが指定時間経過後もカメラクロックを検出した
    "ACL_3311_LUT_NOT_EDIT"						: 0xF632,	# (63026L) BayerLUTを編集できる状態ではない
    "ACL_3311_LUT_EDIT_ALREADY"					: 0xF633,	# (63027L) 既にBayerLUTを編集中なので編集できない
    "ACL_3311_NOT_SUPPORT"						: 0xF6FF,	# (63231L) サポートされていない


    # APX-3662  -------------------------------------------------------------------------
    "_ACL_3662_DRIVER_ERROR"					: 0xF801,	# (63489L) ドライバエラー
    "_ACL_3662_INVALID_PARAM	"				: 0xF802,	# (63490L) パラメータが不正
    "_ACL_3662_NO_DEVICE"						: 0xF803,	# (63491L) デバイスが見つからない
    "_ACL_3662_EVENT_ERROR"						: 0xF804,	# (63492L) イベントが登録エラー
    "_ACL_3662_INVALID_HANDLE"					: 0xF805,	# (63493L) ハンドルが不正
    "_ACL_3662_INVALID_CAPTURE"					: 0xF806,	# (63494L) 取り込みが不正
    "_ACL_3662_CAPTURE_RUNNING"					: 0xF807,	# (63495L) 取り込み中
    "_ACL_3662_TIME_OUT"						: 0xF808,	# (63496L) タイムアウト
    "_ACL_3662_INSUFFICIENT_CONFIG"				: 0xF809,	# (63497L) 設定が不足している
    "_ACL_3662_NOT_CONNECTED_CAMERA"			: 0xF80A,	# (63498L) カメラが接続されていない
    "_ACL_3662_NULL_POINTER_ERROR"				: 0xF80B,	# (63499L) 指定されたポインタがNULLです
    "_ACL_3662_X_SIZE_ERROR"					: 0xF80C,	# (63500L) 不正なXサイズが設定された
    "_ACL_3662_Y_SIZE_ERROR"					: 0xF80D,	# (63501L) 不正なYサイズが設定された
    "_ACL_3662_BITSHIFT_ERROR"					: 0xF80E,	# (63502L) 不正なビットシフト設定された
    "_ACL_3662_TAPNUM_ERROR"					: 0xF80F,	# (63503L) 不正なタップ数が設定された
    "_ACL_3662_SET_BUFFER_ERROR"				: 0xF810,	# (63504L) バッファの登録に失敗した
    "_ACL_3662_CAMERA_KIND_ERROR"				: 0xF811,	# (63505L) カメラ種別(エリア・ライン)が間違っている
    "_ACL_3662_GRAB_ABORT"						: 0xF812,	# (63506L) 入力を強制停止した
    "_ACL_3662_CH_NOT_OPENED"					: 0xF813,	# (63507L) 設定されたチャンネルはオープンされていない
    "_ACL_3662_FIFO_ERROR"						: 0xF814,	# (63508L) FIFOエラーが発生した
    "_ACL_3662_DMA_ERROR"						: 0xF815,	# (63509L) DMAエラーが発生した
    "_ACL_3662_GET_REGISTRY_KEY_ERROR"			: 0xF816,	# (63510L) レジストリキーの取得に失敗
    "_ACL_3662_DLL_DRIVER_ERROR"				: 0xF817,	# (63511L) DLLエラー
    "_ACL_3662_INTERNAL_LIBRARY_ERROR"			: 0xF818,	# (63512L) ライブラリエラー
    "_ACL_3662_UNKNOWN_ERROR"					: 0xF819,	# (63513L) 不明なエラー
    "_ACL_3662_INVALID_CAMBIT"					: 0xF820,	# (63520L) カメラ入力ビットが不正 
    "_ACL_3662_OPEN_ALREADY"					: 0xF821,	# (63521L) 他のプロセスが開いている
    "_ACL_3662_INVALID_EVENT"					: 0xF824,	# (63524L) イベントが不正
    "_ACL_3662_SETEVENT_ALREADY"				: 0xF825,	# (63525L) 既にイベントが登録されている
    "_ACL_3662_CREATEEVENT_FAILED"				: 0xF826,	# (63526L) CreateEventに失敗
    "_ACL_3662_WAITEVENT_ALREADY"				: 0xF827,	# (63527L) 既に待機状態もしくはABORT処理中
    "_ACL_3662_EVENT_NOT_IDLE"					: 0xF828,	# (63528L) 待機中のため、解除できません
    "_ACL_3662_CALLBACK_ALREADY"				: 0xF829,	# (63529L) 既にコールバックが登録されている
    "_ACL_3662_INVALID_CC"						: 0xF82A,	# (63530L) CC周期や幅の関係が不正
    "_ACL_3662_INVALID_BUFFER"					: 0xF82B,	# (63531L) バッファが不正
    "_ACL_3662_INVALID_XDELAY"					: 0xF82C,	# (63532L) XDelayが不正
    "_ACL_3662_INVALID_YDELAY"					: 0xF82D,	# (63533L) YDelayが不正
    "_ACL_3662_POWER_ON_TIMEOUT"				: 0xF830,	# (63536L) 
    "_ACL_3662_NOT_SUPPORT"						: 0xF8FF,	# (63743L) サポートされていない

    #Ver.6.3.0
    #ボードのエラーコードを共通化
    #非対象機種：APX-3311/3312/3313/3318
    "ACL_3662_ERROR_ID"							: 0xF800,	# Ver.7.1.10
    "ACL_3302_ERROR_ID"							: 0xF900,	# Ver.7.1.10
    "ACL_3323_ERROR_ID"							: 0xFA00,	# Ver.7.1.10
    "ACL_3324_ERROR_ID"							: 0xFB00,	# Ver.7.1.10
    "ACL_3326_ERROR_ID"							: 0xFC00,	# Ver.7.1.10
    "ACL_3800_ERROR_ID"							: 0xFD00,	# Ver.6.8.0 Ver.7.1.10
    "ACL_3841_ERROR_ID"							: 0xFE00,	# Ver.6.8.0 Ver.7.1.10
    "ACL_3881_ERROR_ID"							: 0xFF00,	# Ver.7.1.10
    "ACL_3634_ERROR_ID"							: 0x0100,	# Ver.7.1.10
    "ACL_3636_ERROR_ID"							: 0x0200,	# Ver.7.1.10
    "ACL_3664_ERROR_ID"							: 0x0300,	# Ver.7.1.10
    "ACL_3661_ERROR_ID"							: 0x0400,	# Ver.7.1.10
    "ACL_3334_ERROR_ID"							: 0x0500,	# Ver.7.1.10

    "DRIVER_ERROR"								: 0x0001,	# ドライバエラー
    "INVALID_PARAM"								: 0x0002,	# パラメータが不正
    "NO_DEVICE"									: 0x0003,	# デバイスが見つからない
    "EVENT_ERROR"								: 0x0004,	# イベントが登録エラー
    "INVALID_HANDLE"							: 0x0005,	# ハンドルが不正
    "INVALID_CAPTURE"							: 0x0006,	# 取り込みが不正
    "CAPTURE_RUNNING"							: 0x0007,	# 取り込み中
    "TIME_OUT"									: 0x0008,	# タイムアウト
    "INSUFFICIENT_CONFIG"						: 0x0009,	# 設定が不足している
    "NOT_CONNECTED_CAMERA"						: 0x000A,	# カメラが接続されていない
    "NULL_POINTER_ERROR"						: 0x000B,	# 指定されたポインタがNULLです
    "X_SIZE_ERROR"								: 0x000C,	# 不正なXサイズが設定された
    "Y_SIZE_ERROR"								: 0x000D,	# 不正なYサイズが設定された
    "BITSHIFT_ERROR"							: 0x000E,	# 不正なビットシフト設定された
    "TAPNUM_ERROR"								: 0x000F,	# 不正なタップ数が設定された
    "SET_BUFFER_ERROR"							: 0x0010,	# バッファの登録に失敗した
    "CAMERA_KIND_ERROR"							: 0x0011,	# カメラ種別(エリア・ライン)が間違っている
    "GRAB_ABORT"								: 0x0012,	# 入力を強制停止した
    "CH_NOT_OPENED"								: 0x0013,	# 設定されたチャンネルはオープンされていない
    "FIFO_ERROR"								: 0x0014,	# FIFOエラーが発生した
    "DMA_ERROR"									: 0x0015,	# DMAエラーが発生した
    "GET_REGISTRY_KEY_ERROR"					: 0x0016,	# レジストリキーの取得に失敗
    "DLL_DRIVER_ERROR"							: 0x0017,	# DLLエラー
    "INTERNAL_LIBRARY_ERROR"					: 0x0018,	# ライブラリエラー
    "UNKNOWN_ERROR"								: 0x0019,	# 不明なエラー
    "INVALID_CAMBIT"							: 0x0020,	# カメラ入力ビットが不正 
    "OPEN_ALREADY"								: 0x0021,	# 他のプロセスが開いている
    "INVALID_EVENT"								: 0x0024,	# イベントが不正
    "SETEVENT_ALREADY"							: 0x0025,	# 既にイベントが登録されている
    "CREATEEVENT_FAILED"						: 0x0026,	# CreateEventに失敗
    "WAITEVENT_ALREADY"							: 0x0027,	# 既に待機状態もしくはABORT処理中
    "EVENT_NOT_IDLE"							: 0x0028,	# 待機中のため、解除できません
    "CALLBACK_ALREADY"							: 0x0029,	# 既にコールバックが登録されている
    "INVALID_CC"								: 0x002A,	# CC周期や幅の関係が不正
    "INVALID_BUFFER"							: 0x002B,	# バッファが不正
    "INVALID_XDELAY"							: 0x002C,	# XDelayが不正
    "INVALID_YDELAY"							: 0x002D,	# YDelayが不正
    "INVALID_POWER_STATE"						: 0x002E,	# カメラ電源状態が異常
    "POWER_STATE_ERROR"							: 0x002F,	# カメラ電源状態エラー
    "POWER_ON_TIMEOUT"							: 0x0030,	# カメラ電源をONしたが指定時間内にカメラクロックを検出できなかった
    "POWER_OFF_TIMEOUT"							: 0x0031,	# カメラ電源をOFFしたが指定時間経過後もカメラクロックを検出した
    "TAP_SEL_ERROR"								: 0x0032,	# Tap/Bit/Arrangeの関係が不正
    "ARRANGE_X_ERROR"							: 0x0033,	# ArrangeXSizeが不正
    "CXP_ACK_ERROR"								: 0x0040,	# ACKエラー
    "CXP_EMPTY_ERROR"							: 0x0041,	# Emptyエラー
    "OPT_RD_REQ_ERROR"							: 0x0050,	# リードリクエスト

    "NOT_SUPPORT"						: 0x00FF,	# (63743L) サポートされていない

    # 拡張エラー バッファ制御関連 (Ver 4.0.0) -------------------------------------------
    #ACL_BUFFINFO_SUCCESS						: (0)
    "ACL_BUFFINFO_ERR_NUMOFMEM"					: (-1),
    "ACL_BUFFINFO_ERR_ALLOCATE"					: (-2),
    "ACL_BUFFINFO_ERR_EXIST"					: (-3),
    "ACL_BUFFINFO_ERR_XSIZE"					: (-4),
    "ACL_BUFFINFO_ERR_YSIZE"					: (-5),
    "ACL_BUFFINFO_ERR_BITWIDTH"					: (-6),
    "ACL_BUFFINFO_ERR_PTRNULL"					: (-7),
    "ACL_BUFFINFO_ERR_NO_BUFFER"				: (-8),
    "ACL_BUFFINFO_ERR_REGION_SIZE"				: (-9),
    "ACL_BUFFINFO_ERR_REGION_PTRNULL"			: (-10),
    "ACL_BUFFINFO_ERR_REGION_NUM"				: (-11),
    "ACL_BUFFINFO_ERR_INITDMA"					: (-12),
    "ACL_BUFFINFO_ERR_SETBUFFER"				: (-13),
    "ACL_BUFFINFO_ERR_SIZEOF	"				: (-14),
    "ACL_BUFFINFO_ERR_MUTEX"					: (-15),
    "ACL_BUFFINFO_ERR_INCREASE_WORKINGSETSIZE"	: (-16),
    "ACL_BUFFINFO_ERR_DECREASE_WORKINGSETSIZE"	: (-17),
    "ACL_BUFFINFO_ERR_VIRTUAL_LOCK"				: (-18),
    "ACL_BUFFINFO_ERR_ALLOCATE_KNLBUFF"			: (-19),
}

def get_error_value(error_key):
    return error_code_dict[error_key]

def get_error_name(error_value):
    return [k for k, v in error_code_dict.items() if v == error_value][0]


#These parameters are obsolete.
#pragma deprecated(BORADINDEX)
#pragma deprecated(ACAPDMAINFO)

#These functions are obsolete.
#pragma deprecated(AcapSetDmaOption)
#pragma deprecated(AcapGetDmaOption)
#pragma deprecated(AcapSetGPIO)
#pragma deprecated(AcapSetBitAssign)
#pragma deprecated(AcapGetBitAssign)

#ifdef  __cplusplus
#}		/* extern "C" */
#endif	/* __cplusplus */


#endif	/* __AVALCAPLIB2__ */



