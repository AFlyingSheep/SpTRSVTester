import run_baseline as rb
import ssgetpy
import os

def matrix_download(matrix_name):
    current_dic = os.getcwd()
    matrix_path = "/staff/zhaoyang/database/sparse-matrix/" + matrix_name
    
    # check whether have the data
    data_exist = os.path.isdir(os.path.join(current_dic, matrix_path))

    if not data_exist:
        result = ssgetpy.search(name=matrix_name)
        result.download(format='MM', destpath='/staff/zhaoyang/database/sparse-matrix/', extract=True)
        print("Download ", matrix_name, " over.")
    else:
        print("Find ", matrix_name, ".")

# select the matrix which the non_zero count > 10,0000
def select_matrix():
    serach_result = ssgetpy.search(nzbounds=(100, 110663202), limit=3000)
    print("Find result: ", len(serach_result))
    # print(type(serach_result))
    return serach_result
    
def read_cache(cache_file='cache.txt'):
    """Read the cache file and return a set of processed matrix names."""
    if not os.path.exists(cache_file):
        return set()
    
    with open(cache_file, 'r') as f:
        processed_matrices = {line.strip() for line in f}
    return processed_matrices

def write_to_cache(matrix_name, cache_file='cache.txt'):
    """Append a matrix name to the cache file."""
    with open(cache_file, 'a') as f:
        f.write(f"{matrix_name}\n")

def write_to_perf(matrix_name, better_count, perf_file='perf.txt'):
    with open(perf_file, 'a') as f:
        # f.write(f"{matrix_name} {better_count}\n")
        if len(better_count) == 1:
            f.write(f"{matrix_name} {better_count[0]}\n")
        else:
            f.write(f"{matrix_name} {better_count[0]} {better_count[1]}\n")

def run_test():
    matrixs = select_matrix()
    result = [] # Format: matrix domain
    domain_count = {}
    use_matrixs = read_cache("matrix_name.txt")
    
    count = 0
    for matrix in matrixs:
        print(f"Start to compute {matrix.name}, {count}/{len(matrixs)}")
        if matrix.name not in use_matrixs:
            count += 1
            continue
        matrix_download(matrix.name)
        result.append([matrix.name, matrix.kind])
        count = count + 1
        domain_count[matrix.kind] = domain_count.get(matrix.kind, 0) + 1

    # write the result to the file
    with open("./domain.txt", 'w') as f:
        for item in result:
            f.write(f"{item[0]},{item[1]}\n")

    # write the domain count to the perf perf_file
    with open("./domain_count.txt", 'w') as f:
        for key in domain_count:
            f.write(f"{key},{domain_count[key]}\n")

import datetime

if __name__ == "__main__":
    run_test()

