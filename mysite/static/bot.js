const $chatBox = document.getElementById("chat-box");
const $question = document.querySelector("#question");
const $submitBtn = document.querySelector("#ask-button");
const webSocket = new WebSocket("ws://" + window.location.host + "/ws/dialog");
const $$buttons = document.querySelectorAll(".button");
let md = 0;
let received = true;
//button function
Array.from($$buttons).forEach((button) => {
	button.addEventListener("click", (event) => {
		submitMessage(event.target.textContent);
	});
});

//WebSocket methods START

//receive data from server
webSocket.onmessage = function (event) {
	received = true;
	const data = JSON.parse(event.data);
	if (data.mode == 0) {
		md = 0;
		addMessage("Bot", data.message);
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
	submitMessage(message);
};

function submitMessage(message) {
	if (!received) return;
	received = false;
	addMessage("You", message);
	webSocket.send(JSON.stringify({ message: message, mode: md }));
	$question.value = "";
}
//WebSocket methods END

function addMessage(sender, message) {
	const messageDiv = document.createElement("div");

	messageDiv.classList.add("msg_box");
	messageDiv.classList.add(sender === "You" ? "send" : "receive");
	messageDiv.innerHTML = `<span><strong>${sender}:</strong> ${message}</span>`;
	$chatBox.appendChild(messageDiv);
	$chatBox.scrollTop = $chatBox.scrollHeight;
}

function addButton(button_list, mode) {
	const buttonDiv = document.createElement("div");

	button_list.forEach((element) => {
		const button = document.createElement("button");

		button.textContent = element;
		button.onclick = function () {
			handleButtonClick(element, mode);
			console.log(element, mode);
		};
		buttonDiv.appendChild(button);
		$chatBox.appendChild(buttonDiv);
		$chatBox.scrollTop = $chatBox.scrollHeight;
	});
}

// 사용자가 특정 옵션 버튼을 클릭한 경우
function handleButtonClick(option, mode) {
	// 사용자가 클릭한 버튼 옵션을 대화창에 표시
	addMessage("You", option); // 사용자의 옵션을 질문처럼 처리
	webSocket.send(JSON.stringify({ message: option, mode: mode }));
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