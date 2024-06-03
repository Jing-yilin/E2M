import logging
from api.core.marker.postprocessors.editor import load_editing_model
from surya.model.detection import segformer
from texify.model.model import load_model as load_texify_model
from texify.model.processor import load_processor as load_texify_processor
from api.core.marker.settings import settings
from surya.model.recognition.model import load_model as load_recognition_model
from surya.model.recognition.processor import (
    load_processor as load_recognition_processor,
)
from surya.model.ordering.model import load_model as load_order_model
from surya.model.ordering.processor import load_processor as load_order_processor

logger = logging.getLogger(__name__)


class ModelHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ModelHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self, langs=None):
        if not hasattr(self, "models"):
            self.models = self.load_all_models(langs)

    @classmethod
    def get_models(cls, langs=None):
        return cls(langs).models

    def load_all_models(self, langs=None):
        logger.info("Loading all models")
        detection = setup_detection_model()
        layout = setup_layout_model()
        order = setup_order_model()
        edit = load_editing_model()

        ocr = (
            setup_recognition_model(langs)
            if (settings.OCR_ENGINE == "surya" and settings.OCR_ALL_PAGES)
            else None
        )
        texify = setup_texify_model()
        return [texify, layout, order, edit, detection, ocr]


def setup_recognition_model(langs):
    logger.info("Loading recognition model")
    rec_model = load_recognition_model(langs=langs)
    rec_processor = load_recognition_processor()
    rec_model.processor = rec_processor
    return rec_model


def setup_detection_model():
    logger.info("Loading detection model")
    model = segformer.load_model()
    processor = segformer.load_processor()
    model.processor = processor
    return model


def setup_texify_model():
    logger.info("Loading texify model")
    texify_model = load_texify_model(
        checkpoint=settings.TEXIFY_MODEL_NAME,
        device=settings.TORCH_DEVICE_MODEL,
        dtype=settings.TEXIFY_DTYPE,
    )
    texify_processor = load_texify_processor()
    texify_model.processor = texify_processor
    return texify_model


def setup_layout_model():
    logger.info("Loading layout model")
    model = segformer.load_model(checkpoint=settings.LAYOUT_MODEL_CHECKPOINT)
    processor = segformer.load_processor(checkpoint=settings.LAYOUT_MODEL_CHECKPOINT)
    model.processor = processor
    return model


def setup_order_model():
    logger.info("Loading order model")
    model = load_order_model()
    processor = load_order_processor()
    model.processor = processor
    return model
