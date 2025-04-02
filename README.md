

# MTA Project

A Python project that uses PyTorch with CUDA support, along with EasyOCR, PyAutoGUI, and other dependencies.

## Requirements

- Python 3.8 or newer
- NVIDIA GPU with CUDA support
- Git

## Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/yourusername/test.git
cd test
```

### Step 2: Create and activate a virtual environment

```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows
.venv\Scripts\activate

# Activate on macOS/Linux
source .venv/bin/activate
```

### Step 3: Install UV package manager (if not already installed)

```bash
pip install uv
```

### Step 4: Run the installation script

```bash
python install.py
```

This script will:
1. Install the package and its basic dependencies
2. Install PyTorch with CUDA support from the correct source

## Running the Project

After installation, you can run the sample script:

```bash
python -m test.main
```

This should display information about your GPU and confirm that CUDA is available.

## Troubleshooting

If you encounter issues with PyTorch CUDA:
1. Make sure you have compatible NVIDIA drivers installed
2. Verify your CUDA version with `nvidia-smi`
3. If needed, update the CUDA version in `install.py` to match your system
