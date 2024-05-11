import os
import subprocess
import concurrent.futures
from typing import List
from command import logger

def execute(command_list: List[dict], output_dir: str, max_workers: int = 5) -> None:
    """Execute commands in parallel and save output to files

    Args:
        command_list (List[str]): A list of Linux commands
        output_dir (str): The directory where the output files will be saved
        max_workers (int): The maximum number of worker threads to use (default: 5)
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for command in command_list:
            output_file = f"{output_dir}/{command['tag']}.txt"
            futures.append(executor.submit(execute_command, command, output_file))
        for future in concurrent.futures.as_completed(futures):
            future.result()

def execute_command(command: str, output_file: str) -> None:
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except FileExistsError:
            pass    # concurrent execution

    try:
        with open(output_file, "w") as f:
            logger.info(f"Running: {command}")
            subprocess.run(command['command'], shell=True, stdout=f, stderr=subprocess.STDOUT, check=True)
    except subprocess.CalledProcessError as e:
        logger.warning(f"Error executing command '{command}': {e}")