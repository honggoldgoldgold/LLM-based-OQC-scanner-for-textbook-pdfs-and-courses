import gc
import os
import tempfile
import unittest
import warnings

from PIL import Image

from OCRLLM.core.utils import resize_image_if_needed


class ResizeImageResourceTests(unittest.TestCase):
    def test_resize_image_if_needed_closes_source_file_when_copying(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "src.png")
            dest = os.path.join(tmp, "dest.png")
            Image.new("RGB", (8, 8), "white").save(src)

            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always", ResourceWarning)
                resize_image_if_needed(src, max_side=2048, output_path=dest)
                gc.collect()

            resource_warnings = [warning for warning in caught if issubclass(warning.category, ResourceWarning)]
            self.assertEqual(resource_warnings, [])


if __name__ == "__main__":
    unittest.main()
