import json


# 读取JSON配置文件
def read_config_file(file_path):
    with open(file_path, 'r') as file:
        config_data = json.load(file)
    return config_data


# 写入JSON配置文件
def write_config_file(file_path, config_data):
    with open(file_path, 'w') as file:
        json.dump(config_data, file, indent=4)  # indent参数用于美化输出，可选
