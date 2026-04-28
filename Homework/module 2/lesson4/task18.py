S, S_ = input("S: ").split(", "), input("S': ").split(", ")
n, m = len(S), len(S_)
i, j = 0, 0  # указатели на S и S' соответственно

while i < n and j < m:
    if S[i] == S_[j]:
        j += 1
    i += 1

print("S' является подпоследовательностью S" if j == m else "S' не является подпоследовательностью S")
