import command
from typing import List

if __name__ == "__main__":
    # passed: bool = command.check_config(config = command.config)
    passed: bool = True

    if passed:
        command_list: List[str] = command.construct_command(config = command.config)

        with open("commands.txt", "w") as f:
            for command in command_list:
                f.write(command + "\n")