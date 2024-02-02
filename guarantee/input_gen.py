import random
import string

random.seed(0)


STR_LEN_MAX: int = 64
LINE_COUNT: int = 50_000_000
ATTR_COUNT: int = 10
ATTR_KINDS: int = 100
MATCHING_RATE: float = 0.6

# NOTE: サポート文字列(https://en.cppreference.com/w/cpp/string/byte/isgraph)
CHARACTERS = string.digits + string.ascii_letters + string.punctuation


# 英数字64文字
def generate_random_str(len: int = STR_LEN_MAX, comma_num: int = 0) -> str:
    comma_indexs = random.sample(range(len), comma_num)
    result = random.choices(CHARACTERS.replace(",",""), k=len)
    for i in comma_indexs:
        result[i] = ","
    return "".join(result)


# 英数字64文字の文字列をcount個生成
def generate_random_ids_list(count: int) -> list[str]:
    return ["key_" + generate_random_str(len=max(1, STR_LEN_MAX-4)) for _ in range(count)]


# 英数字64文字の文字列をcount個生成
def generate_random_attrs_list(count: int) -> list[str]:
    return [generate_random_str(comma_num=ATTR_COUNT) for _ in range(count)]


def write(id_sets: list[str], attrs: list[str], filename: str):
    id_list = random.sample(id_sets, k=LINE_COUNT)
    attr_list = random.choices(attrs, k=LINE_COUNT)
    with open(filename, "w") as f:
        for id, attr in zip(id_list, attr_list):
            f.write(id + "," + attr + "\n")


if __name__ == "__main__":
    id_sets = generate_random_ids_list(int(LINE_COUNT / MATCHING_RATE))

    attrs_a = generate_random_attrs_list(ATTR_KINDS)
    write(id_sets, attrs_a, "input_a.csv")

    attrs_b = generate_random_attrs_list(ATTR_KINDS)
    write(id_sets, attrs_b, "input_b.csv")
