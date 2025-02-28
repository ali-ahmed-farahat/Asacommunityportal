const chatbox = document.getElementById("chatbox");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const loaderContainer = document.getElementById("loader-container");
const chatContainer = document.getElementById("chat-container");
const loaderText = document.getElementById("loader-text");

// 🎬 Word-by-Word Animation Loader
const words = ["المساعد", "الرقابي", "الذكي"];
let wordIndex = 0;

function typeWords() {
    if (wordIndex < words.length) {
        loaderText.innerHTML += `${words[wordIndex]} `;
        wordIndex++;
        setTimeout(typeWords, 700);
    } else {
        setTimeout(() => {
            loaderContainer.style.display = "none";
            chatContainer.style.display = "flex";
        }, 1000);
    }
}
window.onload = typeWords;

// 🖱️ Auto-scroll function
function scrollToBottom() {
    chatbox.scrollTop = chatbox.scrollHeight;
}

// 💬 Chat Functionality
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
});

function appendMessage(sender, message, isLoading = false) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);

    if (isLoading) {
        msgDiv.innerHTML = `<span class="loader"></span>`;
    } else {
        msgDiv.innerHTML = `${marked.parse(message)}`;
    }
    chatbox.appendChild(msgDiv);
    scrollToBottom();  // ✅ Always scroll down when new message added
    return msgDiv;
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage("user", message);
    userInput.value = "";

    const botMsgDiv = appendMessage("bot", "", true);

    const response = await fetch("/get_response", {
        method: "POST",
        body: JSON.stringify({ message }),
        headers: { "Content-Type": "application/json" }
    }).then(res => res.json());

    botMsgDiv.innerHTML = `${marked.parse(response.response)}`;
    scrollToBottom();  // ✅ Ensure latest message is visible
}
