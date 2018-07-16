# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Nicolargo <nicolas@nicolargo.com>
#

from pprint import pformat
from anytree import NodeMixin, RenderTree


class BaseTmStructure(object):
    """A TM structure"""
    def __init__(self, position, length):
        self.position = position
        self.length = length


class TmStructure(BaseTmStructure, NodeMixin):

    def __init__(self, name, parent=None,
                 position=None,
                 length=None):
        super(TmStructure, self).__init__(position=position,
                                          length=length)
        self.name = name
        self.parent = parent

    def __str__(self):
        ret = u''.encode('utf-8')
        # Note: it is also possible to force ascii with style=AsciiStyle()
        for pre, _, node in RenderTree(self):
            ret += u'{}{}\n'.format(pre, node.name).encode('utf-8')
        return ret
