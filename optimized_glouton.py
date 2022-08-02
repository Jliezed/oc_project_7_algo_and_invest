import pandas
import timeit

# -------------------- READ FILE --------------------
original_dataset = pandas.read_csv("./data/data.csv", delimiter=";")
#print(original_dataset)

# -------------------- GET BASIC INFO --------------------
original_dataset.describe()
original_dataset.info()

# -------------------- CLEAN DATASET --------------------
dataset_new_headers = original_dataset.rename(columns={
    "name": "ACTION",
    "price": "COST",
    "profit": "PROFIT_PERCENTAGE"
})

#print(dataset_new_headers)

# -------------------- ADD NEW CALCULATED COLUMN --------------------
dataset_new_headers["PROFIT_VOLUME"] = dataset_new_headers["COST"] * \
                                       (dataset_new_headers["PROFIT_PERCENTAGE"]/100)
#print(dataset_new_headers)

dataset_new_headers["PROFIT_FOR_1"] = ((dataset_new_headers["PROFIT_PERCENTAGE"]/100) \
                                      * dataset_new_headers["COST"]) / \
                                      dataset_new_headers["COST"]


dataset = dataset_new_headers
print(dataset)
# -------------------- SORT DATASET BY --------------------
data_sort_by_profit_percentage = dataset.sort_values(by=["PROFIT_PERCENTAGE"],
                                                ascending=False,
                                                na_position="first")
#print(data_sort_by_profit_percentage)

data_sort_by_profit_volume = dataset.sort_values(by=["PROFIT_VOLUME"],
                                            ascending=False,
                                            na_position="first")
#print(data_sort_by_profit_volume)
data_sort_by_cost_asc = dataset.sort_values(by=["COST"],
                                       ascending=True,
                                       na_position="first")
#print(data_sort_by_cost_asc)
data_sort_by_cost_desc = dataset.sort_values(by=["COST"],
                                       ascending=False,
                                       na_position="first")
#print(data_sort_by_desc)
data_sort_by_profit_for_1 = dataset.sort_values(by=["PROFIT_FOR_1"],
                                       ascending=False,
                                       na_position="first")
#print(data_sort_by_profit_for_1)

# ITERATE OVER ROWS


def calculateProfit(dataset, MAX_SPEND = 500):
    total_action_cost = 0
    total_profit = 0

    for index, (action, profit) in enumerate(zip(dataset["COST"],
                               dataset["PROFIT_VOLUME"])):
        # Define previous values
        # prev_action_cost = dataset['COST'].iloc[index - 1]
        # prev_profit = dataset["PROFIT_VOLUME"].iloc[index - 1]

        # Add cost & profit to total
        total_action_cost += action
        total_profit += profit

        # Check if total cost over max spend
        if total_action_cost > MAX_SPEND:
            total_action_cost -= action
            total_profit -= profit

    return print(f"Total Cost is: {total_action_cost} "
                 f"for a profit of"
                 f" {total_profit}")


starttime = timeit.default_timer()
print("The start time is :",starttime)
calculateProfit(dataset)
calculateProfit(data_sort_by_profit_percentage)
calculateProfit(data_sort_by_profit_volume)
calculateProfit(data_sort_by_cost_asc)
calculateProfit(data_sort_by_cost_desc)
calculateProfit(data_sort_by_profit_for_1)
print("The time difference is :", timeit.default_timer() - starttime)