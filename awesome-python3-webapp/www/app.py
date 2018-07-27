#!/usr/bin/python3
#!-*-coding:utf-8_*_


import logging ; logging.basicConfig(level=logging.INFO)

import asyncio , os , json , time
from datetime import datetime

from aiohttp import web

def index(request):
	return web.Response(body = '<h1>Awesome</h1>'.encode('utf-8') , content_type = 'text/html')
	#return web.Response(body = b'<h1>Awesome</h1>')

#@asyncio.coroutine 此装饰器不会预激协程 兼容yield from
async def init(loop):
	app = web.Application(loop = loop)
	app.router.add_route('GET' , '/' ,index)
	#srv = yield from loop.create_server(app.make_handler() , '127.0.0.1' , 10086)
	srv = await loop.create_server(app.make_handler() , '127.0.0.1' , 10086)
	logging.info('server started at http://127.0.0.1:10086...')
	return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()	
