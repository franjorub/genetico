from utils.files import delete_linebreak


class Fitness:
    def __init__(self):
        self.covar = self.load_covar()
        self.performances = self.load_performances()

    def load_covar(self):
        f = open('covar.txt', 'r')
        lines = f.readlines()
        f.close()

        lines = list(map(delete_linebreak, lines))

        covar = []
        for raw_line in lines:
            split_line = raw_line.strip().split(',')
            nums_ls = [float(x) for x in split_line]
            covar.append(nums_ls)

        return covar

    def load_performances(self):
        f = open('performance.txt', 'r')
        lines = f.readlines()
        f.close()

        def delete_linebreaks(s):
            return float(s[:len(s) - 1])

        performances = list(map(delete_linebreaks, lines))

        return performances

    def calculate_min_risk(self, chromosome):
        min_risk = 0
        genes = chromosome.split(',')

        for index_i, gen_i in enumerate(genes):
            for index_j, gen_j in enumerate(genes):
                min_risk += (float(gen_i) * float(gen_j) * self.covar[index_i][index_j])

        return min_risk

    def calculate_max_performance(self, chromosome):
        genes = chromosome.split(',')
        max_performance = 0

        for index, gen in enumerate(genes):
            max_performance += (float(gen) * self.performances[int(index)])

        return max_performance

    def calculate_fitness(self, chromosome):
        p = self.calculate_max_performance(chromosome=chromosome)
        r = self.calculate_min_risk(chromosome=chromosome)

        return p / r
