from help_function import calculate_cost
from datetime import date
DATA = [(1, '2015/11/20', 1000, 10), (1, '2015/11/21', 1000, 12), (1, '2015/11/24', 3000, 16),
        (1, '2015/11/24', -1000, 17), (1, '2015/11/25', -1000, 15), (1, '2015/11/26', -3000, 14)]

# print(calculate_cost(DATA))
# calculate_cost(DATA)
assert calculate_cost(DATA)[-2] == (date(2015, 11, 25), 3000, 14.75, 750, 6250)
print("passed")