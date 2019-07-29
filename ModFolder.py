import pathlib
import hashlib
from tools import Tree


class File:
    def __init__(self, path, parent, name=None, loaded: bool=False):
        self.path = pathlib.Path(path)
        self.loaded = loaded
        self.parent = parent
        if name is None:
            self.name = self.path.name
        else:
            self.name = name

    def __str__(self):
        return self.name

    def md5(self):
        hash_md5 = hashlib.md5()
        with open(self.path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()


class Folder(File, Tree.TreeNode):
    def __init__(self, path, name=None, parent=None, loaded: bool=False):
        File.__init__(self, path=path, parent=parent, name=name, loaded=loaded)
        Tree.TreeNode.__init__(self, parent=parent)

        self.checkbox = None
        self.sizer = None

        for temp_path in self.path.iterdir():
            if temp_path.is_file():
                self.children.append(File(temp_path, parent=self))
            if temp_path.is_dir():
                self.children.append(Folder(temp_path, parent=self))
        self.children.sort(key=lambda x: str(x))

    def md5_set(self):
        mset = set()
        for file in self.children:
            if not isinstance(file, Folder):
                mset.add(file.md5())
        return mset





