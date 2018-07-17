# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Nicolargo <nicolas@nicolargo.com>
#

from pprint import pformat
from anytree import NodeMixin, RenderTree


class BaseDecommutationPlan(object):

    def __init__(self, **args):
        self.data = args


class DecommutationPlan(BaseDecommutationPlan, NodeMixin):

    def __init__(self, mnemonic, parent, **args):
        super(DecommutationPlan, self).__init__(**args)
        self.mnemonic = mnemonic
        self.parent = parent

    def __str__(self):
        ret = u''.encode('utf-8')
        # Note: it is also possible to force ascii with style=AsciiStyle()
        for pre, _, node in RenderTree(self):
            # ret += u'{}{} {}\n'.format(pre, node.mnemonic, node.data).encode('utf-8')
            ret += u'{}{}\n'.format(pre, node.mnemonic).encode('utf-8')
        return ret
