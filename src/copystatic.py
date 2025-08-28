import os
import shutil


def copystatic(src, dst):
    abs_src = os.path.abspath(src)
    abs_dst = os.path.abspath(dst)

    if not os.path.exists(abs_dst):
        os.makedirs(abs_dst)

    for item in os.listdir(abs_dst):
        item_path = os.path.join(abs_dst, item)
        if os.path.isfile(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    shutil.copytree(abs_src, abs_dst, dirs_exist_ok=True)
