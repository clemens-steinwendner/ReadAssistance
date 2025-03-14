function showPopover(wordE1, pinyin, translation) {
    let popup = document.getElementById("popup");

    if (!popup) {
        popup = document.createElement("div");
        popup.id = "popup";
        popup.style.position = "absolute";
        popup.style.backgroundColor = "white";
        popup.style.border = "1px solid #333";
        popup.style.padding = "6px";
        popup.style.borderRadius = "4px";
        popup.style.boxShadow = "0 2px 8px rgba(0,0,0,0.2)";
        popup.style.display = "none";

        document.body.appendChild(popup)
    }

    popup.innerHTML = `
        <strong> Pinyin: </strong> ${pinyin}<br>
        <strong> Translation: </strong> ${translation}`;

    const rect = wordE1.getBoundingClientRect();
    popup.style.left = (rect.left + window.scrollX) + "px";
    popup.style.top = (rect.bottom + window.scrollY + 5) + "px";

    popup.style.display = "block";
}

function attachWordListeners() {
    document.querySelectorAll('.word').forEach(wordE1 => {
        wordE1.addEventListener('click', () => {

            document.querySelectorAll('.word').forEach(e1 => {
                e1.classList.remove('highlight');
            })

            wordE1.classList.add('highlight');

            const pinyin = wordE1.dataset.pinyin;
            const translation = wordE1.dataset.translation;

            const word = wordE1.dataset.word;

            if (pinyin && translation) {
                showPopover(wordE1, pinyin, translation);
            } else {
                showPopover(wordE1, "loading...", "loading...");
            }
        })
    })
}

function fullTranslate() {
    fetch('/translate_story')
        .then(response => response.json())
        .then(data => {
            const sentences = data.sentences

            let html = sentences.map(s => {
                return `
                    <div class="sentence-block" style="position: relative; margin-bottom: 1em;">
                        <span class="english-sentence" style="margin: 0;">${s}</span>
                        <span class="cover">
                        </span>
                    </div>
                `;
            }).join('');

            document.getElementById("story-translated").innerHTML = html;

            document.querySelectorAll('.cover').forEach(coverEl => {
                coverEl.addEventListener('click', () => {
                    if (coverEl.style.display !== 'none') {
                        coverEl.style.display = 'none';
                    }
                });
            });
            document.querySelectorAll('.english-sentence').forEach(sentEl => {
                sentEl.addEventListener('click', () => {
                    const coverEl = sentEl.parentNode.querySelector('.cover');
                    if (coverEl && coverEl.style.display === 'none') {
                        coverEl.style.display = 'block';
                    }
                });
            });
        })
        .catch(error => console.error("Error in fullTranslate:", error));
}

function backgroundTranslate() {
    const uniqueWords = new Set();
    document.querySelectorAll('.word').forEach(e1 => {
        uniqueWords.add(e1.dataset.word);
    });

    fetch('/translate_all', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ words: Array.from(uniqueWords) })
    })
        .then(res => res.json())
        .then(data => {
            document.querySelectorAll('.word').forEach(e1 => {
                const w = e1.dataset.word;
                if (data[w]) {
                    e1.dataset.pinyin = data[w].pinyin;
                    e1.dataset.translation = data[w].translation;
                }
            })
        })
        .catch(err => console.error("Error in backgroundTranslate:", err))
}

document.getElementById("new-sentence-button").addEventListener("click", function () {
    const hskLevel = document.getElementById("hsk-level").value;

    document.getElementById("spinner").style.display = "block";

    fetch(`/generate?hsk_level=${hskLevel}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("spinner").style.display = "none";
            document.getElementById("story-container").innerHTML = data.sentence;

            attachWordListeners();
            backgroundTranslate();
            fullTranslate();
        })
        .catch(error => {
            console.error("Error:", error);
            document.getElementById("spinner").style.display = "none";
        })
})

document.getElementById("second-part-button").addEventListener("click", function () {
    const hskLevel = document.getElementById("hsk-level").value

    document.getElementById("spinner").style.display = "block";

    fetch(`/generate_second?hsk_level=${hskLevel}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("spinner").style.display = "none";
            document.getElementById("story-container").innerHTML = data.sentence;

            attachWordListeners();
            backgroundTranslate();
            fullTranslate();
        })
        .catch(error => {
            console.error("Error:", error);
            document.getElementById("spinner").style.display = "none";
        })
})

document.addEventListener("click", (e) => {
    const popup = document.getElementById("popup");
    if (!popup) return;

    if (!e.target.classList.contains("word") && e.target.id !== "popup") {
        popup.style.display = "none";
    }
})

document.addEventListener('DOMContentLoaded', () => {
    attachWordListeners();
    backgroundTranslate();
});