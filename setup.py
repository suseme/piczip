from distutils.core import setup
import py2exe

wx = dict(
    script = 'PicCompressWnd.pyw',
    icon_resources = [(1, "icon.ico")],
)

cx = dict(
    script = 'PicCompressWnd.pyw',
    icon_resources = [(0, "icon.ico")],
)

setup(
    name = "PicCompress.",
    description = "Compress Picture Size.",
    version = "1.1.0.0",
    # console=[cx],
    # windows=[wx],
    windows = [{"script":"PicCompressWnd.py", "icon_resources": [(0, "icon.ico")]} ]
)