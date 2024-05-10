from typing import List

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

def check_config(config: dict) -> bool:
    """Check if errors exist in config variable

    vim
    Copy
    Args:
        config (dict): config dict variable to be check

    Returns:
        bool: true if no errors detected
    """
    res: bool = False

    # checkpoint #1: if the binding argument list size equal
    # add your code here

    # checkpoint #2: template parameter integrity
    # add your code here

    return res

def construct_command(config: dict) -> List[str]:
    """Construct command list from config variable

    Args:
        config (dict): config variable

    Returns:
        List[str]: A list of command string to be execute
    """
    res: List[str] = []

    return res