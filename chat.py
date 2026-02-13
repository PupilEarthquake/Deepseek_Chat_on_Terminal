import asyncio
from openai import AsyncOpenAI
import httpx
import utils
from textual.app import App
from textual.containers import VerticalScroll, Vertical
from textual.widgets import TextArea, Static
from textual.binding import Binding
from rich.markdown import Markdown
from textual import events



class Bubble(Vertical):
    def __init__(self, sender, content):
        super().__init__()
        self.sender = sender
        self.content_raw = content
        self.is_editing = False


    def compose(self):
        yield Static(Markdown(self.content_raw), id='render_view')

        text_area = TextArea(self.content_raw, id='raw_view', read_only=True)
        yield text_area


    def _on_mount(self, event):
        if self.sender == "usr":
            self.add_class("usr-message")
        else:
            self.add_class("ai-message")
        self.border_title = self.sender
        self.query_one("#raw_view").add_class("hidden")


    def update_content(self, new_content):
        self.content_raw = new_content
        self.query_one("#render_view", Static).update(Markdown(new_content))
        raw_view = self.query_one("#raw_view", TextArea)
        raw_view.text = new_content
        

    def on_click(self):
        # 气泡处于焦点时切换编辑模式
        if not self.is_editing:
            self.toggle_mode(edit_mode=True)


    def on_descendant_blur(self, event: events.DescendantBlur):
        # 气泡失焦, 切换回渲染模式
        if self.is_editing:
            self.toggle_mode(edit_mode=False)


    def toggle_mode(self, edit_mode: bool):
        self.is_editing = edit_mode
        render_view = self.query_one("#render_view")
        raw_view = self.query_one("#raw_view", TextArea)

        if edit_mode:
            render_view.add_class("hidden")
            raw_view.remove_class("hidden")
            raw_view.focus()
        else:
            raw_view.add_class("hidden")
            render_view.remove_class("hidden")


class ChatInput(TextArea):
    # 自定义输入窗口, 将Tab键行为替换为缩进2字符
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

        ai_msg = Bubble('ai', 'Thinking')
        # ai_row = Horizontal(
        #         ai_msg,
        #         Static(classes='space-ai'),
        #         classes='message-row'
        #     )
        chatwindow.mount(ai_msg)
        ai_msg.scroll_visible()
        full_response = ""

        try:
            stream = await self.client.chat.completions.create(
                        model=self.model,
                        messages=self.message_list,
                        stream=True,
                        temperature=1.0
                        )

            async for chunk in stream:
                delta = chunk.choices[0].delta.content

                if delta:
                    full_response += delta
                    ai_msg.update_content(full_response)
                    chatwindow.scroll_end(animate=False)

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            ai_msg.update_content(error_msg)

        # 模拟回复流, 调试用
        # response = ""
        # chunks = [
        #     "# AI Response\nHere is a code snippet:\n",
        #     "```python\ndef hello():\n    print('world')\n```\n",
        #     "You can **click** this message to copy source text."
        # ]
        # for chunk in chunks:
        #     await asyncio.sleep(1)
        #     response += chunk
        #     ai_msg.update_content(response)
        #     chatwindow.scroll_end(animate=False)


        self.message_list.append({"role": "assistant", "content": full_response})
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


            usr_msg = Bubble('usr', message_usr)
            chatwindow = self.query_one("#chat-view", VerticalScroll)


            # usr_row = Horizontal(
            #     Static(classes='space-usr'),
            #     usr_msg,
            #     classes='message-row'
            # )
            chatwindow.mount(usr_msg)

            input_widget.text = ''
            usr_msg.scroll_visible()

            self.run_worker(self.get_response(chatwindow))



if __name__ == '__main__':
    app = ChatApp('deepseek-chat', 'test_session1', 'You are a helpful assistant.', '')
    app.run()
