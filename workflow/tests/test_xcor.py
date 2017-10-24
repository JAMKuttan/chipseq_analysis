#!/usr/bin/env python3

import pytest
import os
import pandas as pd

test_output_path = os.path.dirname(os.path.abspath(__file__)) + \
                '/../output/crossReads/'


def test_convert_reads_singleend():
    assert os.path.exists(os.path.join(test_output_path, 'ENCFF833BLU.filt.nodup.tagAlign.15.tagAlign.gz.cc.plot.pdf'))
    df_xcor = pd.read_csv("ENCFF833BLU.filt.nodup.tagAlign.15.tagAlign.gz.cc.qc", sep="\t", header=None)
    assert df_xcor[2].iloc[0] = '195,215,230'
    assert df_xcor[8].iloc[0] = 1.024836
    assert df_xcor[9].iloc[0] = 1.266678


def test_map_qc_pairedend():
    # Do the same thing for paired end data
    pass
