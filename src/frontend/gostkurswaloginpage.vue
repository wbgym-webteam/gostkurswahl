<template>
  <div class="wrapper">
    <div class="noise"></div>

    <div class="card">
      <div class="header">
        <div class="logo">
          <span class="logo-dot"></span>
          <span class="logo-dot"></span>
          <span class="logo-dot"></span>
        </div>
        <h1 class="title">Kurs Wahl</h1>
        <p class="subtitle">Gib den 10 stelligen Code ein, der deiner Email zugesendet wurde.</p>
      </div>

      <div class="otp-grid" @paste="handlePaste">
        <input
          v-for="(_, i) in chars"
          :key="i"
          :ref="el => { if (el) inputs[i] = el }"
          v-model="chars[i]"
          class="otp-box"
          :class="{
            filled: chars[i],
            error: hasError,
            success: isSuccess
          }"
          maxlength="1"
          autocomplete="off"
          spellcheck="false"
          @keydown="handleKeydown($event, i)"
          @input="handleInput($event, i)"
          @focus="handleFocus(i)"
        />
      </div>

      <div class="status-row">
        <transition name="fade">
          <p v-if="hasError" class="status-msg error-msg">
            Falscher Code. Please check your email and try again.
          </p>
          <p v-else-if="isSuccess" class="status-msg success-msg">
            ✓ Code verified! Redirecting…
          </p>
          <p v-else-if="filled" class="status-msg hint-msg">
            Press confirm to verify your code.
          </p>
        </transition>
      </div>

      <button
        class="confirm-btn"
        :class="{ ready: filled, loading: isLoading }"
        :disabled="!filled || isLoading"
        @click="handleSubmit"
      >
        <span v-if="isLoading" class="spinner"></span>
        <span v-else>{{ filled ? 'Confirm Code' : 'Enter your code above' }}</span>
      </button>

      <p class="resend">Didn't receive a code? <a href="#">Resend email</a></p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const LENGTH = 12
const chars = ref(Array(LENGTH).fill(''))
const inputs = ref([])
const hasError = ref(false)
const isSuccess = ref(false)
const isLoading = ref(false)

const filled = computed(() => chars.value.every(c => c !== ''))

onMounted(() => {
  inputs.value[0]?.focus()
})

function handleInput(e, i) {
  hasError.value = false
  const val = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '')
  chars.value[i] = val ? val[val.length - 1] : ''
  if (val && i < LENGTH - 1) {
    inputs.value[i + 1]?.focus()
  }
}

function handleKeydown(e, i) {
  if (e.key === 'Backspace') {
    if (chars.value[i]) {
      chars.value[i] = ''
    } else if (i > 0) {
      inputs.value[i - 1]?.focus()
      chars.value[i - 1] = ''
    }
  } else if (e.key === 'ArrowLeft' && i > 0) {
    inputs.value[i - 1]?.focus()
  } else if (e.key === 'ArrowRight' && i < LENGTH - 1) {
    inputs.value[i + 1]?.focus()
  }
}

function handleFocus(i) {
  inputs.value[i]?.select()
}

function handlePaste(e) {
  e.preventDefault()
  const text = e.clipboardData.getData('text').toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, LENGTH)
  text.split('').forEach((ch, i) => { chars.value[i] = ch })
  const next = Math.min(text.length, LENGTH - 1)
  inputs.value[next]?.focus()
}

async function handleSubmit() {
  if (!filled.value) return
  isLoading.value = true
  const code = chars.value.join('')

  // Simulate API call — replace with your actual verification call
  await new Promise(r => setTimeout(r, 1400))

  isLoading.value = false

  // Mock: codes starting with 'A' succeed, everything else fails
  if (code.startsWith('A')) {
    isSuccess.value = true
  } else {
    hasError.value = true
    chars.value = Array(LENGTH).fill('')
    setTimeout(() => inputs.value[0]?.focus(), 50)
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0b0c0f;
  font-family: 'Syne', sans-serif;
  position: relative;
  overflow: hidden;
}

.noise {
  position: fixed;
  inset: -50%;
  width: 200%;
  height: 200%;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='1'/%3E%3C/svg%3E");
  opacity: 0.03;
  pointer-events: none;
  z-index: 0;
}

.wrapper::before {
  content: '';
  position: fixed;
  top: -30%;
  left: -20%;
  width: 60%;
  height: 70%;
  background: radial-gradient(ellipse, #9B409430 0%, transparent 70%);
  pointer-events: none;
}

.wrapper::after {
  content: '';
  position: fixed;
  bottom: -20%;
  right: -10%;
  width: 50%;
  height: 60%;
  background: radial-gradient(ellipse, rgba(99, 150, 210, 0.06) 0%, transparent 70%);
  pointer-events: none;
}

.card {
  position: relative;
  z-index: 1;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px;
  padding: 48px 40px 40px;
  width: min(560px, calc(100vw - 32px));
  backdrop-filter: blur(24px);
  box-shadow: 0 0 0 1px rgba(0,0,0,0.4), 0 32px 64px rgba(0,0,0,0.4);
  animation: cardIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes cardIn {
  from { opacity: 0; transform: translateY(24px) scale(0.98); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

.header { text-align: center; margin-bottom: 36px; }

.logo {
  display: flex;
  gap: 6px;
  justify-content: center;
  margin-bottom: 20px;
}

.logo-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: #63d2ac;
  animation: pulse 2s ease-in-out infinite;
}
.logo-dot:nth-child(2) { background: #63a0d2; animation-delay: 0.3s; }
.logo-dot:nth-child(3) { background: #d263ac; animation-delay: 0.6s; }

@keyframes pulse {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50%       { opacity: 1;   transform: scale(1.3); }
}

.title {
  font-size: 28px;
  font-weight: 800;
  color: #f0f0f0;
  letter-spacing: -0.5px;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 14px;
  font-weight: 400;
  color: rgba(255,255,255,0.4);
  line-height: 1.6;
  max-width: 320px;
  margin: 0 auto;
}

.otp-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 8px;
  margin-bottom: 16px;
}

.otp-box {
  font-family: 'DM Mono', monospace;
  font-size: 18px;
  font-weight: 500;
  text-align: center;
  text-transform: uppercase;
  color: #f0f0f0;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  height: 56px;
  width: 100%;
  outline: none;
  caret-color: #9B4094;
  transition: border-color 0.15s, background 0.15s, box-shadow 0.15s, transform 0.1s;
}

.otp-box:focus {
  border-color: #9B4094;
  background: #9B409412;
  box-shadow: 0 0 0 3px #9B409412;
  transform: translateY(-1px);
}

.otp-box.filled {
  border-color: rgba(255,255,255,0.2);
  background: rgba(255,255,255,0.08);
}

.otp-box.error {
  border-color: rgba(210, 99, 99, 0.6);
  background: rgba(210,99,99,0.06);
  animation: shake 0.4s cubic-bezier(0.36, 0.07, 0.19, 0.97);
}

.otp-box.success {
  border-color: rgba(99,210,172,0.8);
  background: rgba(99,210,172,0.1);
}

@keyframes shake {
  10%, 90% { transform: translateX(-2px); }
  20%, 80% { transform: translateX(3px); }
  30%, 50%, 70% { transform: translateX(-4px); }
  40%, 60% { transform: translateX(4px); }
}

.status-row {
  min-height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.status-msg {
  font-size: 13px;
  text-align: center;
}
.error-msg   { color: #e88080; }
.success-msg { color: #63d2ac; }
.hint-msg    { color: rgba(255,255,255,0.35); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.25s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.confirm-btn {
  width: 100%;
  padding: 16px;
  border-radius: 12px;
  border: none;
  font-family: 'Syne', sans-serif;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  background: rgba(255,255,255,0.06);
  color: rgba(255,255,255,0.3);
  letter-spacing: 0.2px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 20px;
}

.confirm-btn.ready {
  background: linear-gradient(135deg, #63d2ac, #5ab8d4);
  color: #0b0c0f;
  box-shadow: 0 4px 24px rgba(99,210,172,0.25);
}

.confirm-btn.ready:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 32px rgba(99,210,172,0.35);
}

.confirm-btn.ready:active {
  transform: translateY(0);
}

.confirm-btn:disabled { cursor: not-allowed; }

.spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(11,12,15,0.3);
  border-top-color: #0b0c0f;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.resend {
  text-align: center;
  font-size: 13px;
  color: rgba(255,255,255,0.25);
}
.resend a {
  color: rgba(99,210,172,0.7);
  text-decoration: none;
  font-weight: 600;
}
.resend a:hover { color: #63d2ac; }
</style>
