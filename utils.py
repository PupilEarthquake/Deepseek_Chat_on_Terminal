from datetime import datetime
import subprocess
import os
import json


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"


def get_response(messages, client, chat_config):
    respons = client.chat.completions.create(
        model=chat_config['model'],
        messages=messages,
        stream=chat_config['stream'],
        temperature=chat_config['temperature']
    )

    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_path = f'{chat_config['chat_save_dir']}/{chat_config['chat_name']}.md'

    reasoning_content = ''
    content = ''

    for chunk in respons:
        delta = chunk.choices[0].delta
        reasoning_content_block = getattr(delta, 'reasoning_content', '')
        content_block = getattr(delta, 'content', '')

        if reasoning_content_block:
            reasoning_content += reasoning_content_block
            print(f'{Colors.GRAY}{reasoning_content_block}{Colors.RESET}', end='')

        if content_block:
            if content == '':
                print('\n')

            content += content_block
            print(f'{content_block}', end='')
    print('\n'+'-'*10+'response finished'+'-'*10+'\n')

    with open(save_path, 'a') as md_file:
        md_file.write(f'# DATE: {time_now} \n\n')
        md_file.write(f'## User:\n {messages[-1]['content']} \n\n')
        md_file.write(f'## Deepseek [Reasoning]:\n{reasoning_content} \n\n')
        md_file.write(f'## Deepseek [Answer]:\n{content} \n\n')

    return content, reasoning_content
    

def edit_send_message():
    tempfile_path = 'send_message.txt'
    editor = os.environ.get('EDITOR', 'nano')
    subprocess.run([editor, tempfile_path], check=True)

    with open(tempfile_path, 'r') as f:
        message = f.read()
        
    return message



def load_messages(chat_config):
    path = f'messages/{chat_config['chat_name']}.json'
    if os.path.exists(path):
        with open(path, mode='r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []
    return data
