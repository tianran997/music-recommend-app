
function searchSongs() {
    const query = document.getElementById("search-query").value;
    fetch(`/search?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById("search-results");
            resultsDiv.innerHTML = "";
            data.forEach(song => {
                const p = document.createElement("p");
                p.textContent = `${song.name} [${song.tags.join(', ')}]`;
                resultsDiv.appendChild(p);
            });
        });
}

document.getElementById("upload-form").addEventListener("submit", function(e) {
    e.preventDefault();
    const name = document.getElementById("song-name").value;
    const tags = document.getElementById("tags").value;

    const formData = new FormData();
    formData.append("name", name);
    formData.append("tags", tags);

    fetch("/upload", {
        method: "POST",
        body: formData
    }).then(() => {
        alert("Song uploaded!");
        searchSongs();
    });
});
