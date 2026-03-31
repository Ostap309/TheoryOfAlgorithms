import sys

content = sys.stdin.readlines()
n, m = map(int, content[0].strip().split())
A = list(map(str.split, map(str.strip, content[1:n + 1])))

trucks_pref = {truck_num: w for truck_num, w in enumerate(A)}
result = {i: '0' for i in range(n)}

warehouses_pref = {}
for truck, warehouses in trucks_pref.items():
    for warehouse in warehouses:
        if warehouse != '0':
            if warehouse not in warehouses_pref:
                warehouses_pref[warehouse] = []
            warehouses_pref[warehouse].append(truck)

for warehouse, trucks in warehouses_pref.items():
    trucks.sort(key=lambda tr: trucks_pref[tr].index(warehouse))


def stop_next_warehouse(truck):
    next_preferred_warehouse = trucks_pref[truck].pop(0)
    while next_preferred_warehouse == '0':
        next_preferred_warehouse = trucks_pref[truck].pop(0)

    if next_preferred_warehouse not in result.values():
        result[truck] = next_preferred_warehouse
        return

    old_truck = [k for k in result.keys() if result[k] == next_preferred_warehouse][0]
    if warehouses_pref[next_preferred_warehouse].index(truck) > warehouses_pref[next_preferred_warehouse].index(
            old_truck):
        result[old_truck] = '0'

        result[truck] = next_preferred_warehouse

        stop_next_warehouse(old_truck)


for truck in trucks_pref:
    while result[truck] == '0':
        stop_next_warehouse(truck)

print('\n'.join(result.values()))
