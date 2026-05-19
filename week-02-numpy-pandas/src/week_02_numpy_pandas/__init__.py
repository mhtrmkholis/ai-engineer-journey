import numpy as np
# import time

# n = 1_000_000
# py_list = list(range(n))
# np_arr = np.arange(n)

# # Python list
# start = time.perf_counter()
# result = [x * 2 for x in py_list]
# print(f"Python list: {time.perf_counter() - start:.4f}s")

# # NumPy
# start = time.perf_counter()
# result = np_arr * 2
# print(f"NumPy:       {time.perf_counter() - start:.4f}s")

test1 = np.array([[0, 10, 3], [1, 2, 3]])
test2 = np.array([[2, 4, 3]])
test3 = test1 + test2
print(test3[test3 > 3])
