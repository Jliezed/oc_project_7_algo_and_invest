import pandas
import timeit
from guppy import hpy
import itertools


# Read the dataset
original_dataset = pandas.read_csv("./data/dataset2_Python+P7.csv", delimiter=",")


# Convert the dataset to list
actions_names = original_dataset.name.to_list()
actions_prices = original_dataset.price.round(0).to_list()
actions_profits = original_dataset.profit.round(0).to_list()

prices = {action: int(price) for (action, price) in itertools.zip_longest(actions_names,
                                                             actions_prices)}
profits = {action: profit/100 for (action, profit) in itertools.zip_longest(
    actions_names, actions_profits)}


actions_names = [i for i, j in prices.items()]


# Define Constants
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

    # Loop through each item and each kg in capacity
    for id_item in range(nb_of_items + 1):
        # Get item name
        item_name = actions_names[id_item - 1]
        for unit_spend in range(max_spend + 1):
            # Define some variables
            action_price = actions_prices[item_name]
            item_profit = action_price * actions_profits[item_name]
            max_value_prev_item_memo = memo[id_item-1][unit_spend]
            # Nul case
            if id_item == 0 or unit_spend == 0:
                memo[id_item][unit_spend] = 0

            # if item weight less than kg
            elif action_price <= unit_spend and action_price >0:

                # Define kg gap
                kg_gap = unit_spend - int(action_price)
                value_item_kg_gap = memo[id_item-1][kg_gap]
                # Define max value between item value + item value for kg gap and previous
                # item value in memo
                max_value = max(item_profit + value_item_kg_gap, max_value_prev_item_memo)
                # Push value in memo
                memo[id_item][unit_spend] = round(max_value, 2)

            # If item weight greater than kg
            else:
                # Define some variables
                max_value_prev_item_memo = memo[id_item - 1][unit_spend]

                # Define memo as prev item value in memo
                memo[id_item][unit_spend] = round(max_value_prev_item_memo, 2)
    return memo


def list_items_names(memo):
    length_unit = len(memo[0])-1
    reversed_actions_names = actions_names[::-1]
    reversed_memo = memo[::-1]
    column_to_check = length_unit

    items_names = []
    for (index, row) in enumerate(reversed_memo):
        last_cell = row[column_to_check]
        try:
            last_cell_next = reversed_memo[index+1][column_to_check]
        except IndexError:
            last_cell_next = None

        if last_cell != last_cell_next and last_cell_next != None:
            items_names.append(reversed_actions_names[index])
            item_price = prices[reversed_actions_names[index]]
            column_to_check -= item_price
        else:
            pass
    return items_names


# Calculate time of execution
starttime = timeit.default_timer()
print("The start itme is: ", starttime)
array = calculate_profit(actions_names, profits, prices, MAX_SPEND)

# final = list_items_names(len(actions_names), MAX_SPEND, actions_names, prices, array)
actions_list = list_items_names(array)
print(actions_list)
print(f"Maximum profit: {array[-1][-1]}")
print("The time difference is :", timeit.default_timer() - starttime)


# Calculate space used
heap = hpy()

print("Heap Status At Starting : ")
heap_status1 = heap.heap()
print("Heap Size : ", heap_status1.size, " bytes\n")
print(heap_status1)
