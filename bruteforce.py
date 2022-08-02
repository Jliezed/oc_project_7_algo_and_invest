import itertools
import pandas
import timeit
from guppy import hpy
import numpy as np

# Read the dataset
original_dataset = pandas.read_csv("./data/data.csv", delimiter=",")

# Convert the dataset to dict
dataset = original_dataset.to_dict(orient="records")

# Define Constants
MAX_SPEND = 500


def calculate_profit(dataset, max_spend):
    all_combinaisons = []
    # Iterate through dataset length
    for i in range(1, len(dataset) + 1):
        # Iterate through combinaison
        for comb in itertools.combinations(dataset, i):

            total_profit = 0
            total_cost = 0
            actions = []
            # For each combinaison, define list of actions, total cost & total profit
            for item in comb:
                actions.append(item["name"])
                total_cost += item["price"]
                total_profit += (item["profit"]/100 * item["price"])
            # If total cost under max limit then add it to list of final combinaisons
            if total_cost <= max_spend:
                new_entry = (actions, total_cost, total_profit)
                all_combinaisons.append(new_entry)

    sorted_combinaisons = sorted(all_combinaisons, key=lambda x: x[2], reverse=True)

    return all_combinaisons, print(f"Liste d'actions: {sorted_combinaisons[0][0]} \n"
              f"Coût : {sorted_combinaisons[0][1]}\n"
              f"Profit: {sorted_combinaisons[0][2]}\n")


# Calculate time of execution
start_time = timeit.default_timer()
calculate_profit(dataset, MAX_SPEND)
print("The execution time is :", timeit.default_timer() - start_time, "sec")


# Calculate space used
heap = hpy()

print("Heap Status At Starting : ")
heap_status1 = heap.heap()
print("Heap Size : ", heap_status1.size, " bytes\n")
print(heap_status1)


heap.setref()

print("\nHeap Status After Setting Reference Point : ")
heap_status2 = heap.heap()
print("Heap Size : ", heap_status2.size, " bytes\n")
print(heap_status2)

a = [i for i in range(1000)]
b = "A"
c = np.random.randint(1,100, (1000,))

print("\nHeap Status After Creating Few Objects : ")
heap_status3 = heap.heap()
print("Heap Size : ", heap_status3.size, " bytes\n")
print(heap_status3)

print("\nMemory Usage After Creation Of Objects : ", heap_status3.size - heap_status2.size, " bytes")

