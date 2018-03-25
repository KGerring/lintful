# -*- coding: utf-8 -*-

"""Unit test package for lintplus."""
import sys
import os
to_insert = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, to_insert)
print('sys.path inserted {!r} by {!r}'.format(to_insert, __file__), file=sys.stderr)
del to_insert


import lintful

if __name__ == '__main__':
	print(__file__)