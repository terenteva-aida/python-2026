# Аналитика перелетных птиц за границу

data = {
    1: [("утка", 5), ("лебедь", 5)],
    2: [("утка", 5), ("лебедь", 5)],
    3: [("гусь", 1)],
    4: [("орел", 2)],
    5: [("голубь", 6), ("лебедь", 4)],
    6: [("ласточка", 3)],
    7: [("гусь", 1)],
    10: [("орел", 2)],
    15: [("голубь", 6), ("лебедь", 4)],
    18: [("утка", 5), ("лебедь", 5)],
    22: [("утка", 5), ("лебедь", 5)],
    25: [("ласточка", 3), ("утка", 5)],
    30: [("гусь", 1)]
}

filled_data = {day: data.get(day, []) for day in range(1, 32)}
print(filled_data)

import matplotlib.pyplot as plt

# total_birds_per_day = [
    
# ]

# for day in filled_data:
#     item_as_list_of_birds = filled_data[day]
#     count_per_day = 0
#     for birds in item_as_list_of_birds:
#         count_per_day += birds[1]
    
#     print(count_per_day)
#     total_birds_per_day.append(count_per_day)

total_birds_per_day = [
    sum(count for bird, count in filled_data[day])
    for day in filled_data
]

total_ducks_last_week = [
    sum(count for bird, count in filled_data[day] if bird == "утка")
    for day in range(24, 32)
]

print("Количество уток за последнюю неделю:", total_ducks_last_week)

plt.figure()
plt.plot(range(1, 32), total_birds_per_day)
plt.title("Количество птиц по дням")
plt.xlabel("Дни")
plt.ylabel("Количество птиц")
plt.grid()

plt.figure()
plt.plot(range(24, 32), total_ducks_last_week)
plt.title("Количество уток по дням")
plt.xlabel("Дни")
plt.ylabel("Количество уток")
plt.grid()

plt.show()