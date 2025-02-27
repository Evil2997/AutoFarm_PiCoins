import cv2

from app.logs.logger import logger


def get_image_size(
        image_path: str
) -> tuple[int, int]:
    image = cv2.imread(image_path)
    if image is None:
        logger.error(f"Image not found: {image_path}")
        raise FileNotFoundError(f"Image not found: {image_path}")
    height, width, _ = image.shape
    return width, height
