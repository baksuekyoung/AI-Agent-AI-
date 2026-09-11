# 📚 AI Library Assistant (도서관 AI 비서 서비스)

사용자의 시계열 데이터(도서관 이용 통계 등)를 분석 및 요약하여, 맞춤형 답변을 제공하는 Full-Stack AI 웹 서비스입니다.

## 🚀 서비스 소개
- 일반적인 ChatGPT와 달리, Firestore에 저장된 실제 도서관 운영 데이터를 시스템 프롬프트에 동적 컨텍스트로 주입하여 정밀하고 구체적인 답변을 제공합니다.
- 데이터 관리(CRUD)와 대화 기록 저장 기능을 지원합니다.

## 🛠 기술 스택
- **Backend**: FastAPI, Python, Firebase Firestore, OpenAI API
- **Frontend**: Vanilla HTML / CSS / JavaScript
- **Deployment**: Render (Backend), Vercel (Frontend)

## 🌐 배포 링크
- **프론트엔드 서비스 URL (Vercel)**: [여기에 Vercel 주소 입력]
- **백엔드 API 서버 URL (Render)**: https://ai-agent-ai.onrender.com
- **Swagger UI 문서**: https://ai-agent-ai.onrender.com/docs

## 💻 로컬 실행 방법
1. 백엔드 실행:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload