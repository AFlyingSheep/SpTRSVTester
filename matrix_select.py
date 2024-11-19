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
        return set()

    with open(cache_file, "r") as f:
        processed_matrices = {line.strip() for line in f}
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
        cache_matrix_name = read_cache(cache_file=cache_file)
        if self.config.run_mode == RUN_MODE.RUN_FROM_FILE:
            # read matrix names from matrix file
            matrix_name = read_cache(cache_file=self.config.matrix_file)
        elif self.config.run_mode == RUN_MODE.RUN_FROM_RULES:
            matrixs = select_matrix()
            matrix_name = {matrix.name for matrix in matrixs}

        matrix_name = matrix_name - cache_matrix_name
        return matrix_name


def run_test(result_path):
    cache_file = os.path.join(result_path, "out.cache")
    perf_file = os.path.join(result_path, "out.perf")
    save_file = os.path.join(result_path, "out.result")
    error_file = os.path.join(result_path, "out.error")
    base_error_file = os.path.join(result_path, "out.base_error")
    yy_error_file = os.path.join(result_path, "out.yy_error")

    processed_matrices = read_cache(cache_file)
    skip_matrices = read_cache("skip.txt")
    use_matrices = read_cache("matrix_name.txt")
    if len(use_matrices) > 0:
        print("Find matrixs: ", len(use_matrices))

    matrixs = select_matrix()

    count = 0
    for matrix in matrixs:
        print(f"Start to compute {matrix.name}, {count}/{len(matrixs)}")
        # if matrix.rows != matrix.cols or matrix.psym < 1:
        #     print("Matrix ", matrix.name, "is not a symmetric matrix.")
        #     count = count + 1
        #     continue
        if matrix.name in processed_matrices:
            print(matrix.name, " has been computed.")
            count = count + 1
            continue
        if matrix.name in skip_matrices:
            print(matrix.name, " is in skip list.")
            count = count + 1
            continue
        if len(use_matrices) > 0:
            if matrix.name not in use_matrices:
                print(matrix.name, " not in use matrix")
                continue

        matrix_download(matrix.name)
        # udfrt_time, udfrt_a_256, udfrt_a_512, yy_time, base_time = rb.run_baseline(matrix.name, default_path="/staff/zhaoyang/database/sparse-matrix/" + matrix.name)
        # udfrt_graph = rb.run_baseline(matrix.name, default_path="/staff/zhaoyang/database/sparse-matrix/" + matrix.name)
        udfrt_multiagg = rb.run_baseline(
            matrix.name,
            default_path="/staff/zhaoyang/database/sparse-matrix/" + matrix.name,
        )

        #  rb.append_to_file(save_file, udfrt_time, "UDFRT", matrix=matrix)
        #  rb.append_to_file(save_file, udfrt_a_256, "UDFRT_AGG_256", matrix=matrix)
        #  rb.append_to_file(save_file, udfrt_a_512, "UDFRT_AGG_512", matrix=matrix)
        #  rb.append_to_file(save_file, yy_time, "YYSpTRSV", matrix=matrix)
        #  rb.append_to_file(save_file, base_time, "Sync-Free", matrix=matrix)
        rb.append_to_file(save_file, udfrt_multiagg, "UDFRT_multiagg", matrix=matrix)

        # f_udfrt_time = float(udfrt_time[0])
        # f_udfrt_a_256 = float(udfrt_a_256[0])
        # f_udfrt_a_512 = float(udfrt_a_512[0])
        #
        # f_yy_time = 9999.9999
        # f_base_time = 9999.9999

        # if len(yy_time) > 0:
        #     f_yy_time = float(yy_time[0])
        # if len(base_time) > 0:
        #     f_base_time = float(base_time[0])

        # # Check the better matrix count
        # # for bad result, get the acc of the result
        # bad_acc = []
        # if f_udfrt_time > f_yy_time or f_udfrt_a_256 > f_yy_time or f_udfrt_a_512 > f_yy_time:
        #     bad_acc.append(min(f_udfrt_time, f_udfrt_a_256, f_udfrt_a_512) / f_yy_time)
        # if f_udfrt_time > f_base_time or f_udfrt_a_256 > f_base_time or f_udfrt_a_512 > f_base_time:
        #     bad_acc.append(min(f_udfrt_time, f_udfrt_a_256, f_udfrt_a_512) / f_base_time)

        # if len(bad_acc) > 0:
        #     write_to_perf(matrix.name, bad_acc, perf_file)

        # # Write the error matrix
        # if f_udfrt_time == 9999.9999 or f_udfrt_a_256  == 9999.9999 or f_udfrt_a_512 == 9999.9999:
        #     write_to_cache(matrix.name, error_file)
        # if len(base_time) == 0:
        #     write_to_cache(matrix.name, base_error_file)
        # if len(yy_time) == 0:
        #     write_to_cache(matrix.name, yy_error_file)

        write_to_cache(matrix.name, cache_file)
        count = count + 1
