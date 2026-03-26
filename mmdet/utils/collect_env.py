import os.path as osp
import subprocess
import sys
from collections import defaultdict

import cv2
import mmcv
import torch
import torchvision

import mmdet


def collect_env():
    env_info = {}
    env_info['sys.platform'] = sys.platform
    env_info['Python'] = sys.version.replace('\n', '')

    cuda_available = torch.cuda.is_available()
    env_info['CUDA available'] = cuda_available

    if cuda_available:
        from torch.utils.cpp_extension import CUDA_HOME
        env_info['CUDA_HOME'] = CUDA_HOME

        if CUDA_HOME is not None and osp.isdir(CUDA_HOME):
            try:
                nvcc_path = osp.join(CUDA_HOME, 'bin/nvcc')
                nvcc_out = subprocess.check_output(f'"{nvcc_path}" -V', shell=True)
                nvcc = nvcc_out.decode('utf-8').splitlines()[-1].strip()
            except Exception:
                nvcc = 'Not Available'
            env_info['NVCC'] = nvcc

        devices = defaultdict(list)
        for k in range(torch.cuda.device_count()):
            devices[torch.cuda.get_device_name(k)].append(str(k))
        for name, devids in devices.items():
            env_info['GPU ' + ','.join(devids)] = name

    try:
        gcc_out = subprocess.check_output('gcc --version', shell=True)
        gcc = gcc_out.decode('utf-8').splitlines()[0].strip()
    except Exception:
        gcc = 'Not Available'
    env_info['GCC'] = gcc

    env_info['PyTorch'] = torch.__version__
    env_info['PyTorch compiling details'] = torch.__config__.show()

    env_info['TorchVision'] = torchvision.__version__

    env_info['OpenCV'] = cv2.__version__

    env_info['MMCV'] = mmcv.__version__
    env_info['MMDetection'] = mmdet.__version__
    from mmdet.ops import get_compiler_version, get_compiling_cuda_version
    env_info['MMDetection Compiler'] = get_compiler_version()
    env_info['MMDetection CUDA Compiler'] = get_compiling_cuda_version()
    return env_info


if __name__ == '__main__':
    for name, val in collect_env().items():
        print('{}: {}'.format(name, val))
