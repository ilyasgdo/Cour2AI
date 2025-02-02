

import random
import math

COLORS = ['♠', '♥', '♦', '♣']


def create_individu():

    individu = []
    for v in range(1, 11):
        gene = {
            'value': v,
            'color': random.choice(COLORS),
            'group': None
        }
        individu.append(gene)

    indices = list(range(10))
    random.shuffle(indices)
    product_indices = indices[:5]
    for i in range(10):
        if i in product_indices:
            individu[i]['group'] = 'product'
        else:
            individu[i]['group'] = 'sum'
    return individu


def evaluer_cout(individu):

    product_value = 1
    sum_value = 0
    for gene in individu:
        v = gene['value']
        if gene['group'] == 'product':
            product_value *= v
        elif gene['group'] == 'sum':
            sum_value += v
    cost = abs(product_value - 360) + abs(sum_value - 36)
    return cost


def crossover(parent1, parent2):

    point_coupure = 5
    enfant = []
    for i in range(10):
        if i < point_coupure:
            gene = parent1[i].copy()
        else:
            gene = parent2[i].copy()
        enfant.append(gene)

    # Correction si la répartition des groupes n'est pas respectée
    prod_count = sum(1 for gene in enfant if gene['group'] == 'product')
    if prod_count != 5:
        if prod_count > 5:
            # trop de cartes en 'product': on en change quelques-unes en 'sum'
            indices = [i for i, gene in enumerate(enfant) if gene['group'] == 'product']
            change = random.sample(indices, prod_count - 5)
            for i in change:
                enfant[i]['group'] = 'sum'
        else:
            # trop peu de cartes en 'product': on change quelques cartes 'sum' en 'product'
            indices = [i for i, gene in enumerate(enfant) if gene['group'] == 'sum']
            change = random.sample(indices, 5 - prod_count)
            for i in change:
                enfant[i]['group'] = 'product'
    return enfant


def muter(individu, mutation_rate_color=0.1, mutation_rate_group=0.1):

    for gene in individu:
        if random.random() < mutation_rate_color:
            current_color = gene['color']
            new_colors = [c for c in COLORS if c != current_color]
            gene['color'] = random.choice(new_colors)

    if random.random() < mutation_rate_group:
        prod_indices = [i for i, gene in enumerate(individu) if gene['group'] == 'product']
        sum_indices = [i for i, gene in enumerate(individu) if gene['group'] == 'sum']
        if prod_indices and sum_indices:
            i = random.choice(prod_indices)
            j = random.choice(sum_indices)
            individu[i]['group'], individu[j]['group'] = individu[j]['group'], individu[i]['group']

    return individu


def tournois(population, fitnesses, k=2):

    selected = random.sample(list(zip(population, fitnesses)), k)
    selected.sort(key=lambda x: x[1])
    return selected[0][0]


def select_parents(population, fitnesses):

    parent1 = tournois(population, fitnesses)
    parent2 = tournois(population, fitnesses)
    return parent1, parent2


def genetic_algorithm(pop_size=99, generations=5555):

    population = [create_individu() for _ in range(pop_size)]
    best = None
    best_cost = math.inf

    for gen in range(generations):
        fitnesses = [evaluer_cout(ind) for ind in population]

        for ind, cost in zip(population, fitnesses):
            if cost < best_cost:
                best = ind
                best_cost = cost

        if best_cost == 0:
            print(f"Solution trouvée à la génération {gen} avec un coût de {best_cost}.")
            return best

        new_population = []
        while len(new_population) < pop_size:
            parent1, parent2 = select_parents(population, fitnesses)
            enfant = crossover(parent1, parent2)
            enfant = muter(enfant)
            new_population.append(enfant)
        population = new_population


        print(f"Génération {gen}, meilleur coût jusqu'à présent: {best_cost}")

    print("Aucune solution parfaite n'a été trouvée.")
    return best


def print_individu(individu):

    prod_values = [gene['value'] for gene in individu if gene['group'] == 'product']
    sum_values = [gene['value'] for gene in individu if gene['group'] == 'sum']

    product_result = math.prod(prod_values)
    sum_result = sum(sum_values)

    print("Groupe 'product' :", prod_values, "Produit =", product_result)
    print("Groupe 'sum'     :", sum_values, "Somme =", sum_result)
    print("Détails de l'individu :")
    for gene in individu:
        print(f"Valeur : {gene['value']:2} | Couleur : {gene['color']} | Groupe : {gene['group']}")


best_solution = genetic_algorithm(pop_size=200, generations=5000)
print("\nmeilleure solution trouvée :")
print_individu(best_solution)
