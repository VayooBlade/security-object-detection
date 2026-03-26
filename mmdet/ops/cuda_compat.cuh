#pragma once

#include <ATen/ATen.h>
#include <ATen/cuda/CUDAContext.h>
#include <ATen/cuda/Atomic.cuh>
#include <c10/cuda/CUDAException.h>

#ifndef THCCeilDiv
#define THCCeilDiv(a, b) ((((a) + (b)-1) / (b)))
#endif

#ifndef THCudaCheck
#define THCudaCheck(EXPR) C10_CUDA_CHECK(EXPR)
#endif
