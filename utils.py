from datetime import datetime
import os
import json
import configparser
import shutil


def time_now():
    date = datetime.now().strftime('%Y%m%d%H%M')
    return date

     


def create_save_path(filename):
    base_path = os.path.dirname(os.path.realpath(__file__))
    base_path = base_path + '/chathist'
    if os.path.exists(base_path):
        pass
    else:
        os.mkdir(base_path)
    save_dir_js = f"{base_path}/js"
    save_dir_md = f"{base_path}/md"
    if os.path.exists(save_dir_js):
        pass
    else:
        os.mkdir(save_dir_js)
    if os.path.exists(save_dir_md):
        pass
    else:
        os.mkdir(save_dir_md)
    json_save_path = f'{save_dir_js}/{filename}.json'
    md_save_path = f'{save_dir_md}/{filename}.md'

    return json_save_path, md_save_path




def save_chat_json(path, data):
    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(data, f)


def save_chat_md(path, data):
    with open(path, 'w') as md_file:
        for i in range(len(data)):
            role_i = data[i]['role']
            content_i = data[i]['content']
            if role_i in ['user', 'assistant']:
                md_file.write(f'__{role_i}:__\n {content_i} \n\n')



def loadconf():
    base_path = os.path.dirname(os.path.realpath(__file__))
    conf_path = base_path + '/user.conf'
    config = configparser.ConfigParser()
    config.read(conf_path)

    return config

