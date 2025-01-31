

import numpy as np
import pandas as pd
def calculer_mse(m, b, X, Y):

    Y_pred = m * X + b
    mse = np.mean((Y - Y_pred) ** 2)
    return mse



def best_mse():
    data = pd.read_csv("RK_IA_DG_data.csv", header=None)
    X = data[0].values
    Y = data[1].values

    best_m = None
    best_b = None
    min_error = float('inf')

    m_values = np.arange(-50, 50.01, 0.01)
    b_values = np.arange(-10, 10.01, 0.01)

    for m in m_values:
        for b in b_values:
            error = calculer_mse(m, b, X, Y)
            if error < min_error:
                min_error = error
                best_m = m
                best_b = b

    print(f"Meilleur modèle : m = {best_m}, b = {best_b}, erreur minimale = {min_error}")
best_mse()


def calculer_grandiant(X, Y, m, b):
    """
    calcule les dérivées partielles
    """
    n = len(Y)
    y_prediction = m * X + b
    error = y_prediction - Y

    dm = (2 / n) * np.dot(error, X)
    db = (2 / n) * np.sum(error)

    return dm, db



def decente_gradiant(X, Y, alpha=0.01, seuil=0.00005):
    """
    Descente de gradient
    """
    m, b = 100,89
    previous_error = float('inf')
    iteration = 0

    while True:
        dm, db = calculer_grandiant(X,Y, m, b)

        current_error = calculer_mse(m,b,X,Y)

        if abs(previous_error - current_error) < seuil:
            break


        if not np.isfinite(dm) or not np.isfinite(db):
            break

        m -= alpha * dm
        b -= alpha * db

        previous_error = current_error
        iteration += 1

        print(f"Itération {iteration}: m={m:.5f}, b={b:.5f}, erreur={current_error:.5f}")

    return m, b

def main():
    file_path = "RK_IA_DG_data.csv"
    data = np.loadtxt(file_path, delimiter=",")
    X, Y = data[:, 0], data[:, 1]

    X = (X - np.mean(X)) / np.std(X)
    Y = (Y - np.mean(Y)) / np.std(Y)

    alpha = 0.01
    seuil = 0.00005

    m_optimal, b_optimal = decente_gradiant(X,Y, alpha, seuil)

    print(f"Meilleurs parametres : m = {m_optimal:.5f}, b = {b_optimal:.5f}")
main()