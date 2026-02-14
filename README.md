# DS Assistant CLI (CN)

![demo](demo.gif)

一个 Linux 平台下在终端调用 Deepseek API 的脚本, 主要让 DS 承担 AI 学术助手的工作. v3.0版使用`Textual`库重写了代码.

## 重大调整
1. 删除字典功能, 因为 AI 输出格式不稳定, 现有字典 API 基本都要收费, 爬虫也容易出网络问题.
2. 添加聊天气泡, 用户和 AI 的文本通过`Rich`库渲染为 Markdown 格式, 可以单击气泡进入复制模式.

## 开始

### 环境需求
要求 Python3 安装以下库:
```
openai
textual
rich
pyperclip
```

### 安装

1. 克隆此仓库: `git clone https://github.com/PupilEarthquake/DS_Assistant_CLI.git`.
2. 进入此文件夹: `cd /Path/to/DS_Assistant_CLI`.
3. 在 `ds.py` 首行添加你的 Python 路径, 比如 `#!/home/pupilearthquake/anaconda3/envs/AI/bin/python`.
4. 添加可执行权限: `chmod +x ds.py`.
5. 创建符号链接: `sudo ln -s /path/to/your/ds.py /usr/local/bin/ds`, 注意`/path/to/your/ds.py`必须是绝对路径.


### 配置文件

1. 在 `user.conf` 中填入你的 API key.


## 使用方法


1. `ds -h`: 显示帮助.
2. `ds ce`: 中译英.
    - `ds ce -t` 使用推理模型. 默认使用快速模型.
    - `ds ce -m` 要求 DS 对一个中文句子给出3种翻译.
    - `ds ce -h` 显示帮助, __其他模块同理__.
3. `ds ec`: 英译中.
    - `ds ec -s` 要求 DS 分析句式结构.
6. `ds chat`: 一般聊天.
7. 聊天记录可见和`ds.py`同目录的 `chathist`文件夹 , 若不需要历史记录可以手动删除.



# DS Assistant CLI (EN)

This is a script for calling the Deepseek API from the terminal on Linux, primarily for using DS as an AI academic assistant. Version 3.0 rewrites the code using the `Textual` library.

## Major Updates
1. Removed the dictionary feature. AI output formats are unstable, existing dictionary APIs are mostly paid, and web scraping often encounters network issues.
2. Added chat bubbles. Text from users and the AI is rendered as Markdown via the `Rich` library. Clicking on a bubble enters copy mode.

## Getting Started

### Environment
Requires Python3 and the following libraries installed:
```
openai
textual
rich
pyperclip
```

### Installation

1. Clone this repository: `git clone https://github.com/PupilEarthquake/DS_Assistant_CLI.git`.
2. Navigate to the folder: `cd /Path/to/DS_Assistant_CLI`.
3. Add your Python path at the beginning of `ds.py`, e.g., `#!/home/pupilearthquake/anaconda3/envs/AI/bin/python`.
4. Add execute permissions: `chmod +x ds.py`.
5. Create a symbolic link: `sudo ln -s /path/to/your/ds.py /usr/local/bin/ds`. Note: `/path/to/your/ds.py` must be an absolute path.

### Configuration File

1. Enter your API key in `user.conf`.

## Usage

1. `ds -h`: Display help.
2. `ds ce`: Chinese to English translation.
   - `ds ce -t` Use the reasoning model. The fast model is used by default.
   - `ds ce -m` Request DS to provide three translations for a Chinese sentence.
   - `ds ce -h` Display help. __Other modules follow the same principle.__
3. `ds ec`: English to Chinese translation.
   - `ds ec -s` Request DS to analyze sentence structure.
6. `ds chat`: General chat.
7. Chat history can be found in the `chathist` folder in the same directory as `ds.py`. You can manually delete it if no history is needed. 

