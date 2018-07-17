#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Nicolargo <nicolas@nicolargo.com>
#

# Global name
__appname__ = 'pydecomcli'
__version__ = '1.0_b1'
__author__ = 'Nicolas Hennion <nicolas@nicolargo.com>'
__license__ = 'MIT'

import logging
import getopt
from pydecom import DecommutationNode
from anytree import RenderTree
import xml.etree.ElementTree as ET
import glob
import os

# Global variable for logger
logging.basicConfig(format='%(asctime)-15s %(message)s')
logger = logging.getLogger(__appname__)
logger.setLevel(logging.INFO)

# Others global variables
attrs_list_to_remove = ['mnemonic', 'parent']

def load_DecommutationPlan(xml_tree):
    ret = {}
    type_list = ['Table', 'Structure', 'Parameter']
    for i in xml_tree.getroot().iter():
        decom_type = None
        for t in type_list:
            if i.tag.endswith(t):
                decom_type = t

        if decom_type is not None:
            # Lower all keys
            i.attrib = {k.lower(): v for k, v in i.attrib.iteritems()}
            # Build the DecommutationPlan arguments dict
            all_attrs = {k: v for k, v in i.attrib.iteritems()}
            all_attrs['decom_type'] = decom_type
            if 'parent' in all_attrs:
                all_attrs['parent_name'] = all_attrs['parent']
            else:
                all_attrs['parent_name'] = None
            # Add the new TM Structure to the map_mnemo_node dict
            # The tree (parent argument) will be defined after all the files loading step
            all_attrs = {k: v for k, v in all_attrs.iteritems() if k not in attrs_list_to_remove}
            ret[i.attrib['mnemonic']] = DecommutationNode(i.attrib['mnemonic'],
                                                          parent=None,
                                                          **all_attrs)
    return ret


def build_DecommutationPlan(tree):
    for k, v in tree.iteritems():
        if v.data['parent_name'] in tree:
            v.parent = tree[v.data['parent_name']]
    return tree


def main():
    sdb_path = '/data/sdb/ONEO1S/'
    tm_file_list = glob.glob(os.path.join(sdb_path, 'tmfiles', '*.xml'))

    trees = [ET.parse(tree) for tree in tm_file_list]

    decom_tree = {}

    # Load files
    for tm_file in tm_file_list:
        tree = ET.parse(tm_file)
        if tree.getroot().tag.endswith('DecommutationPlan'):
            logger.info('Load DecommutationPlan from file {}'.format(tm_file))
            decom_tree.update(load_DecommutationPlan(tree))

    # Build decommutation tree
    decom_tree = build_DecommutationPlan(decom_tree)

    # Test
    # for k, v in decom_tree.iteritems():
    #     print(k, v.data, v.parent)
    print(decom_tree['AOCACINTMST00001G'])



if __name__ == '__main__':
    main()
