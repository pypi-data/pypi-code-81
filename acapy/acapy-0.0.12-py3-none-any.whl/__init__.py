__version__ = "0.0.3"

'''
////////////////////////////////////////////////////////////
//  Ver.0.0.12  (2021.04.12) 
////////////////////////////////////////////////////////////
●プレリリース版
'''
from acapy import acaplib2

# pylint: disable=W0311

class AcaPy():
    """description of class"""

    # クラス変数
    OK									= acaplib2.ACL_RTN_OK		# エラーなし
    ERROR							    = acaplib2.ACL_RTN_ERROR	# エラーあり

    def __init__(self, board_id = 0, ch = 1, debug_print = True):
        '''デバイスの初期化
        board_no    : ボード番号
        ch          : チャンネル番号  
        debug_print : デバッグ情報を出力する場合はTrue
        '''
        self.__debug_print = debug_print

        # プロパティ初期値
        self.__is_opened = False
        self.__is_grab = False
        self.last_frame_no = 0

        self.__hHandle = acaplib2.INVALID_HANDLE_VALUE
        self.__board_id = 0
        self.__board_name = b''
        self.__ch = 0
        self.__scan_system = 0
        self.__width = 0
        self.__height = 0
        self.__mem_num = 0
        self.__x_delay = 0
        self.__y_delay = 0
        self.__y_total = 0
        self.__camera_bit = 0
        self.__board_bit = 0
        self.__pix_shift = 0
        self.__timeout = 0
        self.__cc_polarity = 0
        self.__trigger_polarity = 0
        self.__cc1_polarity = 0
        self.__cc2_polarity = 0
        self.__cc3_polarity = 0
        self.__cc4_polarity = 0
        self.__cc_cycle = 0
        self.__cc_cycle_ex = 0
        self.__trigger_cycle = 0
        self.__trigger_cycle_ex = 0
        self.__exposure = 0
        self.__exposure_ex = 0
        self.__trigger_width = 0
        self.__trigger_width_ex = 0
        self.__cc_width = 0
        self.__cc_delay = 0
        self.__cc_out_no = 0
        self.__rolling_shutter = 0
        self.__external_trigger_enable = 0
        self.__external_trigger_mode = 0
        self.__external_trigger_chatter = 0
        self.__external_trigger_delay = 0
        self.__encoder_enable = 0
        self.__encoder_start = 0
        self.__encoder_mode = 0
        self.__encoder_phase = 0
        self.__encoder_direction = 0
        self.__encoder_z_phase = 0
        self.__encoder_compare_reg_1 = 0
        self.__encoder_compare_reg_2 = 0
        self.__encoder_abs_start = 0
        self.__strobe_enable = 0
        self.__strobe_delay = 0
        self.__strobe_time = 0
        self.__reverse_dma_enable = 0
        self.__dval_enable = 0
        self.__tap_num = 0
        self.__tap_arrage = 0
        self.__tap_arrage_x_size = 0
        self.__sync_lt = 0
        self.__gpout_sel = 0
        self.__gpout_pol = 0
        self.__interrupt_line = 0
        self.__trigger_enable = 0
        self.__data_mask_lower = 0
        self.__data_mask_upper = 0
        self.__chatter_separate = 0
        self.__external_pin_sel = 0
        self.__gpin_pin_sel = 0
        self.__sync_ch = 0
        self.__bayer_enable = 0
        self.__bayer_grid = 0
        self.__bayer_input_bit = 0
        self.__bayer_output_bit = 0
        self.__strobe_pol = 0
        self.__vertical_remap = 0
        self.__express_link = 0
        self.__fpga_version = 0
        self.__lval_delay = 0
        self.__line_reverse = 0
        self.__start_frame_no = 0
        self.__buffer_zero_fill = 0
        self.__cc_stop = 0
        self.__lvds_cclk_sel = 0
        self.__lvds_phase_sel = 0
        self.__lvds_synclt_sel = 0
        self.__pocl_lite_enable = 0
        self.__cxp_link_speed = 0
        self.__cxp_bitrate = 0
        self.__cxp_acquision_start_address = 0
        self.__cxp_acquision_start_value = 0
        self.__cxp_acquision_stop_address = 0
        self.__cxp_acquision_stop_value = 0
        self.__cxp_pixel_format_address = 0
        self.__cxp_pixel_format = 0
        self.__rgb_swap_enable = 0
        self.__narrow10bit_enable = 0

        self.__virtual_comport = 0
        self.__driver_name = 0
        self.__hw_protect = 0
        self.__images = []


        # ボード情報の取得
        ret, bdInfo = acaplib2.AcapGetBoardInfoEx()
        if ret != AcaPy.OK:
            self.print_last_error()


        ## boardidのチェック
        #if board_id >= 0:
        #    # ボードを開くとき
        #    if bdInfo.nBoardNum == 0:
        #        return
        #else:
        #    #Virtualのとき
        #    board_id = 0
        #    board_index = bdInfo.boardIndex[board_id]

        boardnum = bdInfo.nBoardNum
        if boardnum == 0:
            boardnum = 1 # Virtualを許容するため

        # 指定されたボード番号の検索
        for i in range(boardnum):
            if board_id == bdInfo.boardIndex[i].nBoardID:
                board_index = bdInfo.boardIndex[i]
                break

        if board_index is None:
            # 指定されたボード番号が見つからなかったとき
            return

        # チャンネル番号の確認
        if ch < 0 or ch > bdInfo.boardIndex[0].nChannelNum:
            return

        # プロパティの値を取得
        self.__board_id = board_id
        self.__board_name = board_index.pBoardName

        # ボードオープン
        self.__hHandle = acaplib2.AcapOpen(board_index.pBoardName, board_index.nBoardID, ch)
        self.__ch = ch

        self.__is_opened = True
        self.__refrect_param_flag = True # refrect_paramが必要な場合はTrue



    def __del__(self):
        if self.__hHandle != acaplib2.INVALID_HANDLE_VALUE:
            acaplib2.AcapClose(self.__hHandle, self.__ch)
        self._debug_print("AcapClose")


        

    ##############################################################

    @property
    def is_opened(self):
        return self.__is_opened 

    @property
    def is_grab(self):
        return self.__is_grab

    @property
    def handle(self):
        return self.__hHandle 

    @property
    def board_id(self):
        return self.__board_id

    @property
    def board_name(self):
        return self.__board_name

    @property
    def ch(self):
        return self.__ch

    @property
    def scan_system(self):
        return self.__scan_system
    @scan_system.setter
    def scan_system(self, value):
        if self.__scan_system == value:
            return
        self.__scan_system = value
        self.set_info(acaplib2.ACL_SCAN_SYSTEM, value)

    @property
    def width(self):
        return self.__width
    @width.setter
    def width(self, value):
        if self.__width == value:
            return
        self.__width = value
        self.set_info(acaplib2.ACL_X_SIZE, value)
        self._create_ring_buffer()

    @property
    def height(self):
        return self.__height
    @height.setter
    def height(self, value):
        if self.__height == value:
            return
        self.__height = value
        self.set_info(acaplib2.ACL_Y_SIZE, value)
        if self.__y_total != 0:
            self.set_info(acaplib2.ACL_Y_TOTAL, value)
        self._create_ring_buffer()

    @property
    def mem_num(self):
        return self.__mem_num
    @mem_num.setter
    def mem_num(self, value):
        if self.__mem_num == value:
            return
        self.__mem_num = value
        self.set_info(acaplib2.ACL_MEM_NUM, value)
        self._create_ring_buffer()

    @property
    def x_delay(self):
        return self.__x_delay
    @x_delay.setter
    def x_delay(self, value):
        if self.__x_delay == value:
            return
        self.__x_delay = value
        self.set_info(acaplib2.ACL_X_DELAY, value)

    @property
    def y_delay(self):
        return self.__y_delay
    @y_delay.setter
    def y_delay(self, value):
        if self.__y_delay == value:
            return
        self.__y_delay = value
        self.set_info(acaplib2.ACL_Y_DELAY, value)

    @property
    def y_total(self):
        return self.__y_total
    @y_total.setter
    def y_total(self, value):
        if self.__y_total == value:
            return
        self.__y_total = value
        self.set_info(acaplib2.ACL_Y_TOTAL, value)

    @property
    def camera_bit(self):
        return self.__camera_bit
    @camera_bit.setter
    def camera_bit(self, value):
        if self.__camera_bit == value:
            return
        self.__camera_bit = value
        self.set_info(acaplib2.ACL_CAM_BIT, value)

    @property
    def board_bit(self):
        return self.__board_bit
    @board_bit.setter
    def board_bit(self, value):
        if self.__board_bit == value:
            return
        self.__board_bit = value
        self.set_info(acaplib2.ACL_BOARD_BIT, value)
        self._create_ring_buffer()

    @property
    def pix_shift(self):
        return self.__pix_shift
    @pix_shift.setter
    def pix_shift(self, value):
        if self.__pix_shift == value:
            return
        self.__pix_shift = value
        self.set_info(acaplib2.ACL_PIX_SHIFT, value)

    @property
    def timeout(self):
        return self.__timeout
    @timeout.setter
    def timeout(self, value):
        if self.__timeout == value:
            return
        self.__timeout = value
        self.set_info(acaplib2.ACL_TIME_OUT, value)

    @property
    def cc_polarity(self):
        return self.__timeout
    @cc_polarity.setter
    def cc_polarity(self, value):
        if self.__cc_polarity == value:
            return
        self.__cc_polarity = value
        self.set_info(acaplib2.ACL_EXP_POL, value)

    @property
    def trigger_polarity(self):
        return self.__trigger_polarity
    @trigger_polarity.setter
    def trigger_polarity(self, value):
        if self.__trigger_polarity == value:
            return
        self.__trigger_polarity = value
        self.cc_polarity = value

    @property
    def cc1_polarity(self):
        return self.__cc1_polarity
    @cc1_polarity.setter
    def cc1_polarity(self, value):
        if self.__cc1_polarity == value:
            return
        self.__cc1_polarity = value
        self.set_info(acaplib2.ACL_CC1_LEVEL, value)

    @property
    def cc2_polarity(self):
        return self.__cc2_polarity
    @cc2_polarity.setter
    def cc2_polarity(self, value):
        if self.__cc2_polarity == value:
            return
        self.__cc2_polarity = value
        self.set_info(acaplib2.ACL_CC2_LEVEL, value)

    @property
    def cc3_polarity(self):
        return self.__cc3_polarity
    @cc3_polarity.setter
    def cc3_polarity(self, value):
        if self.__cc3_polarity == value:
            return
        self.__cc3_polarity = value
        self.set_info(acaplib2.ACL_CC3_LEVEL, value)

    @property
    def cc4_polarity(self):
        return self.__cc4_polarity
    @cc4_polarity.setter
    def cc4_polarity(self, value):
        if self.__cc4_polarity == value:
            return
        self.__cc4_polarity = value
        self.set_info(acaplib2.ACL_CC4_LEVEL, value)

    @property
    def cc_cycle(self):
        return self.__cc_cycle
    @cc_cycle.setter
    def cc_cycle(self, value):
        if self.__cc_cycle == value:
            return
        self.__cc_cycle = value
        self.set_info(acaplib2.ACL_EXP_CYCLE, value)

    @property
    def cc_cycle_ex(self):
        return self.__cc_cycle_ex
    @cc_cycle_ex.setter
    def cc_cycle_ex(self, value):
        if self.__cc_cycle_ex == value:
            return
        self.__cc_cycle_ex = value
        self.set_info(acaplib2.ACL_EXP_CYCLE_EX, value)

    @property
    def trigger_cycle(self):
        return self.__trigger_cycle
    @trigger_cycle.setter
    def trigger_cycle(self, value):
        if self.__trigger_cycle == value:
            return
        self.__trigger_cycle = value
        self.cc_cycle = value

    @property
    def trigger_cycle_ex(self):
        return self.__trigger_cycle_ex
    @trigger_cycle_ex.setter
    def trigger_cycle_ex(self, value):
        if self.__trigger_cycle_ex == value:
            return
        self.__trigger_cycle_ex = value
        self.cc_cycle_ex = value


    @property
    def exposure(self):
        return self.__exposure
    @exposure.setter
    def exposure(self, value):
        if self.__exposure == value:
            return
        self.__exposure = value
        self.set_info(acaplib2.ACL_EXPOSURE, value)

    @property
    def exposure_ex(self):
        return self.__exposure_ex
    @exposure_ex.setter
    def exposure_ex(self, value):
        if self.__exposure_ex == value:
            return
        self.__exposure_ex = value
        self.set_info(acaplib2.ACL_EXPOSURE_EX, value)

    @property
    def trigger_width(self):
        return self.__trigger_width
    @trigger_width.setter
    def trigger_width(self, value):
        if self.__trigger_width == value:
            return
        self.__trigger_width = value
        self.exposure = value

    @property
    def trigger_width_ex(self):
        return self.__trigger_width_ex
    @trigger_width_ex.setter
    def trigger_width_ex(self, value):
        if self.__trigger_width_ex == value:
            return
        self.__trigger_width_ex = value
        self.exposure_ex = value

    @property
    def cc_width(self):
        return self.__cc_width
    @cc_width.setter
    def cc_width(self, value):
        if self.__cc_width == value:
            return
        self.__cc_width = value
        self.exposure = value


    @property
    def cc_delay(self):
        return self.__cc_delay
    @cc_delay.setter
    def cc_delay(self, value):
        if self.__cc_delay == value:
            return
        self.__cc_delay = value
        self.set_info(acaplib2.ACL_CC_DELAY, value)

    @property
    def cc_out_no(self):
        return self.__cc_out_no
    @cc_out_no.setter
    def cc_out_no(self, value):
        if self.__cc_out_no == value:
            return
        self.__cc_out_no = value
        self.set_info(acaplib2.ACL_EXP_CC_OUT, value)

    @property
    def rolling_shutter(self):
        return self.__rolling_shutter
    @rolling_shutter.setter
    def rolling_shutter(self, value):
        if self.__rolling_shutter == value:
            return
        self.__rolling_shutter = value
        self.set_info(acaplib2.ACL_ROLLING_SHUTTER, value)

    @property
    def external_trigger_enable(self):
        return self.__external_trigger_enable
    @external_trigger_enable.setter
    def external_trigger_enable(self, value):
        if self.__external_trigger_enable == value:
            return
        self.__external_trigger_enable = value
        self.set_info(acaplib2.ACL_EXT_EN, value)

    @property
    def external_trigger_mode(self):
        return self.__external_trigger_mode
    @external_trigger_mode.setter
    def external_trigger_mode(self, value):
        if self.__external_trigger_mode == value:
            return
        self.__external_trigger_mode = value
        self.set_info(acaplib2.ACL_EXT_MODE, value)

    @property
    def external_trigger_chatter(self):
        return self.__external_trigger_chatter
    @external_trigger_chatter.setter
    def external_trigger_chatter(self, value):
        if self.__external_trigger_chatter == value:
            return
        self.__external_trigger_chatter = value
        self.set_info(acaplib2.ACL_EXT_CHATTER, value)

    @property
    def external_trigger_delay(self):
        return self.__external_trigger_delay
    @external_trigger_delay.setter
    def external_trigger_delay(self, value):
        if self.__external_trigger_delay == value:
            return
        self.__external_trigger_delay = value
        self.set_info(acaplib2.ACL_EXT_DELAY, value)

    @property
    def encoder_enable(self):
        return self.__encoder_enable
    @encoder_enable.setter
    def encoder_enable(self, value):
        if self.__encoder_enable == value:
            return
        self.__encoder_enable = value
        self.set_info(acaplib2.ACL_ENC_EN, value)

    @property
    def encoder_start(self):
        return self.__encoder_start
    @encoder_start.setter
    def encoder_start(self, value):
        if self.__encoder_start == value:
            return
        self.__encoder_start = value
        self.set_info(acaplib2.ACL_ENC_START, value)

    @property
    def encoder_mode(self):
        return self.__encoder_mode
    @encoder_mode.setter
    def encoder_mode(self, value):
        if self.__encoder_mode == value:
            return
        self.__encoder_mode = value
        self.set_info(acaplib2.ACL_ENC_MODE, value)

    @property
    def encoder_phase(self):
        return self.__encoder_phase
    @encoder_phase.setter
    def encoder_phase(self, value):
        if self.__encoder_phase == value:
            return
        self.__encoder_phase = value
        self.set_info(acaplib2.ACL_ENC_PHASE, value)

    @property
    def encoder_direction(self):
        return self.__encoder_direction
    @encoder_direction.setter
    def encoder_direction(self, value):
        if self.__encoder_direction == value:
            return
        self.__encoder_direction = value
        self.set_info(acaplib2.ACL_ENC_DIRECTION, value)

    @property
    def encoder_z_phase(self):
        return self.__encoder_z_phase
    @encoder_z_phase.setter
    def encoder_z_phase(self, value):
        if self.__encoder_z_phase == value:
            return
        self.__encoder_z_phase = value
        self.set_info(acaplib2.ACL_ENC_ZPHASE_EN, value)

    @property
    def encoder_compare_reg_1(self):
        return self.__encoder_compare_reg_1
    @encoder_compare_reg_1.setter
    def encoder_compare_reg_1(self, value):
        if self.__encoder_compare_reg_1 == value:
            return
        self.__encoder_compare_reg_1 = value
        self.set_info(acaplib2.ACL_ENC_COMPARE_1, value)

    @property
    def encoder_compare_reg_2(self):
        return self.__encoder_compare_reg_2
    @encoder_compare_reg_2.setter
    def encoder_compare_reg_2(self, value):
        if self.__encoder_compare_reg_2 == value:
            return
        self.__encoder_compare_reg_2 = value
        self.set_info(acaplib2.ACL_ENC_COMPARE_2, value)

    @property
    def encoder_abs_start(self):
        return self.__encoder_abs_start
    @encoder_abs_start.setter
    def encoder_abs_start(self, value):
        if self.__encoder_abs_start == value:
            return
        self.__encoder_abs_start = value
        self.set_info(acaplib2.ACL_ENC_ABS_START, value)

    @property
    def encoder_abs_count(self):
        _, count = self.get_info(acaplib2.ACL_ENC_ABS_COUNT)
        return count

    @property
    def strobe_enable(self):
        return self.__strobe_enable
    @strobe_enable.setter
    def strobe_enable(self, value):
        if self.__strobe_enable == value:
            return
        self.__strobe_enable = value
        self.set_info(acaplib2.ACL_STROBE_EN, value)

    @property
    def strobe_delay(self):
        return self.__strobe_delay
    @strobe_delay.setter
    def strobe_delay(self, value):
        if self.__strobe_delay == value:
            return
        self.__strobe_delay = value
        self.set_info(acaplib2.ACL_STROBE_DELAY, value)

    @property
    def strobe_time(self):
        return self.__strobe_time
    @strobe_time.setter
    def strobe_time(self, value):
        if self.__strobe_time == value:
            return
        self.__strobe_time = value
        self.set_info(acaplib2.ACL_STROBE_TIME, value)

    @property
    def reverse_dma_enable(self):
        return self.__reverse_dma_enable
    @reverse_dma_enable.setter
    def reverse_dma_enable(self, value):
        if self.__reverse_dma_enable == value:
            return
        self.__reverse_dma_enable = value
        self.set_info(acaplib2.ACL_REVERSE_DMA, value)

    @property
    def dval_enable(self):
        return self.__dval_enable
    @dval_enable.setter
    def dval_enable(self, value):
        if self.__dval_enable == value:
            return
        self.__dval_enable = value
        self.set_info(acaplib2.ACL_DVAL_EN, value)

    @property
    def tap_num(self):
        return self.__tap_num
    @tap_num.setter
    def tap_num(self, value):
        if self.__tap_num == value:
            return
        self.__tap_num = value
        self.set_info(acaplib2.ACL_TAP_NUM, value)

    @property
    def tap_arrage(self):
        return self.__tap_arrage
    @tap_arrage.setter
    def tap_arrage(self, value):
        if self.__tap_arrage == value:
            return
        self.__tap_arrage = value
        self.set_info(acaplib2.ACL_TAP_ARRANGE, value)

    @property
    def tap_arrage_x_size(self):
        return self.__tap_arrage_x_size
    @tap_arrage_x_size.setter
    def tap_arrage_x_size(self, value):
        if self.__tap_arrage_x_size == value:
            return
        self.__tap_arrage_x_size = value
        self.set_info(acaplib2.ACL_ARRANGE_XSIZE, value)

    @property
    def sync_lt(self):
        return self.__sync_lt
    @sync_lt.setter
    def sync_lt(self, value):
        if self.__sync_lt == value:
            return
        self.__sync_lt = value
        self.set_info(acaplib2.ACL_SYNC_LT, value)

    @property
    def gpout_sel(self):
        return self.__gpout_sel
    @gpout_sel.setter
    def gpout_sel(self, value):
        if self.__gpout_sel == value:
            return
        self.__gpout_sel = value
        self.set_info(acaplib2.ACL_GPOUT_SEL, value)

    @property
    def gpout_pol(self):
        return self.__gpout_pol
    @gpout_pol.setter
    def gpout_pol(self, value):
        if self.__gpout_pol == value:
            return
        self.__gpout_pol = value
        self.set_info(acaplib2.ACL_GPOUT_POL, value)

    @property
    def interrupt_line(self):
        return self.__interrupt_line
    @interrupt_line.setter
    def interrupt_line(self, value):
        if self.__interrupt_line == value:
            return
        self.__interrupt_line = value
        self.set_info(acaplib2.ACL_INTR_LINE, value)

    @property
    def trigger_enable(self):
        return self.__trigger_enable
    @trigger_enable.setter
    def trigger_enable(self, value):
        if self.__trigger_enable == value:
            return
        self.__trigger_enable = value
        self.set_info(acaplib2.ACL_EXP_EN, value)

    @property
    def data_mask_lower(self):
        return self.__data_mask_lower
    @data_mask_lower.setter
    def data_mask_lower(self, value):
        if self.__data_mask_lower == value:
            return
        self.__data_mask_lower = value
        self.set_info(acaplib2.ACL_DATA_MASK_LOWER, value)

    @property
    def data_mask_upper(self):
        return self.__data_mask_upper
    @data_mask_upper.setter
    def data_mask_upper(self, value):
        if self.__data_mask_upper == value:
            return
        self.__data_mask_upper = value
        self.set_info(acaplib2.ACL_DATA_MASK_UPPER, value)

    @property
    def encoder_count(self):
        _, count = self.get_info(acaplib2.ACL_ENC_RLT_COUNT)
        return count

    @property
    def encoder_all_count(self):
        _, count = self.get_info(acaplib2.ACL_ENC_RLT_ALL_COUNT)
        return count

    @property
    def encoder_agr_count(self):
        _, count = self.get_info(acaplib2.ACL_ENC_AGR_COUNT)
        return count

    @property
    def a_cw_ccw(self):
        _, count = self.get_info(acaplib2.ACL_A_CW_CCW)
        return count

    @property
    def b_cw_ccw(self):
        _, count = self.get_info(acaplib2.ACL_B_CW_CCW)
        return count

    @property
    def freq_a(self):
        _, count = self.get_info(acaplib2.ACL_FREQ_A)
        return count

    @property
    def freq_b(self):
        _, count = self.get_info(acaplib2.ACL_FREQ_B)
        return count

    @property
    def freq_z(self):
        _, count = self.get_info(acaplib2.ACL_FREQ_Z)
        return count

    @property
    def chatter_separate(self):
        return self.__chatter_separate
    @chatter_separate.setter
    def chatter_separate(self, value):
        if self.__chatter_separate == value:
            return
        self.__chatter_separate = value
        self.set_info(acaplib2.ACL_EXT_CHATTER_SEPARATE, value)

    @property
    def external_pin_sel(self):
        return self.__external_pin_sel
    @external_pin_sel.setter
    def external_pin_sel(self, value):
        if self.__external_pin_sel == value:
            return
        self.__external_pin_sel = value
        self.set_info(acaplib2.ACL_EXT_PIN_SEL, value)

    @property
    def gpin_pin_sel(self):
        return self.__gpin_pin_sel
    @gpin_pin_sel.setter
    def gpin_pin_sel(self, value):
        if self.__gpin_pin_sel == value:
            return
        self.__gpin_pin_sel = value
        self.set_info(acaplib2.ACL_GPIN_PIN_SEL, value)

    @property
    def sync_ch(self):
        return self.__sync_ch
    @sync_ch.setter
    def sync_ch(self, value):
        if self.__sync_ch == value:
            return
        self.__sync_ch = value
        self.set_info(acaplib2.ACL_SYNC_CH, value)

    @property
    def bayer_enable(self):
        return self.__bayer_enable
    @bayer_enable.setter
    def bayer_enable(self, value):
        if self.__bayer_enable == value:
            return
        self.__bayer_enable = value
        self.set_info(acaplib2.ACL_BAYER_ENABLE, value)

    @property
    def bayer_grid(self):
        return self.__bayer_grid
    @bayer_grid.setter
    def bayer_grid(self, value):
        if self.__bayer_grid == value:
            return
        self.__bayer_grid = value
        self.set_info(acaplib2.ACL_BAYER_GRID, value)

    @property
    def bayer_lut_edit(self):
        _, value = self.get_info(acaplib2.ACL_BAYER_LUT_EDIT)
        return value
    @bayer_lut_edit.setter
    def bayer_lut_edit(self, value):
        self.set_info(acaplib2.ACL_BAYER_LUT_EDIT, value)

    @property
    def bayer_lut_data(self):
        data = []
        for i in range(1024):
            ret, value = self.get_info(acaplib2.ACL_BAYER_LUT_DATA, i)
            if ret != AcaPy.OK:
                return None
            data.append(value)
        return data
    @bayer_lut_data.setter
    def bayer_lut_data(self, lut_data_list):
        for i in len(lut_data_list):
            ret = self.set_info(acaplib2.ACL_BAYER_LUT_EDIT, lut_data_list[i], i)
            if ret != AcaPy.OK:
                return

    @property
    def bayer_input_bit(self):
        return self.__bayer_input_bit
    @bayer_input_bit.setter
    def bayer_input_bit(self, value):
        if self.__bayer_input_bit == value:
            return
        self.__bayer_input_bit = value
        self.set_info(acaplib2.ACL_BAYER_INPUT_BIT, value)

    @property
    def bayer_output_bit(self):
        return self.__bayer_output_bit
    @bayer_output_bit.setter
    def bayer_output_bit(self, value):
        if self.__bayer_output_bit == value:
            return
        self.__bayer_output_bit = value
        self.set_info(acaplib2.ACL_BAYER_OUTPUT_BIT, value)

    @property
    def power_supply(self):
        _, value = self.get_info(acaplib2.ACL_POWER_SUPPLY)
        return value

    @property
    def power_state(self):
        _, value = self.get_info(acaplib2.ACL_POWER_STATE)
        return value
    @power_state.setter
    def power_state(self, value):
        return self.set_info(acaplib2.ACL_POWER_STATE, value)

    @property
    def strobe_pol(self):
        return self.__strobe_pol
    @strobe_pol.setter
    def strobe_pol(self, value):
        if self.__strobe_pol == value:
            return
        self.__strobe_pol = value
        self.set_info(acaplib2.ACL_STROBE_POL, value)

    @property
    def vertical_remap(self):
        return self.__vertical_remap
    @vertical_remap.setter
    def vertical_remap(self, value):
        if self.__vertical_remap == value:
            return
        self.__vertical_remap = value
        self.set_info(acaplib2.ACL_VERTICAL_REMAP, value)

    @property
    def express_link(self):
        return self.__express_link

    @property
    def fpga_version(self):
        return self.__fpga_version

    @property
    def lval_delay(self):
        return self.__lval_delay
    @lval_delay.setter
    def lval_delay(self, value):
        if self.__lval_delay == value:
            return
        self.__lval_delay = value
        self.set_info(acaplib2.ACL_LVAL_DELAY, value)

    @property
    def line_reverse(self):
        return self.__line_reverse
    @line_reverse.setter
    def line_reverse(self, value):
        if self.__line_reverse == value:
            return
        self.__line_reverse = value
        self.set_info(acaplib2.ACL_LINE_REVERSE, value)

    @property
    def camera_state(self):
        _, value = self.get_info(acaplib2.ACL_CAMERA_STATE)
        return value

    @property
    def gpin_pol(self):
        _, value = self.get_info(acaplib2.ACL_GPIN_POL)
        return value

    @property
    def board_error(self):
        _, value = self.get_info(acaplib2.ACL_BOARD_ERROR)
        return value

    @board_error.setter
    def board_error(self, value):
        self.set_info(acaplib2.ACL_BOARD_ERROR, value)

    @property
    def start_frame_no(self):
        return self.__start_frame_no
    @start_frame_no.setter
    def start_frame_no(self, value):
        if self.__start_frame_no == value:
            return
        self.__start_frame_no = value
        self.set_info(acaplib2.ACL_START_FRAME_NO, value)

    @property
    def cancel_initialize(self):
        _, value = self.get_info(acaplib2.ACL_CANCEL_INITIALIZE)
        return value
    @cancel_initialize.setter
    def cancel_initialize(self, value):
        self.set_info(acaplib2.ACL_CANCEL_INITIALIZE, value)

    @property
    def buffer_zero_fill(self):
        return self.__buffer_zero_fill
    @buffer_zero_fill.setter
    def buffer_zero_fill(self, value):
        if self.__buffer_zero_fill == value:
            return
        self.__buffer_zero_fill = value
        self.set_info(acaplib2.ACL_BUFFER_ZERO_FILL, value)

    @property
    def cc_stop(self):
        return self.__cc_stop
    @cc_stop.setter
    def cc_stop(self, value):
        if self.__cc_stop == value:
            return
        self.__cc_stop = value
        self.set_info(acaplib2.ACL_CC_STOP, value)

    @property
    def lvds_cclk_sel(self):
        return self.__lvds_cclk_sel
    @lvds_cclk_sel.setter
    def lvds_cclk_sel(self, value):
        if self.__lvds_cclk_sel == value:
            return
        self.__lvds_cclk_sel = value
        self.set_info(acaplib2.ACL_LVDS_CCLK_SEL, value)

    @property
    def lvds_phase_sel(self):
        return self.__lvds_phase_sel
    @lvds_phase_sel.setter
    def lvds_phase_sel(self, value):
        if self.__lvds_phase_sel == value:
            return
        self.__lvds_phase_sel = value
        self.set_info(acaplib2.ACL_LVDS_PHASE_SEL, value)

    @property
    def lvds_synclt_sel(self):
        return self.__lvds_synclt_sel
    @lvds_synclt_sel.setter
    def lvds_synclt_sel(self, value):
        if self.__lvds_synclt_sel == value:
            return
        self.__lvds_synclt_sel = value
        self.set_info(acaplib2.ACL_LVDS_SYNCLT_SEL, value)
    
    @property
    def count_reset(self):
        pass

    @count_reset.setter
    def count_reset(self, value):
        self.set_info(acaplib2.ACL_COUNT_RESET, value)

    @property
    def count_cc(self):
        _, value = self.get_info(acaplib2.ACL_COUNT_CC)
        return value

    @property
    def count_fval(self):
        _, value = self.get_info(acaplib2.ACL_COUNT_FVAL)
        return value

    @property
    def count_lval(self):
        _, value = self.get_info(acaplib2.ACL_COUNT_LVAL)
        return value

    @property
    def count_exttrig(self):
        _, value = self.get_info(acaplib2.ACL_COUNT_EXTTRIG)
        return value

    @property
    def interval_exttrig_1(self):
        _, value = self.get_info(acaplib2.ACL_INTERVAL_EXTTRIG_1)
        return value

    @property
    def interval_exttrig_2(self):
        _, value = self.get_info(acaplib2.ACL_INTERVAL_EXTTRIG_2)
        return value

    @property
    def interval_exttrig_3(self):
        _, value = self.get_info(acaplib2.ACL_INTERVAL_EXTTRIG_3)
        return value

    @property
    def interval_exttrig_4(self):
        _, value = self.get_info(acaplib2.ACL_INTERVAL_EXTTRIG_4)
        return value

    @property
    def virtual_comport(self):
        _, value = self.get_info(acaplib2.ACL_VIRTUAL_COMPORT)
        self.__virtual_comport = value
        return value

    @property
    def pocl_lite_enable(self):
        return self.__pocl_lite_enable
    @pocl_lite_enable.setter
    def pocl_lite_enable(self, value):
        if self.__pocl_lite_enable == value:
            return
        self.__pocl_lite_enable = value
        self.set_info(acaplib2.ACL_POCL_LITE_ENABLE, value)

    @property
    def cxp_link_reset(self):
        pass
    @cxp_link_reset.setter
    def cxp_link_reset(self, value):
        self.set_info(acaplib2.ACL_CXP_LINK_RESET, value)

    @property
    def cxp_link_speed(self):
        return self.__cxp_link_speed
    @cxp_link_speed.setter
    def cxp_link_speed(self, value):
        if self.__cxp_link_speed == value:
            return
        self.__cxp_link_speed = value
        self.set_info(acaplib2._ACL_CXP_LINK_SPEED, value)

    @property
    def cxp_bitrate(self):
        return self.__cxp_bitrate
    @cxp_bitrate.setter
    def cxp_bitrate(self, value):
        if self.__cxp_bitrate == value:
            return
        self.__cxp_bitrate = value
        self.set_info(acaplib2.ACL_CXP_BITRATE, value)

    @property
    def cxp_acquision_start_address(self):
        return self.__cxp_acquision_start_address
    @cxp_acquision_start_address.setter
    def cxp_acquision_start_address(self, value):
        if self.__cxp_acquision_start_address == value:
            return
        self.__cxp_acquision_start_address = value
        self.set_info(acaplib2.ACL_CXP_ACQ_START_ADR, value)

    @property
    def cxp_acquision_start_value(self):
        return self.__cxp_acquision_start_value
    @cxp_acquision_start_value.setter
    def cxp_acquision_start_value(self, value):
        if self.__cxp_acquision_start_value == value:
            return
        self.__cxp_acquision_start_value = value
        self.set_info(acaplib2.ACL_CXP_ACQ_START_VALUE, value)

    @property
    def cxp_acquision_stop_address(self):
        return self.__cxp_acquision_stop_address
    @cxp_acquision_stop_address.setter
    def cxp_acquision_stop_address(self, value):
        if self.__cxp_acquision_stop_address == value:
            return
        self.__cxp_acquision_stop_address = value
        self.set_info(acaplib2.ACL_CXP_ACQ_STOP_ADR, value)

    @property
    def cxp_acquision_stop_value(self):
        return self.__cxp_acquision_stop_value
    @cxp_acquision_stop_value.setter
    def cxp_acquision_stop_value(self, value):
        if self.__cxp_acquision_stop_value == value:
            return
        self.__cxp_acquision_stop_value = value
        self.set_info(acaplib2.ACL_CXP_ACQ_STOP_VALUE, value)

    @property
    def cxp_pixel_format_address(self):
        return self.__cxp_pixel_format_address
    @cxp_pixel_format_address.setter
    def cxp_pixel_format_address(self, value):
        if self.__cxp_pixel_format_address == value:
            return
        self.__cxp_pixel_format_address = value
        self.set_info(acaplib2.ACL_CXP_PIX_FORMAT_ADR, value)

    @property
    def cxp_pixel_format(self):
        return self.__cxp_pixel_format
    @cxp_pixel_format.setter
    def cxp_pixel_format(self, value):
        if self.__cxp_pixel_format == value:
            return
        self.__cxp_pixel_format = value
        self.set_info(acaplib2.ACL_CXP_PIX_FORMAT, value)

    @property
    def rgb_swap_enable(self):
        return self.__rgb_swap_enable
    @rgb_swap_enable.setter
    def rgb_swap_enable(self, value):
        if self.__rgb_swap_enable == value:
            return
        self.__rgb_swap_enable = value
        self.set_info(acaplib2.ACL_RGB_SWAP_ENABLE, value)

    @property
    def freq_lval(self):
        _, value = self.get_info(acaplib2.ACL_FREQ_LVAL)
        return value

    @property
    def freq_fval(self):
        _, value = self.get_info(acaplib2.ACL_FREQ_FVAL)
        return value

    @property
    def freq_ttl1(self):
        _, value = self.get_info(acaplib2.ACL_FREQ_TTL1)
        return value

    @property
    def freq_ttl2(self):
        _, value = self.get_info(acaplib2.ACL_FREQ_TTL2)
        return value

    @property
    def fifo_full(self):
        _, value = self.get_info(acaplib2.ACL_FIFO_FULL)
        return value

    @property
    def board_temp(self):
        _, value = self.get_info(acaplib2.ACL_BOARD_TEMP)
        return value

    @property
    def fpga_temp(self):
        _, value = self.get_info(acaplib2.ACL_FPGA_TEMP)
        return value

    @property
    def capture_flag(self):
        _, value = self.get_info(acaplib2.ACL_CAPTURE_FLAG)
        return value

    @property
    def narrow10bit_enable(self):
        return self.__narrow10bit_enable
    @narrow10bit_enable.setter
    def narrow10bit_enable(self, value):
        if self.__narrow10bit_enable == value:
            return
        self.__narrow10bit_enable = value
        self.set_info(acaplib2.ACL_NARROW10BIT_ENABLE, value)  

    @property
    def opt_link_reset(self):
        pass
    @opt_link_reset.setter
    def opt_link_reset(self, value):
        self.set_info(acaplib2.ACL_OPT_LINK_RESET, value)  


    ##############################################################
   
    def bgr2rgb(self = None, bgr_image = None):
        return acaplib2.bgr2rgb(bgr_image)

    @staticmethod
    def get_boardInfo():
        return acaplib2.AcapGetBoardInfoEx()

    def get_file_version(self, filename):
        ret = acaplib2.AcapGetFileVersion(filename)
        if ret[0] != self.OK:
            self.print_last_error()
        return acaplib2.AcapGetFileVersion(filename)

    def get_info(self, value_id, mem_num = 0):
        ret, value = acaplib2.AcapGetInfo(self.__hHandle, self.__ch, value_id, mem_num)
        if ret != self.OK:
            value = None
            self._debug_print("[Not Implemented] get_info: value_id =", acaplib2.get_setting_name(value_id))
        return ret, value

    def set_info(self, value_id, value, mem_num = -1):
        if mem_num < 0:
            self.__refrect_param_flag = True
        ret = acaplib2.AcapSetInfo(self.__hHandle, self.__ch, value_id, mem_num, value)
        if ret != self.OK:
            self._debug_print("[Not Implemented] set_info: value_id =", acaplib2.get_setting_name(value_id), ": Value = ", value)
        return ret

    def refrect_param(self):
        '''設定した値の反映'''
        if self.__refrect_param_flag == False:
            return
        self.__refrect_param_flag = False
        return acaplib2.AcapReflectParam(self.__hHandle, self.__ch)

    def select_file(self, inifilename):
        '''iniファイルの選択'''
        ret = acaplib2.AcapSelectFile(self.__hHandle, self.__ch, inifilename)
        if ret != acaplib2.ACL_RTN_OK:
            ret = self.print_last_error()
            return ret    
        # 各種情報の取得
        _, self.__scan_system = self.get_info(acaplib2.ACL_SCAN_SYSTEM)
        _, self.__width = self.get_info(acaplib2.ACL_X_SIZE)
        _, self.__height = self.get_info(acaplib2.ACL_Y_SIZE)
        _, self.__x_delay = self.get_info(acaplib2.ACL_X_DELAY)
        _, self.__y_delay = self.get_info(acaplib2.ACL_Y_DELAY)
        _, self.__y_total = self.get_info(acaplib2.ACL_Y_TOTAL)
        _, self.__camera_bit = self.get_info(acaplib2.ACL_CAM_BIT)
        _, self.__board_bit = self.get_info(acaplib2.ACL_BOARD_BIT)
        _, self.__pix_shift = self.get_info(acaplib2.ACL_PIX_SHIFT)
        _, self.__timeout = self.get_info(acaplib2.ACL_TIME_OUT)
        _, self.__mem_num = self.get_info(acaplib2.ACL_MEM_NUM)

        _, self.__cc_polarity = self.get_info(acaplib2.ACL_EXP_POL)
        _, self.__cc1_polarity = self.get_info(acaplib2.ACL_CC1_LEVEL)
        _, self.__cc2_polarity = self.get_info(acaplib2.ACL_CC2_LEVEL)
        _, self.__cc3_polarity = self.get_info(acaplib2.ACL_CC3_LEVEL)
        _, self.__cc4_polarity = self.get_info(acaplib2.ACL_CC4_LEVEL)
        self.__trigger_polarity = self.__cc_polarity

        _, self.__cc_cycle = self.get_info(acaplib2.ACL_EXP_CYCLE)
        _, self.__cc_cycle_ex = self.get_info(acaplib2.ACL_EXP_CYCLE_EX)

        self.__trigger_cycle = self.__cc_cycle
        self.__trigger_cycle_ex = self.__cc_cycle_ex
        _, self.__trigger_width = self.get_info(acaplib2.ACL_EXPOSURE)
        self.__cc_width = self.__trigger_width
        self.__exposure = self.__trigger_width
        _, self.__exposure_ex = self.get_info(acaplib2.ACL_EXPOSURE_EX)
        self.__trigger_width_ex = self.__exposure_ex

        _, self.__cc_out_no = self.get_info(acaplib2.ACL_EXP_CC_OUT)
        _, self.__cc_delay = self.get_info(acaplib2.ACL_CC_DELAY)
        _, self.__rolling_shutter = self.get_info(acaplib2.ACL_ROLLING_SHUTTER)

        _, self.__external_trigger_enable = self.get_info(acaplib2.ACL_EXT_EN)
        _, self.__external_trigger_mode = self.get_info(acaplib2.ACL_EXT_MODE)
        _, self.__external_trigger_chatter = self.get_info(acaplib2.ACL_EXT_CHATTER)
        _, self.__external_trigger_delay = self.get_info(acaplib2.ACL_EXT_DELAY)
        
        _, self.__encoder_enable = self.get_info(acaplib2.ACL_ENC_EN)
        _, self.__encoder_start = self.get_info(acaplib2.ACL_ENC_START)
        _, self.__encoder_mode = self.get_info(acaplib2.ACL_ENC_MODE)
        _, self.__encoder_phase = self.get_info(acaplib2.ACL_ENC_PHASE)
        _, self.__encoder_direction = self.get_info(acaplib2.ACL_ENC_DIRECTION)
        _, self.__encoder_z_phase = self.get_info(acaplib2.ACL_ENC_ZPHASE_EN)
        _, self.__encoder_compare_reg_1 = self.get_info(acaplib2.ACL_ENC_COMPARE_1)
        _, self.__encoder_compare_reg_2 = self.get_info(acaplib2.ACL_ENC_COMPARE_2)
        _, self.__encoder_abs_start = self.get_info(acaplib2.ACL_ENC_ABS_START)
        
        _, self.__strobe_enable = self.get_info(acaplib2.ACL_STROBE_EN)
        _, self.__strobe_delay = self.get_info(acaplib2.ACL_STROBE_DELAY)
        _, self.__strobe_time = self.get_info(acaplib2.ACL_STROBE_TIME)
        _, self.__strobe_pol = self.get_info(acaplib2.ACL_STROBE_POL)

        
        _, self.__reverse_dma_enable = self.get_info(acaplib2.ACL_REVERSE_DMA)
        _, self.__dval_enable = self.get_info(acaplib2.ACL_DVAL_EN)
        _, self.__tap_num = self.get_info(acaplib2.ACL_TAP_NUM)
        _, self.__tap_arrage = self.get_info(acaplib2.ACL_TAP_ARRANGE)
        _, self.__tap_arrage_x_size = self.get_info(acaplib2.ACL_ARRANGE_XSIZE)
        
        
        _, self.__sync_lt = self.get_info(acaplib2.ACL_SYNC_LT)
        _, self.__gpout_sel = self.get_info(acaplib2.ACL_GPOUT_SEL)
        _, self.__gpout_pol = self.get_info(acaplib2.ACL_GPOUT_POL)

        _, self.__interrupt_line = self.get_info(acaplib2.ACL_INTR_LINE)

        _, self.__trigger_enable = self.get_info(acaplib2.ACL_EXP_EN)

        _, self.__data_mask_lower = self.get_info(acaplib2.ACL_DATA_MASK_LOWER)
        _, self.__data_mask_upper = self.get_info(acaplib2.ACL_DATA_MASK_UPPER)

        _, self.__chatter_separate = self.get_info(acaplib2.ACL_EXT_CHATTER_SEPARATE)

        _, self.__external_pin_sel = self.get_info(acaplib2.ACL_EXT_PIN_SEL)
        _, self.__gpin_pin_sel = self.get_info(acaplib2.ACL_GPIN_PIN_SEL)
        
        _, self.__sync_ch = self.get_info(acaplib2.ACL_SYNC_CH)

        _, self.__bayer_enable = self.get_info(acaplib2.ACL_BAYER_ENABLE)
        _, self.__bayer_grid = self.get_info(acaplib2.ACL_BAYER_GRID)
        _, self.__bayer_input_bit = self.get_info(acaplib2.ACL_BAYER_INPUT_BIT)
        _, self.__bayer_output_bit = self.get_info(acaplib2.ACL_BAYER_OUTPUT_BIT)


        _, self.__vertical_remap = self.get_info(acaplib2.ACL_VERTICAL_REMAP)

        _, self.__express_link = self.get_info(acaplib2.ACL_EXPRESS_LINK)

        _, self.__fpga_version = self.get_info(acaplib2.ACL_FPGA_VERSION)

        #_, self.__tap_direction = self.get_info(acaplib2.ACL_TAP_DIRECTION) 

        _, self.__lval_delay = self.get_info(acaplib2.ACL_LVAL_DELAY)
        _, self.__line_reverse = self.get_info(acaplib2.ACL_LINE_REVERSE)

        _, self.__start_frame_no = self.get_info(acaplib2.ACL_START_FRAME_NO)

        #_, self.__cancel_initialize = self.get_info(acaplib2.ACL_CANCEL_INITIALIZE)

        _, self.__buffer_zero_fill = self.get_info(acaplib2.ACL_BUFFER_ZERO_FILL)

        _, self.__cc_stop = self.get_info(acaplib2.ACL_CC_STOP)

        _, self.__cc_stop = self.get_info(acaplib2.ACL_CC_STOP)

        _, self.__lvds_cclk_sel = self.get_info(acaplib2.ACL_LVDS_CCLK_SEL)
        _, self.__lvds_phase_sel = self.get_info(acaplib2.ACL_LVDS_PHASE_SEL)
        _, self.__lvds_synclt_sel = self.get_info(acaplib2.ACL_LVDS_SYNCLT_SEL)

        _, self.__virtual_comport = self.get_info(acaplib2.ACL_VIRTUAL_COMPORT)
        
        _, self.__pocl_lite_enable = self.get_info(acaplib2.ACL_POCL_LITE_ENABLE)

        _, self.__cxp_link_speed = self.get_info(acaplib2._ACL_CXP_LINK_SPEED)
        _, self.__cxp_bitrate = self.get_info(acaplib2.ACL_CXP_BITRATE)

        _, self.__cxp_acquision_start_address = self.get_info(acaplib2.ACL_CXP_ACQ_START_ADR)
        _, self.__cxp_acquision_start_value = self.get_info(acaplib2.ACL_CXP_ACQ_START_VALUE)
        _, self.__cxp_acquision_stop_address = self.get_info(acaplib2.ACL_CXP_ACQ_STOP_ADR)
        _, self.__cxp_acquision_stop_value = self.get_info(acaplib2.ACL_CXP_ACQ_STOP_VALUE)
        _, self.__cxp_pixel_format_address = self.get_info(acaplib2.ACL_CXP_PIX_FORMAT_ADR)
        _, self.__cxp_pixel_format = self.get_info(acaplib2.ACL_CXP_PIX_FORMAT)
        
        _, self.__rgb_swap_enable = self.get_info(acaplib2.ACL_RGB_SWAP_ENABLE)

        #_, self.__camera_state = self.get_info(acaplib2.ACL_CAMERA_STATE)
        #_, self.__gpin_pol = self.get_info(acaplib2.ACL_GPIN_POL)
        
        _, self.__narrow10bit_enable = self.get_info(acaplib2.ACL_NARROW10BIT_ENABLE)
        



        
        ##Ver.7.1.0
        #ACL_A_CW_CCW					= 0x1A01	# A相の回転方向 (0:CW)
        #ACL_B_CW_CCW					= 0x1A02	# B相の回転方向 (0:CW)
        #ACL_FREQ_A						= 0x1A03	# A相の周波数  (Hz単位)
        #ACL_FREQ_B						= 0x1A04	# B相の周波数  (Hz単位) 
        #ACL_FREQ_Z						= 0x1A05	# Z相の周波数  (Hz単位)
        #ACL_FREQ_TTL1					= 0x1A08	# TTL1の周波数 (Hz単位)
        #ACL_FREQ_TTL2					= 0x1A09	# TTL2の周波数 (Hz単位)
        #ACL_FREQ_TTL3					= 0x1A0A	# TTL3の周波数 (Hz単位)
        #ACL_FREQ_TTL4					= 0x1A0B	# TTL4の周波数 (Hz単位)
        #ACL_FREQ_TTL5					= 0x1A0C	# TTL5の周波数 (Hz単位)
        #ACL_FREQ_TTL6					= 0x1A0D	# TTL6の周波数 (Hz単位)
        #ACL_FREQ_TTL7					= 0x1A0E	# TTL7の周波数 (Hz単位)
        #ACL_FREQ_TTL8					= 0x1A0F	# TTL8の周波数 (Hz単位)
        #ACL_FREQ_OPT1					= 0x1A10	# OPT1の周波数 (Hz単位)
        #ACL_FREQ_OPT2					= 0x1A11	# OPT2の周波数 (Hz単位)
        #ACL_FREQ_OPT3					= 0x1A12	# OPT3の周波数 (Hz単位)
        #ACL_FREQ_OPT4					= 0x1A13	# OPT4の周波数 (Hz単位)
        #ACL_FREQ_OPT5					= 0x1A14	# OPT5の周波数 (Hz単位)
        #ACL_FREQ_OPT6					= 0x1A15	# OPT6の周波数 (Hz単位)
        #ACL_FREQ_OPT7					= 0x1A16	# OPT7の周波数 (Hz単位)
        #ACL_FREQ_OPT8					= 0x1A17	# OPT8の周波数 (Hz単位)
        #ACL_FREQ_D						= 0x1A18	# D相の周波数  (Hz単位)


        _, self.__driver_name = self.get_info(acaplib2.ACL_DRIVER_NAME)
        _, self.__hw_protect = self.get_info(acaplib2.ACL_HW_PROTECT)



        # リングバッファの確保
        self._create_ring_buffer()
        # イベント登録
        acaplib2.AcapSetEvent(self.__hHandle, self.__ch, acaplib2.ACL_INT_FRAMEEND, 1)
        acaplib2.AcapSetEvent(self.__hHandle, self.__ch, acaplib2.ACL_INT_GRABEND, 1)

        # グラブ中のフラグ
        self.__is_grab = False

        # 設定値の反映
        self.refrect_param()
        
    def load_inifile(self, inifilename):
        '''select_fileと同じ'''
        return self.select_file(inifilename)

    def set_power_supply(self, wait_time, value):
        if wait_time < 100:
            wait_time = 100
        self.set_info(acaplib2.ACL_POWER_SUPPLY, value, wait_time)

    def set_tap_direction(self, mem_num, value):
        self.set_info(acaplib2.ACL_TAP_DIRECTION, value, mem_num)

    def get_tap_direction(self, mem_num, value):
        _, value = self.get_info(acaplib2.ACL_TAP_DIRECTION, mem_num)
        return value


    def grab_start(self, input_num = 0):

        if self.__refrect_param_flag == True:
            self.refrect_param()

        self.last_frame_no = 0
        self.__is_grab = True
        return acaplib2.AcapGrabStart(self.__hHandle, self.__ch, input_num )

    def grab_stop(self):
        ret = acaplib2.AcapGrabStop(self.__hHandle, self.__ch)
        self.__is_grab = False
        return ret

    def grab_abort(self):
        ret = acaplib2.AcapGrabAbort(self.__hHandle, self.__ch)
        self.__is_grab = False
        return ret

    def wait_frame_end(self):
        return acaplib2.AcapWaitEvent(self.__hHandle, self.__ch, acaplib2.ACL_INT_FRAMEEND, self.__timeout)

    def wait_grab_end(self):
        return acaplib2.AcapWaitEvent(self.__hHandle, self.__ch, acaplib2.ACL_INT_GRABEND, self.__timeout * self.__mem_num)

    def get_frame_no(self):
        '''
        現在のフレーム番号を取得する
        Returns
        ----------
        ret : int
            成功(1), 失敗(0)
        frame_no : int
            現在の入力が完了したフレーム番号
        line : int
            現在の入力が完了したライン番号
        index : int
            現在入力が完了したメモリ番号(1, 2, 3・・・)
        '''
        return acaplib2.AcapGetFrameNo(self.__hHandle, self.__ch)
    
    def read(self):

        self.wait_frame_end() # フレームの入力完了を待つ

        # 現在のフレーム番号の取得
        ret, frame_no, _, index = self.get_frame_no()
        if ret != self.OK:
            return ret, None, 0

        frame = self.__images[index - 1] # 画像データ(ndarray)

        return ret, frame, frame_no

    def read_frames(self):
        '''
        前回取得したフレーム画像の次のフレームから現在のフレーム画像までを取得
        Returns
        ----------
        ret : int
            成功(1), 失敗(0)
        frames : ndarray
            前回取得したフレーム画像の次のフレームから現在のフレーム画像までの配列
        count : int
            取得したフレーム画像の枚数
        frame_no : int
            現在の入力が完了したフレーム番号
        '''

        self.wait_frame_end() # フレームの入力完了を待つ

        # 現在のフレーム番号の取得
        ret, frame_no, _, index = self.get_frame_no()
        index -= 1

        if ret != self.OK:
            self.print_last_error()
            return ret, None, 0, 0

        count = frame_no - self.last_frame_no

        if count > self.__mem_num:
            self._debug_print("[Warning] read_frames: ring buffer overlapped")
            ret = self.ERROR
        else:
            ret = self.OK

        frames = []

        # 前回のフレーム番号の次から、現在のフレーム番号までを処理する
        for fno in range(self.last_frame_no + 1, frame_no + 1):
            index_no = (index + fno - frame_no + self.__mem_num) % self.__mem_num
            image = self.__images[index_no] # 画像データ(ndarray)
            frames.append(image)

        self.last_frame_no = frame_no

        return ret, frames, count, frame_no

    def _create_ring_buffer(self):
        # リングバッファの確保（mem_numの設定時、サイズ変更時に同時に行う）

        # バッファを解除
        ret = acaplib2.AcapSetBufferAddress(
            self.__hHandle, 
            self.__ch, 
            acaplib2.ACL_IMAGE_PTR, 
            0, 
            0)

        if ret != self.OK:
            self.print_last_error()

        self.__images = acaplib2.CreateRingBuf(self.__hHandle, self.__ch, self.__mem_num)

        for i in range(self.__mem_num):
            ret = acaplib2.AcapSetBufferAddress(
                self.__hHandle, 
                self.__ch, 
                acaplib2.ACL_IMAGE_PTR, 
                -(i + 1), 
                acaplib2.GetRingBufPointer(self.__images, self.__width, self.__height, i)
                )
        #ret = self.refrect_param()
        self.__refrect_param_flag = True

    def snap(self):
        '''Snap:frame_num枚の画像取込(連続取込をする場合はGrabを使用のこと)'''

        if (self.__is_grab == True):
            return None

        # 入力開始
        if self.grab_start(1) != AcaPy.OK:
            self.print_last_error()
            return None

        self.__is_grab = True

        # フレーム画像の読込
        ret, image, _ = self.read()

        # 入力停止
        if self.grab_stop() != AcaPy.OK:
            self.print_last_error()
            self.__is_grab = False
            return None

        self.__is_grab = False

        # 現在のフレーム番号の取得
        return ret, image

    def print_acapy_values(self):
        for key, value in self.__dict__.items():
            if key.startswith("_AcaPy__images") == False:
                self._debug_print(key[8:] + "\t", value)

    def _debug_print(self, str1, str2 = "", str3 = "", str4 = "", str5 = ""):
        if self.__debug_print == False:
            return
        print(str1, str2, str3, str4, str5)

    def get_last_error(self, error_reset = False):
        return acaplib2.AcapGetLastErrorCode(error_reset)

    def print_last_error(self):
        ret, error_info = self.get_last_error()
        self._debug_print(
            "------------------ Error --------------------\n" +
            "Error code\t:"+ str(acaplib2.get_error_name(error_info.dwCommonErrorCode)) + "\n" +
            "Explanation\t:" + str(acaplib2.get_error_name(error_info.dwBoardErrorCode & 0x00FF)) + "\n" +
            "Extend\t\t:" + str(acaplib2.get_error_name(error_info.dwExtendErrorCode)) + "\n" +
            "---------------------------------------------"
            )
        return ret, error_info

    def set_shutter_trigger(self, exp_cycle, exposure, exp_pol, exp_unit, cc_sel):
        ret = acaplib2.AcapSetShutterTrigger(
                self.__hHandle, self.__ch, 
                exp_cycle, exposure, exp_pol, exp_unit, cc_sel
                )
        if ret != self.OK:
            self.print_last_error()
        return ret

    def get_shutter_trigger(self):
        ret = acaplib2.AcapGetShutterTrigger(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    def set_line_trigger(self, exp_cycle, exposure, exp_pol):
        ret = acaplib2.AcapSetLineTrigger(self.__hHandle, self.__ch, exp_cycle, exposure, exp_pol)
        if ret != self.OK:
            self.print_last_error()
        return ret

    def get_line_trigger(self):
        # -> exp_cycle, exposure, exp_pol, exp_unit, cc_sel
        ret = acaplib2.AcapGetLineTrigger(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    def set_external_trigger(self, exp_trg_en, ext_trg_mode, ext_trg_dly, ext_trg_chatter, timeout):
        ret = acaplib2.AcapSetExternalTrigger(self.__hHandle, self.__ch, exp_trg_en, ext_trg_mode, ext_trg_dly, ext_trg_chatter, timeout)
        if ret != self.OK:
            self.print_last_error()
        return ret

    def get_external_trigger(self):
        # -> exp_cycle, exposure, exp_pol, exp_unit, cc_sel
        ret = acaplib2.AcapGetExternalTrigger(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    def set_strobe(self, strobe_en, strobe_delay, strobe_time):
        ret = acaplib2.AcapSetStrobe(self.__hHandle, self.__ch, strobe_en, strobe_delay, strobe_time)
        if ret != self.OK:
            self.print_last_error()
        return ret

    def get_strobe(self):
        ret = acaplib2.AcapGetStrobe(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    def set_encoder(self, strobe_en, enc_enable, enc_mode, enc_start, enc_phase, enc_direction, z_phase_enable, compare1, compare2):
        ret = acaplib2.AcapSetEncoder(self.__hHandle, self.__ch, enc_enable, enc_mode, enc_start, enc_phase, enc_direction, z_phase_enable, compare1, compare2)
        if ret != self.OK:
            self.print_last_error()
        return ret

    def get_encoder(self):
        ret = acaplib2.AcapGetEncoder(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    #def set_bit_assign_ex(self, bit_assign_info):
    #    ret = acaplib2.AcapSetBitAssignEx(self.__hHandle, self.__ch, bit_assign_info)
    #    if ret != self.OK:
    #        self.print_last_error()
    #    return ret

    #def get_bit_assign_ex(self):
    #    ret = acaplib2.AcapGetBitAssignEx(self.__hHandle, self.__ch)
    #    if ret[0] != self.OK:
    #        self.print_last_error()
    #    return ret

    #def set_dma_option_ex(self, mem_num, acl_buffer_info):
    #    ret = acaplib2.AcapSetDmaOptionEx(self.__hHandle, self.__ch, mem_num, acl_buffer_info)
    #    if ret != self.OK:
    #        self.print_last_error()
    #    return ret

    #def get_dma_option_ex(self, mem_num):
    #    ret = acaplib2.AcapGetDmaOptionEx(self.__hHandle, self.__ch, mem_num)
    #    if ret[0] != self.OK:
    #        self.print_last_error()
    #    return ret


    def serial_open(self):
        ret = acaplib2.AcapSerialOpen(self.__hHandle, self.__ch)
        if ret != self.OK:
            self.print_last_error()
        return ret

    def serial_close(self):
        ret = acaplib2.AcapSerialClose(self.__hHandle, self.__ch)
        if ret != self.OK:
            self.print_last_error()
        return ret

    def serial_write(self, ascii, write_command, start_str = None, end_str = None):
        ret = acaplib2.AcapSerialWrite(self.__hHandle, self.__ch, ascii, write_command, start_str, end_str)
        if ret != self.OK:
            self.print_last_error()
        return ret
    
    def serial_read(self, ascii, time_out, buffer_size, end_str = None):
        ret = acaplib2.AcapSerialRead(self.__hHandle, self.__ch, ascii, time_out, buffer_size, end_str)
        if ret != self.OK:
            self.print_last_error()
        return ret
    