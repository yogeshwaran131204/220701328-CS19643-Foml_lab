async function showStudyNotes(topic) {
    try {
        document.getElementById('studyNotes').innerHTML = `<h2>📝 Study Notes</h2><p>Loading...</p>`;

        const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_API_KEY}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                contents: [{ parts: [{ text: `Explain about ${topic} in detailed study notes.` }] }]
            })
        });

        const data = await res.json();
        const text = data?.candidates?.[0]?.content?.parts?.[0]?.text;

        if (text) {
            document.getElementById('studyNotes').innerHTML = `
                <h2>📝 Study Notes for ${topic}</h2>
                <p>${text}</p>
            `;
        } else {
            document.getElementById('studyNotes').innerHTML = `<p>Failed to load study notes!</p>`;
        }
    } catch (error) {
        console.error('Error loading study notes:', error);
        document.getElementById('studyNotes').innerHTML = `<p>Error loading study notes!</p>`;
    }
}
