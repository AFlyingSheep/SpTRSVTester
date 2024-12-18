import subprocess
import sys
import re
import os


# input:
#   project: tilesptrsv, yysptrsv...
#   input_file: path of matrix
#   timeout: second
# output:
#   output_lines: [stdout lines splitted by \n]
def run_executable(project, input_file, device_id, timeout):
    executable = project.get_run_command(input_file)
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = str(device_id)

    retry_time = 0
    while retry_time < 15:
        try:
            # print(f"Running command: {executable}")
            # split commaned to list
            executable_list = executable.split()
            # print(executable_list)
            result = subprocess.run(
                executable,
                shell=True,
                capture_output=True,
                text=True,
                errors="replace",
                timeout=timeout,
                env=env,
            )
            result.check_returncode()  # Raise an exception if the process exited with a non-zero status
            output_lines = result.stdout.strip().split("\n")
            print("Success to get output.")
            return output_lines

        except subprocess.CalledProcessError as e:
            print(f"Error running {executable}: {e}", file=sys.stderr)
            print("Standard Error:", e.stderr)
            retry_time += 1
            # return ["Error"]

        except subprocess.TimeoutExpired as e:
            print(f"Timeout running {executable}: {e}", file=sys.stderr)
            # retry_time += 1
            return ["Error"]

        print(f"Retry time: {retry_time}")

    return ["Error"]


# input:
#   project: tilesptrsv, yysptrsv...
#   output: [stdout lines splitted by \n]
# output:
#   solving_times: [seconds]
def get_run_time(project, output):
    solving_times = []
    for re_str in project.get_extract_re():
        solving_time_pattern = re.compile(re_str)
        if len(output) == 0 or output[0] == "Error":
            solving_times.append("9999.9999")
        else:
            for line in output:
                match = solving_time_pattern.search(line)
                if match:
                    solving_times.append(match.group(1))
    
    # print(output)
    # print(solving_times)

    return solving_times


def run_project(project, matrix_path, device_id, timeout):
    output = run_executable(project, matrix_path, device_id, timeout)
    solving_times = get_run_time(project, output)
    return solving_times
