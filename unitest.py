#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Nicolargo <nicolas@nicolargo.com>
#

import unittest
from pydecom import DecommutationPlan
from anytree import RenderTree
import xml.etree.ElementTree as ET


class TestPydecom(unittest.TestCase):
    """Test class."""

    # def test_001_structure(self):
    #     print('=' * 80)
    #     s1 = DecommutationPlan('TOP', None)
    #     s2 = DecommutationPlan('FIRST', s1)
    #     s3 = DecommutationPlan('SECOND', s2)
    #     s4 = DecommutationPlan('THIRD', s2)
    #     s5 = DecommutationPlan('LAST', s1)
    #     print(s1)

    def test_002_loadxml(self):
        print('=' * 80)

        map_mnemonic_node = {}
        type_list = ['Table', 'Structure', 'Parameter']
        attrs_list_to_remove = ['mnemonic', 'parent']

        trees = [ET.parse(tree) for tree in ['/data/sdb/ONEO1S/tmfiles/algo_decom.xml',
                                             '/data/sdb/ONEO1S/tmfiles/decomm_top.xml',
                                             '/data/sdb/ONEO1S/tmfiles/pkt_decom.xml']]
        # Build one instance per structure
        for t in trees:
            for i in t.getroot().iter():
                decom_type = None
                for t in type_list:
                    if i.tag.endswith(t):
                        decom_type = t

                if decom_type is not None:
                    # Lower all keys
                    i.attrib = {k.lower(): v for k, v in i.attrib.iteritems()}
                    # Build the DecommutationPlan arguments dict
                    all_attrs = {k: v for k, v in i.attrib.iteritems() if k not in attrs_list_to_remove}
                    all_attrs['decom_type'] = decom_type
                    # Add the new TM Structure to the map_mnemo_node dict
                    map_mnemonic_node[i.attrib['mnemonic']] = DecommutationPlan(i.attrib['mnemonic'],
                                                                                parent=None,
                                                                                **all_attrs)
        # Build tree
        for t in trees:
            for i in t.getroot().iter():
                decom_type = None
                for t in type_list:
                    if i.tag.endswith(t):
                        decom_type = t

                if decom_type is not None:
                    # Lower all keys
                    i.attrib = {k.lower(): v for k, v in i.attrib.iteritems()}
                    if i.attrib['parent'] in map_mnemonic_node:
                        map_mnemonic_node[i.attrib['mnemonic']].parent = map_mnemonic_node[i.attrib['parent']]
                    else:
                        # ERROR: structure i.attrib['parent'] not defined
                        pass
        # Test
        # print(map_mnemonic_node['AOCACINTMST00001G'])
        print(map_mnemonic_node['APID_0x1_S_129'])



if __name__ == '__main__':
    unittest.main()
