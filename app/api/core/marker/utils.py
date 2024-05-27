import torch
from api.core.marker.settings import settings


def flush_cuda_memory():
    if settings.TORCH_DEVICE_MODEL == "cuda":
        torch.cuda.empty_cache()
