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
import sys

# Global variable for logger
logging.basicConfig(format='%(asctime)-15s %(message)s')
logger = logging.getLogger(__appname__)
logger.setLevel(logging.INFO)

# Others global variables
attrs_list_to_remove = ['mnemonic', 'parent']

def _load(xml_tree, type_list):
    ret = {}
    for i in xml_tree.getroot().iter():
        decom_type = None
        for t in type_list:
            if i.tag.split('}')[1] == t:
                decom_type = t

        # print("="*80)
        # print(i.tag)
        # print(i.attrib)
        # print(decom_type)

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
            # Note: The tree (parent argument) will be defined after all the files loading step
            all_attrs = {k: v for k, v in all_attrs.iteritems() if k not in attrs_list_to_remove}
            key = i.attrib['mnemonic']
            # TODO: add subtree management (get LongDescription, Alias...)
            ret[key] = DecommutationNode(i.attrib['mnemonic'],
                                         parent=None,
                                         **all_attrs)
    return ret

def load_DecommutationPlan(xml_tree):
    return _load(xml_tree, ['Table', 'Structure', 'Parameter'])

def load_TelemetryParameters(xml_tree):
    return _load(xml_tree, ['NumericParameter', 'StatusParameter', 'MotherParameter', 'HexaParameter'])

def build_DecommutationPlan(tree):
    for _, v in tree.iteritems():
        if v.data['parent_name'] in tree:
            v.parent = tree[v.data['parent_name']]
    return tree

def main():
    decom_tree = {}
    trees = []

    # Load SDB
    sdb_path = '/data/sdb/ONEO1S/'
    tm_file_list = glob.glob(os.path.join(sdb_path, 'tmfiles', '*.xml'))
    xml_item_list = ['DecommutationPlan', 'TelemetryParameters']
    #xml_item_list = ['DecommutationPlan']
    for tm_file in tm_file_list:
        logger.debug('Load SDB file {}'.format(tm_file))
        tree = ET.parse(tm_file)
        for xml_item in xml_item_list:
            if tree.getroot().tag.endswith(xml_item):
                logger.info('Load {} from file {}'.format(xml_item, tm_file))
                decom_tree.update(getattr(sys.modules[__name__], 'load_' + xml_item)(tree))

    # Build decommutation tree
    logger.info('Build decommutation tree')
    decom_tree = build_DecommutationPlan(decom_tree)

    # Tests

    # Top level structure
    #print(decom_tree['AOCACINTMST00001G'])

    # On simple TM
    #  <NumericParameter Mnemonic="AOCACSWE005BQG" Nature="G" ShortDescription="GYR_1_AJFM_TMP_R0" ParamId="2132673023" ReadOnly="true">
    #    <LongDescription>GYR1 R0 coefficient for sensor temperature computation from voltage measurement   C  </LongDescription>
    #    <AliasSet>
    #      <Alias Alias="AO_AJ_FM_GYR1_TEMP_R0_COEF" NameSpace="OBSW"/>
    #      <Alias Alias="GYR_1_AJFM_TMP_R0" NameSpace="NEOSAT"/>
    #    </AliasSet>
    #    <Length>64</Length>
    #    <BinaryConversion>IF</BinaryConversion>
    #  </NumericParameter>
    print(decom_tree['AOCACSWE005BQG'])


if __name__ == '__main__':
    main()
