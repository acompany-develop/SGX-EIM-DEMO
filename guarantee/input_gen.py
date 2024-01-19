import random
import string

random.seed(0)


STR_LEN_MAX: int = 64
LINE_COUNT: int = 50_000_000
ATTR_KINDS: int = 100
MATCHING_RATE: float = 0.6

CHARACTERS = string.ascii_letters + string.digits + "|"


# 英数字64文字
def generate_random_hash() -> str:
    return "".join(random.choices(CHARACTERS, k=STR_LEN_MAX))


# 英数字64文字以下
def generate_random_attr() -> str:
    return "".join(random.choices(CHARACTERS, k=STR_LEN_MAX))


# 英数字64文字の文字列をcount個生成
def generate_random_hashs(count: int) -> list[str]:
    return [generate_random_hash() for _ in range(count)]


# 英数字64文字以下の文字列をcount個生成
def generate_random_attrs(count: int) -> list[str]:
    return [generate_random_attr() for _ in range(count)]


def write(key_sets: list[str], attrs: list[str], filename: str):
    key_list = random.sample(key_sets, k=LINE_COUNT)
    attr_list = random.choices(attrs, k=LINE_COUNT)
    with open(filename, "w") as f:
        for key, attr in zip(key_list, attr_list):
            f.write(key + "," + attr + "\n")


if __name__ == "__main__":
    key_sets = generate_random_hashs(int(LINE_COUNT / MATCHING_RATE))

    attrs_a = generate_random_attrs(ATTR_KINDS)
    write(key_sets, attrs_a, "input_a_10m.csv")

    attrs_b = generate_random_attrs(ATTR_KINDS)
    write(key_sets, attrs_b, "input_b_10m.csv")
