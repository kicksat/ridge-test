#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Command Tx
# Generated: Mon Dec  3 15:29:45 2018
##################################################


from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import osmosdr
import time


class Command_TX(gr.top_block):

    def __init__(self, command_select=0):
        gr.top_block.__init__(self, "Command Tx")

        ##################################################
        # Parameters
        ##################################################
        self.command_select = command_select

        ##################################################
        # Variables
        ##################################################
        self.tx_rate = tx_rate = 2e6
        self.freq = freq = 433.5e6
        self.file_rate = file_rate = 160e3

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_sink_0.set_sample_rate(tx_rate)
        self.osmosdr_sink_0.set_center_freq(433.150e6, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(10, 0)
        self.osmosdr_sink_0.set_if_gain(1, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)

        self.blocks_file_source_2 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/tane/Documents/RExLab/ridge-test/Commands/command3.iq', False)
        self.blocks_file_source_1 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/tane/Documents/RExLab/ridge-test/Commands/command2.iq', False)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/tane/Documents/RExLab/ridge-test/Commands/command1.iq', False)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blks2_selector_1 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=3,
        	num_outputs=1,
        	input_index=command_select,
        	output_index=0,
        )
        self.audio_sink_0 = audio.sink(int(file_rate), '', True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_selector_1, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blks2_selector_1, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blks2_selector_1, 0))
        self.connect((self.blocks_file_source_1, 0), (self.blks2_selector_1, 1))
        self.connect((self.blocks_file_source_2, 0), (self.blks2_selector_1, 2))

    def get_command_select(self):
        return self.command_select

    def set_command_select(self, command_select):
        self.command_select = command_select
        self.blks2_selector_1.set_input_index(int(self.command_select))

    def get_tx_rate(self):
        return self.tx_rate

    def set_tx_rate(self, tx_rate):
        self.tx_rate = tx_rate
        self.osmosdr_sink_0.set_sample_rate(self.tx_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_file_rate(self):
        return self.file_rate

    def set_file_rate(self, file_rate):
        self.file_rate = file_rate


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    return parser


def main(top_block_cls=Command_TX, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
