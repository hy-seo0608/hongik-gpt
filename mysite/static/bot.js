const $chatBox = document.getElementById("chat-box");
const $question = document.querySelector("#question");
const $submitBtn = document.querySelector("#ask-button");
const webSocket = new WebSocket("ws://" + window.location.host + "/ws/dialog");
const $$buttons = document.querySelectorAll(".button");
let $botsChat;
let md = 0;
let received = true;

const buttonQuestion = [
	"학식을 알려줘",
	"편의시설이 궁금해",
	"연락처 검색을 하고 싶어",
	"학사일정 알려줘",
	"공지사항 올라온 거 있어?",
	"홍대 주변 날씨는 어떄?",
	"홍대 기본 상식을 알려줘",
	"졸업 요건 검색을 해줘",
	"지금 열람실 현황은 어떄?",
];
//button function
Array.from($$buttons).forEach((button) => {
	button.addEventListener("click", (event) => {
		const index = parseInt(event.target.id);
		console.log(buttonQuestion[index]);
		submitMessage(buttonQuestion[index], md);
	});
});

//WebSocket methods START

//receive data from server
webSocket.onmessage = function (event) {
	received = true;
	const data = JSON.parse(event.data);
	$botsChat.querySelector("#message").innerHTML = `<strong>Bot:</strong>${data.message}`;
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
	$question.value = "";
}
//WebSocket methods END

function addLoading() {
	const loadingDiv = document.createElement("div");
	loadingDiv.classList.add("msg_box");
	loadingDiv.classList.add("receive");
	loadingDiv.innerHTML = `<span id="message"><strong>Bot:</strong><div>로딩 중 인데용</div><div id ="loading-spinner"></div><span> `;
	$chatBox.appendChild(loadingDiv);
	$chatBox.scrollTop = $chatBox.scrollHeight;
	$botsChat = loadingDiv;
}

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
