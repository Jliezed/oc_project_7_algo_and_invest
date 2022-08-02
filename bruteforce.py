import itertools
import pandas
import timeit
from guppy import hpy

# Read the dataset
original_dataset = pandas.read_csv("./data/data.csv", delimiter=",")

# Convert the dataset to dict
dataset = original_dataset.to_dict(orient="records")

# Define Constants
MAX_SPEND = 20


def calculate_profit(dataset, max_spend):
    all_combinaisons = []
    for i in range(1, len(dataset) + 1):
        for comb in itertools.combinations(dataset, i):
            total_profit = 0
            total_cost = 0
            actions = []
            for item in comb:
                actions.append(item["name"])
                total_cost += item["price"]
                total_profit += (item["profit"]/100 * item["price"])
            if total_cost <= max_spend:
                new_entry = (actions, total_cost, total_profit)
                all_combinaisons.append(new_entry)

    sorted_combinaisons = sorted(all_combinaisons, key=lambda x: x[2], reverse=True)

    for i in sorted_combinaisons[:5]:
        print(f"Liste d'actions: {i[0]} \n"
              f"Coût : {i[1]}\n"
              f"Profit: {i[2]}\n")


# Calculate time of execution
starttime = timeit.default_timer()
print("The start itme is: ", starttime)
calculate_profit(dataset, MAX_SPEND)
print("The time difference is :", timeit.default_timer() - starttime)


# Calculate space used
heap = hpy()

print("Heap Status At Starting : ")
heap_status1 = heap.heap()
print("Heap Size : ", heap_status1.size, " bytes\n")
print(heap_status1)

