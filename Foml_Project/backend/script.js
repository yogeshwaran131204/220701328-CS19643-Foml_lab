async function searchTopic() {
  const topic = document.getElementById('searchInput').value.trim();
  if (!topic) return;

  saveTopicToBackend(topic);
  fetchRecommendations(topic);
  showStudyNotes(topic);
  showFlashcards(topic);
  showQuiz(topic);
}

async function saveTopicToBackend(topic) {
  try {
      await fetch('http://localhost:5000/add_topic', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ topic })
      });
  } catch (error) {
      console.error('Error saving topic:', error);
  }
}

async function fetchRecommendations(topic) {
  try {
      const res = await fetch(`http://localhost:5000/recommend?query=${topic}`);
      const data = await res.json();
      document.getElementById('recommendations').innerHTML = `
          <h2>🔥 Recommended Topics:</h2>
          <ul>${data.recommendations.map(t => `<li>${t}</li>`).join('')}</ul>
      `;
  } catch (error) {
      console.error('Error fetching recommendations:', error);
  }
}
