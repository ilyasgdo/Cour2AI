import numpy as np
import random

# ----------------------------------
# Configuration initiale
# ----------------------------------
matrice_interventions = np.array([
    [5, 2, 4, 8, 9, 0, 3, 3, 8, 7],
    [5, 5, 3, 4, 4, 6, 4, 1, 9, 1],
    [4, 1, 2, 1, 3, 8, 7, 8, 9, 1],
    [1, 7, 1, 6, 9, 3, 1, 9, 6, 9],
    [4, 7, 4, 9, 9, 8, 6, 5, 4, 2],
    [7, 5, 8, 2, 5, 2, 3, 9, 8, 2],
    [1, 4, 0, 6, 8, 4, 0, 1, 2, 1],
    [1, 5, 2, 1, 2, 8, 3, 3, 6, 2],
    [4, 5, 9, 6, 3, 9, 7, 6, 5, 10],
    [0, 6, 2, 8, 7, 1, 2, 1, 5, 3]
])
hauteur, largeur = matrice_interventions.shape
total_operations = matrice_interventions.sum()


# ----------------------------------
# Définition des structures
# ----------------------------------
class Individu:
    def __init__(self, x=None, y=None):
        # Accès aux variables globales
        self.x = x if x is not None else random.randint(0, largeur - 1)
        self.y = y if y is not None else random.randint(0, hauteur - 1)
        self.adaptation = 0

    def calculer_adaptation(self):
        j_grid, i_grid = np.meshgrid(np.arange(largeur), np.arange(hauteur))
        distances = np.sqrt((self.x - j_grid) ** 2 + (self.y - i_grid) ** 2)
        cout_total = np.sum(matrice_interventions * distances)
        print(f"cout total: {cout_total}")
        self.adaptation = cout_total / total_operations
        return self.adaptation
# ----------------------------------
# Opérateurs génétiques
# ----------------------------------
def croisement(parent1, parent2):
    """Crée deux enfants par échange de coordonnées"""
    enfant1 = Individu(parent1.x, parent2.y)
    enfant2 = Individu(parent2.x, parent1.y)
    return enfant1, enfant2


def mutation(individu):
    """Modifie légèrement la position"""
    if random.random() < 0.5:
        nouveau_x = individu.x + random.choice([-1, 0, 1])
        individu.x = np.clip(nouveau_x, 0, largeur - 1)
    else:
        nouveau_y = individu.y + random.choice([-1, 0, 1])
        individu.y = np.clip(nouveau_y, 0, hauteur - 1)
    return individu


# ----------------------------------
# Algorithme principal
# ----------------------------------
def algorithme_evolutionnaire():
    taille_population = 5999
    population = [Individu() for _ in range(taille_population)]
    meilleur_historique = None
    generation = 0

    while True:
        # Évaluation de l'adaptation
        for individu in population:
            individu.calculer_adaptation()

        # Tri par performance
        population.sort(key=lambda x: x.adaptation)
        meilleur_actuel = population[0]

        # Condition d'arrêt
        if meilleur_historique and np.linalg.norm([meilleur_actuel.x - meilleur_historique.x,
                                                   meilleur_actuel.y - meilleur_historique.y]) <= 0.001:
            print(f"Convergence à la génération {generation}")
            break

        meilleur_historique = meilleur_actuel

        # Sélection des meilleurs (20%)
        selectionnes = population[:int(taille_population * 0.2)]

        # Reproduction
        descendants = []
        while len(descendants) < taille_population - len(selectionnes):
            p1, p2 = random.choices(selectionnes, k=2)
            e1, e2 = croisement(p1, p2)
            descendants.append(mutation(e1))
            descendants.append(mutation(e2))

        population = selectionnes + descendants[:taille_population - len(selectionnes)]
        generation += 1

    return meilleur_historique


# ----------------------------------
# Exécution et résultats
# ----------------------------------
solution_optimale = algorithme_evolutionnaire()
print(f"Position optimale: ({solution_optimale.x}, {solution_optimale.y})")
print(f"Coût moyen: {solution_optimale.adaptation:.2f} km/intervention")

print("testtttt")
ao=Individu(0,0)
ao.calculer_adaptation()
