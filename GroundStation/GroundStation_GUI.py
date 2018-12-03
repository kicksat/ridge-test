#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Groundstation Gui
# Generated: Mon Dec  3 15:26:40 2018
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

from Command_TX import Command_TX  # grc-generated hier_block
from PyQt5 import Qt
from PyQt5 import Qt, QtCore
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
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
        self.tx_button_2 = tx_button_2 = 0
        self.tx_button_1 = tx_button_1 = 0
        self.samp_rate = samp_rate = 2e6
        self.freq = freq = 433e6

        ##################################################
        # Blocks
        ##################################################
        _tx_button_2_push_button = Qt.QPushButton("Command 2")
        self._tx_button_2_choices = {'Pressed': 1, 'Released': 0}
        _tx_button_2_push_button.pressed.connect(lambda: self.set_tx_button_2(self._tx_button_2_choices['Pressed']))
        _tx_button_2_push_button.released.connect(lambda: self.set_tx_button_2(self._tx_button_2_choices['Released']))
        self.top_layout.addWidget(_tx_button_2_push_button)
        _tx_button_1_push_button = Qt.QPushButton("Command 1")
        self._tx_button_1_choices = {'Pressed': 1, 'Released': 0}
        _tx_button_1_push_button.pressed.connect(lambda: self.set_tx_button_1(self._tx_button_1_choices['Pressed']))
        _tx_button_1_push_button.released.connect(lambda: self.set_tx_button_1(self._tx_button_1_choices['Released']))
        self.top_layout.addWidget(_tx_button_1_push_button)
        self.Command_TX_0 = Command_TX(
            command_select=0,
        )

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "GroundStation_GUI")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tx_button_2(self):
        return self.tx_button_2

    def set_tx_button_2(self, tx_button_2):
        self.tx_button_2 = tx_button_2

    def get_tx_button_1(self):
        return self.tx_button_1

    def set_tx_button_1(self, tx_button_1):
        self.tx_button_1 = tx_button_1
	if tx_button_1 == 1:
		self.Command_TX_0.blocks_file_source_0.seek(long(0),int(0))
		self.Command_TX_0.run()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq


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
