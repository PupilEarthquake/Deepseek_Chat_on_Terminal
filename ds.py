#!/home/an/miniconda3/envs/AI/bin/python3

import argparse
from chat import ChatApp
import utils



parser = argparse.ArgumentParser(prog="ds")
parser.add_argument("--version", "-v", action="version", version="DS Assistant CLI v3.1")
subparsers = parser.add_subparsers(dest="cmd")


parser_c = subparsers.add_parser("chat", help="chat with ai")
parser_c.add_argument("--think", "-t", help="use the thinking mode", action="store_true")


parser_ec = subparsers.add_parser("ec", help="translate en to cn")
parser_ec.add_argument("--think", "-t", help="use the thinking mode", action="store_true")

# 
# parser_ce = subparsers.add_parser("ce", help="translate cn to en")
# parser_ce.add_argument("--think", "-t", help="use the thinking mode", action="store_true")
# parser_ce.add_argument("--mtrs", "-m", help="provide multiple translations", action="store_true")
# 
# 
# parser_dict = subparsers.add_parser("dict", help="youdao dict")




model_options = ["deepseek-v4-flash", "deepseek-v4-pro"]


args = parser.parse_args()



# if args.cmd == "ec":
#     if args.think:
#         model = model_options[1]
#     else:
#         model = model_options[0]
#     
#     text_head = text_head_ls["ec"]
#     if args.syns:
#         text_head = text_head + f",{text_head_options_ls["ec-ss"]}"
# 
#     sys_announce = "你是一个AI学术助手"
#     tempreture = 1.3
#     filename = f"{utils.time_now()}_{str.upper(args.cmd)}"
#     App = ChatApp(model, filename, sys_announce, text_head, tempreture)
#     App.run()
# 
# 
# if args.cmd == "ce":
#     if args.think:
#         model = model_options[1]
#     else:
#         model = model_options[0]
#     
#     text_head = text_head_ls["ce"]
#     if args.mtrs:
#         text_head = text_head + f", {text_head_options_ls["ce-mt"]}"
# 
#     sys_announce = "你是一个AI学术助手"
#     tempreture = 1.3
#     filename = f"{utils.time_now()}_{str.upper(args.cmd)}"
#     App = ChatApp(model, filename, sys_announce, text_head, tempreture)
#     App.run()
# 

if args.cmd == "chat":
    if args.think:
        model = model_options[1]
        reasoning_effort = "max"
    else:
        model = model_options[0]
        reasoning_effort = "high"
    
    text_head = ""
    sys_announce = ""
    extra_body = {"thinking": {"type": "enabled"}}
    tempreture = 1.0
    filename = f"{utils.time_now()}_{str.upper(args.cmd)}"
    App = ChatApp(model, filename, sys_announce, text_head, reasoning_effort, extra_body, tempreture)
    App.run()



elif args.cmd == "ec":
    if args.think:
        model = model_options[1]
        reasoning_effort = "max"
    else:
        model = model_options[0]
        reasoning_effort = "high"
    
    text_head = "翻译下面内容, 请直接输出翻译结果:"
    sys_announce = "你是一个翻译器, 负责中英互译"
    extra_body = {"thinking": {"type": "enabled"}}
    tempreture = 1.0
    filename = f"{utils.time_now()}_{str.upper(args.cmd)}"
    App = ChatApp(model, filename, sys_announce, text_head, reasoning_effort, extra_body, tempreture)
    App.run()


