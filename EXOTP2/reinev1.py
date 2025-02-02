import random


def cost_function(individual):
    """Calcule le nombre de conflits (uniquement sur les diagonales) dans l'individu."""
    conflicts = 0
    n = len(individual)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(individual[i] - individual[j]) == abs(i - j):
                conflicts += 1
    return conflicts


def generate_random_individual():
    """Crée un individu valide (permutation des chiffres 1 à 8)."""
    return random.sample(range(1, 9), 8)


def crossover(parent1, parent2):

    #découpage en segments
    seg_p1_1 = parent1[:3]
    seg_p1_2 = parent1[3:5]
    seg_p1_3 = parent1[5:]

    seg_p2_1 = parent2[:3]
    seg_p2_2 = parent2[3:5]
    seg_p2_3 = parent2[5:]

    #sélection aléatoire des segments (le segment 2 est inversé)
    segment1 = seg_p1_1 if random.random() < 0.5 else seg_p2_1
    segment2 = seg_p1_2[::-1] if random.random() < 0.5 else seg_p2_2[::-1]
    segment3 = seg_p1_3 if random.random() < 0.5 else seg_p2_3

    #combinaison des segments pour former le nouvel individu
    new_individual = segment1 + segment2 + segment3

    return new_individual


def mutate(individual):
    """Effectue une mutation en échangeant deux valeurs aléatoires dans la permutation."""
    n = len(individual)
    i, j = random.sample(range(n), 2)
    individual[i], individual[j] = individual[j], individual[i]
    return individual


def genetic_algorithm(max_iterations=5000000):
    """Cherche une solution au problème des 8 reines avec un algorithme génétique."""
    best_individual = generate_random_individual()
    best_cost = cost_function(best_individual)

    for iteration in range(max_iterations):
        if best_cost == 0:
            print(f"Solution trouvée en {iteration} itérations : {best_individual}")
            return best_individual

        # Sélection d'un partenaire aléatoire
        partner = generate_random_individual()

        # Croisement entre le meilleur individu et le partenaire
        new_individual = crossover(best_individual, partner)

        # Mutation avec une probabilité de 50%
        if random.random() < 0.5:
            new_individual = mutate(new_individual)

        # Évaluation du nouvel individu
        new_cost = cost_function(new_individual)

        # Mise à jour du meilleur individu si l'individu courant est meilleur
        if new_cost < best_cost:
            best_individual = new_individual
            best_cost = new_cost

        # Affichage de la progression toutes les 5000 itérations

        print(f"Itération {iteration} : Meilleur coût = {best_cost} Individu = {best_individual}")

    print(f"Aucune solution trouvée après {max_iterations} itérations.")
    return None


# Lancer l'algorithme
genetic_algorithm()
