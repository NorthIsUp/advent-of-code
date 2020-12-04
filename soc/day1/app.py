#!/usr/bin/env python3
# Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

# For example, suppose your expense report contained the following:

# 1721
# 979
# 366
# 299
# 675
# 1456
# In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.

# Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply them together?
from __future__ import annotations

with open('input.txt') as numbers_strs:
    numbers = [int(_) for _ in numbers_strs.readlines() if _]

from itertools import product
from functools import reduce

def check_numbers(numbers: List[int], dims=2) -> None:
    nums = [numbers for _ in range(1, dims)]
    
    for p in product(*([numbers] * dims)):
        if reduce(int.__add__, p, 0) == 2020:
            return reduce(int.__mul__, p, 1)

    

print(check_numbers(numbers, dims=2))
print(check_numbers(numbers, dims=3))


# --- Part Two ---

# The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over from a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the same criteria.

# Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together produces the answer, 241861950.

# In your expense report, what is the product of the three entries that sum to 2020?
