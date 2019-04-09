#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################################################
#
# add_ids_to_xml.py
#
# In order to tell visualization systems, "highlight this
# thing at this time", the document has to be able to identify
# particular elements.  If the original document does NOT have
# id tags on its elements, this module adds some.
#
# The auto-generated IDs have formats like "s0w2m1" meaning
# "sentence 0, word 2, morpheme 1".  But it's flexible if some elements
# already have ids, or if the markup uses different tags than a TEI document.
#
###################################################

from __future__ import print_function, unicode_literals, division, absolute_import
from io import open
import logging, argparse
import soundfile as sf
from math import ceil
from svgwrite import Drawing
import pystache

SVG_TEMPLATE = '''<svg height="200" width="256">
    <polygon points="{{#points}}{{x}},{{y}}{{/points}}">
</svg>
'''


def make_svg(output_path, max_amplitudes, min_amplitudes, height=200, width=256):
    data = { "points": [] }
    for i, max_amp in enumerate(max_amplitudes):
        x = (1.0 - max_amp) * (height / 2)
        y = float(i)
        data["points"].append({"x":x, "y":y})
    return pystache.render(SVG_TEMPLATE, data)

def go(input_path, output_path, num_buckets=256):
    data, samplerate = sf.read('mouse1.wav', always_2d=True)
    data = data.max(axis=1)
    num_samples = data.shape[0]
    samples_per_bucket = int(ceil(num_samples / num_buckets))
    max_amplitudes = []
    min_amplitudes = []
    for i in range(0, num_samples, samples_per_bucket):
        max_amplitudes.append(data[i:i+256].max())
        min_amplitudes.append(data[i:i+256].min())


if __name__ == '__main__':
     parser = argparse.ArgumentParser(description='Convert a WAV file to a SVG file of its waveform')
     parser.add_argument('input', type=str, help='Input WAV file')
     parser.add_argument('output', type=str, help='Output SVG file')

     parser.add_argument('--nbuckets', type=int, default=256, help='Number of sample buckets (default: 256)')
     args = parser.parse_args()
     go(args.input, args.output, args.nbuckets)
