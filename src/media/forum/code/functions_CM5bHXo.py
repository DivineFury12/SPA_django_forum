"""
Sample code automatically generated on 2025-12-12 15:17:00

by www.matrixcalculus.org

from input

d/dx x'*A*x + c*sin(y)'*x = 2*A*x+c*sin(y)

where

A is a symmetric matrix
c is a scalar
x is a vector
y is a vector

The generated code is provided "as is" without warranty of any kind.
"""

from __future__ import division, print_function, absolute_import

import numpy as np

def fAndG(A, c, x, y):
    assert isinstance(A, np.ndarray)
    dim = A.shape
    assert len(dim) == 2
    A_rows = dim[0]
    A_cols = dim[1]
    if isinstance(c, np.ndarray):
        dim = c.shape
        assert dim == (1, )
    assert isinstance(x, np.ndarray)
    dim = x.shape
    assert len(dim) == 1
    x_rows = dim[0]
    assert isinstance(y, np.ndarray)
    dim = y.shape
    assert len(dim) == 1
    y_rows = dim[0]
    assert A_rows == x_rows == A_cols == y_rows

    t_0 = (A).dot(x)
    t_1 = np.sin(y)
    functionValue = ((x).dot(t_0) + (c * (t_1).dot(x)))
    gradient = ((2 * t_0) + (c * t_1))

    return functionValue, gradient

def checkGradient(A, c, x, y):
    # numerical gradient checking
    # f(x + t * delta) - f(x - t * delta) / (2t)
    # should be roughly equal to inner product <g, delta>
    t = 1E-6
    delta = np.random.randn(3)
    f1, _ = fAndG(A, c, x + t * delta, y)
    f2, _ = fAndG(A, c, x - t * delta, y)
    f, g = fAndG(A, c, x, y)
    print('approximation error',
          np.linalg.norm((f1 - f2) / (2*t) - np.tensordot(g, delta, axes=1)))

def generateRandomData():
    A = np.random.randn(3, 3)
    A = 0.5 * (A + A.T)  # make it symmetric
    c = np.random.randn(1)
    x = np.random.randn(3)
    y = np.random.randn(3)

    return A, c, x, y

if __name__ == '__main__':
    A, c, x, y = generateRandomData()
    functionValue, gradient = fAndG(A, c, x, y)
    print('functionValue = ', functionValue)
    print('gradient = ', gradient)

    print('numerical gradient checking ...')
    checkGradient(A, c, x, y)
