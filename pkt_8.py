#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: pkt_8
# Author: Barry Duggan
# Description: packet transmit
# GNU Radio version: 3.10.9.2

from gnuradio import blocks
from gnuradio import blocks, gr
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import network




class pkt_8(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "pkt_8", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.access_key = access_key = '11100001010110101110100010010011'
        self.thresh = thresh = 1
        self.sync_word2 = sync_word2 = [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
        self.sync_word1 = sync_word1 = [0, 0, 0, 0, 0, 0, 0, 1.41421356, 0, -1.41421356, 0, 1.41421356, 0, -1.41421356, 0, -1.41421356, 0, -1.41421356, 0, 1.41421356, 0, -1.41421356, 0, 1.41421356, 0, -1.41421356, 0, -1.41421356, 0, -1.41421356, 0, -1.41421356, 0, 1.41421356, 0, -1.41421356, 0, 1.41421356, 0, 1.41421356, 0, 1.41421356, 0, -1.41421356, 0, 1.41421356, 0, 1.41421356, 0, 1.41421356, 0, -1.41421356, 0, 1.41421356, 0, 1.41421356, 0, 1.41421356, 0, 0, 0, 0, 0, 0]
        self.hdr_format = hdr_format = digital.header_format_default(access_key, 0)

        ##################################################
        # Blocks
        ##################################################

        self.pdu_tagged_stream_to_pdu_0_0_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'packet_len_1')
        self.pdu_tagged_stream_to_pdu_0_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'rx_packets')
        self.pdu_pdu_to_tagged_stream_0_1 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len_1')
        self.pdu_pdu_to_tagged_stream_0_0_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len_1')
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len_0')
        self.network_tuntap_pdu_0_0 = network.tuntap_pdu('tnc1', 576, False)
        self.network_tuntap_pdu_0 = network.tuntap_pdu('tnc0', 576, False)
        self.digital_protocol_formatter_async_0_0 = digital.protocol_formatter_async(hdr_format)
        self.digital_ofdm_tx_0_0 = digital.ofdm_tx(
            fft_len=64,
            cp_len=16,
            packet_length_tag_key='packet_len_0',
            occupied_carriers=((-4,-3,-2,-1,1,2,3,4),),
            pilot_carriers=((-6,-5,5,6),),
            pilot_symbols=((-1,1,-1,1),),
            sync_word1=None,
            sync_word2=None,
            bps_header=1,
            bps_payload=2,
            rolloff=0,
            debug_log=False,
            scramble_bits=False)
        self.digital_ofdm_tx_0_0.set_min_output_buffer(100000)
        self.digital_ofdm_rx_0_0 = digital.ofdm_rx(
            fft_len=64, cp_len=16,
            frame_length_tag_key='frame_'+'rx_packets',
            packet_length_tag_key='rx_packets',
            occupied_carriers=((-4,-3,-2,-1,1,2,3,4),),
            pilot_carriers=((-6,-5,5,6),),
            pilot_symbols=((-1,1,-1,1),),
            sync_word1=None,
            sync_word2=None,
            bps_header=1,
            bps_payload=2,
            debug_log=False,
            scramble_bits=False)
        self.digital_ofdm_rx_0_0.set_min_output_buffer(100000)
        self.digital_crc_check_0_0 = digital.crc_check(32, 0x4C11DB7, 0xFFFFFFFF, 0xFFFFFFFF, True, True, False, True, 0)
        self.digital_crc_check_0 = digital.crc_check(32, 0x4C11DB7, 0xFFFFFFFF, 0xFFFFFFFF, True, True, False, True, 0)
        self.digital_crc_append_0_0 = digital.crc_append(32, 0x4C11DB7, 0xFFFFFFFF, 0xFFFFFFFF, True, True, False, 0)
        self.digital_crc_append_0 = digital.crc_append(32, 0x4C11DB7, 0xFFFFFFFF, 0xFFFFFFFF, True, True, False, 0)
        self.digital_correlate_access_code_xx_ts_0_0 = digital.correlate_access_code_bb_ts(access_key,
          thresh, 'packet_len_1')
        self.blocks_tagged_stream_mux_0_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len_1', 0)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_char*1, 'Rx Packets', "")
        self.blocks_tag_debug_0.set_display(False)
        self.blocks_repack_bits_bb_1_0_1 = blocks.repack_bits_bb(8, 1, "packet_len_1", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_1_0_0_0 = blocks.repack_bits_bb(1, 8, "packet_len_1", False, gr.GR_MSB_FIRST)
        self.blocks_message_debug_0 = blocks.message_debug(True, gr.log_levels.info)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_crc_append_0, 'out'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.digital_crc_append_0_0, 'out'), (self.digital_protocol_formatter_async_0_0, 'in'))
        self.msg_connect((self.digital_crc_check_0, 'ok'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.digital_crc_check_0, 'ok'), (self.network_tuntap_pdu_0_0, 'pdus'))
        self.msg_connect((self.digital_crc_check_0_0, 'ok'), (self.network_tuntap_pdu_0, 'pdus'))
        self.msg_connect((self.digital_protocol_formatter_async_0_0, 'payload'), (self.pdu_pdu_to_tagged_stream_0_0_0, 'pdus'))
        self.msg_connect((self.digital_protocol_formatter_async_0_0, 'header'), (self.pdu_pdu_to_tagged_stream_0_1, 'pdus'))
        self.msg_connect((self.network_tuntap_pdu_0, 'pdus'), (self.digital_crc_append_0, 'in'))
        self.msg_connect((self.network_tuntap_pdu_0_0, 'pdus'), (self.digital_crc_append_0_0, 'in'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0_0, 'pdus'), (self.digital_crc_check_0, 'in'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0_0_0, 'pdus'), (self.digital_crc_check_0_0, 'in'))
        self.connect((self.blocks_repack_bits_bb_1_0_0_0, 0), (self.pdu_tagged_stream_to_pdu_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_1_0_1, 0), (self.digital_correlate_access_code_xx_ts_0_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_0, 0), (self.blocks_repack_bits_bb_1_0_1, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0_0, 0), (self.blocks_repack_bits_bb_1_0_0_0, 0))
        self.connect((self.digital_ofdm_rx_0_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.digital_ofdm_rx_0_0, 0), (self.pdu_tagged_stream_to_pdu_0_0, 0))
        self.connect((self.digital_ofdm_tx_0_0, 0), (self.digital_ofdm_rx_0_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.digital_ofdm_tx_0_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0_0_0, 0), (self.blocks_tagged_stream_mux_0_0, 1))
        self.connect((self.pdu_pdu_to_tagged_stream_0_1, 0), (self.blocks_tagged_stream_mux_0_0, 0))


    def get_access_key(self):
        return self.access_key

    def set_access_key(self, access_key):
        self.access_key = access_key
        self.set_hdr_format(digital.header_format_default(self.access_key, 0))

    def get_thresh(self):
        return self.thresh

    def set_thresh(self, thresh):
        self.thresh = thresh

    def get_sync_word2(self):
        return self.sync_word2

    def set_sync_word2(self, sync_word2):
        self.sync_word2 = sync_word2

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format




def main(top_block_cls=pkt_8, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
