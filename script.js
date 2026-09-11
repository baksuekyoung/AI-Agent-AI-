const API_BASE_URL = "http://localhost:8000"; // 배포 시 Render URL로 변경

// 페이지 로드 시 실행
window.onload = function() {
    loadSummary();
    loadDataList();
};

// 1. 데이터 요약 로드
async function loadSummary() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/data/summary`);
        const data = await res.json();
        document.getElementById("summaryCard").innerHTML = `
            <b>[데이터 요약]</b> 기간: ${data.period} | 총 레코드: ${data.count}개<br>
            일평균 방문객: ${data.metrics.average}명 (최대: ${data.metrics.max}명)
        `;
    } catch (e) {
        document.getElementById("summaryCard").innerText = "요약 정보를 불러오지 못했습니다.";
    }
}

// 2. AI 채팅 전송
async function sendMessage() {
    const input = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");
    const text = input.value.trim();
    if (!text) return;

    // 유저 메시지 표시
    chatBox.innerHTML += `<div class="msg user"><b>나:</b> ${text}</div>`;
    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    // 로딩 표시
    const loadingId = "loading_" + Date.now();
    chatBox.innerHTML += `<div id="${loadingId}" class="msg ai"><b>AI:</b> 답변 생성 중...</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const res = await fetch(`${API_BASE_URL}/api/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        
        // 로딩 삭제 및 AI 답변 표시
        document.getElementById(loadingId).remove();
        chatBox.innerHTML += `<div class="msg ai"><b>AI:</b> ${data.reply}</div>`;
    } catch (e) {
        document.getElementById(loadingId).remove();
        chatBox.innerHTML += `<div class="msg ai" style="color:red;"><b>AI:</b> 오류가 발생했습니다.</div>`;
    }
    chatBox.scrollTop = chatBox.scrollHeight;
}

// 3. 데이터 목록 조회 및 표시
async function loadDataList() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/data`);
        const items = await res.json();
        const tbody = document.querySelector("#dataTable tbody");
        tbody.innerHTML = "";
        
        items.slice(0, 20).forEach(item => { // 상위 20개만 표시
            tbody.innerHTML += `
                <tr>
                    <td>${item.date}</td>
                    <td>${item.visitors}</td>
                    <td>${item.checkouts}</td>
                    <td><button onclick="deleteData('${item.id}')" style="background:#dc3545; padding:2px 5px; font-size:0.75rem;">삭제</button></td>
                </tr>
            `;
        });
    } catch (e) {
        console.error("데이터 로드 실패", e);
    }
}

// 4. 데이터 추가
async function addData() {
    const date = document.getElementById("inputDate").value;
    const visitors = parseInt(document.getElementById("inputVisitors").value);
    const checkouts = parseInt(document.getElementById("inputCheckouts").value);
    const memo = document.getElementById("inputMemo").value;

    if (!date || isNaN(visitors) || isNaN(checkouts)) {
        alert("날짜, 방문객, 대출건수를 올바르게 입력해주세요.");
        return;
    }

    await fetch(`${API_BASE_URL}/api/data`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ date, visitors, checkouts, memo })
    });

    // 서버에 데이터 전송 완료 후
    await fetch(`${API_BASE_URL}/api/data`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ date, visitors, checkouts, memo })
    });

    // ✨ 알림을 띄우기 전에 화면 표에 바로 추가하기
    const tableBody = document.querySelector("table tbody") || document.getElementById("dataTable"); // 표의 tbody 선택
    if (tableBody) {
        const newRow = document.createElement("tr");
        newRow.innerHTML = `<td>${date}</td><td>${visitors}</td><td>${checkouts}</td><td>${memo}</td>`;
        tableBody.appendChild(newRow);
    }

    alert("추가되었습니다!");
}

// 5. 데이터 삭제
async function deleteData(id) {
    if (!confirm("정말 삭제하시겠습니까?")) return;
    await fetch(`${API_BASE_URL}/api/data/${id}`, { method: "DELETE" });
    loadDataList();
    loadSummary();
}