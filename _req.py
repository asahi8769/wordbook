from utils.functions import subprocess_cmd, install, force_reinstall
from utils.settings import SCRIPTS_DIR

_install = True

if _install :
    subprocess_cmd(rf'cd {SCRIPTS_DIR} && python -m venv {SCRIPTS_DIR} && activate')

    # subprocess_cmd(f'{force_reinstall("pandas>=0.25.3,<0.26.0")}')
    # subprocess_cmd(f'{force_reinstall("numpy>=1.18.1,<1.19.0")}')
    # subprocess_cmd(f'{install("selenium")}')
    subprocess_cmd(f'{install("tqdm")}')



