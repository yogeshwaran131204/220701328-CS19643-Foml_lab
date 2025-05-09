const YT_API_KEY = "AIzaSyDkBGdyvDcRtq8HhGbVB1MU0wl1CDOshh8";

async function showYouTubeVideos(topic) {
  const res = await fetch(`https://www.googleapis.com/youtube/v3/search?key=${YT_API_KEY}&q=${encodeURIComponent(topic)}&part=snippet&type=video&maxResults=5`);
  const data = await res.json();

  const videos = data.items
    .filter(item => item.id.kind === "youtube#video")
    .map(video => `
      <div class="card">
        <iframe width="100%" height="200" src="https://www.youtube.com/embed/${video.id.videoId}" frameborder="0" allowfullscreen></iframe>
        <p><strong>${video.snippet.title}</strong></p>
      </div>
    `).join("");

  document.getElementById("youtubeVideos").innerHTML = `
    <section>
      <h2>🎥 YouTube Videos</h2>
      ${videos}
    </section>
  `;
}
