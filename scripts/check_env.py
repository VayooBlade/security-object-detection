import subprocess, sys

result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
lines = result.stdout.splitlines()

wanted = ["torch", "ultralytics", "mmdet", "opencv", "numpy", "pillow", "scipy"]
found = []
for line in lines:
    if any(w in line.lower() for w in wanted):
        found.append(line.strip())

output_lines = ["=== Installed relevant packages ==="]
output_lines.extend(found if found else ["  (none found)"])

try:
    import torch
    output_lines.append(f"\nPyTorch: {torch.__version__}")
    output_lines.append(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        output_lines.append(f"GPU: {torch.cuda.get_device_name(0)}")
except ImportError:
    output_lines.append("\nPyTorch: NOT INSTALLED")

output_lines.append(f"\nPython: {sys.version}")

text = "\n".join(output_lines)
with open("f:/security-dataset/env_check.txt", "w") as f:
    f.write(text)
print("saved to env_check.txt")
print(text)
