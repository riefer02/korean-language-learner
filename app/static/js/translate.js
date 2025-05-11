document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("phrase-form");
  const resultDiv = document.getElementById("result");
  const loadingDiv = document.getElementById("loading");
  const translateBtn = document.getElementById("translate-btn");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const englishText = document.getElementById("english-text").value.trim();

    // Basic validation
    if (!englishText) {
      showError("Please enter a phrase to translate.");
      return;
    }

    // Show loading state
    translateBtn.disabled = true;
    resultDiv.classList.add("hidden");
    loadingDiv.classList.remove("hidden");
    loadingDiv.setAttribute("aria-hidden", "false");

    try {
      const response = await fetch("/api/translate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: englishText }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Translation failed");
      }

      // Update the result div
      resultDiv.querySelector(".phrase-english").textContent =
        data.english_text;
      resultDiv.querySelector(".phrase-korean").textContent = data.korean_text;

      const audio = resultDiv.querySelector("audio");
      audio.src = data.audio_path;
      audio.load();

      // Show result
      resultDiv.classList.remove("hidden");

      // Automatically play audio when loaded
      audio.addEventListener("canplaythrough", function audioLoaded() {
        playAudioWithFallback(audio);
        audio.removeEventListener("canplaythrough", audioLoaded);
      });
    } catch (error) {
      console.error("Error:", error);
      showError(error.message || "Failed to translate. Please try again.");
    } finally {
      // Hide loading state
      translateBtn.disabled = false;
      loadingDiv.classList.add("hidden");
      loadingDiv.setAttribute("aria-hidden", "true");
    }
  });
});
