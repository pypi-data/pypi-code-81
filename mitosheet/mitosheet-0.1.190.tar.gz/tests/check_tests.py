"""
Helper python script that throws an error
if a test contains test.only.
"""

from pathlib import Path

for name in Path('./').rglob('*.ts'):
    with open(name) as f:
        for line in f.readlines():
            if '.only' in line:
                raise Exception(f'Error: {name} contains test.only')