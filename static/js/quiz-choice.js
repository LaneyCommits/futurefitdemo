/**
 * Interactive quiz choice pages – short/full selector and path cards
 * with hover effects, selection states, and playful animations.
 */
(function() {
  'use strict';

  function initLengthSelector() {
    var container = document.getElementById('quiz-length-selector');
    if (!container) return;

    var shortCard = container.querySelector('[data-length="short"]');
    var fullCard = container.querySelector('[data-length="full"]');
    if (!shortCard || !fullCard) return;

    function setActive(card) {
      shortCard.classList.remove('active');
      fullCard.classList.remove('active');
      card.classList.add('active');
    }

    shortCard.addEventListener('mouseenter', function() { setActive(shortCard); });
    shortCard.addEventListener('focus', function() { setActive(shortCard); });
    fullCard.addEventListener('mouseenter', function() { setActive(fullCard); });
    fullCard.addEventListener('focus', function() { setActive(fullCard); });

    setActive(fullCard);
  }

  function initPathCards() {
    var cards = document.querySelectorAll('.quiz-choice-card[href]');
    cards.forEach(function(card) {
      card.addEventListener('click', function(e) {
        card.classList.add('clicked');
        card.style.pointerEvents = 'none';
      });
      card.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
          card.classList.add('clicked');
        }
      });
    });
  }

  function init() {
    initLengthSelector();
    initPathCards();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
