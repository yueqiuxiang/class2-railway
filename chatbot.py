from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from openai import OpenAI
import os

# 你的AI配置
client = OpenAI(
    api_key=os.environ.get("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

app = FastAPI()

# 客服提示词（和你调试界面一模一样）
SYSTEM_PROMPT = """你是一个家护家电产品客服，请依据知识库准确的回复用户的问题，关联知识库回答，不要胡编乱造，不知道的信息就说不知道，这个是家护家电产品的客服。"""

# 页面：和你调试界面一样的聊天机器人
@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>家电客服机器人</title>
        <style>
            body{max-width:700px;margin:30px auto;font-family:Arial}
            .chat{border:1px solid #ddd;padding:20px;border-radius:10px;height:400px;overflow-y:auto;background:#f9f9f9}
            .msg{margin:10px 0;padding:10px;border-radius:8px}
            .user{background:#e3f2fd;text-align:right}
            .ai{background:#f1f1f1}
            input{width:80%;padding:12px;border:1px solid #ddd;border-radius:8px}
            button{padding:12px 20px;background:#0d6efd;color:white;border:none;border-radius:8px;cursor:pointer}
        </style>
    </head>
    <body>
        <h2>家电客服机器人</h2>
        <div class="chat" id="chat"></div>
        <br>
        <input id="input" placeholder="输入问题...">
        <button onclick="send()">发送</button>

        <script>
            async function send(){
                let input = document.getElementById("input");
                let text = input.value.trim();
                if(!text) return;

                let chat = document.getElementById("chat");
                chat.innerHTML += `<div class='msg user'>你：${text}</div>`;
                input.value = "";

                let res = await fetch("/chat", {
                    method:"POST",
                    headers:{"Content-Type":"application/x-www-form-urlencoded"},
                    body:"user_input="+encodeURIComponent(text)
                });
                let reply = await res.text();
                chat.innerHTML += `<div class='msg ai'>AI：${reply}</div>`;
                chat.scrollTop = chat.scrollHeight;
            }
        </script>
    </body>
    </html>
    """

# 聊天接口
@app.post("/chat")
async def chat_response(user_input: str = Form(...)):
    try:
        response = client.chat.completions.create(
            model="qwen-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"出错：{str(e)}"

# 启动
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)