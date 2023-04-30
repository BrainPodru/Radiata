import os
from typing import *

from pydantic import BaseModel

from . import config


class DiffusersModel(BaseModel):
    model_id: str
    IF_model_id_1: Optional[str] = None
    IF_model_id_2: Optional[str] = None
    IF_model_id_3: Optional[str] = None

    def get_model_dir(self):
        return os.path.join(config.get("model_dir"), self.model_id.replace("/", os.sep))

    def get_trt_path(self):
        return os.path.join(
            config.get("model_dir"),
            "accelerate",
            "tensorrt",
            self.model_id.replace("/", os.sep),
        )

    def trt_available(self):
        trt_path = self.get_trt_path()
        necessary_files = [
            "engine/clip.plan",
            "engine/unet.plan",
            "engine/vae.plan",
            "engine/vae_encoder.plan",
            "onnx/clip.opt.onnx",
            "onnx/unet.opt.onnx",
            "onnx/vae.opt.onnx",
            "onnx/vae_encoder.opt.onnx",
        ]
        for file in necessary_files:
            filepath = os.path.join(trt_path, *file.split("/"))
            if not os.path.exists(filepath):
                return False
        return True

    def is_if(self):
        return (
            self.IF_model_id_1 is not None,
            self.IF_model_id_2 is not None,
            self.IF_model_id_3 is not None,
        )
