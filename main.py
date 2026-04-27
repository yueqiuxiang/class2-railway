from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from openai import OpenAI
import os

# AI 配置
client = OpenAI(
    api_key=os.environ.get("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

app = FastAPI()


# 漂亮聊天框界面
@app.get("/", response_class=HTMLResponse)
async def get_chat_page():
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>AI聊天机器人</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }
        body {
            max-width: 800px;
            margin: 30px auto;
            padding: 0 20px;
            background: #f5f5f5;
        }
        .chat-box {
            width: 100%;
            height: 500px;
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow-y: auto;
        }
        .message {
            margin: 12px 0;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 75%;
            line-height: 1.5;
        }
        .user {
            background: #007bff;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        .ai {
            background: #e9e9eb;
            color: #333;
            margin-right: auto;
            text-align: left;
        }
        .input-form {
            display: flex;
            gap: 10px;
        }
        input {
            flex: 1;
            padding: 14px;
            border: 1px solid #ddd;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
        }
        button {
            padding: 14px 22px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background: #0056b3;
        }
    </style>
</head>
<body>
    <div class="chat-box" id="chatBox"></div>
    <form class="input-form" id="chatForm">
        <input type="text" id="userInput" placeholder="请输入你的问题..." autocomplete="off">
        <button type="submit">发送</button>
    </form>

    <script>
        const chatBox = document.getElementById('chatBox');
        const chatForm = document.getElementById('chatForm');
        const userInput = document.getElementById('userInput');

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = userInput.value.trim();
            if (!text) return;

            // 显示用户消息
            chatBox.innerHTML += `<div class='message user'>${text}</div>`;
            userInput.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            // 请求AI回复
            const res = await fetch('/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'user_input=' + encodeURIComponent(text)
            });

            const data = await res.text();
            const temp = document.createElement('div');
            temp.innerHTML = data;
            const reply = temp.querySelector('p:last-child').textContent.replace('AI：', '');

            // 显示AI消息
            chatBox.innerHTML += `<div class='message ai'>${reply}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        });
    </script>
</body>
</html>
    """


# 聊天逻辑（你原来的功能，完全不变）
@app.post("/", response_class=HTMLResponse)
async def chat(user_input: str = Form(...)):
    try:
        response = client.chat.completions.create(
            model="qwen-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content
        return f"""
        <h1>AI聊天机器人</h1>
        <p>你：{user_input}</p>
        <p>AI：{reply}</p>
        <a href="/">返回</a>
        """
    except Exception as e:
        return f"<p>出错了：{str(e)}</p><a href='/'>返回</a>"


# 启动（适配 Railway）
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)