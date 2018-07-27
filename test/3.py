#/usr/bin/env python3
# -*- coding:utf-8 -*-

def __func1_private(name):
	return "hello %s " % name

def __func2_private(name):
	return "Hi %s" % name


def greeting(name):
	if len(name) > 3:
		return __func1_private()
	else:
		return __func2_private()