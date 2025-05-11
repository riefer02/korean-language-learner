document.addEventListener("DOMContentLoaded", function () {
  // Implement lazy loading for audio files
  const lazyLoadAudio = function () {
    const audioElements = document.querySelectorAll("audio[data-src]");

    audioElements.forEach((audio) => {
      if (isElementInViewport(audio)) {
        audio.src = audio.dataset.src;
        audio.removeAttribute("data-src");
      }
    });
  };

  // Check if element is in viewport
  function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <=
        (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  }

  // Initial check and event listeners
  lazyLoadAudio();
  window.addEventListener("scroll", lazyLoadAudio);
  window.addEventListener("resize", lazyLoadAudio);
});
