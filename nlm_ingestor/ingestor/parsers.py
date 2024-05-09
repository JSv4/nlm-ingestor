import re


def get_word_positions(word_pos_str: str) -> list[tuple[float, float]]:
    pattern = r'\(([-+]?\d*\.\d+),\s*([-+]?\d*\.\d+)\)'
    tuples = re.findall(pattern, word_pos_str)
    return [(float(x), float(y)) for x, y in tuples]


def get_kv_from_attr(attr_str, sep=" "):
    kv_string = attr_str.split(";")
    kvs = {}
    for kv in kv_string:
        parts = kv.strip().split(sep)
        k = parts[0]
        v = parts[1:]
        if len(v) == 1:
            v = v[0].strip()
        kvs[k] = v
    return kvs
