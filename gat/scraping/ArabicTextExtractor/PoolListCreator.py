import math
dense_nodes = 5875
pool_list = []

while dense_nodes!=0:
    root = math.sqrt(dense_nodes)
    root = math.floor(root)
    dense_nodes-=root*root
    pool_list.append(root)
pool_list.reverse()
print(pool_list)