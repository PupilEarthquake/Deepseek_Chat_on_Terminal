import sys
from openai import AsyncOpenAI
import asyncio
import utils
import httpx


VERSION = "3.1"

client = AsyncOpenAI(
            api_key = "sk-0a391a7dd3ec4c8eae679d24c16c8526",
            base_url = "https://api.deepseek.com",
            http_client=httpx.AsyncClient(proxy="http://127.0.0.1:7890")
            )


def show_welcome():
    print("Welcome to DSAS")
    print(f"version {VERSION}")
    print()



def quit_input():
    while True:
        ans = input("sys > quit? ([y]/n)").strip().lower()
        if ans == "y":
            sys.exit(0)
        elif ans == "n":
            return
        else:
            sys.exit(0)



def send_input(text):
    while True:
        ans = input("sys > send? ([y]/n)").strip().lower()
        if ans == "y":
            return 0
        elif ans == "n":
            return 1
        else:
            return 0




def model_selection():
    while True:
        print("sys > select a model : 1. mod1   2. mod2")
        try:
            ans = input("usr > ").strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)

        if ans == "1":
            return "mod 1"
        elif ans == "2":
            return "mod 2"
        else:
            print("sys > please input the model number")
        


async def spinner(stop_event):
    chars = ["|", "/", "-", "\\"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\rthinking {chars[i % 4]}  ")
        sys.stdout.flush()
        await asyncio.sleep(0.5)
        i += 1

    sys.stdout.write("\r \r")
    sys.stdout.flush()


async def get_response(msglist):
    full_response = ""
    stop_event = asyncio.Event()
    
    stream = await client.chat.completions.create(
            model = "deepseek-v4-pro",
            messages = msglist,
            stream = True,
            temperature = 1.0,
            reasoning_effort = "max",
            extra_body = {"thinking": {"type": "enabled"}}
            )
    stop_event.set()

    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            full_response += delta
            sys.stdout(delta)
    
    return full_response



def main():
    show_welcome()
    msglist = []

    while True:
        try:
            usr_input = input("usr > ").strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)

        if usr_input == ":q":
            quit_input()

        elif usr_input == ":m":
            mod_sel = model_selection()
            print(f"sys > {mod_sel}")

        elif usr_input.startswith(":"):
            print(f"unkonwn command {usr_input}")

        else:
            send_command = send_input(usr_input)
            if send_command == 0:
                msglist.append({"role": "user", "content": usr_input})
                print(f"ds  > ")
                full_response = asyncio.run(get_response(msglist))
                msglist.append({"role": "assistant", "content": full_response})




if __name__ == "__main__":
    main()

