async function showFlashcards(topic) {
  try {
      const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_API_KEY}`, {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify({
              contents: [{ parts: [{ text: `Create 5 flashcards for learning about ${topic}` }] }]
          })
      });

      const data = await res.json();
      const text = data?.candidates?.[0]?.content?.parts?.[0]?.text;

      if (text) {
          const cards = text.trim().split("\n").map(card => `<div class="flashcard">${card}</div>`).join('');
          document.getElementById('flashcards').innerHTML = `<h2>📚 Flashcards</h2>${cards}`;
      } else {
          document.getElementById('flashcards').innerHTML = `<h2>📚 Flashcards</h2><p>No flashcards available.</p>`;
      }
  } catch (error) {
      console.error('Error loading flashcards:', error);
      document.getElementById('flashcards').innerHTML = `<p>Flashcards generation failed!</p>`;
  }
}
