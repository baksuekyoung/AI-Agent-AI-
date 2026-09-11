# 📚 도서관 AI 비서 & 데이터 관리

작은도서관의 방문객·대출 데이터를 관리하고, AI 챗봇에게 데이터에 대해 질문할 수 있는 웹 서비스입니다.

![도서관 AI 비서](./도서관%20ai%20비서.PNG)

## ✨ 주요 기능

- **AI 챗봇**: "이번 달 방문객 어때?" 같은 질문에 저장된 데이터를 바탕으로 답변
- **데이터 관리(CRUD)**: 날짜별 방문객 수 / 대출 건수 / 메모 추가·조회·삭제
- **요약 카드**: 전체 기간, 총 레코드 수, 일평균·최대 방문객 자동 계산

## 🛠 기술 스택

| 영역 | 기술 |
|---|---|
| Frontend | HTML, CSS, Vanilla JavaScript |
| Backend | Python, FastAPI |
| 데이터 저장 | JSON 파일 (`backend/data.json`, 서버 실행 시 자동 생성) |

## 📁 폴더 구조

```
.
├── frontend/
│   ├── index.html      # 화면 UI
│   └── script.js        # API 호출 로직
├── backend/
│   ├── main.py           # FastAPI 서버 (API 엔드포인트)
│   └── requirements.txt
└── README.md
```

## 🔌 API 명세

| Method | 경로 | 설명 |
|---|---|---|
| GET | `/api/data` | 전체 데이터 목록 조회 |
| POST | `/api/data` | 데이터 추가 (`date`, `visitors`, `checkouts`, `memo`) |
| DELETE | `/api/data/{id}` | 데이터 삭제 |
| GET | `/api/data/summary` | 기간·평균·최대값 요약 |
| POST | `/api/chat` | AI 챗봇에게 질문 (`message`) |

## 🚀 로컬에서 실행하기

### 1) 백엔드 실행

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

정상 실행되면 `http://localhost:8000` 에서 API가 동작합니다.

### 2) 프론트엔드 실행

`frontend/index.html` 파일을 브라우저로 바로 열면 됩니다.
(예: VS Code의 Live Server 확장 사용, 또는 `python -m http.server` 로 `frontend` 폴더를 서빙)

> `frontend/script.js` 상단의 `API_BASE_URL` 이 `http://localhost:8000` 으로 되어 있어야 로컬 백엔드와 연결됩니다.

## ☁️ 배포 방법

### 백엔드 → Render

1. [Render](https://render.com) 에 GitHub 저장소 연동
2. **New Web Service** 생성, Root Directory를 `backend` 로 지정
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. 배포가 끝나면 발급된 URL(예: `https://your-app.onrender.com`)을 복사

### 프론트엔드 → GitHub Pages / Vercel / Netlify

1. `frontend/script.js` 상단의 `API_BASE_URL` 값을 위에서 발급받은 Render URL로 변경
   ```js
   const API_BASE_URL = "https://your-app.onrender.com";
   ```
2. 변경 사항을 커밋 후, GitHub Pages(저장소 Settings → Pages) 또는 Vercel/Netlify에 `frontend` 폴더를 배포

## ⚠️ 참고 (백엔드 코드 복구 안내)

기존 저장소의 `backend` 폴더가 Git 서브모듈로 잘못 연결되어 있어 실제 코드가 비어 있는 상태였습니다.
이 저장소에 포함된 `backend/main.py` 는 프론트엔드(`script.js`)가 호출하는 API 규격에 맞춰 새로 작성된 기본 버전입니다.
기존에 작성해두었던 백엔드 로직(특히 AI 챗봇 응답 부분)이 따로 있다면, `chat()` 함수 부분만 교체해서 사용하시면 됩니다.
