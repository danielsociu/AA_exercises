import math
import random


class Polinom:
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



    def __init__(self, coef_1, coef_2, coef_3, inf_domain, sup_domain):
        """
        Constructor for a function that is a polynomial of degree 2
        """
        self.coef_1 = coef_1
        self.coef_2 = coef_2
        self.coef_3 = coef_3
        self.inf_domain = inf_domain
        self.sup_domain = sup_domain
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
            print ('{}: {} x = {} f = {}'.format(
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
            print ("Initial generated population:")
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
            print ()
        return population

    def __population_selection_probabilities__(self, population, population_size, show = 1):
        """
        Generates the probabilities for all the
        chromosomes in the population to be selected
        """
        sum_f = 0.0
        probabilities = []
        if show:
            print ("Selection probabilities")
        for data in population:
            sum_f += data["f_value"]
        for i, data in enumerate(population):
            probabilities.append(data["f_value"] / sum_f)
            if show:
                print ("Chromosome {} with probability: {}".format(
                    str(i + 1).rjust(math.ceil(math.log(population_size, 10))), 
                    probabilities[i]
                    ))
        if show:
            print ()
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
            selected_chromosomes.append(population[j])
            
            if show:
                print ('u = {} selectam cromozomul {}'.format(
                    str(runif)[:15],
                    str(j + 1).rjust(math.ceil(math.log(population_size, 10)))
                    ))
        if show:
            print()
        return selected_chromosomes

    def __do_crossover__(self, population, population_size, pc, chromosome_length, show = 1):
        part_chromosomes = []
        for i in range(population_size):
            runif = random.random()
            if runif < pc:
                part_chromosomes.append(i)
            if show:
                if runif < pc:
                    print ('{}: {} u = {} < {} participates'.format(
                        str(i + 1).rjust(math.ceil(math.log(population_size, 10))),
                        ''.join(map(str, population[i]['chromosome'])),
                        str(runif)[:15],
                        pc
                        ))
                else:
                    print ("{}: {} u = {}".format(
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

            chromosome_1 = population[part_chromosomes[i + 1]]['chromosome'][:break_point] +\
                    population[part_chromosomes[i]]['chromosome'][break_point:]

            chromosome_2 = population[part_chromosomes[i]]['chromosome'][:break_point] +\
                    population[part_chromosomes[i + 1]]['chromosome'][break_point:]

            x_1 = self.__float_converter__(chromosome_1)
            x_2 = self.__float_converter__(chromosome_2)
            f_1 = self.coef_1 * math.pow(x_1, 2) + self.coef_2 * x_1 + self.coef_3
            f_2 = self.coef_1 * math.pow(x_2, 2) + self.coef_2 * x_2 + self.coef_3

            if show:
                print ("Crossover between chromosome {} and {}".format(
                    part_chromosomes[i],
                    part_chromosomes[i + 1]
                    ))
                print (''.join(map(str, population[part_chromosomes[i]]['chromosome'])),
                        ''.join(map(str, population[part_chromosomes[i + 1]]['chromosome'])),
                        "at:", break_point
                    )
                print ("Outcome:", 
                        ''.join(map(str, chromosome_1)),
                        ''.join(map(str, chromosome_2))
                    )
            population[part_chromosomes[i]] = {
                    'chromosome': chromosome_1,
                    'x_value': x_1,
                    'f_value': f_1
                    }
            population[part_chromosomes[i + 1]] = {
                    'chromosome': chromosome_2,
                    'x_value': x_2,
                    'f_value': f_2
                    }
        if show:
            print()
        return population

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
            print ("Intervals of selection:")
            print (' '.join(map(str, selection_intervals)))

        # Selecting chromosomes
        selected_chromosomes = self.__select_chromosomes__(
                selection_intervals = selection_intervals,
                population = population,
                population_size = self.population_size,
                show = show
            )
        if show:
            print("After selection:")
            self.__output_population__(selected_chromosomes, self.population_size)
            print()

        crossed_population = self.__do_crossover__(
                population = population,
                population_size = self.population_size,
                pc = self.pc,
                chromosome_length = self.chromosome_length,
                show = show
            )

        if show:
            print("After crossover:")
            self.__output_population__(crossed_population, self.population_size)
            print()




        # for i in range(generations):
        #     selection_probabilities = self.__population_selection_probabilities__(
        #             population = population,
        #             population_size = self.population_size,
        #             show = show
        #         )
        #     selection_intervals 

        #     if i > 0:
        #         show = False




def main():
    polinom = Polinom(-1, 1, 2, -1, 2)
    polinom.find_maximum(20, 6, 0.25, 0.01, 50)

if __name__=="__main__":
    main()


