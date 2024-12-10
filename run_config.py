import ssgetpy
import os
from enum import Enum
import configparser
import datetime


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
        return "./bin/mixsptrsv-block " + matrix_path

    def get_extract_re(self):
        return [
            r"Not Reorder execute time:\s*([\d.]+)\s*ms",
            r"cuda graph time:\s*([\d.]+)\s*ms",
            r"level set time:\s*([\d.]+)\s*ms",
            r"cuSPARSE time:\s*([\d.]+)\s*ms",
        ]

    def get_name(self):
        return ["YYSpTRSV", "MixSpTRSVWithGraph", "MixSpTRSVWithLevelSet", "CudaSparse"]


class CudaSparse:
    def get_run_command(self, matrix_path):
        return "./bin/cuda_sparse " + matrix_path

    def get_extract_re(self):
        return [r"cuSPARSE time:\s*([\d.]+)\s*ms"]

    def get_name(self):
        return ["CudaSparse"]


class RunConfig:
    def __init__(self):
        self.run_mode = RUN_MODE.RUN_FROM_FILE
        self.read_config("config.ini")
        print("========== Read config file successfully. ==========")
        print(f"Run mode: {self.run_mode}")
        print(f"Cache file: {self.cache_file}")
        print(f"Matrix file: {self.matrix_file}")
        print(f"Matrix database path: {self.matrix_database_path}")
        print(f"Save file: {self.save_file}")
        print(f"Error file: {self.error_file}")
        print(f"Save folder: {self.save_folder}")
        print(f"Timeout: {self.timeout}")
        print(f"Device id: {self.device_id}")
        print("====================================================")

    def read_config(self, config_file):
        # 创建 ConfigParser 对象
        config = configparser.ConfigParser()
        config.read(config_file)

        self.cache_file = config["InputFile"]["cache_file"]
        self.matrix_file = config["InputFile"]["matrix_file"]
        self.matrix_database_path = config["InputFile"]["matrix_database_path"]

        self.save_file = config["OutputFile"]["save_file"]
        self.error_file = config["OutputFile"]["error_file"]
        self.save_folder = config["OutputFile"]["save_folder"]

        if len(self.save_folder.strip()) == 0:
            # 获取当前年份、月份、日期
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day
            folder_name = str(year) + "-" + str(month) + "-" + str(day)

            # 如果不存在文件夹，则创建文件夹
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            self.save_folder = folder_name

        self.timeout = config.getint("Settings", "timeout")

        self.device_id = config.getint("Settings", "device_id")
