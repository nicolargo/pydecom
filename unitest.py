#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Nicolargo <nicolas@nicolargo.com>
#

import unittest
import pydecom


class TestPydecom(unittest.TestCase):
    """Test class."""

    def test_000_structure(self):
        print('=' * 80)
        s1 = pydecom.DecommutationNode('TOP', None)
        s2 = pydecom.DecommutationNode('FIRST', s1)
        s3 = pydecom.DecommutationNode('SECOND', s2)
        s4 = pydecom.DecommutationNode('THIRD', s2)
        s5 = pydecom.DecommutationNode('LAST', s1)
        print(s1)


if __name__ == '__main__':
    unittest.main()
