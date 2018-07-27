#!/usr/bin/python3
#!_*_coding:utf-8_*_

import asynico , logging

import aiomysql

def log(sql , args=()):
	logigin.info('SQL:%s' % sql)

async def create_pool(loop , **kw):
	logging_info('create database connection pool...')
	global __pool
	__pool = await aiomysql.create_pool(
		host = kw.get('host' , 'localhost'),
		port = kw.get('port' , '3306'),
		user = kw['user'],
		password = kw['password'],
		db = kw['db'],
		charcommit = kw,get('autocommit' , True),
		maxsize = kw.get('maxsize' , 10),
		minsize = kw.get('minsize' , 1),
		loop = loop
		)

