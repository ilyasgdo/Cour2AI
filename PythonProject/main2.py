import numpy as np

def mean_squared_error(y_true, y_pred):
    """
    Calcule l'erreur quadratique moyenne (MSE).
    """
    return np.mean((y_true - y_pred) ** 2)

def compute_gradients(X, y, m, b):
    """
    Calcule les dérivées partielles de l'erreur MSE par rapport à m et b.
    """
    n = len(y)
    y_pred = m * X + b
    error = y_pred - y

    dm = (2 / n) * np.dot(error, X)
    db = (2 / n) * np.sum(error)

    return dm, db

def gradient_descent(X, y, learning_rate=0.01, threshold=0.00005):
    """
    Implémente la descente de gradient pour trouver les meilleurs paramètres m et b.
    """
    m, b = 0.0, 0.0  # Initialisation des paramètres
    previous_error = float('inf')

    while True:
        # Calcul des prédictions et de l'erreur
        y_pred = m * X + b
        current_error = mean_squared_error(y, y_pred)

        # Vérification de la condition d'arrêt
        if abs(previous_error - current_error) < threshold:
            break

        # Mise à jour des gradients
        dm, db = compute_gradients(X, y, m, b)

        # Mise à jour des paramètres
        m -= learning_rate * dm
        b -= learning_rate * db

        # Mise à jour de l'erreur précédente
        previous_error = current_error

    return m, b

# Exemple d'utilisation
if __name__ == "__main__":
    # Charger les données (remplacer par le chemin vers le fichier si nécessaire)
    data = np.loadtxt("RK_IA_DG_data.csv", delimiter=",")  # Fichier contenant deux colonnes : X, Y
    X, y = data[:, 0], data[:, 1]

    # Hyperparamètres
    learning_rate = 0.01
    threshold = 0.00005

    # Exécution de la descente de gradient
    m_optimal, b_optimal = gradient_descent(X, y, learning_rate, threshold)

    print(f"Paramètres optimaux : m = {m_optimal}, b = {b_optimal}")
