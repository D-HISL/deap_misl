from .my_emo import selNSGA2, selTournamentDCD
from .selNSGA3 import selNSGA3

from .twodim import cxTwoPoint2d, cx2d, mate2d, mutate2d

class AdaptiveParameterWrapper:
    def __init__(self, func, arg_name, arg_logic):
        self.func = func
        self.arg_name = arg_name
        self.arg_logic = arg_logic
        self.call_count = 0

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        kwargs[self.arg_name] = self.arg_logic(self.call_count)
        return self.func(*args, **kwargs)
