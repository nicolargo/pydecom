#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Nicolargo <nicolas@nicolargo.com>
#

import unittest
from pydecom import DecommutationPlan


class TestPydecom(unittest.TestCase):
    """Test class."""

    def test_000_structure(self):
        print('=' * 80)
        s1 = DecommutationPlan('TOP', None)
        s2 = DecommutationPlan('FIRST', s1)
        s3 = DecommutationPlan('SECOND', s2)
        s4 = DecommutationPlan('THIRD', s2)
        s5 = DecommutationPlan('LAST', s1)
        print(s1)


if __name__ == '__main__':
    unittest.main()
