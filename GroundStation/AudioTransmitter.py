#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Audiotransmitter
# Generated: Mon Dec  3 14:49:32 2018
##################################################


from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser


class AudioTransmitter(gr.top_block):

    def __init__(self, command_select=0):
        gr.top_block.__init__(self, "Audiotransmitter")

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
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blks2_selector_1 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=4,
        	num_outputs=1,
        	input_index=command_select,
        	output_index=0,
        )
        self.audio_sink_0 = audio.sink(int(file_rate), '', True)
        self.analog_sig_source_x_0_1 = analog.sig_source_c(file_rate, analog.GR_COS_WAVE, 440, 1, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(file_rate, analog.GR_COS_WAVE, 440, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(file_rate, analog.GR_COS_WAVE, 440, 1, 0)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blks2_selector_1, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blks2_selector_1, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blks2_selector_1, 2))
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blks2_selector_1, 3))
        self.connect((self.blks2_selector_1, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.audio_sink_0, 0))

    def get_command_select(self):
        return self.command_select

    def set_command_select(self, command_select):
        self.command_select = command_select
        self.blks2_selector_1.set_input_index(int(self.command_select))

    def get_tx_rate(self):
        return self.tx_rate

    def set_tx_rate(self, tx_rate):
        self.tx_rate = tx_rate

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_file_rate(self):
        return self.file_rate

    def set_file_rate(self, file_rate):
        self.file_rate = file_rate
        self.analog_sig_source_x_0_1.set_sampling_freq(self.file_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.file_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.file_rate)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    return parser


def main(top_block_cls=AudioTransmitter, options=None):
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
