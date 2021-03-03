import numpy as np

def PrepareData(X, V, chunck=1_000):
        assert X.shape[1] == V.shape[1] == 3
        assert X.shape[0] == V.shape[0]
        n = X.shape[0] // chunck
        X = X[:n * chunck].reshape(n, chunck, 3)
        V = V[:n * chunck].reshape(n, chunck, 3)
        return X, V
