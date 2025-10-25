
"""
check_pytorch_device.py
-----------------------
A simple script to check what hardware backend PyTorch is using:
- CUDA (NVIDIA GPU)
- MPS (Apple Silicon GPU)
- CPU (default fallback)

Author: Dr. Adrian Dominguez Castro
"""

import torch

def check_device():
    """
    Detects and prints which device PyTorch will use.
    """

    # Check for CUDA (NVIDIA)
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"✅ CUDA is available!")
        print(f"Using GPU: {torch.cuda.get_device_name(0)}")
    
    # Check for MPS (Apple Silicon)
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
        print("✅ MPS (Metal Performance Shaders) is available on this Mac!")
        print("Using Apple Silicon GPU via MPS backend.")
    
    # Default to CPU
    else:
        device = torch.device("cpu")
        print("⚙️ Running on CPU (no GPU backend available).")
    
    print(f"\nCurrent PyTorch device: {device}")
    return device


if __name__ == "__main__":
    print("🔍 Checking PyTorch device compatibility...\n")
    device = check_device()
    print("\nDone ✅")

