# Test program for 'image_altar' or 'project.py'

from pytest import raises
from project import grayscale
import numpy as np


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
