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
        return [r"CUDA TileSpTRSV runtime\s*([\d.]+)\sms"]

    def get_name(self):
        return ["TileSpTRSV"]


class YYSpTRSV:
    def get_run_command(self, matrix_path):
        return "./bin/YYSpTRSV " + matrix_path

    def get_extract_re(self):
        return [r"solving time\s*=\s*([\d.]+)\s*"]

    def get_name(self):
        return ["YYSpTRSV"]


class MixSpTRSVWithGraph:
    def get_run_command(self, matrix_path):
        return "~/runtime/swtask/bin/SpTRSV " + matrix_path

    def get_extract_re(self):
        return [r"cuda graph time:\s*([\d.]+)\s*ms"]

    def get_name(self):
        return ["MixSpTRSVWithGraph"]


class MixSpTRSVWithLevelSet:
    def get_run_command(self, matrix_path):
        return "~/runtime/swtask/bin/SpTRSV " + matrix_path

    def get_extract_re(self):
        return [r"level set time:\s*([\d.]+)\s*ms"]

    def get_name(self):
        return ["MixSpTRSVWithLevelSet"]


class MixSpTRSVAll:
    def get_run_command(self, matrix_path):
        return "./bin/mixsptrsv " + matrix_path

    def get_extract_re(self):
        return [
            r"Not Reorder execute time:\s*([\d.]+)\s*ms",
            r"cuda graph time:\s*([\d.]+)\s*ms",
            r"level set time:\s*([\d.]+)\s*ms",
        ]

    def get_name(self):
        return ["YYSpTRSV", "MixSpTRSVWithGraph", "MixSpTRSVWithLevelSet"]


class RunConfig:
    def __init__(self):
        self.run_mode = RUN_MODE.RUN_FROM_FILE

        self.cache_file = "out.cache"
        self.matrix_file = "matrix_test_2024_12_4.txt"

        self.matrix_database_path = "/staff/zhaoyang/database/sparse-matrix/"

        self.save_file = "out.result"
        self.error_file = "out.error"

        self.timeout = 90
        self.save_folder = ""

        self.device_id = 1
