import random
import math

def cxTwoPoint2d(ind1, ind2):
    row_size = len(ind1)
    col_size = len(ind1[0])
    
    cx_row1 = random.randint(0, row_size - 1)
    cx_row2 = random.randint(0, row_size - 1)
    if cx_row2 >= cx_row1:
        cx_row2 += 1
    else:
        cx_row1, cx_row2 = cx_row2, cx_row1
    
    cx_col1 = random.randint(0, col_size)
    cx_col2 = random.randint(0, col_size - 1)
    if cx_col2 >= cx_col1:
        cx_col2 += 1
    else:
        cx_col1, cx_col2 = cx_col2, cx_col1
    
    for i in range(cx_row1, cx_row2):
        ind1[i][cx_col1:cx_col2], ind2[i][cx_col1:cx_col2] \
            = ind2[i][cx_col1:cx_col2], ind1[i][cx_col1:cx_col2]
    
    return ind1, ind2

def cx2d(ind1, ind2, area_max, rounding):
    row_size = len(ind1)
    col_size = len(ind1[0])

    area = random.randint(1, area_max)

    # calcurate min value to ensure col_len <= col_size
    row_min = math.ceil(area / col_size)
    row_max = min(area, row_size)
    row_len = random.randint(row_min, row_max)
    row_start = random.randint(0, row_size - row_len)
    cx_row1 = row_start
    cx_row2 = row_start + row_len

    col_len = rounding(area / (cx_row2 - cx_row1))
    col_start = random.randint(0, col_size - col_len)
    cx_col1 = col_start
    cx_col2 = col_start + col_len

    for i in range(cx_row1, cx_row2):
        ind1[i][cx_col1:cx_col2], ind2[i][cx_col1:cx_col2] \
            = ind2[i][cx_col1:cx_col2], ind1[i][cx_col1:cx_col2]
    
    return ind1, ind2

def mate2d(ind1, ind2, toolbox):
    row_size = len(ind1)
    for i in range(row_size):
        toolbox.mate1d(ind1[i], ind2[i])
    return ind1, ind2

def mutate2d(individual, toolbox):
    for row in individual:
        toolbox.mutate1d(row)
    return individual,
