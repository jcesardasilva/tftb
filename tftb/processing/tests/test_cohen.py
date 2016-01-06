#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 jaidev <jaidev@newton>
#
# Distributed under terms of the MIT license.

"""
Tests for tftb.processing.cohen
"""

import unittest
import numpy as np
from scipy.signal import kaiser
from tftb.processing import cohen
from tftb.generators import fmsin, fmlin
from tftb.tests.base import TestBase
from nose import SkipTest


class TestCohen(TestBase):

    def test_spectrogram_reality(self):
        signal, _ = fmlin(128, 0.1, 0.4)
        window = kaiser(17, 3 * np.pi)
        tfr, _, _ = cohen.Spectrogram(signal, n_fbins=64, fwindow=window).run()
        self.assertTrue(np.all(np.isreal(tfr)))

    def test_spectrogram_linearity(self):
        signal, _ = fmlin(128, 0.1, 0.4)
        window = kaiser(17, 3 * np.pi)
        tfr1, _, _ = cohen.Spectrogram(signal, n_fbins=64,
                                       fwindow=window).run()
        tfr2, _, _ = cohen.Spectrogram(signal * 2, n_fbins=64,
                                       fwindow=window).run()
        x = np.sum(np.sum(tfr2))
        y = np.sum(np.sum(tfr1))
        self.assertEqual(x / y, 4)

    def test_wigner_ville_energy(self):
        """Test the energy property of the Wigner Ville representation."""
        signal, _ = fmsin(128)
        signal = signal / 128.0
        tfr, _, _ = cohen.WignerVilleDistribution(signal).run()
        x = np.sum(np.sum(tfr))
        y = np.sum(np.abs(signal) ** 2) * 128
        self.assertEqual(x, y)

    def test_wigner_ville_projection(self):
        """Test the projection property of the Wigner Ville representation."""
        signal, _ = fmsin(128)
        tfr, _, _ = cohen.WignerVilleDistribution(signal).run()
        x = np.abs(signal) ** 2
        y = np.sum(tfr, axis=0) / 128
        np.testing.assert_allclose(x, y)

    def test_reality(self):
        """Test the reality property of the Wigner Ville representation."""
        signal, _ = fmsin(128)
        tfr, _, _ = cohen.WignerVilleDistribution(signal).run()
        self.assertTrue(np.all(np.isreal(tfr)))

    def test_wigner_ville_regionprops(self):
        """Test the regional property of the Wigner Ville representation."""
        signal, _ = fmsin(128)
        signal[64:] = 0
        tfr, _, _ = cohen.WignerVilleDistribution(signal).run()
        self.assertTrue(np.all(tfr[:, 64:] == 0))

        signal, _ = fmsin(128)
        signal[:64] = 0
        tfr, _, _ = cohen.WignerVilleDistribution(signal).run()
        self.assertTrue(np.all(tfr[:, :64] == 0))

    def test_pseudo_wv_energy(self):
        """Test the energy property of the pseudo WV representation."""
        raise SkipTest("Known failure.")
        signal, _ = fmsin(128)
        signal = signal / 128.0
        tfr, _, _ = cohen.PseudoWignerVilleDistribution(signal).run()
        x = np.sum(np.sum(tfr))
        y = np.sum(np.abs(signal) ** 2) * 128
        self.assertAlmostEqual(x, y, places=3)

    def test_pseudo_wv_reality(self):
        """Test the reality property of the pseudo WV representation."""
        signal, _ = fmsin(128)
        tfr, _, _ = cohen.PseudoWignerVilleDistribution(signal).run()
        self.assertTrue(np.all(np.isreal(tfr)))

if __name__ == '__main__':
    unittest.main()
