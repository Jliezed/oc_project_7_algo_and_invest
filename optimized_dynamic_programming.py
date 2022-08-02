import pandas
import timeit
from guppy import hpy
import numpy as np
import itertools


# Read the dataset
dataset_path = "./data/data.csv"
original_dataset = pandas.read_csv(dataset_path, delimiter=",")


# Convert the dataset to list
actions_names = original_dataset.name.to_list()
actions_prices = original_dataset.price.to_list()
actions_profits = original_dataset.profit.to_list()


# Define variables used for calculate profit functions
prices = {action: price for (action, price) in itertools.zip_longest(
    actions_names, actions_prices)}
profits = {action: profit/100 for (action, profit) in itertools.zip_longest(
    actions_names, actions_profits)}
actions_names = [i for i, j in prices.items()]

# Define Constant
MAX_SPEND = 500


# Function to calculate max profit
def calculate_profit(actions_names, actions_profits, actions_prices, max_spend):
    nb_of_items = len(actions_names)

    # Create the memo array
    memo = []
    for action_price in range(len(actions_prices) + 1):
        row = []
        for unit_spend in range(max_spend + 1):
            row.append(0)
        memo.append(row)

    # Loop through each item and each unit of max spend
    for id_item in range(nb_of_items + 1):
        # Get item name
        item_name = actions_names[id_item - 1]

        for unit_spend in range(max_spend + 1):
            # Define some variables
            action_price = actions_prices[item_name]
            action_profit = action_price * actions_profits[item_name]
            max_value_prev_item_memo = memo[id_item-1][unit_spend]
            
            # Nul case
            if id_item == 0 or unit_spend == 0:
                memo[id_item][unit_spend] = 0

            # if action price above 0 and under unit spend
            elif action_price > 0 and action_price <= unit_spend  :

                # Define unit gap
                unit_gap = unit_spend - int(action_price)
                profit_action_unit_gap = memo[id_item-1][unit_gap]
                # Define max value between action profit + action profit for unit gap
                # and previous action profit in memo
                max_value = max(action_profit + profit_action_unit_gap, max_value_prev_item_memo)
                # Push value in memo
                memo[id_item][unit_spend] = round(max_value, 2)

            # If item weight greater than kg
            else:
                # Define max value of prev item in memo
                max_value_prev_item_memo = memo[id_item - 1][unit_spend]

                # Define memo equal to prev item value in memo
                memo[id_item][unit_spend] = round(max_value_prev_item_memo, 2)
    return memo


def list_items_names_cost(memo):
    # Define some variables
    units_length = len(memo[0])-1
    reversed_actions_names = actions_names[::-1]
    reversed_memo = memo[::-1]
    column_to_check = units_length

    items_names = []
    # Iterate through reversed memo
    for (index, row) in enumerate(reversed_memo):
        # Get value of last cell and last cell of next row
        last_cell = row[column_to_check]
        try:
            last_cell_next_row = reversed_memo[index+1][column_to_check]
        except IndexError:
            last_cell_next_row = None

        # If last cell value is different to the last cell of next row
        if last_cell != last_cell_next_row and last_cell_next_row != None:
            # Then add it to final list
            items_names.append(reversed_actions_names[index])
            # Define new value of column to check
            item_price = prices[reversed_actions_names[index]]
            column_to_check -= item_price
        else:
            pass

    # Get total cost
    total_cost = 0
    for action in items_names:
        total_cost += prices[action]

    return print(f"List of Actions: {items_names[::-1]}\n"
                 f"Cost: {total_cost}")


# Calculate time of execution
start_time = timeit.default_timer()
array = calculate_profit(actions_names, profits, prices, MAX_SPEND)

# final = list_items_names(len(actions_names), MAX_SPEND, actions_names, prices, array)
actions_list = list_items_names_cost(array)
print(f"Profit: {array[-1][-1]}")
print("\nThe execution time is :", timeit.default_timer() - start_time, "sec\n")


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
