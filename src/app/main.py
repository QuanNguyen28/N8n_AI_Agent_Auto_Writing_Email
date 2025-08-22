from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Agent - Python Service")

# ---- Healthcheck ------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ---- Models -----------------------------------------------------------------
class ChatIn(BaseModel):
    user_id: str
    message: str

class EmailIn(BaseModel):
    to: str
    subject: str
    body: str

# ---- LLM mock: quyết định có gọi hàm send_email hay không -------------------
@app.post("/internal/llm-chat")
def llm_chat(payload: ChatIn):
    txt = payload.message.lower().strip()
    if "gửi email" in txt or "send email" in txt:
        # n8n sẽ đọc 'function_call' và nhánh TRUE sẽ gọi /internal/send-email
        return {
            "function_call": {
                "name": "send_email",
                "arguments": {
                    "to": "someone@example.com",
                    "subject": "Hello from agent",
                    "body": f"User {payload.user_id} asked to send an email."
                }
            }
        }
    # Không gọi hàm gì: trả lời text cho nhánh FALSE
    return {"reply": f"Bạn vừa nói: {payload.message}"}

# ---- Gửi email (mock) -------------------------------------------------------
@app.post("/internal/send-email")
def send_email(payload: EmailIn):
    # Hôm nay mock: chưa gửi thật, chỉ trả OK
    return {"ok": True, "sent_to": payload.to, "subject": payload.subject}
