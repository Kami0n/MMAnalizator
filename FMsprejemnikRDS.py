#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: FM sprejemnik RDS
# Generated: Mon Mar 23 11:59:16 2020
##################################################


if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import digital;import cmath
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import rds
import time
import wx


class FMsprejemnikRDS(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="FM sprejemnik RDS")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.sampleOut = sampleOut = 30000
        self.samp_rate = samp_rate = 2.8e6
        self.quadrature = quadrature = 280000
        self.frekvenca = frekvenca = 106900000

        ##################################################
        # Blocks
        ##################################################
        self.nbook = self.nbook = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.nbook.AddPage(grc_wxgui.Panel(self.nbook), "Vhodni Spekter")
        self.nbook.AddPage(grc_wxgui.Panel(self.nbook), "MPX spekter")
        self.nbook.AddPage(grc_wxgui.Panel(self.nbook), "L+R")
        self.nbook.AddPage(grc_wxgui.Panel(self.nbook), "RDS spekter")
        self.nbook.AddPage(grc_wxgui.Panel(self.nbook), "RDS scope")
        self.Add(self.nbook)
        _frekvenca_sizer = wx.BoxSizer(wx.VERTICAL)
        self._frekvenca_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_frekvenca_sizer,
        	value=self.frekvenca,
        	callback=self.set_frekvenca,
        	label='Frekvenca',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._frekvenca_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_frekvenca_sizer,
        	value=self.frekvenca,
        	callback=self.set_frekvenca,
        	minimum=80000000,
        	maximum=110000000,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_frekvenca_sizer)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_c(
        	self.nbook.GetPage(4).GetWin(),
        	title='Scope Plot',
        	sample_rate=2375,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=True,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label='Counts',
        )
        self.nbook.GetPage(4).Add(self.wxgui_scopesink2_0.win)
        self.wxgui_fftsink2_3 = fftsink2.fft_sink_c(
        	self.nbook.GetPage(3).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=280000,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=0.1333,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.nbook.GetPage(3).Add(self.wxgui_fftsink2_3.win)
        self.wxgui_fftsink2_2 = fftsink2.fft_sink_c(
        	self.nbook.GetPage(0).GetWin(),
        	baseband_freq=frekvenca,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.1333,
        	title='SDR sprejem',
        	peak_hold=False,
        )
        self.nbook.GetPage(0).Add(self.wxgui_fftsink2_2.win)
        self.wxgui_fftsink2_1 = fftsink2.fft_sink_f(
        	self.nbook.GetPage(2).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=sampleOut,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.1333,
        	title='Audio',
        	peak_hold=False,
        )
        self.nbook.GetPage(2).Add(self.wxgui_fftsink2_1.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_f(
        	self.nbook.GetPage(1).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=140000,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.1333,
        	title='MPX spectrum',
        	peak_hold=False,
        )
        self.nbook.GetPage(1).Add(self.wxgui_fftsink2_0.win)
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=140,
                decimation=280,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=sampleOut/1000,
                decimation=quadrature/1000,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(frekvenca, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.low_pass_filter_0 = filter.fir_filter_ccf(10, firdes.low_pass(
        	1, samp_rate, 75000, 25000, firdes.WIN_HAMMING, 6.76))
        self.gr_rds_parser_0 = rds.parser(True, False, 0)
        self.gr_rds_panel_0 = rds.rdsPanel(frekvenca, self.GetWin())
        self.Add(self.gr_rds_panel_0.panel)
        self.gr_rds_decoder_0 = rds.decoder(False, False)
        self.digital_mpsk_receiver_cc_0 = digital.mpsk_receiver_cc(4, 0, cmath.pi/100.0, -0.06, 0.06, 0.25, 0.05, 117.895, 0.001, 0.005)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_char*1, 2)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.band_pass_filter_0 = filter.fir_filter_fcc(1, firdes.complex_band_pass(
        	2, quadrature, 55000, 59000, 500, firdes.WIN_HANN, 6.76))
        self.audio_sink_0 = audio.sink(sampleOut, 'hw:0,0', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=quadrature,
        	audio_decimation=1,
        )



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gr_rds_decoder_0, 'out'), (self.gr_rds_parser_0, 'in'))
        self.msg_connect((self.gr_rds_parser_0, 'out'), (self.gr_rds_panel_0, 'in'))
        self.connect((self.analog_wfm_rcv_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.band_pass_filter_0, 0), (self.digital_mpsk_receiver_cc_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.wxgui_fftsink2_3, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.gr_rds_decoder_0, 0))
        self.connect((self.digital_mpsk_receiver_cc_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.digital_mpsk_receiver_cc_0, 0), (self.wxgui_scopesink2_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.wxgui_fftsink2_2, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.audio_sink_0, 1))
        self.connect((self.rational_resampler_xxx_0, 0), (self.wxgui_fftsink2_1, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.wxgui_fftsink2_0, 0))

    def get_sampleOut(self):
        return self.sampleOut

    def set_sampleOut(self, sampleOut):
        self.sampleOut = sampleOut
        self.wxgui_fftsink2_1.set_sample_rate(self.sampleOut)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_2.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 75000, 25000, firdes.WIN_HAMMING, 6.76))

    def get_quadrature(self):
        return self.quadrature

    def set_quadrature(self, quadrature):
        self.quadrature = quadrature
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(2, self.quadrature, 55000, 59000, 500, firdes.WIN_HANN, 6.76))

    def get_frekvenca(self):
        return self.frekvenca

    def set_frekvenca(self, frekvenca):
        self.frekvenca = frekvenca
        self._frekvenca_slider.set_value(self.frekvenca)
        self._frekvenca_text_box.set_value(self.frekvenca)
        self.wxgui_fftsink2_2.set_baseband_freq(self.frekvenca)
        self.osmosdr_source_0.set_center_freq(self.frekvenca, 0)
        self.gr_rds_panel_0.set_frequency(self.frekvenca);


def main(top_block_cls=FMsprejemnikRDS, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
