# Test program for 'image_altar' or 'project.py'
# Note that the unit test will refer to files "test.png" and "test.svg", if these already exist errrors will be raised

from pytest import raises
from project import grayscale, distribute_both_ends, setup_vector_draw, pix_to_image, pixellate
import numpy as np
import os
import sys


def test_grayscale_inputtypes():
    with raises(TypeError):
        grayscale("APPLE")
    with raises(TypeError):
        grayscale(1)
    with raises(TypeError):
        grayscale(1.0)
    with raises(TypeError):
        grayscale([1])
    with raises(TypeError):
        grayscale(np.array([[1]]))


def test_grayscale_outputs():
    assert np.allclose(grayscale(np.array([[[0.25, 0.5, 0.75]]])), np.array([[[0.5, 0.5, 0.5]]]))
    assert np.allclose(grayscale(np.array([[[0.11, 0.2, 0.29], [0.7, 0.8, 0.9]]])),
                       np.array([[[0.2, 0.2, 0.2], [0.8, 0.8, 0.8]]]))
    assert np.allclose(grayscale(np.array([[[0.1, 0.2, 0.6]]])), np.array([[[0.3, 0.3, 0.3]]]))


# noinspection PyTypeChecker
def test_distribute_input():
    with raises(ValueError):
        distribute_both_ends("APPLE")
    with raises(TypeError):
        distribute_both_ends([1, 2])
    with raises(TypeError):
        distribute_both_ends(np.array([1, 2]))
    with raises(TypeError):
        distribute_both_ends()


def test_distribute_output():
    assert distribute_both_ends(6) == [0, 1, 2, -3, -2, -1]
    assert distribute_both_ends(5) == [0, 1, -3, -2, -1]
    assert distribute_both_ends(1) == [-1]
    assert distribute_both_ends(0) == []
    assert distribute_both_ends('0') == []


def test_vectordraw():
    cmarray = np.array([[[256, 256, 256], [128, 128, 128]], [[64, 64, 64], [32, 32, 32]]])
    test_svd_run = setup_vector_draw(cmarray, 50, filename='test.svg')
    assert len(test_svd_run) == 3
    assert np.allclose(test_svd_run[2],
                       np.array([[[1.0, 1.0, 1.0], [0.5, 0.5, 0.5]], [[0.25, 0.25, 0.25], [0.125, 0.125, 0.125]]]))


def test_pix_save():
    if os.path.exists('test.png'):
        print("File 'test.png' already exists, aborting to avoid overwrite")
        sys.exit()
    imarray = np.array([[[255, 255, 255], [128, 128, 128]], [[64, 64, 64], [32, 32, 32]]], dtype=np.uint8)
    pix_to_image(imarray, filename='test.png')
    assert os.path.exists('test.png')
    if os.path.exists('test.png'):
        os.remove('test.png')
    with raises(TypeError):
        pix_to_image(np.array([[[255, 255, 255], [128, 128, 128]], [[64, 64, 64], [32, 32, 32]]]))
    with raises(AttributeError):
        pix_to_image(4)
    with raises(AttributeError):
        pix_to_image('APPLE')


def test_pixellate():
    if os.path.exists('test.png'):
        print("File 'test.png' already exists, aborting to avoid overwrite")
        sys.exit()
    else:
        imarray = np.array([[[255, 255, 255]] * 50] * 60, dtype=np.uint8)
        pix_to_image(imarray, filename='test.png')
        assert pixellate('test.png').shape == (4, 3, 3)
        assert pixellate('test.png', blocksize=5).shape == (12, 10, 3)
        with raises(ValueError):
            pixellate('test.png', blocksize=70)
        imarray = np.array([[[255, 255, 255]] * 400] * 300, dtype=np.uint8)
        pix_to_image(imarray, filename='test.png')
        assert pixellate('test.png').shape == (20, 26, 3)
        imarray = np.array([[[255, 255, 255]] * 50] * 60, dtype=np.uint8)
        pix_to_image(imarray, filename='test.png')
        assert pixellate('test.png', blocksize=3).shape == (20, 16, 3)
        if os.path.exists('test.png'):
            os.remove('test.png')
        with raises(FileNotFoundError):
            pixellate('DONT NAME A FILE THIS OR YOU WILL BREAK THE PYTEST.png')
        with raises(AttributeError):
            pixellate(123)
