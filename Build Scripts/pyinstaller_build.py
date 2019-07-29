import os

options = ' --windowed --noconfirm --name "Mod Loader" --icon icon.icns'

spec_check = input("Is spec file configured? (Y/N)").lower()
if spec_check == "y":
    os.system('python3 -m PyInstaller "Mod Loader.spec" ' + options)
else:
    os.system('python3 -m PyInstaller ModLoader.py ' + options)

'''
place in app BUNDLE:

 info_plist={
    'NSHighResolutionCapable': 'True'
    },
'''