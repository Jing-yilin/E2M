from api.core.converters.base_converter import (
    BaseConverter,
)

# logging
import logging

logger = logging.getLogger(__name__)


class TxtConverter(BaseConverter):

    def convert(self, **kwargs) -> str:
        # directly read the txt file
        content = ""
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading file: {self.file}, error: {e}")
        finally:
            self.rm_file()
        return content
