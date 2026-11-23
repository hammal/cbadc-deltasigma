# -*- coding: utf-8 -*-
# test_scaleABCD.py
# This module provides the tests for the scaleABCD function.
# Copyright 2014 Giuseppe Venturini
# This file is part of python-deltasigma.
#
# python-deltasigma is a 1:1 Python replacement of Richard Schreier's
# MATLAB delta sigma toolbox (aka "delsigma"), upon which it is heavily based.
# The delta sigma toolbox is (c) 2009, Richard Schreier.
#
# python-deltasigma is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LICENSE file for the licensing terms.

"""This module provides the test class for the scaleABCD() function.
"""

from __future__ import division, print_function

import unittest
import numpy as np
import cbadc_deltasigma as ds


class TestScaleABCD(unittest.TestCase):
    """Test class for scaleABCD()"""

    def setUp(self):
        order = 8
        osr = 32
        self.nlev = 2
        self.f0 = 0.125
        Hinf = 1.5
        form = "CRFB"
        # Optimized zero placement
        ntf = ds.synthesizeNTF(order, osr, 2, Hinf, self.f0)
        a, g, b, c = ds.realizeNTF(ntf, form)
        # A single input feed-in; feedback still reaches every state.
        self.ABCD0 = ds.stuffABCD(a, g, b[0], c, form)

    def test_scaleABCD(self):
        """Scaling must preserve the eighth-order loop's dynamics and decisions."""
        ABCD, umax, S = ds.scaleABCD(self.ABCD0, self.nlev, self.f0)
        # Noisy state maxima and stability estimates vary across platforms.
        # The coordinate change must still satisfy As*S=S*A, Bs=S*B, Cs*S=C.
        self.assertTrue(0 < umax <= self.nlev - 1, f"Estimated umax={umax:.17g}")
        self.assertTrue(np.all(np.isfinite(S)))
        self.assertTrue(np.all(np.diag(S) > 0))
        np.testing.assert_array_equal(S, np.diag(np.diag(S)))
        A, B, C, D = ds.partitionABCD(self.ABCD0)
        As, Bs, Cs, Ds = ds.partitionABCD(ABCD)
        np.testing.assert_allclose(As @ S, S @ A, atol=1e-12)
        np.testing.assert_allclose(Bs, S @ B, atol=1e-12)
        np.testing.assert_allclose(Cs @ S, C, atol=1e-12)
        np.testing.assert_array_equal(Ds, D)

        # Scaling changes state coordinates, not the modulator's readout.
        u = 0.2 * np.sin(2 * np.pi * self.f0 * np.arange(128))
        v0, x0, _, y0 = ds.simulateDSM(u, self.ABCD0, self.nlev)
        v1, x1, _, y1 = ds.simulateDSM(u, ABCD, self.nlev)
        np.testing.assert_array_equal(v1, v0)
        np.testing.assert_allclose(x1, S @ x0, atol=1e-10)
        np.testing.assert_allclose(y1, y0, atol=1e-10)

    def test_scaleABCD_first_order_stability(self):
        """A first-order binary loop accepts full scale: x[n+1]=x[n]+u[n]-v[n]."""
        ABCD = np.array([[1., 1., -1.], [1., 1., 0.]])
        _, umax, _ = ds.scaleABCD(ABCD, N_sim=4096)
        self.assertEqual(umax, 1.0)

    def test_scaleABCD_first_order_state_limit(self):
        """A first-order loop with |x|<=1 needs S=2 for the requested xlim=2."""
        ABCD = np.array([[1., 1., -1.], [1., 1., 0.]])
        scaled, umax, S = ds.scaleABCD(ABCD, umax=0.5, xlim=2., N_sim=4096)
        # Finite noisy records approach, rather than exactly attain, |x|=1.
        np.testing.assert_allclose(S, [[2.]], rtol=0.01)
        np.testing.assert_allclose(scaled, [[1., 2., -2.], [0.5, 1., 0.]], rtol=0.01)
        self.assertEqual(umax, 0.5)

    def test_scaleABCD_Q(self):
        """Test function for scaleABCD() with Imag ABCD"""
        ABCD_IN = np.array(
            [
                [
                    0.888 + 0.4598j,
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                    0.0516 + 0.0j,
                    0.0516 + 0.0j,
                ],
                [
                    0.6073 + 0.7945j,
                    0.9530 + 0.3028j,
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                    0.3230 + 0.0j,
                ],
                [
                    0.0 + 0.0j,
                    0.9459 + 0.3245j,
                    0.9239 + 0.3827j,
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                    0.9162 + 0.0j,
                ],
                [
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                    0.9239 - 0.3827j,
                    0.0 + 0.0j,
                    0.1778 + 0.0j,
                ],
                [
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                    -0.9935 - 0.1138j,
                    -0.7405 - 0.672j,
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                ],
            ]
        )

        ABCD, umax, S = ds.scaleABCD(ABCD_IN, nlev=9, f=1.0 / 16)

        # references here because I prefer to have 1 file
        umax_ref = 8
        S_ref = np.array(
            [
                [0.3586, 0.0, 0.0, 0.0],
                [0.0, 0.1207, 0.0, 0.0],
                [0.0, 0.0, 0.0805, 0.0],
                [0.0, 0.0, 0.0, 0.3671],
            ]
        )
        ABCD_ref = np.array(
            [
                [
                    0.888037198535288 + 0.459771610712905j,
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                    0.0185052748572140 + 0.0j,
                    0.0185052748572140 + 4.35415940995948e-18j,
                ],
                [
                    0.204472470161495 + 0.267520232240738j,
                    0.953044748762363 + 0.302829501298050j,
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                    0.0389934281708177 + 0.0j,
                ],
                [
                    0.0 + 0.0j,
                    0.630626110921381 + 0.216330153871036j,
                    0.923879532511340 + 0.382683432365112j,
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                    0.0737451799430360 - 1.22879569706001e-17j,
                ],
                [
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                    0.923879532511287 - 0.382683432365090j,
                    0.0 + 0.0j,
                    0.0652579452814600 + 1.01879713420556e-17j,
                ],
                [
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                    -12.3424213726332 - 1.41434395098423j,
                    -2.01750453626270 - 1.83077728688503j,
                    0.0 + 0.0j,
                    0.0 + 0.0j,
                ],
            ]
        )
        assert np.allclose(ABCD, ABCD_ref, atol=1e-2, rtol=1e-1)
        assert np.allclose(S, S_ref, atol=1e-3, rtol=1e-2)
        assert umax == umax_ref
