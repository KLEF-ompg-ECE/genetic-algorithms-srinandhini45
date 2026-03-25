import random
import matplotlib.pyplot as plt
import os

# =============================================================================
# PROBLEM DATA
# =============================================================================

ITEMS = [
    ("Water bottle", 2.0, 9),
    ("First aid kit", 1.5, 10),
    ("Tent", 4.0, 10),
    ("Sleeping bag", 3.0, 9),
    ("Torch", 0.5, 6),
    ("Energy bars (x6)", 1.0, 7),
    ("Rain jacket", 1.0, 8),
    ("Map & compass", 0.3, 7),
    ("Camera", 1.2, 5),
    ("Extra clothes", 2.0, 4),
    ("Cooking stove", 1.5, 6),
    ("Rope (10 m)", 2.5, 5),
    ("Sunscreen", 0.3, 4),
    ("Trekking poles", 1.5, 5),
    ("Power bank", 0.8, 6),
]

NUM_ITEMS = len(ITEMS)
MAX_WEIGHT = 15.0

WEIGHTS = [item[1] for item in ITEMS]
VALUES = [item[2] for item in ITEMS]
NAMES = [item[0] for item in ITEMS]

# =============================================================================
# FITNESS FUNCTION
# =============================================================================

def fitness(chromosome):
    total_weight = sum(WEIGHTS[i] for i in range(NUM_ITEMS) if chromosome[i] == 1)
    total_value = sum(VALUES[i] for i in range(NUM_ITEMS) if chromosome[i] == 1)
    if total_weight > MAX_WEIGHT:
        return 0
    return total_value

# =============================================================================
# GA OPERATORS
# =============================================================================

def tournament_select(population, fitnesses, k=3):
    candidates = random.sample(range(len(population)), k)
    winner = max(candidates, key=lambda i: fitnesses[i])
    return population[winner][:]

def crossover(p1, p2, rate=0.8):
    if random.random() > rate:
        return p1[:]
    cut = random.randint(1, NUM_ITEMS - 1)
    return p1[:cut] + p2[cut:]

def mutate(chromosome, rate):
    result = chromosome[:]
    for i in range(NUM_ITEMS):
        if random.random() < rate:
            result[i] = 1 - result[i]
    return result

# =============================================================================
# GENETIC ALGORITHM
# =============================================================================

def run_ga(
    population_size=20,
    generations=50,
    crossover_rate=0.8,
    mutation_rate=0.05,
    tournament_size=3,
    seed=42,
):
    random.seed(seed)

    population = [
        [random.randint(0, 1) for _ in range(NUM_ITEMS)]
        for _ in range(population_size)
    ]

    best_chromosome = None
    best_value = -1
    value_log = []

    for _ in range(generations):
        fitnesses = [fitness(c) for c in population]

        gen_best_i = max(range(population_size), key=lambda i: fitnesses[i])
        if fitnesses[gen_best_i] > best_value:
            best_value = fitnesses[gen_best_i]
            best_chromosome = population[gen_best_i][:]

        value_log.append(best_value)

        next_gen = [best_chromosome[:]]

        while len(next_gen) < population_size:
            p1 = tournament_select(population, fitnesses, tournament_size)
            p2 = tournament_select(population, fitnesses, tournament_size)
            child = crossover(p1, p2, crossover_rate)
            child = mutate(child, mutation_rate)
            next_gen.append(child)

        population = next_gen

    return best_chromosome, best_value, value_log

# =============================================================================
# OUTPUT HELPERS
# =============================================================================

def print_solution(chromosome):
    total_weight = sum(WEIGHTS[i] for i in range(NUM_ITEMS) if chromosome[i] == 1)
    total_value = sum(VALUES[i] for i in range(NUM_ITEMS) if chromosome[i] == 1)
    packed = [NAMES[i] for i in range(NUM_ITEMS) if chromosome[i] == 1]

    print("\nBest Packing List")
    print("-" * 30)
    for item in packed:
        print(f" + {item}")
    print("-" * 30)
    print(f"Weight: {total_weight:.1f}/{MAX_WEIGHT}")
    print(f"Value : {total_value}")

def save_plot(value_log, filename, title):
    os.makedirs("plots", exist_ok=True)

    plt.figure(figsize=(8, 4))
    plt.plot(value_log, marker='o')
    plt.title(title)
    plt.xlabel("Generation")
    plt.ylabel("Best Value")
    plt.grid()

    plt.savefig(filename)
    print(f"✅ Saved plot: {filename}")

    plt.show()  # 👈 display graph
    plt.close()

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":

    # EXPERIMENT 1
    print("=" * 48)
    print("EXPERIMENT 1 - Baseline")
    print("=" * 48)

    best_chr, best_val, val_log = run_ga(mutation_rate=0.05)
    print_solution(best_chr)
    print(f"Final best value: {best_val}")
    save_plot(val_log, "plots/experiment_1.png", "Baseline")

    # EXPERIMENT 2a
    print("=" * 48)
    print("EXPERIMENT 2a - mutation_rate = 0.01")
    print("=" * 48)

    chr2, val2, vl2 = run_ga(mutation_rate=0.01)
    print_solution(chr2)
    print(f"Final best value: {val2}")
    save_plot(vl2, "plots/experiment_2a.png", "Mutation 0.01")

    # EXPERIMENT 2b
    print("=" * 48)
    print("EXPERIMENT 2b - mutation_rate = 0.05")
    print("=" * 48)

    chr3, val3, vl3 = run_ga(mutation_rate=0.05)
    print_solution(chr3)
    print(f"Final best value: {val3}")
    save_plot(vl3, "plots/experiment_2b.png", "Mutation 0.05")

    # EXPERIMENT 2c
    print("=" * 48)
    print("EXPERIMENT 2c - mutation_rate = 0.30")
    print("=" * 48)

    chr4, val4, vl4 = run_ga(mutation_rate=0.30)
    print_solution(chr4)
    print(f"Final best value: {val4}")
    save_plot(vl4, "plots/experiment_2c.png", "Mutation 0.30")