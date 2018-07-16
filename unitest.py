#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Nicolargo <nicolas@nicolargo.com>
#

import unittest
from pydecom import TmStructure
from anytree import RenderTree


class TestPydecom(unittest.TestCase):
    """Test class."""

    def test_001_ok(self):
        print('=' * 80)
        s1 = TmStructure('TOP', None)
        s2 = TmStructure('FIRST', s1)
        s3 = TmStructure('SECOND', s2)
        s4 = TmStructure('THIRD', s2)
        s5 = TmStructure('LAST', s1)
        print(s1)


if __name__ == '__main__':
    unittest.main()
