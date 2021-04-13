#!/usr/bin/env python
# encoding: utf-8
""" 
日志中间件
"""
from loguru import logger
from lycium.microsvc.context import Context

async def LogMiddleware(context:Context):
    """ """
    logger.info(context.request)
    result = await context.next()
    logger.info(result)
    return result