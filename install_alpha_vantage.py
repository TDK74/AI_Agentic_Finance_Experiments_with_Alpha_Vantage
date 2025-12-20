import subprocess
import sys  # Import sys module, required for accessing sys.executable


def install(package):
    """Install a Python package using pip if not already available."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
    import alpha_vantage
except ImportError:
    install('alpha_vantage')

# Print instruction to get an API key from Alpha Vantage
print("Please visit 'https://www.alphavantage.co/support/#api-key' to get your free API key.")
