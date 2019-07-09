import math
def get_posttime_data(td):
    if td < 60:
        return 'just now'
    elif td < 3600:
        return str(math.trunc(td / 60)) + 'm'
    elif td < 86400:
        return str(math.trunc(td / 3600)) + 'h'
    else:
        return str(math.trunc(td / 86400)) + 'd'