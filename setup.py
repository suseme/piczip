from distutils.core import setup
import py2exe

wx = dict(
    script = 'Piczip.pyw',
    icon_resources = [(1, "icon.ico")],
)

cx = dict(
    script = 'Piczip.pyw',
    icon_resources = [(0, "icon.ico")],
)

py2exe_options = {
        "includes": ["sip"],
        "dll_excludes": ["MSVCP90.dll", 'MSVCR90.dll'],
        "compressed": 1,
        "optimize": 2,
        "ascii": 0,
        }

setup(
    name = "Piczip",
    description = "Compress Picture Size.",
    version = "1.1.0.0",
    # console=[cx],
    # windows=[wx],
    windows = [{"script":"PiczipWnd_qt.py", "icon_resources": [(0, "icon.ico")]} ],
    options = {'py2exe': py2exe_options}
)