import requests
from sklearn import datasets
import numpy as np


def load_correct_results():
    return np.load("../correct_output.npy")


def load_data():
    iris = datasets.load_iris()
    x = iris.data
    x_true = load_correct_results()
    return x, x_true


def main():
    x, x_true = load_data()
    results = []
    for sample in x:
        serialized = sample.tolist()
        response = requests.post("http://localhost:8000/predict", json=serialized)
        results.append(response.json())
    results = np.array(results)
    correct = np.allclose(results, x_true)
    if correct:
        print("Tests pass!")
    else:
        print("Tests failed!")


if __name__=="__main__":
    main()
