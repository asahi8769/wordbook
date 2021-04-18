import os, time
from subprocess import Popen, PIPE
from os.path import basename
from zipfile import ZipFile
from functools import reduce
import threading
import pickle
from datetime import datetime


def make_dir(dirname):
    try:
        os.mkdir(dirname)
        print("Directory ", dirname, " Created ")
        return dirname
    except FileExistsError:
        pass


def path_find(name, *paths):
    for path in paths:
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)


def subprocess_cmd(command):
    print(command)
    try :
        process = Popen(command, stdout=PIPE, shell=True, universal_newlines=True)
        proc_stdout = process.communicate()[0].strip()
    except Exception as e:
        process = Popen(command, stdout=PIPE, shell=True, universal_newlines=False)
        proc_stdout = process.communicate()[0].strip()
    print(proc_stdout)


def packaging(filename, *bindings):
    zipname = r'dist\Objections.zip'
    with ZipFile(zipname, 'w') as zipObj:
        if os.path.exists(os.path.join('dist',filename)):
            zipObj.write(os.path.join('dist', filename), basename(filename))
        for binding in bindings:
            for folderName, subfolders, filenames in os.walk(binding):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    print(os.path.join(binding, basename(filePath)))
                    zipObj.write(filePath, os.path.join(basename(folderName), basename(filePath)))
        print(f'패키징을 완료하였습니다. {zipname}')


def install(lib):
    return f'pip --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org install {lib}'


def force_reinstall(lib):
    return f'pip --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org install ' \
           f'"{lib}" --force-reinstall'


def venv_dir(foldername='venv'):
    return os.path.join(os.getcwd(), foldername)


def threading_timer(function, sec, Daemon=True):
    t = threading.Timer(sec, function)
    t.setDaemon(Daemon)
    t.start()
    return t


def show_elapsed_time(function):
    def wrapper(*args, **kwargs):
        start = time.time()
        returns = function(*args, **kwargs)
        print(function.__name__, 'Elapsed {0:02d}:{1:02d}'.format(*divmod(int(time.time() - start), 60)))
        return returns
    return wrapper


def try_until_success(function):
    def wrapper(*args, **kwargs):
        while True:
            try:
                returns = function(*args, **kwargs)
            except Exception as e:
                # print(e)
                # print(f"{function.__name__} failed. Trying Again...")
                pass
            else :
                return returns
    return wrapper


def flatten(ls):
    """
    ls : list
    flattens multi-dimensional list
    """
    return list(set([i for i in reduce(lambda x, y: x + y, ls)]))


def remove_duplication(ls):
    """
    ls : list
    remove duplicated items while maintaining order
    """
    seen = set()
    seen_add = seen.add
    return [i for i in ls if not (i in seen or seen_add(i))]


def get_norm_slope(ls:list):

    import numpy as np
    mean = np.mean(ls)
    std = np.std(ls)
    if std == 0 :
        std += 0.00001
    normalized = [i for i in [(i - mean) / std for i in ls][0]]
    return np.polyfit([i for i in range(len(normalized))], normalized, 1)[0]


class PickledItems:

    def __init__(self, name):

        self.name = name
        self.item_dict = dict()
        self.path = f"data/{self.name}.pickle"

    def read(self, key=datetime.today().strftime('%y%m%d')):
        if not os.path.exists(self.path):
            self.save()
        with open(self.path, "rb") as p:
            self.item_dict = pickle.load(p)
        if not type(self.item_dict.get(key, None)) == list:
            self.item_dict[key] = list()
        return self.item_dict[key]

    def add(self, *val, key=datetime.today().strftime('%y%m%d')):
        if not type(self.item_dict.get(key, None)) == list:
            self.item_dict[key] = list()
        for i in val:
            if i not in self.item_dict[key]:
                self.item_dict[key].append(i)
        self.save()

    def reset(self, key=datetime.today().strftime('%y%m%d')):
        self.item_dict[key] = list()
        self.save()

    def save(self):
        with open(self.path, "wb+") as p:
            pickle.dump(self.item_dict, p)