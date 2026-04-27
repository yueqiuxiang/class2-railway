from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from openai import OpenAI  # 这里改成新版的导入方式
import os

# 从环境变量读取 API Key
client = OpenAI(
    api_key=os.environ.get("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

app = FastAPI()

# 聊天页面
@app.get("/", response_class=HTMLResponse)
async def get_chat_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>AI聊天机器人</title>
    </head>
    <body>
        <h1>和AI聊天</h1>
        <form method="post">
            <input type="text" name="user_input" placeholder="请输入你的问题">
            <button type="submit">发送</button>
        </form>
    </body>
    </html>
    """

# 聊天接口（改成新版的调用方式）
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

# 启动配置
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)