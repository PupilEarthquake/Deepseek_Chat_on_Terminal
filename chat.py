from openai import OpenAI
import json
from datetime import datetime
from utils import Colors, get_response, edit_send_message, load_messages

with open('user.json', 'r') as f:
    usr_conf = json.load(f)

client = OpenAI(api_key=usr_conf['api_key'], base_url=usr_conf['base_url'])

chat_config = {'model': 'deepseek-chat',
               'stream': True,
               'temperature': 1.0,
               'chat_save_dir': 'chats',
               'chat_name': 'v0_test(1)'}


if __name__ == '__main__':
    # messages = []
    messages = load_messages(chat_config)

    while True:
        short_message = input(f'{Colors.BOLD}{Colors.GREEN}YOU: {Colors.RESET}\n')

        if short_message.lower() in ['exit', 'quit', 'bye']:
            break
        elif short_message.lower() in ['nano:', 'editor:', 'nano', 'editor']:
            message = edit_send_message()
            print(f'{message}')
        else:
            message = short_message.lower()

        messages.append({'role': 'user', 'content': message})

        print(f'\n{Colors.BOLD}{Colors.CYAN}AI: {Colors.RESET}')
        answer, _ = get_response(messages, client, chat_config)

        messages.append({'role': 'assistant', 'content': answer})
    
    with open(f'messages/{chat_config['chat_name']}.json', mode='w', encoding='utf-8') as f:
        json.dump(messages, f)
