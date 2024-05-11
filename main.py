import command
import json
from typing import List, Dict
from execution import execute

if __name__ == "__main__":
    # passed: bool = command.check_config(config = command.config)
    passed: bool = True

    if passed:
        command: Dict[dict, list] = command.construct_command(config = command.config)

        with open("commands.json", "w") as f:
            json.dump(command, f, indent=4)

        for project in command.keys():
            for script in command[project].keys():
                output_dir: str = f"./output/{project}/{script}"
                execute(command_list = command[project][script], output_dir = output_dir, max_workers = 4)