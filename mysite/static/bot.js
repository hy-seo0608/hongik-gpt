const $chatBox = document.getElementById("chat-box");
const $question = document.querySelector("#question");
const $submitBtn = document.querySelector("#ask-button");
const webSocket = new WebSocket("ws://" + window.location.host + "/ws/dialog");
const $$buttons = document.querySelectorAll(".button");
const $feedback =document.querySelector("#feedback-form");
const modal=document.querySelector(".modal");
$feedback.addEventListener('submit',submitFeedback);

let $botsChat;
let md = 0;
let received = true;
let loadingDiv;	// 로딩 메세지 변수

// 피드백 테이블에 저장용
let currentUserQuestion = "";		// 사용자 질문
let currentBotResponse = ""; 		// 챗봇 응답

//button function
Array.from($$buttons).forEach((button) => {
	button.addEventListener("click", (event) => {
		submitMessage(event.target.textContent, md);
	});
});


//WebSocket methods START

//receive data from server
webSocket.onmessage = function (event) {
	received = true;
	const data = JSON.parse(event.data); 
	$botsChat.querySelector("#message").innerHTML = `<strong>Bot:</strong>${data.message}`;

	// 챗봇 답변 메세지
	currentBotResponse = data.message;  // 챗봇 응답 저장
	addMessage("Bot", data.message, data.responseId);	// responseId 추가(피드백)
	
	if (data.mode == 0) {
		md = 0;
	} else if (data.mode == 1) {
		// 학사일정
		md = 0;
		addButton(data.button, data.mode);
	} else if (data.mode == 2) {
		// 열람실 현황
		md = 2;
		addButton(data.button, data.mode);
	} else if (data.mode == 3) {
		// 연락처
		md = 3;
		addContactButton();
	}
};


//WebSocket closed unexpectedly
webSocket.onclose = function (event) {
	console.error("socket closed unexpectedly");
};

$question.onkeyup = function (event) {
	if (event.key === "Enter") {
		event.preventDefault();
		event.stopPropagation();
		$submitBtn.click();
	}
};

$submitBtn.onclick = function () {
	const message = $question.value;
	if (message === "") return;
	submitMessage(message, md);
};

function submitMessage(message, my_mode) {
	if (!received) return;
    received = false;
    addMessage("You", message);
    addLoading();
    webSocket.send(JSON.stringify({ message: message, mode: my_mode }));
	currentUserQuestion = message; // 사용자가 입력한 질문 저장
	$question.value = "";
}

//WebSocket methods END

function addMessage(sender, message, responseId = null) {
	const messageDiv = document.createElement("div");

	messageDiv.classList.add("msg_box");
	messageDiv.classList.add(sender === "You" ? "send" : "receive");
	//messageDiv.innerHTML = `<span><strong>${sender}:</strong> ${message}</span>`;
	
	// 챗봇 응답에 피드백 버튼 추가
    if (sender === "Bot") {
        const feedbackButton = addFeedbackButton(responseId);
        feedbackButton.classList.add("feedback-button");
        messageDiv.appendChild(feedbackButton);
    }

    $chatBox.appendChild(messageDiv);
    $chatBox.scrollTop = $chatBox.scrollHeight;
}


// 피드백 서버로 전달
function submitFeedback(event) {
	event.preventDefault();
    const feedbackText = document.getElementById("feedback-text").value;
    const responseId = document.getElementById("feedback-form").dataset.responseId; // 모달에 저장된 responseId 가져오기
	
	// 디버그 출력
    console.log("user_question:", currentUserQuestion);
    console.log("model_answer:", currentBotResponse);

    fetch("dialog/feedback/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // CSRF 토큰 추가
        },
        body: JSON.stringify({
            user_desired_answer: feedbackText,  	// 사용자가 입력한 피드백
            responseId: responseId, 	// 서버로 responseId 전달
			user_question: currentUserQuestion, // 사용자 질문
			model_answer: currentBotResponse 	// 챗봇 응답
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "피드백을 주셔서 감사합니다!") {
            alert(data.message);  // 피드백 성공 메시지 표시
            closeFeedbackModal(); // 모달 창 닫기
        } else {
            alert("피드백 전송에 실패했습니다.");
        }
    })
    .catch(error => {
        console.error("Error submitting feedback:", error);
    });
}


// 모달 창 열기 함수
function openFeedbackModal(responseId) {
    document.getElementById("feedback-modal").style.display = "block";
	modal.dataset.responseId = responseId;  // responseId 저장
}

// 모달 창 닫기 함수
function closeFeedbackModal() {
    document.getElementById("feedback-modal").style.display = "none";
	document.getElementById("feedback-text").value = ""; // 피드백 내용 초기화
}

function addFeedbackButton(responseId) {
	const feedbackButton = document.createElement("button");
	feedbackButton.className = "feedback-button";
	feedbackButton.textContent = "피드백";
	feedbackButton.onclick = function () {
		openFeedbackModal(responseId);
	};
	return feedbackButton;
}

function addLoading() {
	const loadingDiv = document.createElement("div");
	loadingDiv.classList.add("msg_box");
	loadingDiv.classList.add("receive");
	loadingDiv.innerHTML = `<span id="message"><strong>Bot:</strong><div>로딩 중 인데용</div><div id ="loading-spinner"></div><span> `;
	$chatBox.appendChild(loadingDiv);
	$chatBox.scrollTop = $chatBox.scrollHeight;
	$botsChat = loadingDiv;
}

function addButton(button_list, mode) {
    const buttonDiv = document.createElement("div");
    button_list.forEach((element) => {
        const button = document.createElement("button");
        button.textContent = element;
        button.onclick = function () {
            handleButtonClick(element, mode);
        };
        buttonDiv.appendChild(button);
    });
    $chatBox.appendChild(buttonDiv);
    $chatBox.scrollTop = $chatBox.scrollHeight;
}

// 사용자가 특정 옵션 버튼을 클릭한 경우
function handleButtonClick(option, mode) {
	// 사용자가 클릭한 버튼 옵션을 대화창에 표시
	submitMessage(option, mode);
}

function addContactButton() {
	const buttonDiv = document.createElement("div");

	const button1 = document.createElement("button");
	button1.textContent = "교직원/교수 연락처";
	button1.onclick = function () {
		addMessage("Bot", "검색하고 싶은 교직원/교수를 입력해주세요");
		md = 3;
	};

	const button2 = document.createElement("button");
	button2.textContent = "학과 연락처";
	button2.onclick = function () {
		addMessage("Bot", "검색하고 싶은 학과를 입력해주세요");
		md = 3;
	};

	buttonDiv.appendChild(button1);
	buttonDiv.appendChild(button2);
	$chatBox.appendChild(buttonDiv);
	$chatBox.scrollTop = $chatBox.scrollHeight;
}


