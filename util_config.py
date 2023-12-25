import json
import os

path = "config.json"


def init_conf() -> None:
    if os.path.exists(path) is False:  # 如果文件不存在
        content = '{"products":[]}'
        j = open(path, 'w', encoding='UTF-8')
        j.write(content)
        j.close()


def update_all(value):
    with open(path, 'w', encoding="UTF-8") as f:
        json.dump(value, f, ensure_ascii=False)
    f.close()


def update(key, value):
    content = get()
    content[key] = value
    with open(path, 'w', encoding="UTF-8") as f:
        json.dump(content, f, ensure_ascii=False)
    f.close()
    return True


def get(key=None):
    with open(path, encoding="UTF-8") as j:
        r = json.load(j)
    j.close()
    if key is None:
        return r
    else:
        return r[str(key)]


def append_list(key, value) -> bool:
    content = get()
    li = list(content[key])
    li.append(value)  # 追加
    content[key] = li
    with open(path, 'w', encoding="UTF-8") as f:
        json.dump(content, f, ensure_ascii=False)
    f.close()
    return True


def delete_list(key, index: int) -> bool:
    content = get()
    li = list(content[key])
    del li[index]  # 移除
    content[key] = li
    with open(path, 'w', encoding="UTF-8") as f:
        json.dump(content, f, ensure_ascii=False)
    f.close()
    return True


def update_list(key, index: int, value) -> bool:
    content = get()
    li = list(content[key])
    li[index] = value  # 修改
    content[key] = li
    with open(path, 'w', encoding="UTF-8") as f:
        json.dump(content, f, ensure_ascii=False)
    f.close()
    return True


def delete(key: str) -> bool:
    content = get()
    for item in content:
        del item[key]
    with open(path, 'w', encoding="UTF-8") as f:
        json.dump(content, f, ensure_ascii=False)
    f.close()
    return True


def add(key: str, value: any) -> bool:
    content = get()
    content[key] = value
    with open(path, 'w', encoding="UTF-8") as f:
        json.dump(content, f, ensure_ascii=False)
    f.close()
    return True
