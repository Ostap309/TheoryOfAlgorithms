houses_coords = sorted(map(int, input().split()))
coverage_i = 0
radius = 4
answer = []
while coverage_i < len(houses_coords):
    pos = houses_coords[coverage_i:][0] + radius
    answer.append(pos)
    while coverage_i < len(houses_coords) and houses_coords[coverage_i] <= pos + radius:
        coverage_i += 1

print(len(answer))
print(*answer)
