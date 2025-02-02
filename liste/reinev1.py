import random

def cost_function(individual):
    """Calcule le nombre de conflits dans l'individu."""
    conflicts = 0
    n = len(individual)

    for i in range(n):
        for j in range(i + 1, n):
            if abs(individual[i] - individual[j]) == abs(i - j):
                conflicts += 1

    return conflicts

def generate_random_individual():
    """Génère un individu valide (permutation des chiffres 1 à 8)."""
    return random.sample(range(1, 9), 8)

def custom_crossover(individual):
    """Effectue un croisement en swap des blocs 3-2-3."""
    first_three = individual[:3]
    middle_two = individual[3:5]
    last_three = individual[5:]

    new_individual = last_three + middle_two[::-1] + first_three

    return new_individual

def mutate(individual):
    """Effectue une mutation en échangeant deux valeurs aléatoires."""
    n = len(individual)
    i, j = random.sample(range(n), 2)
    individual[i], individual[j] = individual[j], individual[i]

    return individual

# === Algorithme Génétique ===
def genetic_algorithm(max_iterations=5000000):
    """Cherche une solution au problème des 8 reines avec un algorithme génétique."""
    current_individual = generate_random_individual()
    best_individual = current_individual
    best_cost = cost_function(current_individual)

    for iteration in range(max_iterations):
        if best_cost == 0:
            print(f"Solution trouvée en {iteration} itérations : {best_individual}")
            return best_individual

        # Croisement
        new_individual = custom_crossover(best_individual)

        # Mutation avec une probabilité de 50%
        if random.random() < 0.5:
            new_individual = mutate(new_individual)

        # Évaluation du nouvel individu
        new_cost = cost_function(new_individual)

        # Mise à jour du meilleur individu
        if new_cost < best_cost:
            best_individual = new_individual
            best_cost = new_cost

        # Affichage de progression toutes les 5000 itérations

        print(f"Itération {iteration} : Meilleur coût = {best_cost} tab= {best_individual}")

    print("Aucune solution trouvée après 50 000 itérations.")
    return None

# Lancer l'algorithme
genetic_algorithm()
