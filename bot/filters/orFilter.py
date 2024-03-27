from aiogram.filters import Filter


class Or(Filter):
    def __init__(self, *filters):
        self.filters = filters

    async def __call__(self, *args):
        for f in self.filters:
            if await f(*args):
                return True
        return False
