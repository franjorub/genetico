from population import Population

# Utils
from utils.population import generate_random_population
from utils.files import generate_csv


if __name__ == '__main__':

    results = []
    generate_random_population(1000)
    population = Population()
    results.append(['#', 'BTC', 'USDT', 'XRP', 'BHC', 'ETH',	'EOS', 'LTC', 'BNB', 'ADA', 'Fitness', 'Performance', 'Risk'])

    for i in range(30):
        population.genetic_algorithm()
        best_chromosome, fitness, performance, risk = population.get_best_chromosome()
        results.append(
            [i+1, *best_chromosome, fitness, performance, risk]
        )

    generate_csv(results)
