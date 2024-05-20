import requests
from random import randint

org_unique_numbers = []
rand_unique_numbers = []
for i in range(20):
    url = "https://www.random.org/integers/?num=1000&min=1&max=100000&col=1&base=10&format=plain&rnd=new"

    response = requests.get(url)
    nums = list(map(int, response.text.strip().split('\n')))
    rand_nums = [randint(1, 100000) for _ in range(1000)]

# for i in range(500):
#     print(f"Random.org: {nums[i]}, randint: {rand_nums[i]}")

    print("random.org average", sum(nums) / 1000)
    print("randint average", sum(rand_nums) / 1000)

    print("unique numbers from random.org", len(set(nums)))
    print("unique numbers from randint", len(set(rand_nums)))
    org_unique_numbers.append(len(set(nums)))
    rand_unique_numbers.append(len(set(rand_nums)))

print("Average unique numbers from random.org", sum(org_unique_numbers) / 10)
print("Average unique numbers from randint", sum(rand_unique_numbers) / 10)
