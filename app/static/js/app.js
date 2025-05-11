// Common utility functions for Korean Language Learner

// Safely play audio with error handling
function playAudioWithFallback(audioElement) {
  const playPromise = audioElement.play();

  if (playPromise !== undefined) {
    playPromise.catch((error) => {
      console.error("Audio playback error:", error);
      // Show a message to the user, if appropriate
      const errorContainer = document.getElementById("error-message");
      if (errorContainer) {
        errorContainer.textContent = "Audio playback failed. Please try again.";
        errorContainer.classList.remove("hidden");
        setTimeout(() => {
          errorContainer.classList.add("hidden");
        }, 3000);
      }
    });
  }
}

// Show error message
function showError(message) {
  const errorContainer = document.getElementById("error-message");
  if (errorContainer) {
    errorContainer.textContent = message;
    errorContainer.classList.remove("hidden");
    // Focus the error message for screen readers
    errorContainer.setAttribute("tabindex", "-1");
    errorContainer.focus();

    // Auto-hide after 5 seconds
    setTimeout(() => {
      errorContainer.classList.add("hidden");
    }, 5000);
  }
}

// Handle repeat button clicks
document.addEventListener("click", function (e) {
  if (e.target.classList.contains("repeat-btn")) {
    const audio = e.target.closest(".audio-player").querySelector("audio");
    audio.currentTime = 0;
    playAudioWithFallback(audio);
  }
});

// Handle keyboard accessibility
document.addEventListener("keydown", function (e) {
  // Space or Enter on repeat buttons
  if (
    (e.key === " " || e.key === "Enter") &&
    document.activeElement.classList.contains("repeat-btn")
  ) {
    e.preventDefault();
    document.activeElement.click();
  }
});
