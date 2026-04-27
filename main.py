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

# 极简首页，无任何复杂JS，百分百能加载
@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
    <head>
        <meta charset="utf-8">
        <title>AI聊天机器人</title>
    </head>
    <body>
        <h2>AI聊天机器人</h2>
        <form method="post">
            <input name="user_input" placeholder="输入问题">
            <button>发送</button>
        </form>
    </body>
    </html>
    """

# 聊天接口
@app.post("/", response_class=HTMLResponse)
async def chat(user_input: str = Form(...)):
    res = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    ans = res.choices[0].message.content
    return f"""
    <h2>AI聊天机器人</h2>
    <p>你：{user_input}</p>
    <p>AI：{ans}</p>
    <a href="/">返回</a>
    """

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)