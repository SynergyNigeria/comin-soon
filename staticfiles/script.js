// ...existing code...

// Countdown timer functionality
function updateCountdown() {
    // Set launch date (30 days from now for demo)
    const launchDate = new Date();
    launchDate.setDate(launchDate.getDate() + 30);

    const now = new Date();
    const timeLeft = launchDate - now;

    if (timeLeft > 0) {
        const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
        const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

        // Update countdown digits
        const digits = document.querySelectorAll('.countdown-digit');
        if (digits.length >= 4) {
            digits[0].textContent = days.toString().padStart(2, '0');
            digits[1].textContent = hours.toString().padStart(2, '0');
            digits[2].textContent = minutes.toString().padStart(2, '0');
            digits[3].textContent = seconds.toString().padStart(2, '0');
        }
    } else {
        // Launch date has passed
        const countdown = document.getElementById('countdown');
        if (countdown) {
            countdown.innerHTML = '<div class="text-center"><span class="text-3xl font-bold text-[#008751]">We\'re Live!</span><br><span class="text-sm text-gray-500">Join us now</span></div>';
        }
    }
}

// Hero image carousel functionality
let currentSlide = 0;
const slides = document.querySelectorAll('.carousel-slide');
const dots = document.querySelectorAll('.carousel-dot');

function showSlide(index) {
    // Hide all slides
    slides.forEach(slide => slide.classList.remove('opacity-100'));
    slides.forEach(slide => slide.classList.add('opacity-0'));

    // Remove active dot
    dots.forEach(dot => dot.classList.remove('bg-white/70'));
    dots.forEach(dot => dot.classList.add('bg-white/40'));

    // Show current slide
    slides[index].classList.remove('opacity-0');
    slides[index].classList.add('opacity-100');

    // Activate current dot
    dots[index].classList.remove('bg-white/40');
    dots[index].classList.add('bg-white/70');

    currentSlide = index;
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(currentSlide);
}

// Auto-play carousel
let carouselInterval = setInterval(nextSlide, 4000);

// Event listeners for carousel controls
document.getElementById('next-slide')?.addEventListener('click', () => {
    clearInterval(carouselInterval);
    nextSlide();
    carouselInterval = setInterval(nextSlide, 4000);
});

document.getElementById('prev-slide')?.addEventListener('click', () => {
    clearInterval(carouselInterval);
    prevSlide();
    carouselInterval = setInterval(nextSlide, 4000);
});

// Dot navigation
dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
        clearInterval(carouselInterval);
        showSlide(index);
        carouselInterval = setInterval(nextSlide, 4000);
    });
});

// Floating elements animation
document.getElementById('floating-shopping')?.addEventListener('click', function() {
    this.style.transform = 'scale(1.2) rotate(10deg)';
    setTimeout(() => {
        this.style.transform = 'scale(1) rotate(0deg)';
    }, 300);
});

document.getElementById('floating-heart')?.addEventListener('click', function() {
    this.style.transform = 'scale(1.2) rotate(-10deg)';
    setTimeout(() => {
        this.style.transform = 'scale(1) rotate(0deg)';
    }, 300);
});

// Email Signup with Verification (Django backend integration)
const notifyForm = document.getElementById('notify-form');
const verifyModal = document.getElementById('verification-modal');
const verifyEmailSpan = document.getElementById('verification-email');
const verifyErrorMsg = document.getElementById('verification-error');
const codeInputs = document.querySelectorAll('.verification-input');
const verifyButton = document.getElementById('verify-code');
const resendButton = document.getElementById('resend-code');
const closeModal = document.getElementById('close-modal');
const notifyMessage = document.getElementById('notify-message');

let userEmail = '';

// Show modal
function showModal() {
  verifyModal.classList.remove('opacity-0', 'pointer-events-none');
  verifyModal.classList.add('opacity-100');
  verifyModal.querySelector('.transform').classList.remove('scale-95');
  verifyModal.querySelector('.transform').classList.add('scale-100');
  document.body.style.overflow = 'hidden';
  codeInputs[0].focus();
}

// Hide modal
function hideModal() {
  verifyModal.classList.add('opacity-0', 'pointer-events-none');
  verifyModal.classList.remove('opacity-100');
  verifyModal.querySelector('.transform').classList.add('scale-95');
  verifyModal.querySelector('.transform').classList.remove('scale-100');
  document.body.style.overflow = '';
  // Clear inputs
  codeInputs.forEach(input => input.value = '');
  verifyErrorMsg.textContent = '';
}

// Handle form submission (subscribe)
if (notifyForm) {
  notifyForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    userEmail = document.getElementById('notify-email').value.trim();
    notifyMessage.textContent = '';
    notifyMessage.className = 'text-green-600 text-sm mt-4 min-h-[1.2em] text-center w-full';
    if (!userEmail) return;
    try {
      const response = await fetch('/subscribe/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: userEmail })
      });
      const data = await response.json();
      if (data.success) {
        verifyEmailSpan.textContent = userEmail;
        showModal();
      } else {
        notifyMessage.textContent = data.message || 'Failed to send verification code.';
        notifyMessage.className = 'text-red-600 text-sm mt-4 min-h-[1.2em] text-center w-full';
      }
    } catch (err) {
      notifyMessage.textContent = 'Network error. Please try again.';
      notifyMessage.className = 'text-red-600 text-sm mt-4 min-h-[1.2em] text-center w-full';
    }
  });
}

// Handle verification code inputs (UI only)
codeInputs.forEach((input, index) => {
  input.addEventListener('input', function(e) {
    this.value = this.value.replace(/[^0-9]/g, '');
    if (this.value && index < codeInputs.length - 1) {
      codeInputs[index + 1].focus();
    }
    if (verifyErrorMsg.textContent) {
      verifyErrorMsg.textContent = '';
    }
  });
  input.addEventListener('keydown', function(e) {
    if (e.key === 'Backspace' && !this.value && index > 0) {
      codeInputs[index - 1].focus();
    }
  });
  input.addEventListener('paste', function(e) {
    e.preventDefault();
    const paste = (e.clipboardData || window.clipboardData).getData('text');
    const pasteNumbers = paste.replace(/[^0-9]/g, '').slice(0, 6);
    pasteNumbers.split('').forEach((num, i) => {
      if (codeInputs[i]) {
        codeInputs[i].value = num;
      }
    });
    const lastFilledIndex = Math.min(pasteNumbers.length - 1, 5);
    codeInputs[lastFilledIndex].focus();
  });
});

// Handle verification (verify code)
if (verifyButton) {
  verifyButton.addEventListener('click', async function() {
    const enteredCode = Array.from(codeInputs).map(input => input.value).join('');
    if (enteredCode.length !== 6) {
  verifyErrorMsg.textContent = 'Please enter all 6 digits';
      return;
    }
    try {
      const response = await fetch('/verify/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: userEmail, code: enteredCode })
      });
      const data = await response.json();
      if (data.success) {
        notifyMessage.textContent = '✅ Email verified! We\'ll notify you when we launch.';
        notifyMessage.className = 'text-green-600 text-sm mt-4 min-h-[1.2em] text-center w-full';
        notifyForm.reset();
        hideModal();
        setTimeout(() => { notifyMessage.textContent = ''; }, 5000);
      } else {
        verifyErrorMsg.textContent = data.message || 'Invalid verification code. Please try again.';
        verifyModal.querySelector('.transform').classList.add('animate-pulse');
        setTimeout(() => {
          verifyModal.querySelector('.transform').classList.remove('animate-pulse');
        }, 500);
      }
    } catch (err) {
  verifyErrorMsg.textContent = 'Network error. Please try again.';
    }
  });
}

// Handle resend code
if (resendButton) {
  resendButton.addEventListener('click', async function() {
    if (!userEmail) return;
    try {
      const response = await fetch('/resend/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: userEmail })
      });
      const data = await response.json();
      if (data.success) {
  verifyErrorMsg.textContent = 'New code sent! Check your email.';
  verifyErrorMsg.className = 'text-green-600 text-sm mt-3 text-center min-h-[1.2em]';
      } else {
  verifyErrorMsg.textContent = data.message || 'Failed to resend code.';
  verifyErrorMsg.className = 'text-red-600 text-sm mt-3 text-center min-h-[1.2em]';
      }
      codeInputs.forEach(input => input.value = '');
      codeInputs[0].focus();
      setTimeout(() => {
        verifyErrorMsg.textContent = '';
        verifyErrorMsg.className = 'text-red-500 text-sm mt-3 text-center min-h-[1.2em]';
      }, 3000);
    } catch (err) {
  verifyErrorMsg.textContent = 'Network error. Please try again.';
  verifyErrorMsg.className = 'text-red-600 text-sm mt-3 text-center min-h-[1.2em]';
    }
  });
}


// Handle modal close
if (closeModal) {
  closeModal.addEventListener('click', hideModal);
}

// Close modal when clicking outside
verifyModal.addEventListener('click', function(e) {
  if (e.target === verifyModal) {
    hideModal();
  }
});

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape' && !verifyModal.classList.contains('pointer-events-none')) {
    hideModal();
  }
});

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize countdown
    updateCountdown();
    setInterval(updateCountdown, 1000);

    // Initialize carousel
    if (slides.length > 0) {
        showSlide(0);
    }

    // Initialize Feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
});