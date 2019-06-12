# -*- coding: utf-8 -*-
import asyncio
import contextlib
import time


@contextlib.contextmanager
def patch_select(*, loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    old_select = loop._selector.select

    # Define the new select method, used as a context
    def new_select(timeout):
        if timeout == 0:
            return old_select(timeout)
        start = time.time()
        result = old_select(timeout)
        total = time.time() - start
        new_select.iotime += total
        return result

    new_select.iotime = 0.0
    # Patch the select method
    try:
        loop._selector.select = new_select
        yield new_select
    finally:
        loop._selector.select = old_select


@contextlib.contextmanager
def timeit(name, loop=None):
    start = time.time()
    with patch_select() as context:
        yield
    total = time.time() - start
    io_time = context.iotime
    print("[{:12s}]\tIO time: {:.6f}\tCPU time: {:.6f}\tTotal time: {:.6f}\t".format(name, io_time, total - io_time,
                                                                                     total))

#
# loop = asyncio.get_event_loop()
# with timeit(loop=loop):
#     coro = asyncio.sleep(1, result=3)
#     result = loop.run_until_complete(coro)
#     print("Result: {}".format(result))
