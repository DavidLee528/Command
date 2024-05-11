import re
from typing import List, Dict
import logging
import colorlog
import hashlib

config: dict = {
    # project #1: torch
    "torch": {
        # project base directory
        "base": "/home/topsec/code_formal/code/drills/torch/",
        # script #1: attack_test
        "attack_test": {
            # command template to execute script
            # content within ## should be found in `template_parameters`
            "template": "#python# #base##path# \
                            --network #network# \
                            --model_path #model_path# \
                            --adv_data_path #base#attack/attack_demo/#network#/#attack#/adv_data.npy \
                            --clean_data_path #base#attack/attack_demo/#network#/#attack#/clean_data.npy \
                            --clean_label_path #base#attack/attack_demo/#network#/#attack#/label.npy",
            # parameters dict for template
            "template_parameters": {
                # Absolute path of python interpreter
                "python": ["/home/topsec/anaconda3/envs/ai_server/bin/python"],
                # relative path of script under project base directory
                "path": ["attack_test.py"],
                # argument pools
                "network, model_path": [
                    [
                        "vgg19",
                        "/home/topsec/code_formal/code/drills/torch/normal_train/normal_trained_models/vgg19/best_acc.pth",
                    ],
                    [
                        "resnet18",
                        "/home/topsec/code_formal/code/drills/torch/normal_train/normal_trained_models/resnet18/best_acc.pth",
                    ],
                    [
                        "googlenet",
                        "/home/topsec/code_formal/code/drills/torch/normal_train/normal_trained_models/googlenet/best_acc.pth",
                    ],
                    [
                        "mobilenet",
                        "/home/topsec/code_formal/code/drills/torch/normal_train/normal_trained_models/mobilenet/best_acc.pth",
                    ],
                ],
                "attack": [
                    "bim",
                    "cw",
                    "deepfool",
                    "difgsm",
                    "fgsm",
                    "mifgsm",
                    "pgd",
                    "tifgsm",
                ],
            },
        },
    }, 
    "torch2": {
        # project base directory
        "base": "/home/topsec/code_formal/code/drills/torch2/",
        # script #1: attack_test
        "attack_test": {
            # command template to execute script
            # content within ## should be found in `template_parameters`
            "template": "#python# #base##path# \
                            --network #network# \
                            --model_path #model_path# \
                            --adv_data_path #base#attack/attack_demo/#network#/#attack#/adv_data.npy \
                            --clean_data_path #base#attack/attack_demo/#network#/#attack#/clean_data.npy \
                            --clean_label_path #base#attack/attack_demo/#network#/#attack#/label.npy",
            # parameters dict for template
            "template_parameters": {
                # Absolute path of python interpreter
                "python": ["/home/topsec/anaconda3/envs/ai_server/bin/python"],
                # relative path of script under project base directory
                "path": ["attack_test.py"],
                # argument pools
                "network, model_path": [
                    [
                        "vgg19",
                        "/home/topsec/code_formal/code/drills/torch2/normal_train/normal_trained_models/vgg19/best_acc.pth",
                    ],
                    [
                        "resnet18",
                        "/home/topsec/code_formal/code/drills/torch2/normal_train/normal_trained_models/resnet18/best_acc.pth",
                    ],
                    [
                        "googlenet",
                        "/home/topsec/code_formal/code/drills/torch2/normal_train/normal_trained_models/googlenet/best_acc.pth",
                    ],
                    [
                        "mobilenet",
                        "/home/topsec/code_formal/code/drills/torch2/normal_train/normal_trained_models/mobilenet/best_acc.pth",
                    ],
                ],
                "attack": [
                    "bim",
                    "cw",
                    "deepfool",
                    "difgsm",
                    "fgsm",
                    "mifgsm",
                    "pgd",
                    "tifgsm",
                ],
            },
        },
    }
}


def init_logger(logger_name: str = "AutoTest") -> logging.Logger:
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'ed',
            'CRITICAL': 'ed,bg_white',
        }
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    global logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    logger.info("Program start.")
    return logger

def generate_short_hash(input_string):
    hash_object = hashlib.md5(input_string.encode())
    return hash_object.hexdigest()[:8]

def check_config(config: dict) -> bool:
    """Check if errors exist in config variable

    Args:
        config (dict): config dict variable to be checked

    Returns:
        bool: true if no errors detected
    """
    logger.info("Start checking config")

    # checkpoint #1: if the binding argument list size equal
    for project, project_config in config.items():
        for script, script_config in project_config.items():
            if script != "base":
                binding_args: List[str] = script_config.get("binding", [])
                len_list: List[int] = []
                for check_item in binding_args:
                    len_list.append(len(script_config['template_parameters'].get(check_item, [])))
                if len(set(len_list)) != 1:
                    logger.error("Config check failed, wrong binding.")
                    return False
                
    # checkpoint #2: template parameter integrity
    for project, project_config in config.items():
        for script, script_config in project_config.items():
            if script != "base":
                template = script_config.get("template", "")
                template_params = script_config.get("template_parameters", {})
                for param in template_params:
                    if f"#{param}#" not in template:
                        logger.error("Config check failed, wrong template parameters.")
                        return False
                    
    logger.info("Config check passed.")
    return True

def construct_command(config: Dict) -> Dict[dict, list]:
    """Construct command list from config variable

    Args:
        config (dict): config variable

    Returns:
        List[str]: A list of command string to be execute
    """
    res: Dict[dict, list] = {}

    for project, project_config in config.items():
        res.update({f'{project}': []})
        for script, script_config in project_config.items():
            res[project] = {f'{script}': []}
            if script!= "base":
                template = script_config["template"]
                template_parameters = script_config["template_parameters"]

                # Extract parameters from template_parameters
                python_interpreter = template_parameters["python"][0]
                script_path = template_parameters["path"][0]
                network_model_path_pairs = template_parameters["network, model_path"]
                attacks = template_parameters["attack"]

                # Generate commands for each combination of network, model_path, and attack
                for network, model_path in network_model_path_pairs:
                    for attack in attacks:
                        command = template.replace("#python#", python_interpreter)
                        command = command.replace("#base#", project_config["base"])
                        command = command.replace("#path#", script_path)
                        command = command.replace("#network#", network)
                        command = command.replace("#model_path#", model_path)
                        command = command.replace("#attack#", attack)

                        # transform consecutive spaces to one space
                        command = re.sub(r'\s+', ' ', command)

                        # 8-digits short hash value for filename
                        hash: str = generate_short_hash(command)

                        res[project][script].append({'command': command, 'tag': hash})

    logger.info("Finish constructing commands.")
    return res

logger = init_logger()
