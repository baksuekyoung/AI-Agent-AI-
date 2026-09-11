import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from openai import OpenAI

# 환경 변수 로드
load_dotenv()

# Firebase 초기화 및 안전한 db 객체 선언
cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON", "serviceAccountKey.json")
db = None

if not firebase_admin._apps:
    try:
        if os.path.exists(cred_path) and os.path.getsize(cred_path) > 0:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("🔥 Firebase 연결 성공!")
        else:
            print("⚠️ 경고: serviceAccountKey.json 파일이 비어있거나 없습니다. (오프라인 모드)")
    except Exception as e:
        print(f"⚠️ Firebase 초기화 중 오류 발생: {e}")

# 혹시 다른 곳에서 db를 호출할 때 에러가 나지 않도록 방어 코드 추가
if db is None:
    class DummyDB:
        def collection(self, *args, **kwargs):
            return self
        def document(self, *args, **kwargs):
            return self
        def get(self, *args, **kwargs):
            return None
        def set(self, *args, **kwargs):
            pass
        def add(self, *args, **kwargs):
            return (None, None)
    db = DummyDB()


# OpenAI 클라이언트 안전 초기화 (API 키가 없어도 에러 안 나게 방어)
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    openai_client = OpenAI(api_key=openai_api_key)
else:
    openai_client = None
    print("⚠️ 경고: OPENAI_API_KEY가 없습니다. AI 기능은 작동하지 않습니다.")

# 여기가 핵심입니다! (app 객체가 있어야 아래 라우터들이 에러 없이 등록됩니다)
app = FastAPI(title="Library AI Assistant API", version="1.0")

# CORS 설정 (프론트엔드에서의 연결 허용)
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic 모델 정의 ---
class DataItem(BaseModel):
    date: str
    visitors: int
    checkouts: int
    memo: Optional[str] = ""

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ConversationSaveRequest(BaseModel):
    conversation_id: Optional[str] = None
    messages: List[dict]


# --- 1. 데이터 API (CRUD + Summary) ---

@app.post("/api/data", status_code=201)
def create_data(item: DataItem):
    try:
        doc_ref = db.collection("data").document()
        doc_ref.set(item.dict())
        return {"id": doc_ref.id, "message": "데이터가 성공적으로 추가되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data")
def get_data_list():
    try:
        docs = db.collection("data").stream()
        result = []
        for doc in docs:
            d = doc.to_dict()
            d["id"] = doc.id
            result.append(d)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/data/{item_id}")
def update_data(item_id: str, item: DataItem):
    try:
        doc_ref = db.collection("data").document(item_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="데이터를 찾을 수 없습니다.")
        doc_ref.update(item.dict())
        return {"message": "데이터가 수정되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/data/{item_id}")
def delete_data(item_id: str):
    try:
        doc_ref = db.collection("data").document(item_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="데이터를 찾을 수 없습니다.")
        doc_ref.delete()
        return {"message": "데이터가 삭제되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data/summary")
def get_data_summary():
    try:
        docs = list(db.collection("data").stream())
        if not docs:
            return {
                "period": "데이터 없음",
                "count": 0,
                "metrics": {"total": 0, "average": 0, "max": 0, "min": 0},
                "trend": "데이터 없음"
            }

        visitors_list = []
        dates = []
        for doc in docs:
            d = doc.to_dict()
            visitors_list.append(d.get("visitors", 0))
            dates.append(d.get("date", ""))

        dates.sort()
        count = len(visitors_list)
        total = sum(visitors_list)
        avg = round(total / count, 1) if count > 0 else 0
        max_v = max(visitors_list) if visitors_list else 0
        min_v = min(visitors_list) if visitors_list else 0

        period = f"{dates[0]} ~ {dates[-1]}" if dates else "N/A"

        return {
            "period": period,
            "count": count,
            "metrics": {
                "total": total,
                "average": avg,
                "max": max_v,
                "min": min_v
            },
            "trend": "최근 방문/대출 추이 요약"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- 2. 대화 기록 API ---

@app.post("/api/conversations")
def save_conversation(req: ConversationSaveRequest):
    try:
        if req.conversation_id:
            doc_ref = db.collection("conversations").document(req.conversation_id)
            doc_ref.update({"messages": req.messages})
            conv_id = req.conversation_id
        else:
            doc_ref = db.collection("conversations").document()
            doc_ref.set({"messages": req.messages})
            conv_id = doc_ref.id
        return {"conversation_id": conv_id, "message": "대화가 저장되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations")
def get_conversations():
    try:
        docs = db.collection("conversations").stream()
        result = []
        for doc in docs:
            d = doc.to_dict()
            result.append({"id": doc.id, "messages": d.get("messages", [])})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/conversations/{conv_id}")
def delete_conversation(conv_id: str):
    try:
        db.collection("conversations").document(conv_id).delete()
        return {"message": "대화가 삭제되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- 3. AI 챗봇 API (컨텍스트 주입) ---

@app.post("/api/chat")
def chat_with_ai(req: ChatRequest):
    try:
        summary = get_data_summary()

        system_prompt = f"""
당신은 도안휴먼시아4단지 작은도서관 데이터 분석 비서입니다.

[데이터 요약]
- 데이터 기간: {summary['period']}
- 총 레코드 수: {summary['count']}건
- 주요 지표(방문객): 총합 {summary['metrics']['total']}명, 평균 {summary['metrics']['average']}명, 최대 {summary['metrics']['max']}명, 최소 {summary['metrics']['min']}명
- 최근 트렌드: {summary['trend']}

위 데이터를 기반으로 사용자의 질문에 친절하고 정확하게 맞춤형 답변을 제공하세요.
"""

        if openai_client is None:
            raise HTTPException(status_code=503, detail="OPENAI_API_KEY가 설정되지 않아 AI 기능을 사용할 수 없습니다.")

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.message}
            ],
            temperature=0.7
        )

        ai_reply = response.choices[0].message.content

        return {
            "reply": ai_reply,
            "summary_used": summary
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Library AI Assistant API"}