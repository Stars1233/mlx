# Copyright © 2023 Apple Inc.
import unittest

import mlx.core as mx
import mlx.nn.init as init
import mlx_tests
import numpy as np


class TestInit(mlx_tests.MLXTestCase):
    def test_constant(self):
        value = 5.0

        for dtype in [mx.float32, mx.float16]:
            initializer = init.constant(value, dtype)
            for shape in [(3,), (3, 3), (3, 3, 3)]:
                result = initializer(mx.array(mx.zeros(shape)))
                with self.subTest(shape=shape):
                    self.assertEqual(result.shape, shape)
                    self.assertEqual(result.dtype, dtype)

    def test_normal(self):
        mean = 0.0
        std = 1.0
        for dtype in [mx.float32, mx.float16]:
            initializer = init.normal(mean, std, dtype=dtype)
            for shape in [(3,), (3, 3), (3, 3, 3)]:
                result = initializer(mx.array(np.empty(shape)))
                with self.subTest(shape=shape):
                    self.assertEqual(result.shape, shape)
                    self.assertEqual(result.dtype, dtype)

    def test_uniform(self):
        low = -1.0
        high = 1.0

        for dtype in [mx.float32, mx.float16]:
            initializer = init.uniform(low, high, dtype)
            for shape in [(3,), (3, 3), (3, 3, 3)]:
                result = initializer(mx.array(np.empty(shape)))
                with self.subTest(shape=shape):
                    self.assertEqual(result.shape, shape)
                    self.assertEqual(result.dtype, dtype)
                    self.assertTrue(mx.all(result >= low) and mx.all(result <= high))

    def test_identity(self):
        for dtype in [mx.float32, mx.float16]:
            initializer = init.identity(dtype)
            for shape in [(3,), (3, 3), (3, 3, 3)]:
                result = initializer(mx.zeros((3, 3)))
                self.assertTrue(mx.array_equal(result, mx.eye(3)))
                self.assertEqual(result.dtype, dtype)
                with self.assertRaises(ValueError):
                    result = initializer(mx.zeros((3, 2)))

    def test_glorot_normal(self):
        for dtype in [mx.float32, mx.float16]:
            initializer = init.glorot_normal(dtype)
            for shape in [(3, 3), (3, 3, 3)]:
                result = initializer(mx.array(np.empty(shape)))
                with self.subTest(shape=shape):
                    self.assertEqual(result.shape, shape)
                    self.assertEqual(result.dtype, dtype)

    def test_glorot_uniform(self):
        for dtype in [mx.float32, mx.float16]:
            initializer = init.glorot_uniform(dtype)
            for shape in [(3, 3), (3, 3, 3)]:
                result = initializer(mx.array(np.empty(shape)))
                with self.subTest(shape=shape):
                    self.assertEqual(result.shape, shape)
                    self.assertEqual(result.dtype, dtype)

    def test_he_normal(self):
        for dtype in [mx.float32, mx.float16]:
            initializer = init.he_normal(dtype)
            for shape in [(3, 3), (3, 3, 3)]:
                result = initializer(mx.array(np.empty(shape)))
                with self.subTest(shape=shape):
                    self.assertEqual(result.shape, shape)
                    self.assertEqual(result.dtype, dtype)

    def test_he_uniform(self):
        for dtype in [mx.float32, mx.float16]:
            initializer = init.he_uniform(dtype)
            for shape in [(3, 3), (3, 3, 3)]:
                result = initializer(mx.array(np.empty(shape)))
                with self.subTest(shape=shape):
                    self.assertEqual(result.shape, shape)
                    self.assertEqual(result.dtype, dtype)

    def test_sparse(self):
        mean = 0.0
        std = 1.0
        sparsity = 0.5
        for dtype in [mx.float32, mx.float16]:
            initializer = init.sparse(sparsity, mean, std, dtype=dtype)
            for shape in [(3, 2), (2, 2), (4, 3)]:
                result = initializer(mx.array(np.empty(shape)))
                with self.subTest(shape=shape):
                    self.assertEqual(result.shape, shape)
                    self.assertEqual(result.dtype, dtype)
                    self.assertEqual(
                        (mx.sum(result == 0) >= 0.5 * shape[0] * shape[1]), True
                    )
            with self.assertRaises(ValueError):
                result = initializer(mx.zeros((1,)))

    def test_orthogonal(self):
        initializer = init.orthogonal(gain=1.0, dtype=mx.float32)

        # Test with a square matrix
        shape = (4, 4)
        result = initializer(mx.zeros(shape, dtype=mx.float32))
        self.assertEqual(result.shape, shape)
        self.assertEqual(result.dtype, mx.float32)

        I = result @ result.T
        eye = mx.eye(shape[0], dtype=mx.float32)
        self.assertTrue(
            mx.allclose(I, eye, atol=1e-5), "Orthogonal init failed on a square matrix."
        )

        # Test with a rectangular matrix: more rows than cols
        shape = (6, 4)
        result = initializer(mx.zeros(shape, dtype=mx.float32))
        self.assertEqual(result.shape, shape)
        self.assertEqual(result.dtype, mx.float32)

        I = result.T @ result
        eye = mx.eye(shape[1], dtype=mx.float32)
        self.assertTrue(
            mx.allclose(I, eye, atol=1e-5),
            "Orthogonal init failed on a rectangular matrix.",
        )


if __name__ == "__main__":
    mlx_tests.MLXTestRunner()
