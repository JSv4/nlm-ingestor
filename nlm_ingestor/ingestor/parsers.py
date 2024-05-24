import re


def find_tokens_in_block(tokens, block):
    """
    Given a block - named tuple of form x0, y0, x1, y1 - and a list of tokens of form
    PawlsTokenPythonType, get a list of token ids of tokens that are entirely contained
    within the provided box (if any).
    """
    x0, y0, x1, y1 = block
    contained_tokens = []
    fuzz_factor = .05

    for tok_index, token in enumerate(tokens):

        print(f"Is token x {token['x']} >= x1 {x0 * (1 - fuzz_factor)}")
        print(f"Is token y {token['y']} >= y1 {y0 * (1 - fuzz_factor)}")
        print("Is token x2 " + str(token["x"] + token["width"]) + f" <= {x1 * (1 + fuzz_factor)}")
        print(f"Is token y2 " + str(token["y"] + token["height"]) + f" <= {y1 * (1 + fuzz_factor)}")

        in_block = (token["x"] >= x0 * (1-fuzz_factor) and
                token["y"] >= y0 * (1-fuzz_factor) and
                (token["x"] + token["width"]) <= x1 * (1 + fuzz_factor) and
                (token["y"] + token["height"]) <= y1 * (1+fuzz_factor))

        print(f"Token: {token['text']} {token} in block {block}: {in_block}")

        if in_block:
            contained_tokens.append(tok_index)

    return contained_tokens


def get_word_positions(word_pos_str: str) -> list[tuple[float, float]]:
    print(f"word_pos_str: {word_pos_str}")
    pattern = r'\(([-+]?\d*\.\d+),\s*([-+]?\d*\.\d+)\)'
    tuples = re.findall(pattern, word_pos_str)
    print( [(float(x), float(y)) for x, y in tuples])
    return [(float(x), float(y)) for x, y in tuples]


def get_kv_from_attr(attr_str, sep=" "):

    if not isinstance(attr_str, str):
        return {}

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
