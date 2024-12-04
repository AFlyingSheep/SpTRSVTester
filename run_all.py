import ssgetpy
import os
from enum import Enum
import run_config as rc
from run_config import RunConfig
from matrix_select import MatrixSelector
import profiling_runner as pr
import matrix_select as ms


def test_output():
    udfrt_time = rb.run_baseline(
        "atmosmodd",
        default_path="/staff/zhaoyang/database/sparse-matrix/" + "atmosmodd",
    )
    udfrt_time = min(udfrt_time)
    print(udfrt_time)


def run_test(config, projects):
    selector = MatrixSelector(config=config)
    # Get the matrix names
    names = selector.get_matrix_names()
    # print(names)

    # For project, run the matrix
    for index, name in enumerate(names):
        print(f"Running matrix({name}) {index}/{len(names)}.")
        matrix_path = os.path.join(config.matrix_database_path, name, name + ".mtx")
        # print(matrix_path)
        for project in projects:
            times = pr.run_project(
                project=project,
                matrix_path=matrix_path,
                timeout=config.timeout,
                device_id=config.device_id,
            )
            # transform from str to double
            times = [float(time) for time in times]

            # write the result to file
            if len(times) != len(project.get_name()):
                print(
                    f"Error: {len(times)} times for {len(project.get_name())} projects."
                )
                return

            # print(times)
            # print(project.get_name())
            for time, project_name in zip(times, project.get_name()):
                with open(os.path.join(config.save_folder, config.save_file), "a") as f:
                    f.write(f"{name},{project_name},{str(time)}\n")

        # write matrix name to cache
        ms.write_to_cache(name, os.path.join(config.save_folder, config.cache_file))


import datetime

if __name__ == "__main__":
    # 获取当前年份、月份、日期
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    folder_name = str(year) + "-" + str(month) + "-" + str(day)

    # 如果不存在文件夹，则创建文件夹
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    config = RunConfig()
    config.save_folder = folder_name

    # projects = [rc.TileSpTRSV()]
    # projects = [rc.YYSpTRSV(), rc.TileSpTRSV()]
    # projects = [rc.MixSpTRSVWithGraph(), rc.MixSpTRSVWithLevelSet()]
    projects = [rc.MixSpTRSVAll()]
    run_test(config=config, projects=projects)
