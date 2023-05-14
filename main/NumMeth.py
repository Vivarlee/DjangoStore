import numpy as np
from sympy import Symbol
from sympy.core import sympify
import math

def gauss(n, a):
    print(n, a)
    x = np.zeros(n)
    print(a)
    # Applying Gauss Elimination
    for i in range(n):
        for j in range(i + 1, n):
            ratio = a[j][i] / a[i][i]

            for k in range(n+1):
                a[j][k] = a[j][k] - ratio * a[i][k]

    # Back Substitution
    x[n - 1] = a[n - 1][n] / a[n - 1][n - 1]

    for i in range(n - 2, -1, -1):
        x[i] = a[i][n]

        for j in range(i + 1, n):
            x[i] = x[i] - a[i][j] * x[j]

        x[i] = x[i] / a[i][i]

    # Displaying solution
    print('\nRequired solution is: ')
    for i in range(n):
        print('X%d = %0.2f' % (i, x[i]), end='\t')
    # Returning solution
    return x.tolist()


def newton_root(function: str, x0, atol=0.001):
    expr: Symbol = sympify(function)
    diff = expr.diff()

    iterations_amount = 10000
    x = x0
    for i in range(iterations_amount):
        prev_x = x
        x = x - expr.evalf(subs={Symbol('x'): x}) / diff.evalf(subs={Symbol('x'): x})
        if (abs(x - prev_x) < 2*atol):
            print('Found')
            break

    return x


def jacobi_roots(A, b, atol=0.001):
    x = np.zeros_like(b)
    iterations = 1000
    found_early = False
    for it_count in range(iterations):
        x_new = np.zeros_like(x)

        for i in range(A.shape[0]):
            s1 = np.dot(A[i, :i], x[:i])
            s2 = np.dot(A[i, i + 1:], x[i + 1:])
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
            if x_new[i] == x_new[i-1]:
                break

        if np.allclose(x, x_new, atol=1e-10, rtol=0.):
            found_early = True
            break

        x = x_new

    return x

def gauss_seidel_roots(A, b):
    n = len(A)
    x = np.zeros(n)

    for j in range(0, n):
        d = b[j]

        for i in range(0, n):
            if(j != i):
                d-=A[j][i] * x[i]
        x[j] = d / A[j][j]

    return x