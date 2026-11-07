import io
import unittest

from PIL import Image

from modules.skin_analysis import prepare_image_bytes, validate_image


class FakeUpload:
    def __init__(self, data, name="photo.png"):
        self._data = data
        self.name = name
        self.size = len(data)

    def getvalue(self):
        return self._data


def image_bytes(image_format="PNG", mode="RGB"):
    output = io.BytesIO()
    color = (20, 40, 60, 128) if mode == "RGBA" else (20, 40, 60)
    Image.new(mode, (32, 24), color).save(output, format=image_format)
    return output.getvalue()


class SkinImageTests(unittest.TestCase):
    def test_valid_png_is_accepted_and_converted_to_jpeg(self):
        upload = FakeUpload(image_bytes("PNG", "RGBA"))

        self.assertEqual(validate_image(upload), (True, None))
        prepared = prepare_image_bytes(upload)

        with Image.open(io.BytesIO(prepared)) as image:
            self.assertEqual(image.format, "JPEG")
            self.assertEqual(image.mode, "RGB")
            self.assertEqual(image.size, (32, 24))

    def test_invalid_image_is_rejected(self):
        valid, message = validate_image(FakeUpload(b"not an image", "fake.jpg"))

        self.assertFalse(valid)
        self.assertIn("not a valid", message)


if __name__ == "__main__":
    unittest.main()
