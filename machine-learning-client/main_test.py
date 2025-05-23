'''tests for main'''



import pytest
from PIL import Image
import torch  # PyTorch dynamic attributes cause linting false positives

# pylint: disable=no-member
from main import load_image, draw_bounding_boxes



# pylint: disable=redefined-outer-name


@pytest.fixture
def make_dummy_image():
    '''use blank image for testing'''
    return Image.new("RGB", (100, 100), color='white')




def test_load_image_valid_path(tmp_path):
    '''temp image file'''
    image_path = tmp_path / "test.jpg"
    image = Image.new("RGB", (10, 10))
    image.save(image_path)

    loaded = load_image(str(image_path))
    assert isinstance(loaded, Image.Image)
    assert loaded.mode == "RGB"





def test_draw_bounding_boxes_with_confident_detection(make_dummy_image):
    '''test to draw bounding boxes'''
    boxes = torch.tensor([[10, 10, 50, 50]])
    labels = ["cat"]
    scores = torch.tensor([0.9])
    result = draw_bounding_boxes(make_dummy_image.copy(), boxes, labels, scores, threshold=0.5)
    assert isinstance(result, Image.Image)




def test_draw_bounding_boxes_below_threshold(make_dummy_image):
    '''test to make sure no boxes drawn if confidence is low'''
    boxes = torch.tensor([[10, 10, 50, 50]])
    labels = ["dog"]
    scores = torch.tensor([0.3])
    result = draw_bounding_boxes(make_dummy_image.copy(), boxes, labels, scores, threshold=0.5)
    assert isinstance(result, Image.Image)
