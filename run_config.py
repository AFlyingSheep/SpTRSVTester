import ssgetpy
import os
from enum import Enum

class RUN_MODE(Enum):
    RUN_FROM_FILE = 1
    RUN_FROM_RULES = 2

# def extract_base(lines):
#     return extract_solving_time(lines, r'solve used\s*([\d.]+)')

# def extract_graph(lines):
#     return extract_solving_time(lines, r'cuda Graph Time:\s*([\d.]+)')

# def extract_udfrt(lines):
#     # 如果 lines 有字符串 Error
#     if 'Error' in lines:
#         return ['9999.9999']
#     return extract_solving_time(lines, r'Elapsed time:\s*([\d.]+)\s*ms.')

class TileSpTRSV:
    def get_run_command(self, matrix_path):
        return "./bin/tilesptrsv -d $CUDA_VISIBLE_DEVICES " + matrix_path
    def get_extract_re(self):
        return r'CUDA TileSpTRSV runtime\s*([\d.]+)\sms'
    def get_name(self):
        return "TileSpTRSV"

class YYSpTRSV:
    def get_run_command(self, matrix_path):
        return "./bin/YYSpTRSV " + matrix_path
    def get_extract_re(self):
        return r'solving time\s*=\s*([\d.]+)\s*'
    def get_name(self):
        return "YYSpTRSV"
        

class RunConfig:
    def __init__(self):
        self.run_mode = RUN_MODE.RUN_FROM_RULES

        self.cache_file = "out.cache"
        self.matrix_file = "test_matrix_name.txt"

        self.matrix_database_path = "/staff/zhaoyang/database/sparse-matrix/"

        self.save_file = "out.result"
        self.error_file = "out.error"

        self.timeout = 90
        self.save_folder = ""
