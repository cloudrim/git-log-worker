import os
import shutil


def remove_tmp():
    if os.path.isdir("tmp"):
        shutil.rmtree('tmp')