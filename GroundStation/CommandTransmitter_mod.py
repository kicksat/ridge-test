#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Commandtransmitter V2
# Generated: Sun Nov 11 11:21:49 2018
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

from PyQt5 import Qt
from PyQt5 import Qt, QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import sip
import sys
from gnuradio import qtgui

import amp_controller	#Controlls arduino


class CommandTransmitter_v2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Commandtransmitter V2")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Commandtransmitter V2")
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

        self.settings = Qt.QSettings("GNU Radio", "CommandTransmitter_v2")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.file_rate = file_rate = 160e3
        self.command_select = command_select = 0
        self.TX_Command_3 = TX_Command_3 = 0
        self.TX_Command_2 = TX_Command_2 = 0
        self.TX_Command_1 = TX_Command_1 = 0

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
        	1024, #size
        	file_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

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

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	file_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_win)

        self.qtgui_sink_x_0.enable_rf_freq(False)



        self.blocks_throttle_0_1 = blocks.throttle(gr.sizeof_gr_complex*1, file_rate,True)
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, file_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, file_rate,True)
        self.blocks_file_source_0_1 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/tane/Documents/RExLab/ridge-test/Commands/command3.iq', False)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/tane/Documents/RExLab/ridge-test/Commands/command2.iq', False)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/tane/Documents/RExLab/ridge-test/Commands/command1.iq', False)
        self.blks2_selector_1 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=4,
        	num_outputs=1,
        	input_index=command_select,
        	output_index=0,
        )
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)
        _TX_Command_3_push_button = Qt.QPushButton("Command_3")
        self._TX_Command_3_choices = {'Pressed': 3, 'Released': 0}
        _TX_Command_3_push_button.pressed.connect(lambda: self.set_TX_Command_3(self._TX_Command_3_choices['Pressed']))
        _TX_Command_3_push_button.released.connect(lambda: self.set_TX_Command_3(self._TX_Command_3_choices['Released']))
        self.top_layout.addWidget(_TX_Command_3_push_button)
        _TX_Command_2_push_button = Qt.QPushButton("Command_2")
        self._TX_Command_2_choices = {'Pressed': 2, 'Released': 0}
        _TX_Command_2_push_button.pressed.connect(lambda: self.set_TX_Command_2(self._TX_Command_2_choices['Pressed']))
        _TX_Command_2_push_button.released.connect(lambda: self.set_TX_Command_2(self._TX_Command_2_choices['Released']))
        self.top_layout.addWidget(_TX_Command_2_push_button)
        _TX_Command_1_push_button = Qt.QPushButton("Command_1")
        self._TX_Command_1_choices = {'Pressed': 1, 'Released': 0}
        _TX_Command_1_push_button.pressed.connect(lambda: self.set_TX_Command_1(self._TX_Command_1_choices['Pressed']))
        _TX_Command_1_push_button.released.connect(lambda: self.set_TX_Command_1(self._TX_Command_1_choices['Released']))
        self.top_layout.addWidget(_TX_Command_1_push_button)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blks2_selector_1, 0))
        self.connect((self.blks2_selector_1, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blks2_selector_1, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_throttle_0_1, 0))
        self.connect((self.blocks_file_source_0_1, 0), (self.blocks_throttle_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blks2_selector_1, 1))
        self.connect((self.blocks_throttle_0_0, 0), (self.blks2_selector_1, 3))
        self.connect((self.blocks_throttle_0_1, 0), (self.blks2_selector_1, 2))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "CommandTransmitter_v2")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_file_rate(self):
        return self.file_rate

    def set_file_rate(self, file_rate):
        self.file_rate = file_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.file_rate)
        self.qtgui_sink_x_0.set_frequency_range(0, self.file_rate)
        self.blocks_throttle_0_1.set_sample_rate(self.file_rate)
        self.blocks_throttle_0_0.set_sample_rate(self.file_rate)
        self.blocks_throttle_0.set_sample_rate(self.file_rate)

    def get_command_select(self):
        return self.command_select

    def set_command_select(self, command_select):
        self.command_select = command_select
        self.blks2_selector_1.set_input_index(int(self.command_select))

    def get_TX_Command_3(self):
        return self.TX_Command_3

    def set_TX_Command_3(self, TX_Command_3):
        self.TX_Command_3 = TX_Command_3
	self.blocks_file_source_0_1.seek(long(0),int(0))
	self.set_command_select(TX_Command_3)
	if TX_Command_3 == 0:		#If transmit button released
		amp_controller.rx()	#Switch radio to receive
	else:
		amp_controller.tx()	#Switch Radio to transmit

    def get_TX_Command_2(self):
        return self.TX_Command_2

    def set_TX_Command_2(self, TX_Command_2):
        self.TX_Command_2 = TX_Command_2
	self.blocks_file_source_0_0.seek(long(0),int(0))
	self.set_command_select(TX_Command_2)
	if TX_Command_2 == 0:		#If transmit button released
		amp_controller.rx()	#Switch radio to receive
	else:
		amp_controller.tx()	#Switch Radio to transmit

    def get_TX_Command_1(self):
        return self.TX_Command_1

    def set_TX_Command_1(self, TX_Command_1):
        self.TX_Command_1 = TX_Command_1
	self.set_command_select(TX_Command_1)
	self.blocks_file_source_0.seek(long(0),int(0))
	if TX_Command_1 == 0:		#If transmit button released
		amp_controller.rx()	#Switch radio to receive
	else:
		amp_controller.tx()	#Switch Radio to transmit
			


def main(top_block_cls=CommandTransmitter_v2, options=None):

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
