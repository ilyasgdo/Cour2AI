import numpy as np
from numpy import random as rd


class EvolutionaryAlgorithm:
    def __init__(self):
        self.population_size = 5999
        self.population = []

    def generate_individual(self):
        return np.random.permutation(np.arange(1, 11)).tolist()

    def evaluate_cost(self, individu):
        cost1 = abs(360 - np.prod(individu))
        cost2 = abs(36 - sum(individu))
        return (cost1 + cost2) / 2

    def crossover(self, parent1, parent2):
        child = parent1.copy()
        i = rd.randint(len(parent1))
        j = rd.randint(i + 1, len(parent1))
        segment = parent2[i:j].copy()
        while not any(s in child for s in segment):
            if rd.random() < 0.5:
                k = rd.randint(len(parent1))
                l = rd.randint(k + 1, len(parent1))
                segment = parent2[k:l].copy()
        return [child[:i] + list(segment) + child[j:],
                [x for x in parent1 if x not in segment] + [y for y in parent2 if y not in child]]

    def mutation(self, individual):
        mutated = individual.copy()
        i, j = rd.randint(0, len(individual)), rd.randint(i + 1, len(individual))
        while any(x == mutated[i] for x in mutated[j:]):
            i, j = rd.randint(0, len(individual)), rd.randint(i + 1, len(individual))
        mutated[i], mutated[j] = mutated[j], mutated[i]
        return mutated

    def selection(self):
        fitnesses = [self.evaluate_cost(x) for x in self.population]
        total_fitness = sum(fitnesses)
        probabilities = [f / total_fitness for f in fitnesses]
        parents = rd.choices(self.population, weights=probabilities, k=self.population_size // 2)
        children = []

        for i in range(0, len(parents), 2):
            if i + 1 >= len(parents):
                break
            parent1 = parents[i]
            parent2 = parents[i + 1]

            child1, child2 = self.crossover(parent1, parent2)
            children.extend([child1.copy(), child2.copy()])

        self.population = self.mutation(children) + [self.generate_individual() for _ in
                                                     range(self.population_size - len(children))]

    def run_algorithm(self):
        best = []
        history = []
        population = [[rd.permutation(10).tolist() for _ in range(5999)]]

        while True:
            current_population = []
            for individual in population[-1]:
                fitness = self.evaluate_cost(individual)
                if fitness < max([self.evaluate_cost(x) for x in best]):
                    best.append([individual.copy(), fitness])

            average_fitness = sum([self.evaluate_cost(b[0]) for b in best]) / len(best)
            history.append(average_fitness)

            if len(history) > 1 and abs(history[-1] - history[-2]) < 0.0001:
                break

            self.population = population[-1]
            population.append(self.selection())
            print("Average fitness: ", average_fitness)
            print("Population size: ", len(population))
            print(f"")

        return best