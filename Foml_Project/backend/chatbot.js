async function sendMessage() {
  const input = document.getElementById('chatInput').value.trim();
  if (!input) return;

  const chatbox = document.getElementById('chatbox');
  chatbox.innerHTML += `<div class="user">You: ${input}</div>`;

  try {
      const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_API_KEY}`, {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify({
              contents: [{ parts: [{ text: `Be as a tutor and Answer: ${input}` }] }]
          })
      });

      const data = await res.json();
      const botReply = data?.candidates?.[0]?.content?.parts?.[0]?.text;

      chatbox.innerHTML += `<div class="bot">Bot: ${botReply || "Sorry, I couldn't understand."}</div>`;
      document.getElementById('chatInput').value = "";
  } catch (error) {
      console.error('Error chatting with bot:', error);
      chatbox.innerHTML += `<div class="bot">Bot: Sorry, something went wrong!</div>`;
  }
}
