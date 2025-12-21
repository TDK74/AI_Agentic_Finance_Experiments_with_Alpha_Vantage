import subprocess
import sys  # Import sys module, required for accessing sys.executable


def install(package):
    """Install a Python package using pip if not already available."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
    import yfinance
except ImportError:
    install('yfinance')

try:
    import matplotlib.pyplot as plt
except ImportError:
    install('matplotlib')
