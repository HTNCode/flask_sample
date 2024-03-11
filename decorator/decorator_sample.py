def outer(func):
    def inner(*a, **b):
        print("before")
        func(*a, **b)
        print("after")
    return inner

nums = (10,20,30,40,50)

@outer
def show_sum(nums):
    sum = 0
    for num in nums:
        sum += num
    print(sum)

users = {"山田": 20, "田中": 30, "佐藤": 40}
@outer
def show_info(users):
    for name, age in users.items():
        print(f"名前: {name}, 年齢: {age}歳")

show_sum(nums)
show_info(users)
