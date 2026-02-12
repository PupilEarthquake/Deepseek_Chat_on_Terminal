import asyncio
from openai import AsyncOpenAI
import httpx
import utils
from textual.app import App
from textual.containers import VerticalScroll, Horizontal
from textual.widgets import TextArea, Static
from textual.binding import Binding
from rich.markdown import Markdown
from textual import events



class Bubble(Static):
    '''
    自定义聊天气泡部件
    '''
    def __init__(self, sender, content):
        super().__init__(content)
        self.sender = sender

    def _on_mount(self):
        if self.sender == "usr":
            self.add_class("usr-message")
        else:
            self.add_class("ai-message")
        self.border_title = self.sender



class ChatInput(TextArea):
    '''
    自定义输入窗口, 将Tab键行为替换为缩进2字符
    '''
    def _on_key(self, event: events.Key):
        if event.key == 'tab':
            event.stop()
            event.prevent_default()
            self.insert('  ')



class ChatApp(App):
    CSS_PATH = 'chat.tcss'
    BINDINGS = [
        Binding('ctrl+c', 'quit', 'Exit', show=True),
        Binding('ctrl+s', 'send_message', 'Send', show=True)
    ]

    def __init__(self, model, filename, sys_anno, msghead):
        super().__init__()
        self.model = model
        self.filename = filename
        # 给AI的系统提示
        self.sys_anno = sys_anno  
        self.msg_head = msghead

        # 加载配置文件
        config = utils.loadconf()
        apikey = config['network']['apikey']
        proxy_url = config['network']['proxy']

        if proxy_url in ['None', 'False']:
            self.client = AsyncOpenAI(
            api_key=apikey, 
            base_url="https://api.deepseek.com"
            )
        else:
            self.client = AsyncOpenAI(
            api_key=apikey, 
            base_url="https://api.deepseek.com",
            http_client=httpx.AsyncClient(proxy=proxy_url)
        )

        # 生成保存路径
        self.js_path, self.md_path = utils.create_save_path(filename)

        # 创建消息列表
        self.message_list = []


    def compose(self):
        yield VerticalScroll(id='chat-view')
        yield ChatInput(id='input', placeholder='Ctrl+S Send')
        

    def on_mount(self):
        self.query_one(ChatInput).focus()


    async def get_response(self, chatwindow):
        # loading_spinner = LoadingIndicator()
        ai_msg = Bubble('ai', 'Thinking')
        # ai_row = Horizontal(
        #         ai_msg,
        #         Static(classes='space-ai'),
        #         classes='message-row'
        #     )
        chatwindow.mount(ai_msg)

        ai_msg.scroll_visible()
        resobj = await self.client.chat.completions.create(
                    model=self.model,
                    messages=self.message_list,
                    stream=False,
                    temperature=1.0
                    )
        
        response = resobj.choices[0].message.content

        # 模拟回复
        # response = '# SIMUL RES\n`async def simul_response(self, chatwindow):`'
        # await asyncio.sleep(3)
        ai_msg.update(Markdown(response))


        self.message_list.append({"role": "assistant", "content": response})
        utils.save_chat_json(self.js_path, self.message_list)
        utils.save_chat_md(self.md_path, self.message_list)
        chatwindow.scroll_end(animate=False)


    def action_send_message(self):
        input_widget = self.query_one('#input', ChatInput)
        message_usr = input_widget.text.strip()

        if message_usr:
            message = Markdown(message_usr)


            self.message_list.append({"role": "system", "content": self.sys_anno})
            self.message_list.append({"role": "user", "content": f"{self.msg_head}\n\n{message_usr}"})


            usr_smg = Bubble('usr', message_usr)
            chatwindow = self.query_one("#chat-view", VerticalScroll)


            # usr_row = Horizontal(
            #     Static(classes='space-usr'),
            #     usr_smg,
            #     classes='message-row'
            # )
            chatwindow.mount(usr_smg)

            input_widget.text = ''
            usr_smg.scroll_visible()

            self.run_worker(self.get_response(chatwindow))



if __name__ == '__main__':
    app = ChatApp('resoning', 'test', 'sys_anno', 'head')
    app.run()
    