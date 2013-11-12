# This file is for testing/playing the codes.
# python -i play.py

import ast
import astpp
import inspect

from xmlGenerator import *

def check(node):
    for x, y in ast.iter_fields(node):
        print x
        print y
        print


# vvadd
n = 1024*1024*16
va = {
      'y' : ('float', [n]),
      'a' : ('float', [n]),
      'b' : ('float', [n]),
      'n' : ('int', [])
      }
def vvadd(y, a, b, n):
    for i in range(0,n):
        y[i] = a[i]+b[i]




# matmul
mm = {
      'A' : ('float', [2048, 2048]),
      'B' : ('float', [2048, 2048]),
      'Y' : ('float', [2048, 2048]),
      'n' : ('int', [])
}
def matmul(A,B,Y,n):
    for i in range(0,n):
        for j in range(0,n):
            for k in range(0,n):
                Y[i][j] = Y[i][j] + A[i][k]*B[k][j];




# array doubler
ad = {
      'y' : ('float', [1024]),
      'a' : ('float', [1024])
}
def array_doubler(y, a):
    for i in range(0,1024):
        y[i] = 2.0 * a[i];




# fuck me...
fu = {
      'A' : ('float', [16]),
      'X' : ('float', [16])
}
def fuckMe(A, X):
    for i in range(0,15):
        A[i] = X[i+1] + X[i];
        X[i+1] = A[i] + 10;



















s = inspect.getsource(matmul)
a = ast.parse(s)
xg = xmlGenerator(mm)
