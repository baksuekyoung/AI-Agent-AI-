# 📚 AI Library Assistant (AI 도서관 어시스턴트)

작은도서관 및 교육 현장의 효율적인 운영을 지원하기 위한 **AI 기반 데이터 관리 및 챗봇 어시스턴트 웹 서비스**입니다.

---

## 🛠️ Tech Stack

### Frontend
* HTML5, JavaScript (Vanilla JS)
* **Deployment:** Vercel ([Live Link](https://ai-agent-ai.vercel.app))

### Backend
* Python, FastAPI, Pydantic
* **Deployment:** Render ([API Docs](https://ai-agent-ai.onrender.com/docs))
* **Database:** Firebase Firestore

---

## ✨ Key Features

1. **도서관 데이터 관리 (CRUD)**
   * 운영 데이터(날짜, 값, 메모) 실시간 등록, 조회 및 관리
   * 프론트엔드와 백엔드 간 Pydantic 모델 검증을 통한 안정적인 데이터 통신 (`/api/data`)
2. **AI 도서관 어시스턴트 및 요약**
   * 등록된 데이터를 기반으로 한 AI 요약 및 트렌드 분석 기능
   * 실시간 질의응답이 가능한 AI 챗봇 인터페이스

---

## 🚀 Deployment Architecture

* **Frontend:** Vercel을 통해 정적 웹 파일 배포
* **Backend:** Render를 통해 FastAPI 서버 호스팅 및 자동 배포 연동 (`git push` 연동)

---

## 📁 Project Structure

```text
ai-library-assistant/
├── backend/
│   ├── main.py         # FastAPI 서버 메인 로직 및 데이터 모델 (DataItem)
│   ├── requirements.txt # Python 패키지 의존성 파일
│   └── .env            # 환경 변수 (Firebase, OpenAI API 등)
├── index.html          # 프론트엔드 메인 페이지
└── script.js           # API 통신 및 UI 인터랙션 로직
