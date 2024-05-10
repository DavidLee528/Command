from typing import List
from logging import basicConfig, getLogger, INFO, Logger

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
                            --networks #network# \
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
                "network": ["vgg19", "resnet18", "googlenet", "mobilenet"],
                "attack": ["bim", "cw", "deepfool", "difgsm", "fgsm", "mifgsm", "pgd", "tifgsm"], 
                "model_path": [
                    "/home/topsec/code_formal/code/drills/torch/normal_train/normal_trained_models/vgg19/best_acc.pth", 
                    "/home/topsec/code_formal/code/drills/torch/normal_train/normal_trained_models/resnet18/best_acc.pth",
                    "/home/topsec/code_formal/code/drills/torch/normal_train/normal_trained_models/googlenet/best_acc.pth",
                    "/home/topsec/code_formal/code/drills/torch/normal_train/normal_trained_models/mobilenet/best_acc.pth"
                ],
            }, 

            # argument binding config
            "binding": ["network", "model_path"]
        }
    }
}

def init_logger(logger_name: str = "lab4") -> Logger:
    basicConfig(level = INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    global logger
    logger = getLogger("AutoTest")
    logger.info("Program start.")
    return logger

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

def construct_command(config: dict) -> List[str]:
    """Construct command list from config variable

    Args:
        config (dict): config variable

    Returns:
        List[str]: A list of command string to be execute
    """
    res: List[str] = []

    return res

logger: Logger = init_logger()