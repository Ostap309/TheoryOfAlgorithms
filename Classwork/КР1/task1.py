import sys

content = sys.stdin.readlines()
# content = ['8 9\n', '7 8 0 4 6 3 2 1 5\n', '0 2 1 7 4 8 6 5 3\n', '5 1 4 8 0 7 3 6 2\n', '2 7 6 0 8 5 4 3 1\n',
#            '1 6 3 5 2 0 8 4 7\n', '3 4 8 2 5 1 0 7 6\n', '4 3 5 1 0 6 7 2 8\n', '0 5 6 3 7 4 1 8 0']
n, m = map(int, content[0].strip().split())
A = list(map(str.split, map(str.strip, content[1:n + 1])))
result = {}
# to do

for i in range(n):
    result[i] = '0'


def stop(track, warehouses):
    global result, t

    if result[track] == '0':
        current = warehouses[t]
        if current != '0' and current in result.values():
            other_track = [k for k in result.keys() if result[k] == current][0]
            result[other_track] = '0'
            stop(other_track, A[other_track])

        result[track] = current


for t in range(m):
    if not '0' in result.values():
        break
    for track, warehouses in enumerate(A):
        stop(track, warehouses)

print("\n".join(result.values()))

2 6
1 2 3 4 0 0
0 0 0 0 0 1