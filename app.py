from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from openai import OpenAI

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# 配置大模型（把这里换成你自己的真实API Key）
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
api_key = "sk-dfba4304557541baac5b7a0af2db668c"

client = OpenAI(
    api_key=api_key,
    base_url=QWEN_BASE_URL
)

# 打开网页
@app.get("/")
async def index():
    return FileResponse("static/index.html")

# 聊天接口
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    question = data.get("question", "")

    response = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": question}]
    )
    answer = response.choices[0].message.content
    return {"answer": answer}

# 启动服务器（关键！不能丢！）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)