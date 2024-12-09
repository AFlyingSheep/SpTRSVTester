import ssgetpy
import os
import run_config
from run_config import RUN_MODE


# download the matrix
def matrix_download(matrix_name, destpath="/staff/zhaoyang/database/sparse-matrix/"):
    current_dic = os.getcwd()
    matrix_path = "/staff/zhaoyang/database/sparse-matrix/" + matrix_name

    # check whether have the data
    data_exist = os.path.isdir(os.path.join(current_dic, matrix_path))

    if not data_exist:
        result = ssgetpy.search(name=matrix_name)
        result.download(format="MM", destpath=destpath, extract=True)
        print("Download ", matrix_name, " over.")
    else:
        pass


# select the matrix which the non_zero count > 10,0000
# return ssgetpy
def select_matrix():
    serach_result = ssgetpy.search(nzbounds=(100000, 110663202), limit=3000)
    print("Find result, count: ", len(serach_result))
    # print(type(serach_result))
    return serach_result


# processing cache or skip matrixs
def read_cache(cache_file="cache.txt"):
    # Read the cache file and return a set of processed matrix names.
    if not os.path.exists(cache_file):
        return []

    with open(cache_file, "r") as f:
        processed_matrices = [line.strip() for line in f]
    return processed_matrices


# write the matrix's name to cache file
def write_to_cache(matrix_name, cache_file="cache.txt"):
    # Append a matrix name to the cache file.
    with open(cache_file, "a") as f:
        f.write(f"{matrix_name}\n")


class MatrixSelector:
    def __init__(self, config):
        self.config = config

    def get_matrix_names(self):
        cache_file = os.path.join(self.config.save_folder, self.config.cache_file)
        cache_matrix_name = set(read_cache(cache_file=cache_file))
        if self.config.run_mode == RUN_MODE.RUN_FROM_FILE:
            # read matrix names from matrix file
            matrix_name = read_cache(cache_file=self.config.matrix_file)
        elif self.config.run_mode == RUN_MODE.RUN_FROM_RULES:
            matrixs = select_matrix()
            matrix_name = [matrix.name for matrix in matrixs]

        matrix_name_ret = [
            item for item in matrix_name if item not in cache_matrix_name
        ]
        return matrix_name_ret
