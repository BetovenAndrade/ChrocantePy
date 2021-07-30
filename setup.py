from cx_Freeze import setup, Executable
 
setup(name='DownloadChromeDriver',
    version='1.0',
    description='Download automático de driver do Chrome',
    options={'build_exe': {'packages': ['temp']}},
    executables = [Executable(
                   script='Main.py',
                   base=None,
                   icon='Chrocante.ico')]
)