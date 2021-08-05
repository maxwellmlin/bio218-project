"""
Installs the package requirements and Git repositories needed for the Biological Clocks class
"""

import os, subprocess

def rmdir(dir):
    # change permissions of all files in dir to ensure automatic deletion
    for root, dirs, files in os.walk(dir):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o777)
        for f in files:
            os.chmod(os.path.join(root, f), 0o777)

    # completely delete dir and all its contents
    if dir[-1] == os.sep: dir = dir[:-1]
    files = os.listdir(dir)
    for file in files:
        if file == '.' or file == '..': continue
        path = dir + os.sep + file
        if os.path.isdir(path):
            rmdir(path)
        else:
            os.unlink(path)
    os.rmdir(dir)

# Delete previous repositories
for dir in ['pydl', 'pyjtk', 'lempy']:
    if os.path.isdir(dir):
        rmdir(dir)

# Clone the necessary repositories into the src folder
os.chdir('src')
os.system('git clone https://gitlab.com/biochron/pydl.git')
os.system('git clone https://gitlab.com/biochron/pyjtk.git')
os.system('git clone https://gitlab.com/biochron/lempy.git')

# install modules that require installation
os.chdir('pyjtk')
subprocess.call(['pip install -e .'], shell=True)
os.chdir('../pydl')
subprocess.call(['pip install -e .'], shell=True)


