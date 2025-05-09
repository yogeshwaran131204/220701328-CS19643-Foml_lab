async function showQuiz(topic) {
  try {
      const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_API_KEY}`, {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify({
              contents: [{ parts: [{ text: `Create 5 MCQ quiz questions about ${topic}` }] }]
          })
      });

      const data = await res.json();
      const text = data?.candidates?.[0]?.content?.parts?.[0]?.text;

      if (text) {
          const questions = text.trim().split("\n").map(q => `<li>${q}</li>`).join('');
          document.getElementById('quiz').innerHTML = `<h2>🧠 Quiz</h2><ul>${questions}</ul>`;
      } else {
          document.getElementById('quiz').innerHTML = `<h2>🧠 Quiz</h2><p>No quiz available.</p>`;
      }
  } catch (error) {
      console.error('Error loading quiz:', error);
      document.getElementById('quiz').innerHTML = `<p>Quiz generation failed!</p>`;
  }
}
