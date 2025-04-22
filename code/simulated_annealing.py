import csv
import argparse
import random
import math
import sys

T_init = 0.0
T_fin = 0.0
decay_k = 0.0
decay_func = int(0)
N_cities = int(0)
matrix = []

def process_csv(csv_path):
    global N_cities
    # Read the CSV file and build the matrix
    try:
        with open(csv_path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                matrix.append([int(value) for value in row])
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return
    N_cities = int(len(matrix[0]))
    # Print the matrix and the other parameters
    # print(f"Matrix ({N_cities}x{N_cities}):")
    # for row in matrix:
    #     print(row)
    # print("\nParameters:")
    # print(f"T_init: {T_init}")
    # print(f"T_fin: {T_fin}")
    # print(f"decay_k: {decay_k}")
    # print(f"decay_func: {decay_func}")

def calculate_cost(route):
    # Calculate the cost of the given route based on the matrix
    cost = 0
    for i in range(N_cities - 1):
        cost += matrix[route[i]][route[i + 1]]
    # Add the cost to return to the starting city
    cost += matrix[route[-1]][route[0]]
    return cost

def decay(steps):
    if decay_func == 0: # exponential decay
        return T_init * math.exp(-steps / decay_k)
    elif decay_func == 1: # linear decay
        return T_init - (decay_k * steps)
    elif decay_func == 2: # quadratic decay
        return T_init - (decay_k * (steps ** 2))
    else:
        print("Invalid decay function. Using exponential decay by default.")
        return T_init * math.exp(-steps / decay_k)

def random_swap(route):
    # Randomly swap two cities in the route
    new_route = route.copy()
    i, j = random.sample(range(N_cities), 2)
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route

def solve_execution():
    # Initial state
    current_route = []
    steps = 0
    T_curr = T_init
    for i in range(N_cities):
        current_route.append(i)
    random.shuffle(current_route)
    while(1):
        steps += 1
        T_curr = decay(steps)
        if T_curr <= T_fin:
            return calculate_cost(current_route), steps
        candidate_route = random_swap(current_route)
        cost_diff = calculate_cost(current_route) - calculate_cost(candidate_route)
        if cost_diff > 0:
            current_route = candidate_route
        else:
            prob = math.exp(cost_diff / T_curr)
            if random.random() < prob:
                current_route = candidate_route
    return -1

def append_to_csv_description(description):
    with open("output/simulated_annealing.csv", "a", newline='') as f:
        f.write('\n' + description)

def append_to_csv_value(value):
    with open("output/simulated_annealing.csv", "a", newline='') as f:
        f.write(';' + value)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a CSV file and parameters.")
    parser.add_argument("T_init", type=float, help="First parameter (float)")
    parser.add_argument("T_fin", type=float, help="Second parameter (float)")
    parser.add_argument("decay_k", type=float, help="Third parameter (float)")
    parser.add_argument("decay_func", type=int, help="Fourth parameter (int)")
    parser.add_argument("n_executions", type=int, help="Fifth parameter (int)")
    parser.add_argument("csv_path", type=str, help="Path to the CSV file")

    args = parser.parse_args()

    T_init = args.T_init
    T_fin = args.T_fin
    decay_k = args.decay_k
    decay_func = args.decay_func
    n_executions = args.n_executions

    process_csv(args.csv_path)
    append_to_csv_description("T_init = " + str(T_init) + " T_fin = " + str(T_fin) + " decay_k = " + str(decay_k) + " decay_func = " + str(decay_func) + " n_executions = " + str(args.n_executions) + " input = " + args.csv_path)

    for i in range(n_executions):
        cost, steps = solve_execution()
        append_to_csv_value(str(cost))
        print(f"Execution {i + 1}: Cost = {cost}")

    append_to_csv_value("steps:" + str(steps))
