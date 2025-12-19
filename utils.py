from __future__ import annotations

import asyncio
from typing import AsyncIterator, TypeVar

T = TypeVar("T")

async def merge_async_iters(*iterables: AsyncIterator[T]) -> AsyncIterator[T]:
    queue = asyncio.Queue()
    sentinel = object()

    async def drain(iterator: AsyncIterator[T]) -> None:
        try:
            async for item in iterator:
                await queue.put(item)
        finally:
            await queue.put(sentinel)

    tasks = [asyncio.create_task(drain(it)) for it in iterables]
    finished = 0

    try:
        while finished < len(tasks):
            item = await queue.get()
            if item is sentinel:
                finished += 1
                continue
            yield item
    finally:
        for task in tasks:
            task.cancel()
