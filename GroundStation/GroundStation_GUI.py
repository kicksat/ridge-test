#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Groundstation Gui
# Generated: Wed Dec 12 13:44:59 2018
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from PyQt5 import Qt, QtCore
from TX_Commands import TX_Commands  # grc-generated hier_block
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import math
import osmosdr
import sip
import time
from gnuradio import qtgui


class GroundStation_GUI(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Groundstation Gui")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Groundstation Gui")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "GroundStation_GUI")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Variables
        ##################################################
        self.tx_button_5 = tx_button_5 = 0
        self.tx_button_4 = tx_button_4 = 0
        self.tx_button_3 = tx_button_3 = 0
        self.tx_button_2 = tx_button_2 = 0
        self.tx_button_1 = tx_button_1 = 0
        self.samp_rate = samp_rate = 2e6
        self.data_rate = data_rate = 1200
        self.command_selection = command_selection = (tx_button_1+tx_button_2+tx_button_3+tx_button_4+tx_button_5)
        self.channel_spacing = channel_spacing = 200e3
        self.tx_rf_gain = tx_rf_gain = 14
        self.tx_rate = tx_rate = 2e6
        self.tx_if_gain = tx_if_gain = 47
        self.samp_per_sym = samp_per_sym = (samp_rate/data_rate)
        self.rx_rf_gain = rx_rf_gain = 14
        self.rx_if_gain = rx_if_gain = 24
        self.rx_bb_gain = rx_bb_gain = 20
        self.record_switch = record_switch = 0
        self.fsk_deviation_hz = fsk_deviation_hz = 32e3
        self.freq_offset = freq_offset = (channel_spacing/2)+(channel_spacing*0.10)
        self.freq_0 = freq_0 = 433.5e6
        self.freq = freq = 315e6
        self.file_rate = file_rate = 160e3
        self.channel_trans = channel_trans = (channel_spacing*0.4)
        self.TxRxSwitch = TxRxSwitch = int(command_selection>0)

        ##################################################
        # Blocks
        ##################################################
        self.sig_tabs = Qt.QTabWidget()
        self.sig_tabs_widget_0 = Qt.QWidget()
        self.sig_tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.sig_tabs_widget_0)
        self.sig_tabs_grid_layout_0 = Qt.QGridLayout()
        self.sig_tabs_layout_0.addLayout(self.sig_tabs_grid_layout_0)
        self.sig_tabs.addTab(self.sig_tabs_widget_0, 'Raw RX')
        self.sig_tabs_widget_1 = Qt.QWidget()
        self.sig_tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.sig_tabs_widget_1)
        self.sig_tabs_grid_layout_1 = Qt.QGridLayout()
        self.sig_tabs_layout_1.addLayout(self.sig_tabs_grid_layout_1)
        self.sig_tabs.addTab(self.sig_tabs_widget_1, 'Filtered')
        self.sig_tabs_widget_2 = Qt.QWidget()
        self.sig_tabs_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.sig_tabs_widget_2)
        self.sig_tabs_grid_layout_2 = Qt.QGridLayout()
        self.sig_tabs_layout_2.addLayout(self.sig_tabs_grid_layout_2)
        self.sig_tabs.addTab(self.sig_tabs_widget_2, 'Demodulated')
        self.top_grid_layout.addWidget(self.sig_tabs, 0, 1, 5, 5)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(0,5)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(1,6)]
        self._rx_rf_gain_range = Range(0, 14, 14, 14, 200)
        self._rx_rf_gain_win = RangeWidget(self._rx_rf_gain_range, self.set_rx_rf_gain, "rx_rf_gain", "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_rf_gain_win, 6, 3, 1, 3)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(6,7)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(3,6)]
        self._rx_if_gain_range = Range(0, 40, 8, 24, 200)
        self._rx_if_gain_win = RangeWidget(self._rx_if_gain_range, self.set_rx_if_gain, "rx_if_gain", "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_if_gain_win, 7, 3, 1, 3)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(7,8)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(3,6)]
        self._rx_bb_gain_range = Range(0, 62, 2, 20, 200)
        self._rx_bb_gain_win = RangeWidget(self._rx_bb_gain_range, self.set_rx_bb_gain, "rx_bb_gain", "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_bb_gain_win, 8, 3, 1, 3)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(8,9)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(3,6)]
        self._tx_rf_gain_range = Range(0, 14, 14, 14, 200)
        self._tx_rf_gain_win = RangeWidget(self._tx_rf_gain_range, self.set_tx_rf_gain, "tx_rf_gain", "counter_slider", float)
        self.top_grid_layout.addWidget(self._tx_rf_gain_win, 6, 0, 1, 3)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(6,7)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,3)]
        self._tx_if_gain_range = Range(0, 47, 1, 47, 200)
        self._tx_if_gain_win = RangeWidget(self._tx_if_gain_range, self.set_tx_if_gain, "tx_if_gain", "counter_slider", float)
        self.top_grid_layout.addWidget(self._tx_if_gain_win, 7, 0, 1, 3)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(7,8)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,3)]
        _tx_button_5_push_button = Qt.QPushButton("Command 5")
        self._tx_button_5_choices = {'Pressed': 5, 'Released': 0}
        _tx_button_5_push_button.pressed.connect(lambda: self.set_tx_button_5(self._tx_button_5_choices['Pressed']))
        _tx_button_5_push_button.released.connect(lambda: self.set_tx_button_5(self._tx_button_5_choices['Released']))
        self.top_grid_layout.addWidget(_tx_button_5_push_button, 4, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(4,5)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        _tx_button_4_push_button = Qt.QPushButton("Command 4")
        self._tx_button_4_choices = {'Pressed': 4, 'Released': 0}
        _tx_button_4_push_button.pressed.connect(lambda: self.set_tx_button_4(self._tx_button_4_choices['Pressed']))
        _tx_button_4_push_button.released.connect(lambda: self.set_tx_button_4(self._tx_button_4_choices['Released']))
        self.top_grid_layout.addWidget(_tx_button_4_push_button, 3, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(3,4)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        _tx_button_3_push_button = Qt.QPushButton("Command 3")
        self._tx_button_3_choices = {'Pressed': 3, 'Released': 0}
        _tx_button_3_push_button.pressed.connect(lambda: self.set_tx_button_3(self._tx_button_3_choices['Pressed']))
        _tx_button_3_push_button.released.connect(lambda: self.set_tx_button_3(self._tx_button_3_choices['Released']))
        self.top_grid_layout.addWidget(_tx_button_3_push_button, 2, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(2,3)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        _tx_button_2_push_button = Qt.QPushButton("Command 2")
        self._tx_button_2_choices = {'Pressed': 2, 'Released': 0}
        _tx_button_2_push_button.pressed.connect(lambda: self.set_tx_button_2(self._tx_button_2_choices['Pressed']))
        _tx_button_2_push_button.released.connect(lambda: self.set_tx_button_2(self._tx_button_2_choices['Released']))
        self.top_grid_layout.addWidget(_tx_button_2_push_button, 1, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(1,2)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        _tx_button_1_push_button = Qt.QPushButton("Command 1")
        self._tx_button_1_choices = {'Pressed': 1, 'Released': 0}
        _tx_button_1_push_button.pressed.connect(lambda: self.set_tx_button_1(self._tx_button_1_choices['Pressed']))
        _tx_button_1_push_button.released.connect(lambda: self.set_tx_button_1(self._tx_button_1_choices['Released']))
        self.top_grid_layout.addWidget(_tx_button_1_push_button, 0, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(0,1)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        _record_switch_check_box = Qt.QCheckBox('Record Raw Signal')
        self._record_switch_choices = {True: 1, False: 0}
        self._record_switch_choices_inv = dict((v,k) for k,v in self._record_switch_choices.iteritems())
        self._record_switch_callback = lambda i: Qt.QMetaObject.invokeMethod(_record_switch_check_box, "setChecked", Qt.Q_ARG("bool", self._record_switch_choices_inv[i]))
        self._record_switch_callback(self.record_switch)
        _record_switch_check_box.stateChanged.connect(lambda i: self.set_record_switch(self._record_switch_choices[bool(i)]))
        self.top_grid_layout.addWidget(_record_switch_check_box, 8, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(8,9)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        self.record = blocks.multiply_const_vcc((record_switch, ))
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(tx_rate),
                decimation=int(file_rate),
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-50, 50)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.sig_tabs_layout_2.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	freq, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.sig_tabs_layout_1.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	freq+freq_offset, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.sig_tabs_layout_0.addWidget(self._qtgui_freq_sink_x_0_win)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "soapy=0,driver=hackrf" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq+freq_offset, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rx_rf_gain, 0)
        self.osmosdr_source_0.set_if_gain(rx_if_gain, 0)
        self.osmosdr_source_0.set_bb_gain(rx_bb_gain, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "soapy=0,driver=hackrf" )
        self.osmosdr_sink_0.set_sample_rate(tx_rate)
        self.osmosdr_sink_0.set_center_freq(433.150e6, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(10, 0)
        self.osmosdr_sink_0.set_if_gain(1, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)

        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (firdes.low_pass(1,  samp_rate, channel_spacing, channel_trans, firdes.WIN_BLACKMAN, 6.76)), -freq_offset, samp_rate)
        self.dc_blocker_xx_0 = filter.dc_blocker_cc(32, True)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/tane/Documents/RExLab/ridge-test/GroundStation/Recordings/raw.dat', False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blks2_selector_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=2,
        	num_outputs=2,
        	input_index=TxRxSwitch,
        	output_index=TxRxSwitch,
        )
        self.audio_sink_0 = audio.sink(int(file_rate), '', True)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(samp_rate/(2*math.pi*fsk_deviation_hz/8.0))
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(-200, 1e-4, 0, True)
        self.TX_Commands_0 = TX_Commands(
            command_select=command_selection,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.TX_Commands_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.TX_Commands_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blks2_selector_0, 0), (self.dc_blocker_xx_0, 0))
        self.connect((self.blks2_selector_0, 1), (self.osmosdr_sink_0, 0))
        self.connect((self.blks2_selector_0, 0), (self.record, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.audio_sink_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blks2_selector_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blks2_selector_0, 1))
        self.connect((self.record, 0), (self.analog_pwr_squelch_xx_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "GroundStation_GUI")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tx_button_5(self):
        return self.tx_button_5

    def set_tx_button_5(self, tx_button_5):
        self.tx_button_5 = tx_button_5
        self.set_command_selection((self.tx_button_1+self.tx_button_2+self.tx_button_3+self.tx_button_4+self.tx_button_5))

    def get_tx_button_4(self):
        return self.tx_button_4

    def set_tx_button_4(self, tx_button_4):
        self.tx_button_4 = tx_button_4
        self.set_command_selection((self.tx_button_1+self.tx_button_2+self.tx_button_3+self.tx_button_4+self.tx_button_5))

    def get_tx_button_3(self):
        return self.tx_button_3

    def set_tx_button_3(self, tx_button_3):
        self.tx_button_3 = tx_button_3
        self.set_command_selection((self.tx_button_1+self.tx_button_2+self.tx_button_3+self.tx_button_4+self.tx_button_5))

    def get_tx_button_2(self):
        return self.tx_button_2

    def set_tx_button_2(self, tx_button_2):
        self.tx_button_2 = tx_button_2
        self.set_command_selection((self.tx_button_1+self.tx_button_2+self.tx_button_3+self.tx_button_4+self.tx_button_5))

    def get_tx_button_1(self):
        return self.tx_button_1

    def set_tx_button_1(self, tx_button_1):
        self.tx_button_1 = tx_button_1
        self.set_command_selection((self.tx_button_1+self.tx_button_2+self.tx_button_3+self.tx_button_4+self.tx_button_5))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_per_sym((self.samp_rate/self.data_rate))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq+self.freq_offset, self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1,  self.samp_rate, self.channel_spacing, self.channel_trans, firdes.WIN_BLACKMAN, 6.76)))
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/(2*math.pi*self.fsk_deviation_hz/8.0))

    def get_data_rate(self):
        return self.data_rate

    def set_data_rate(self, data_rate):
        self.data_rate = data_rate
        self.set_samp_per_sym((self.samp_rate/self.data_rate))

    def get_command_selection(self):
        return self.command_selection

    def set_command_selection(self, command_selection):
        self.command_selection = command_selection
        self.set_TxRxSwitch(int(self.command_selection>0))
        self.TX_Commands_0.set_command_select(self.command_selection)

    def get_channel_spacing(self):
        return self.channel_spacing

    def set_channel_spacing(self, channel_spacing):
        self.channel_spacing = channel_spacing
        self.set_freq_offset((self.channel_spacing/2)+(self.channel_spacing*0.10))
        self.set_channel_trans((self.channel_spacing*0.4))
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1,  self.samp_rate, self.channel_spacing, self.channel_trans, firdes.WIN_BLACKMAN, 6.76)))

    def get_tx_rf_gain(self):
        return self.tx_rf_gain

    def set_tx_rf_gain(self, tx_rf_gain):
        self.tx_rf_gain = tx_rf_gain

    def get_tx_rate(self):
        return self.tx_rate

    def set_tx_rate(self, tx_rate):
        self.tx_rate = tx_rate
        self.osmosdr_sink_0.set_sample_rate(self.tx_rate)

    def get_tx_if_gain(self):
        return self.tx_if_gain

    def set_tx_if_gain(self, tx_if_gain):
        self.tx_if_gain = tx_if_gain

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym

    def get_rx_rf_gain(self):
        return self.rx_rf_gain

    def set_rx_rf_gain(self, rx_rf_gain):
        self.rx_rf_gain = rx_rf_gain
        self.osmosdr_source_0.set_gain(self.rx_rf_gain, 0)

    def get_rx_if_gain(self):
        return self.rx_if_gain

    def set_rx_if_gain(self, rx_if_gain):
        self.rx_if_gain = rx_if_gain
        self.osmosdr_source_0.set_if_gain(self.rx_if_gain, 0)

    def get_rx_bb_gain(self):
        return self.rx_bb_gain

    def set_rx_bb_gain(self, rx_bb_gain):
        self.rx_bb_gain = rx_bb_gain
        self.osmosdr_source_0.set_bb_gain(self.rx_bb_gain, 0)

    def get_record_switch(self):
        return self.record_switch

    def set_record_switch(self, record_switch):
        self.record_switch = record_switch
        self._record_switch_callback(self.record_switch)
        self.record.set_k((self.record_switch, ))

    def get_fsk_deviation_hz(self):
        return self.fsk_deviation_hz

    def set_fsk_deviation_hz(self, fsk_deviation_hz):
        self.fsk_deviation_hz = fsk_deviation_hz
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/(2*math.pi*self.fsk_deviation_hz/8.0))

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq+self.freq_offset, self.samp_rate)
        self.osmosdr_source_0.set_center_freq(self.freq+self.freq_offset, 0)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(-self.freq_offset)

    def get_freq_0(self):
        return self.freq_0

    def set_freq_0(self, freq_0):
        self.freq_0 = freq_0

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq+self.freq_offset, self.samp_rate)
        self.osmosdr_source_0.set_center_freq(self.freq+self.freq_offset, 0)

    def get_file_rate(self):
        return self.file_rate

    def set_file_rate(self, file_rate):
        self.file_rate = file_rate

    def get_channel_trans(self):
        return self.channel_trans

    def set_channel_trans(self, channel_trans):
        self.channel_trans = channel_trans
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1,  self.samp_rate, self.channel_spacing, self.channel_trans, firdes.WIN_BLACKMAN, 6.76)))

    def get_TxRxSwitch(self):
        return self.TxRxSwitch

    def set_TxRxSwitch(self, TxRxSwitch):
        self.TxRxSwitch = TxRxSwitch
        self.blks2_selector_0.set_input_index(int(self.TxRxSwitch))
        self.blks2_selector_0.set_output_index(int(self.TxRxSwitch))


def main(top_block_cls=GroundStation_GUI, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
