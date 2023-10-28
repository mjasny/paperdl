import subprocess
import platform


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def open_pdf(file_path):
    try:
        if platform.system() == 'Darwin':  # macOS
            subprocess.Popen(('open', file_path))
        elif platform.system() == 'Windows':  # Windows
            subprocess.Popen(('start', file_path), shell=True)
        else:  # linux variants
            subprocess.Popen(('xdg-open', file_path))
    except Exception as e:
        print(f"Failed to open file with error: {e}")