import math
import random
import copy


class Polinom:
    ### output file
    f_in = None

    ### Polinom data
    coef_1 = 0
    coef_2 = 0
    coef_3 = 0

    inf_domain = 0
    sup_domain = 0

    ### Genetic algorithm data
    population_size = 10
    precision = 10
    pc = 0.25
    pm = 0.01
    generations = 10
    interval = 0
    chromosome_length = 0



    def __init__(self, coef_1, coef_2, coef_3, inf_domain, sup_domain, f_in):
        """
        Constructor for a function that is a polynomial of degree 2
        """
        self.coef_1 = coef_1
        self.coef_2 = coef_2
        self.coef_3 = coef_3
        self.inf_domain = inf_domain
        self.sup_domain = sup_domain
        self.f_in = f_in
        self.interval = (sup_domain - inf_domain) * math.pow(10, self.precision)
        self.chromosome_length = math.ceil(math.log(self.interval, 2))


    def __binary_converter__(self, x_value):
        """
        Converts a x_value to its coresponding binary value
        """
        pass

    def __float_converter__(self, bin_vector):
        """
        Converts a binary vector to its x value
        """
        number = 0
        pow_2 = 1
        for b in bin_vector[::-1]:
            if b == 1:
                number += pow_2
            pow_2 *= 2
        value = ((self.sup_domain - self.inf_domain) / (pow_2 - 1)) * number + self.inf_domain 
        return value

    def __output_population__(self, population, population_size):
        for i, data in enumerate(population):
            self.f_in.write ('{}: {} x = {} f = {}\n'.format(
                str(i + 1).rjust(math.ceil(math.log(population_size, 10))), 
                ''.join(map(str, data["chromosome"])), 
                str(data['x_value'])[:15], 
                str(data["f_value"])[:15]
                ))

    def __generate_chromosome__ (self, chromosome_length):
        """
        Generates a random chromosome of length chromosome_length
        """
        chrome = []
        for i in range(chromosome_length):
            runif = random.random()
            if (runif < 0.5):
                chrome.append(0)
            else:
                chrome.append(1)
        return chrome

    def __generate_population__ (self, population_size, chromosome_length, show = 1):
        """
        Generates population_size of chromosomes
        returns an array of dictionaries with the next values:
        {
        chromosome: [Chromosome] the array of alleles
        x_value: x equivalent from domain
        f_value: heuristic function value
        }
        """
        population = []
        if show:
            self.f_in.write ("Initial generated population:\n")
        for i in range(population_size):
            chrome = self.__generate_chromosome__(chromosome_length)
            x = self.__float_converter__(chrome)
            f = self.coef_1 * math.pow(x, 2) + self.coef_2 * x + self.coef_3
            population.append({
                'chromosome': chrome,
                'x_value': x,
                'f_value': f
                })

        if show:
            self.__output_population__(population, population_size)
            self.f_in.write ('\n')
        return population

    def __population_selection_probabilities__(self, population, population_size, show = 1):
        """
        Generates the probabilities for all the
        chromosomes in the population to be selected
        """
        sum_f = 0.0
        probabilities = []
        population_copy = []
        mini = (1<<60)
        for data in population:
            new = copy.deepcopy(data)
            population_copy.append(new)
        if show:
            self.f_in.write ("Selection probabilities:\n")
        for data in population:
            mini = min( data["f_value"], mini) 
        mini = abs(mini) + 1
        for data in population:
            sum_f += (data["f_value"] + mini)
        for i, data in enumerate(population):
            probabilities.append((data["f_value"] + mini) / sum_f)
            if show:
                self.f_in.write ("Chromosome {} with probability: {}\n".format(
                    str(i + 1).rjust(math.ceil(math.log(population_size, 10))), 
                    probabilities[i]
                    ))
        if show:
            self.f_in.write ('\n')
        return probabilities


    def __select_chromosomes__(self, selection_intervals, population, population_size, show = 1):
        """
        Selecting the chromosomes based on the selection_intervals
        """
        selected_chromosomes = []
        for i in range(population_size):
            runif = random.random()
            j = 0
            while selection_intervals[j + 1] < runif:
                j += 1
            new = copy.deepcopy(population[j])
            selected_chromosomes.append(new)
            
            if show:
                self.f_in.write ('u = {} selecting chromosome {}\n'.format(
                    str(runif)[:15],
                    str(j + 1).rjust(math.ceil(math.log(population_size, 10)))
                    ))
        if show:
            self.f_in.write("\n")
        return selected_chromosomes

    def __crossover_population__(self, population, population_size, pc, chromosome_length, show = 1):
        part_chromosomes = []
        population_copy = []
        if show:
            self.f_in.write("Probaility of crossover {}:\n".format(pc))
        for data in population:
            new = copy.deepcopy(data)
            population_copy.append(new)
        for i in range(population_size):
            runif = random.random()
            if runif < pc:
                part_chromosomes.append(i)
            if show:
                if runif < pc:
                    self.f_in.write ('{}: {} u = {} < {} participates\n'.format(
                        str(i + 1).rjust(math.ceil(math.log(population_size, 10))),
                        ''.join(map(str, population[i]['chromosome'])),
                        str(runif)[:15],
                        pc
                        ))
                else:
                    self.f_in.write ("{}: {} u = {}\n".format(
                        str(i + 1).rjust(math.ceil(math.log(population_size, 10))),
                        ''.join(map(str, population[i]['chromosome'])),
                        str(runif)[:15]
                        ))
        # Now combining the chromosomes
        # Instead of choosing 2 random elements from part_chromosomes
        # and popping (O(n)) we can instead just shuffle and iterate:
        random.shuffle(part_chromosomes)
        for i in range(0, len(part_chromosomes) - 1, 2):
            break_point = random.randint(0, chromosome_length - 1)

            chromosome_1 = population_copy[part_chromosomes[i + 1]]['chromosome'][:break_point] +\
                    population_copy[part_chromosomes[i]]['chromosome'][break_point:]

            chromosome_2 = population_copy[part_chromosomes[i]]['chromosome'][:break_point] +\
                    population_copy[part_chromosomes[i + 1]]['chromosome'][break_point:]

            x_1 = self.__float_converter__(chromosome_1)
            x_2 = self.__float_converter__(chromosome_2)
            f_1 = self.coef_1 * math.pow(x_1, 2) + self.coef_2 * x_1 + self.coef_3
            f_2 = self.coef_1 * math.pow(x_2, 2) + self.coef_2 * x_2 + self.coef_3

            if show:
                self.f_in.write ("Crossover between chromosome {} and {}\n".format(
                    part_chromosomes[i],
                    part_chromosomes[i + 1]
                    ))
                self.f_in.writelines([
                        ''.join(map(str, population_copy[part_chromosomes[i]]['chromosome'])),
                        ' ',
                        ''.join(map(str, population_copy[part_chromosomes[i + 1]]['chromosome'])),
                        " at: ", str(break_point), "\n"
                        ] )
                self.f_in.writelines (["Outcome: ", 
                        ''.join(map(str, chromosome_1)),
                        " ",
                        ''.join(map(str, chromosome_2)),
                        "\n"
                        ])
            population_copy[part_chromosomes[i]] = {
                    'chromosome': chromosome_1,
                    'x_value': x_1,
                    'f_value': f_1
                    }
            population_copy[part_chromosomes[i + 1]] = {
                    'chromosome': chromosome_2,
                    'x_value': x_2,
                    'f_value': f_2
                    }
        if show:
            self.f_in.write("\n")
        return population_copy

    def __mutate_population__(self, population, population_size, pm, chromosome_length, show):
        modified_chromosomes = []
        population_copy = []
        for data in population:
            new = copy.deepcopy(data)
            population_copy.append(new)

        for i, data in enumerate(population_copy):
            for j in range(chromosome_length):
                runif = random.random()
                changed = False
                if runif < pm:
                    data['chromosome'][j] ^= 1
                    modified_chromosomes.append(i)
                    changed = True
                if changed:
                    data['x_value'] = self.__float_converter__(data['chromosome'])
                    data['f_value'] = self.coef_1 * math.pow(data['x_value'], 2) + self.coef_2 * data['x_value'] + self.coef_3
        if show:
            self.f_in.writelines ("Probability of mutation is {}\n".format(pm))
            self.f_in.write ("The next chromosomes had their genes modififed:\n")
            for chromos in set(modified_chromosomes):
                self.f_in.write (str (chromos + 1) + '\n')
        return population_copy




    def find_maximum (self, population_size = 10, precision = 10, pc = 0.25, pm = 0.01, generations = 50, show = 1):
        """
        Find the maximum of the function with a genetic algorithm
        population_size = number of chromosomes
        precision = precision for a real interval
        pc = probability for a chromosome to be selected for crossover
        pm = probability for a chromosome for mutation
        generations = number of evolutions
        """
        # Initiliazing the data
        self.population_size = population_size
        self.precision = precision
        self.pc = pc
        self.pm = pm
        self.generations = generations
        self.interval = (self.sup_domain - self.inf_domain) * math.pow(10, self.precision)
        self.chromosome_length = math.ceil(math.log(self.interval, 2))

        # Getting initial population
        initial_population = self.__generate_population__(
                population_size = self.population_size,
                chromosome_length = self.chromosome_length,
                show = show
            )

        population = initial_population

        for i in range(generations):

            # getting the probabilities of selecting
            selection_probabilities = self.__population_selection_probabilities__(
                    population = population,
                    population_size = self.population_size,
                    show = show
                )

            # getting intervals of selecting
            selection_intervals = [0.0]
            for i in range(1, self.population_size):
                selection_intervals.append(selection_intervals[i - 1] + selection_probabilities[i - 1]) 
            selection_intervals.append(1.0)

            if show:
                self.f_in.write ("Intervals of selection:\n")
                self.f_in.write (' '.join(map(str, selection_intervals)))
                self.f_in.write ("\n")

            # Selecting chromosomes
            selected_chromosomes = self.__select_chromosomes__(
                    selection_intervals = selection_intervals,
                    population = population,
                    population_size = self.population_size,
                    show = show
                )
            if show:
                self.f_in.write("After selection:\n")
                self.__output_population__(selected_chromosomes, self.population_size)
                self.f_in.write("\n")


            crossed_population = self.__crossover_population__(
                    population = population,
                    population_size = self.population_size,
                    pc = self.pc,
                    chromosome_length = self.chromosome_length,
                    show = show
                )

            if show:
                self.f_in.write("After crossover:\n")
                self.__output_population__(crossed_population, self.population_size)
                self.f_in.write("\n")

            
            mutated_data = self.__mutate_population__(
                    population = crossed_population,
                    population_size = self.population_size,
                    pm = self.pm,
                    chromosome_length = self.chromosome_length,
                    show = show
                )
            if show:
                self.f_in.write("After mutation:\n")
                self.__output_population__(mutated_data, self.population_size)
                self.f_in.write("\n")


            if show:
                self.f_in.write ("Evolutia maximului:\n")
            maximum = -(1<<60)
            for data in mutated_data:
                maximum = max(data['f_value'], maximum)
            self.f_in.write (str(maximum) + '\n')
            
            # copying the new data for next operation
            show = 0
            population = []
            for data in mutated_data:
                new = copy.deepcopy(data)
                population.append(new)


def main():
    my_file = open ("Evolution.txt", "w")
    polinom = Polinom(
            coef_1 = 1,
            coef_2 = 1, 
            coef_3 = 2, 
            inf_domain = -10, 
            sup_domain = 0,
            f_in = my_file
        )
    polinom.find_maximum(
            population_size = 20,
            precision = 6,
            pc = 0.25,
            pm = 0.01,
            generations = 50,
            show = 1
        )


if __name__=="__main__":
    main()
