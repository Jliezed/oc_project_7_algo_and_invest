import pandas
import timeit
from guppy import hpy

# -------------------- READ FILE --------------------
filename = "data.csv"
original_dataset = pandas.read_csv("./data/" + filename, delimiter=",")

# -------------------- GET BASIC INFO --------------------
original_dataset.describe()
original_dataset.info()

# -------------------- CLEAN DATASET --------------------
dataset_new_headers = original_dataset.rename(columns={
    "name": "ACTION",
    "price": "COST",
    "profit": "PROFIT_PERCENTAGE"
})


# -------------------- ADD NEW CALCULATED COLUMN --------------------
dataset_new_headers["PROFIT_VOLUME"] = dataset_new_headers["COST"] * \
                                       (dataset_new_headers["PROFIT_PERCENTAGE"]/100)

dataset_new_headers["PROFIT_FOR_1"] = ((dataset_new_headers["PROFIT_PERCENTAGE"]/100) \
                                      * dataset_new_headers["COST"]) / \
                                      dataset_new_headers["COST"]


dataset = dataset_new_headers
print(dataset)
# -------------------- SORT DATASET BY --------------------
data_sort_by_profit_percentage = dataset.sort_values(by=["PROFIT_PERCENTAGE"],
                                                ascending=False,
                                                na_position="first")

data_sort_by_profit_volume = dataset.sort_values(by=["PROFIT_VOLUME"],
                                            ascending=False,
                                            na_position="first")

data_sort_by_cost_asc = dataset.sort_values(by=["COST"],
                                       ascending=True,
                                       na_position="first")

data_sort_by_cost_desc = dataset.sort_values(by=["COST"],
                                       ascending=False,
                                       na_position="first")

data_sort_by_profit_for_1 = dataset.sort_values(by=["PROFIT_FOR_1"],
                                       ascending=False,
                                       na_position="first")


def calculateProfit(dataset, max_spend=500):
    total_action_cost = 0
    total_profit = 0

    for index, (action, profit) in enumerate(zip(dataset["COST"],
                               dataset["PROFIT_VOLUME"])):

        # Add cost & profit to total
        total_action_cost += action
        total_profit += profit

        # Check if total cost over max spend
        if total_action_cost > max_spend:
            total_action_cost -= action
            total_profit -= profit

    return print(f"Total Cost is: {total_action_cost} "
                 f"for a profit of"
                 f" {total_profit}")


start_time = timeit.default_timer()
calculateProfit(dataset)
calculateProfit(data_sort_by_profit_percentage)
calculateProfit(data_sort_by_profit_volume)
calculateProfit(data_sort_by_cost_asc)
calculateProfit(data_sort_by_cost_desc)
calculateProfit(data_sort_by_profit_for_1)
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

calculateProfit(dataset)
calculateProfit(data_sort_by_profit_percentage)
calculateProfit(data_sort_by_profit_volume)
calculateProfit(data_sort_by_cost_asc)
calculateProfit(data_sort_by_cost_desc)
calculateProfit(data_sort_by_profit_for_1)

print("\nHeap Status After Creating Few Objects : ")
heap_status3 = heap.heap()
print("Heap Size : ", heap_status3.size, " bytes\n")
print(heap_status3)

print("\nMemory Usage After Creation Of Objects : ",
      heap_status3.size - heap_status2.size, " bytes")