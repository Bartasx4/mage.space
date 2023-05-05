import asyncio
import random

from asyncio.futures import Future


class Async:

    def __init__(self):
        self.run = True
        self.tasks = []
        self.results = []

    async def show(self, i, lst):
        print(f'Start ({i})')
        await asyncio.sleep(random.randint(1, 4))
        print('To jest: ', i)
        print('')
        lst.append(i.upper())
        return i.upper()

    async def start(self):
        print('start')
        self.results = []
        running_tasks = []
        for task in self.tasks:
            new_task = task
            print('adding ', new_task)
            running_tasks.append(asyncio.create_task(self.show(new_task, self.results)))
        return asyncio.gather(*running_tasks)


if __name__ == '__main__':
    ...
    # asyncio.run(__main__(['test', 'dupa', 'bla bla bla', 'koniec']))
