import os
from pathlib import Path
p = Path(r'.\log')
for file in p.rglob('*.jpg*'):
    if os.path.isfile(file):
        os.remove(file)
