_CACHE = []

def cache(f):
    def inner(*args, **kwargs):
        key = (f, args, kwargs)
        for (cache_key, val) in _CACHE:
            if key == cache_key:
                return val
        ret = f(*args, **kwargs)
        _CACHE.append((key, ret))
        return ret
    return inner
