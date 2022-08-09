from population import Population

# Utils
from utils.population import generate_random_population
from utils.files import generate_csv


if __name__ == '__main__':

    results = []

    for i in range(30):
        generate_random_population(220)
        population = Population()

        for _ in range(100):
            population.genetic_algorithm()

        best_chromosome, fitness, performance, risk = population.get_best_chromosome()

        results.append(
            [i + 1, *best_chromosome, fitness, performance, risk]
        )

    generate_csv(results)
