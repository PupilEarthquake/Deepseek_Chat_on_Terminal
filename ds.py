#!/home/xiao/anaconda3/envs/AI/bin/python

import argparse
from chat import ChatApp
import utils



parser = argparse.ArgumentParser(prog="ds")
parser.add_argument("--version", "-v", action="version", version="DS Assistant CLI 3.0 Beta")
subparsers = parser.add_subparsers(dest="cmd")


parser_c = subparsers.add_parser("chat", help="chat with ai")
parser_c.add_argument("--think", "-t", help="use the thinking mode", action="store_true")


parser_ec = subparsers.add_parser("ec", help="translate en to cn")
parser_ec.add_argument("--think", "-t", help="use the thinking mode", action="store_true")
parser_ec.add_argument("--syns", "-s", help="analyze the sentence structure", action="store_true")


parser_ce = subparsers.add_parser("ce", help="translate cn to en")
parser_ce.add_argument("--think", "-t", help="use the thinking mode", action="store_true")
parser_ce.add_argument("--mtrs", "-m", help="provide multiple translations", action="store_true")


parser_dict = subparsers.add_parser("dict", help="youdao dict")




model_options = ["deepseek-chat", "deepseek-reasoner"]

text_head_ls = {
    "ec": "你是一个翻译器, 将下面内容翻译成中文",
    "ce": "你是一个翻译器, 将下面内容翻译成英文"}

text_head_options_ls = {
    "ec-ss": "分析句子的结构", 
    "ce-mt": "给出3种翻译"}




args = parser.parse_args()



if args.cmd == "ec":
    if args.think:
        model = model_options[1]
    else:
        model = model_options[0]
    
    text_head = text_head_ls["ec"]
    if args.syns:
        text_head = text_head + f", {text_head_options_ls["ec-ss"]}"

    sys_announce = "你是一个AI学术助手"

    filename = f"{utils.time_now()}_{str.upper(args.cmd)}"
    App = ChatApp(model, filename, sys_announce, text_head)
    App.run()


if args.cmd == "ce":
    if args.think:
        model = model_options[1]
    else:
        model = model_options[0]
    
    text_head = text_head_ls["ce"]
    if args.mtrs:
        text_head = text_head + f", {text_head_options_ls["ce-mt"]}"

    sys_announce = "你是一个AI学术助手"

    filename = f"{utils.time_now()}_{str.upper(args.cmd)}"
    App = ChatApp(model, filename, sys_announce, text_head)
    App.run()


elif args.cmd == "chat":
    if args.think:
        model = model_options[1]
    else:
        model = model_options[0]
    
    text_head = ""
    sys_announce = "你是一个AI学术助手"
    filename = f"{utils.time_now()}_{str.upper(args.cmd)}"
    App = ChatApp(model, filename, sys_announce, text_head)
    App.run()



