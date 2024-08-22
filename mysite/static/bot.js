function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
console.log("CSRF Token:", csrftoken);  // CSRF 토큰이 올바르게 출력되는지 확인

document.addEventListener('DOMContentLoaded', function () {
    // 페이지가 로드될 때 환영 메시지를 추가
    addMessage('Bot', '안녕하세요! 홍익대학교 챗봇 Hongik-gpt입니다:)<br>학교에 대해 궁금한 것을 물어보세요!');
    
    document.getElementById('question').addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
          event.preventDefault();
          askQuestion();
        }
    });
});

function addMessage(sender, message) {
    var chatBox = document.getElementById('chat-box');
    var messageDiv = document.createElement('div');
    
    messageDiv.classList.add('msg_box');
    messageDiv.classList.add(sender === 'You' ? 'send' : 'receive');
    messageDiv.innerHTML = `<span><strong>${sender}:</strong> ${message}</span>`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}


function askQuestion() {
  // 사용자 입력 값 가져오기
  var question = document.getElementById('question').value;
  var chatBox = document.getElementById('chat-box');
  document.querySelector("#form").question.value='';
  // 사용자 메세지 화면에 표시하기
  addMessage('You', question);

  // 서버에 POST 요청 보내기
  fetch('/dialog/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken  // 쿠키에서 가져온 CSRF 토큰 사용
      },
      body: new URLSearchParams({'question': question}) // 사용자 입력을 서버로 전송
  })  // 서버 응답 처리
      .then(response => response.json())
      .then(data => {
        // 두 가지의 선택 옵션 제공하는 경우
        if (data.button) {
          var buttonDiv = document.createElement('div');
          data.button.forEach(element => {
            const button = document.createElement('button');
            button.textContent = element;
            button.setAttribute('onclick', `handleButtonClick('${element}')`);
            buttonDiv.appendChild(button);
          });
          chatBox.appendChild(buttonDiv);
        } else {
          addMessage('Bot', data.answer);
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
}

// 사용자가 특정 옵션 버튼을 클릭한 경우
function handleButtonClick(option) {
  // 사용자가 클릭한 버튼 옵션을 대화창에 표시
    addMessage('You', option); // 사용자의 옵션을 질문처럼 처리
    fetch('/dialog/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrftoken  // 쿠키에서 가져온 CSRF 토큰 사용
      },
      body: new URLSearchParams({'question': option})
    })  // 서버로부터의 응답 json 형식
      .then(response => response.json())
      .then(data => {
        addMessage('Bot', data.answer);
      })
      .catch(error => {
        console.error('Error:', error);
      });
}
