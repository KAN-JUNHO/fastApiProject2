from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import openai

app = FastAPI()

openai.api_key = "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"
templates = Jinja2Templates(directory="templates")

messages = [{"role": "system", "content": "이미지 생성 챗봇에 오신 것을 환영합니다!"}]

@app.get("/")
def read_root():
    return templates.TemplateResponse("index.html", {"request": {}, "messages": messages})

@app.post("/chat/")
async def chat_response(request: Request, user_message: str = Form(...)):
    global messages
    messages.append({"role": "user", "content": user_message})
    print(messages)
    try:
        response = openai.Image.create(
            prompt=user_message,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        messages.append({"role": "assistant", "content": "다음은 요청하신 이미지입니다:", "image_url": image_url})
    except Exception as e:
        messages.append({"role": "assistant", "content": f"오류: {e}"})

    return templates.TemplateResponse("index.html", {"request": request, "messages": messages})

