# Check PyTorch Device
A small Python project to automatically detect which hardware backend PyTorch will use on your system:

- ✅ CUDA (NVIDIA GPU)
- ✅ MPS (Apple Silicon GPU)
- ⚙️ CPU (fallback if no GPU is available)

This is useful for making sure your PyTorch models will run on the optimal device before training.

---

## Usage

Run the device check:

```bash
python check_pytorch_device.py
```
