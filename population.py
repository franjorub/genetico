from random import randint, random, sample

# Fitness
from fitness import Fitness

# Utils
from utils.utils import decision
from utils.files import delete_linebreak


class Population:
    def __init__(self):
        self.fitness = Fitness()

        self.main_population = self.load_population()
        self.population_fitness = self.calculate_fitness(population=self.main_population)
        self.population_length = len(self.main_population)

        # Percentages
        self.cross_probability = 0.80
        self.mutation_probability = 0.025
        # TODO: change to 0.1 for 220 input-population - 0.25 test for 10
        self.selection_percentage = 0.1

    def load_population(self):
        file = open('input-population.txt')
        lines = file.readlines()
        file.close()

        p = list(map(delete_linebreak, lines))

        return p

    def calculate_fitness(self, population):
        calc = []

        for chromosome in population:
            f = self.fitness.calculate_fitness(chromosome=chromosome)
            calc.append(f)

        return calc

    def normalize_chromosome(self, chromosome):
        sum_chromosome = sum(chromosome)
        normalized_chromosome = [float(gen / sum_chromosome) for gen in chromosome]

        return normalized_chromosome

    def genetic_algorithm(self):
        # First Step: Selection
        selected_chromosomes = self.selection()

        # Second Step: Cross
        for index, paired_chromosomes in enumerate(selected_chromosomes):
            if decision(self.cross_probability):
                selected_chromosomes[index] = self.cross(chromosomes=paired_chromosomes)

        # Third Step: Mutation
        for i, paired_chromosomes in enumerate(selected_chromosomes):
            for j, chromosome in enumerate(paired_chromosomes):
                if decision(self.mutation_probability):
                    selected_chromosomes[i][j] = self.mutation(chromosome=chromosome)

        # Fourth Step: Substitution
        for index, paired_chromosomes in enumerate(selected_chromosomes):
            self.substitution(
                crossed_chromosomes=paired_chromosomes
            )

    def selection(self):
        qty = int(self.population_length * self.selection_percentage)

        tournament = []
        remaining_population = [*self.population_fitness]

        while len(remaining_population) >= qty:
            sample_pop = sample(remaining_population, qty)
            tournament.append(sample_pop)

            for element in sample_pop:
                remaining_population.remove(element)

        best_chromosomes = []

        for x in tournament:
            best_fitness = max(x)
            best_fitness_position = self.population_fitness.index(best_fitness)
            best_chromosomes.append(self.main_population[best_fitness_position])

        paired_chromosomes = []
        while len(best_chromosomes) > 0:
            sample_pop = sample(best_chromosomes, 2)

            parsed_chromosome_a = [float(gen) for gen in sample_pop[0].split(',')]
            parsed_chromosome_b = [float(gen) for gen in sample_pop[1].split(',')]

            paired_chromosomes = [*paired_chromosomes, [parsed_chromosome_a, parsed_chromosome_b]]

            for element in sample_pop:
                best_chromosomes.remove(element)

        return paired_chromosomes

    def cross(self, chromosomes):
        cross_position = randint(1, 9)

        split_a = chromosomes[0][:cross_position]
        split_b = chromosomes[0][cross_position:]

        split_c = chromosomes[1][:cross_position]
        split_d = chromosomes[1][cross_position:]

        crossed_chromosome_a = [*split_a, *split_d]
        crossed_chromosome_b = [*split_c, *split_b]

        crossed_chromosome_a = self.normalize_chromosome(chromosome=crossed_chromosome_a)
        crossed_chromosome_b = self.normalize_chromosome(chromosome=crossed_chromosome_b)

        crossed_chromosomes = [crossed_chromosome_a, crossed_chromosome_b]

        return crossed_chromosomes

    def mutation(self, chromosome):
        random_gen = randint(0, 8)
        new_gen = random()

        chromosome[random_gen] = new_gen

        mutated_chromosome = self.normalize_chromosome(chromosome=chromosome)

        return mutated_chromosome

    def substitution(self, crossed_chromosomes):
        population = [','.join(list(map(str, chromosome))) for chromosome in crossed_chromosomes]

        calc_fitness = self.calculate_fitness(population=population)

        better_chromosome_index = calc_fitness.index(max(calc_fitness))
        worst_chromosome_in_population = self.population_fitness.index(min(self.population_fitness))

        self.main_population[worst_chromosome_in_population] = population[better_chromosome_index]
        self.population_fitness[worst_chromosome_in_population] = calc_fitness[better_chromosome_index]

    def get_best_chromosome(self):
        index = self.population_fitness.index(max(self.population_fitness))
        best_chromosome = self.main_population[index]

        performance = self.fitness.calculate_max_performance(best_chromosome)
        risk = self.fitness.calculate_min_risk(best_chromosome)
        best_chromosome = [float(gen) for gen in best_chromosome.split(',')]
        fitness = self.population_fitness[index]

        return best_chromosome, fitness, performance, risk
