from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from openai import OpenAI
import os

# 从环境变量读取 API Key
client = OpenAI(
    api_key=os.environ.get("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

app = FastAPI()

# 带精美聊天框的首页
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
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: "微软雅黑",Arial,sans-serif;
        }
        body {
            max-width: 850px;
            margin: 40px auto;
            padding: 0 20px;
            background-color: #f4f5f7;
        }
        h1 {
            text-align: center;
            color: #222;
            margin-bottom: 20px;
            font-size: 28px;
        }
        .chat-container {
            width: 100%;
            height: 520px;
            background: #ffffff;
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            overflow-y: auto;
        }
        .msg-item {
            margin: 15px 0;
            max-width: 75%;
            line-height: 1.6;
            padding: 12px 18px;
            border-radius: 20px;
        }
        .user-msg {
            background-color: #1677ff;
            color: #fff;
            margin-left: auto;
        }
        .ai-msg {
            background-color: #e8e8eb;
            color: #333;
            margin-right: auto;
        }
        .send-box {
            display: flex;
            gap: 12px;
        }
        #userInput {
            flex: 1;
            padding: 15px 20px;
            border: 1px solid #ddd;
            border-radius: 30px;
            font-size: 16px;
        }
        #sendBtn {
            padding: 15px 30px;
            background-color: #1677ff;
            color: #fff;
            border: none;
            border-radius: 30px;
            font-size: 16px;
            cursor: pointer;
        }
        #sendBtn:hover {
            background-color: #0958d9;
        }
    </style>
</head>
<body>
    <h1>AI聊天机器人</h1>
    <div class="chat-container" id="chatBox"></div>
    <div class="send-box">
        <input type="text" id="userInput" placeholder="请输入你的问题..." autocomplete="off">
        <button id="sendBtn">发送</button>
    </div>

    <script>
        const chatBox = document.getElementById("chatBox");
        const userInput = document.getElementById("userInput");
        const sendBtn = document.getElementById("sendBtn");

        // 发送消息
        async function sendMessage(){
            let text = userInput.value.trim();
            if(!text) return;

            // 展示用户消息
            chatBox.innerHTML += `<div class="msg-item user-msg">${text}</div>`;
            userInput.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;

            // 提交请求
            let res = await fetch("/",{
                method:"POST",
                headers:{"Content-Type":"application/x-www-form-urlencoded"},
                body:"user_input="+encodeURIComponent(text)
            });
            let html = await res.text();
            let reply = html.split("AI：")[1].split("<a")[0];

            // 展示AI回复
            chatBox.innerHTML += `<div class="msg-item ai-msg">${reply}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        sendBtn.addEventListener("click",sendMessage);
        userInput.addEventListener("keydown",e=>e.key==="Enter"&&sendMessage());
    </script>
</body>
</html>
    """

# 聊天接口 完全保留你原来的代码
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

# Railway 专用启动
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)