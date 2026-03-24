<template>
  <div class="kw-app">

    <!-- ── Header ───────────────────────────────────────────────────── -->
    <header class="kw-header">
      <div class="kw-header__inner">
        <h1 class="kw-header__title">Kurswahl</h1>
        <p class="kw-header__sub">Wähle deine Leistungs- und Grundkurse für die Qualifikationsphase</p>
        <div class="kw-progress">
          <div class="kw-progress__bar">
            <div class="kw-progress__fill" :style="{ width: progressPct + '%' }" />
          </div>
          <div class="kw-progress__labels">
            <span>{{ totalSelected }} von 8 Kursen gewählt</span>
            <span>{{ progressPct }}%</span>
          </div>
        </div>
      </div>
    </header>

    <div class="kw-page">

      <Transition name="kw-slide">
        <div v-if="totalSelected === 8" class="kw-banner">
          <span class="kw-banner__icon">✓</span>
          Alle Kurse gewählt! Bitte überprüfe deine Auswahl und sende das Formular ab.
        </div>
      </Transition>

      <div class="kw-layout">

        <!-- ── Main column ──────────────────────────────────────────── -->
        <div class="kw-main">

          <!-- LK 1 — fest: EN / DE / MA -->
          <div class="kw-card">
            <div class="kw-card__head kw-card__head--lk">
              <span class="kw-badge kw-badge--lk">LK 1</span>
              <span class="kw-card__title">1. Leistungskurs</span>
              <span class="kw-card__hint">Pflichtfach</span>
            </div>
            <div class="kw-card__body">
              <div class="kw-opts">
                <button
                  v-for="id in LK1_OPTIONS" :key="id"
                  class="kw-opt kw-opt--lk"
                  :class="{ 'kw-opt--selected': selection[1] === id }"
                  @click="select(1, id)"
                >
                  <span class="kw-opt__dot" />{{ LABELS[id] }}
                </button>
              </div>
            </div>
          </div>

          <!-- LK 2 & GK 1–6 — Optionen kommen von der API -->
          <template v-for="card in CARDS" :key="card.slot">
            <div class="kw-card" :class="{ 'kw-card--locked': !isUnlocked(card.slot) }">
              <div class="kw-card__head" :class="card.isLK ? 'kw-card__head--lk' : 'kw-card__head--gk'">
                <span class="kw-badge" :class="card.isLK ? 'kw-badge--lk' : 'kw-badge--gk'">
                  {{ card.badge }}
                </span>
                <span class="kw-card__title">{{ card.title }}</span>
                <span v-if="loadingSlot === card.slot" class="kw-loading-dot">
                  <span /><span /><span />
                </span>
                <span v-else class="kw-card__hint">{{ card.hint }}</span>
              </div>

              <div class="kw-card__body">
                <!-- Noch nicht entsperrt -->
                <p v-if="!isUnlocked(card.slot)" class="kw-hint-text kw-hint-text--lock">
                  🔒 Bitte erst die vorherigen Kurse wählen
                </p>

                <!-- Lädt -->
                <div v-else-if="loadingSlot === card.slot" class="kw-skeleton">
                  <div class="kw-skeleton__btn" v-for="n in 4" :key="n" />
                </div>

                <!-- Fehler -->
                <p v-else-if="errors[card.slot]" class="kw-hint-text kw-hint-text--error">
                  ⚠ {{ errors[card.slot] }}
                  <button class="kw-retry" @click="loadOptions(card.slot)">Erneut versuchen</button>
                </p>

                <!-- Keine Optionen -->
                <p v-else-if="options[card.slot] && options[card.slot].length === 0" class="kw-hint-text">
                  Keine weiteren Optionen verfügbar.
                </p>

                <!-- Optionen -->
                <div v-else-if="options[card.slot]" class="kw-opts">
                  <button
                    v-for="id in options[card.slot]" :key="id"
                    class="kw-opt"
                    :class="[
                      card.isLK ? 'kw-opt--lk' : 'kw-opt--gk',
                      { 'kw-opt--selected': selection[card.slot] === id }
                    ]"
                    @click="select(card.slot, id)"
                  >
                    <span class="kw-opt__dot" />{{ LABELS[id] ?? id }}
                  </button>
                </div>
              </div>
            </div>
          </template>

        </div><!-- /kw-main -->

        <!-- ── Sidebar ──────────────────────────────────────────────── -->
        <aside class="kw-sidebar">
          <div class="kw-summary">
            <h2 class="kw-summary__title">Deine Auswahl</h2>

            <div v-for="row in summaryRows" :key="row.label" class="kw-summary__row">
              <span class="kw-summary__label">{{ row.label }}</span>
              <span
                class="kw-summary__val"
                :class="row.val
                  ? (row.isLK ? 'kw-summary__val--lk' : 'kw-summary__val--gk')
                  : 'kw-summary__val--empty'"
              >{{ row.val ? (LABELS[row.val] ?? row.val) : '—' }}</span>
            </div>

            <button
              class="kw-btn kw-btn--submit"
              :disabled="totalSelected < 8 || isSubmitting"
              @click="submit"
            >
              <span v-if="isSubmitting" class="kw-loading-dot"><span /><span /><span /></span>
              <span v-else>Kurswahl abschicken</span>
            </button>

            <button class="kw-btn kw-btn--reset" @click="reset">Alles zurücksetzen</button>


          </div>
        </aside>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'

// ─── Konfiguration ────────────────────────────────────────────────────────────

// Basis-URL der Flask API — anpassen für Produktion
const API_BASE = 'http://localhost:5000'

// LK1 ist fest vorgegeben (nicht vom Modul)
const LK1_OPTIONS = ['EN', 'DE', 'MA']

// Karten-Definitionen — nur UI-Metadaten, keine Logik
const CARDS = [
  { slot: 2, isLK: true,  badge: 'LK 2', title: '2. Leistungskurs', hint: 'Pflichtfach' },
  { slot: 3, isLK: false, badge: '1. GK', title: '1. Grundkurs',     hint: 'Kunst · Musik · DS' },
  { slot: 4, isLK: false, badge: '2. GK', title: '2. Grundkurs',     hint: 'Geschichte' },
  { slot: 5, isLK: false, badge: '3. GK', title: '3. Grundkurs',     hint: 'Naturwiss. / Fremdsprache / MA' },
  { slot: 6, isLK: false, badge: '4. GK', title: '4. Grundkurs',     hint: 'Abhängig vom Pfad' },
  { slot: 7, isLK: false, badge: '5. GK', title: '5. Grundkurs',     hint: 'Freie Wahl' },
  { slot: 8, isLK: false, badge: '6. GK', title: '6. Grundkurs',     hint: 'Freie Wahl' },
]

// Anzeigebezeichnungen (nur für die UI — die IDs kommen vom Server)
const LABELS = {
  EN: 'Englisch',   DE: 'Deutsch',     MA: 'Mathematik',
  GE: 'Geschichte', GEBI: 'Geschichte Bilingual', PB: 'Politische Bildung',
  EK: 'Erdkunde',   BI: 'Biologie',    CH: 'Chemie',     PH: 'Physik',
  INF: 'Informatik', TK: 'Technik',    FR: 'Französisch', SN: 'Spanisch',
  LA: 'Latein',      KU: 'Kunst',      MU: 'Musik',       DS: 'Darstellendes Spiel',
}

// ─── State ────────────────────────────────────────────────────────────────────

// Aktuelle Selektion: selection[slot] = gewähltes Fach-ID (oder null)
const selection = reactive({ 1: null, 2: null, 3: null, 4: null, 5: null, 6: null, 7: null, 8: null })

// Vom Server geladene Optionen pro Slot
const options     = reactive({})
const errors      = reactive({})
const loadingSlot = ref(null)
const isSubmitting = ref(false)

// ─── API-Schnittstellen ───────────────────────────────────────────────────────

/**
 * Fragt den Server nach den verfügbaren Optionen für einen Slot.
 *
 * Flask-Endpunkt: POST /api/optionen
 * Payload:        { taken_courses: [wahlstufe, lk1, lk2, gk1, gk2, gk3, gk4, gk5, gk6] }
 * Antwort:        { optionen: ["EN", "DE", ...] }
 *
 * Das taken_courses-Array entspricht 1:1 dem Format des Python-Moduls.
 */
async function apiGetOptionen(slot) {
  const taken_courses = buildTakenCourses(slot)

  const response = await fetch(`${API_BASE}/api/optionen`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ taken_courses }),
  })

  if (!response.ok) throw new Error(`Server-Fehler: ${response.status}`)

  const data = await response.json()
  return data.optionen // erwartet: string[]
}

/**
 * Schickt die fertige Kurswahl an den Server.
 *
 * Flask-Endpunkt: POST /api/abschicken
 * Payload:        { taken_courses: [0, lk1, lk2, gk1, gk2, gk3, gk4, gk5, gk6] }
 *                 (Wahlstufe 0 = abgeschlossen)
 * Antwort:        { erfolg: true, nachricht: "..." }
 */
async function apiSubmitKurswahl() {
  const taken_courses = buildTakenCourses(0) // 0 = fertig

  const response = await fetch(`${API_BASE}/api/abschicken`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ taken_courses }),
  })

  if (!response.ok) throw new Error(`Server-Fehler: ${response.status}`)

  const data = await response.json()
  return data // { erfolg: bool, nachricht: string }
}

// ─── Hilfsfunktionen ──────────────────────────────────────────────────────────

/**
 * Baut das taken_courses-Array auf, das an das Python-Modul übergeben wird.
 * Format: [wahlstufe, lk1, lk2, gk1, gk2, gk3, gk4, gk5, gk6]
 */
function buildTakenCourses(wahlstufe) {
  return [
    wahlstufe,
    selection[1], // LK1
    selection[2], // LK2
    selection[3], // GK1
    selection[4], // GK2
    selection[5], // GK3
    selection[6], // GK4
    selection[7], // GK5
    selection[8], // GK6
  ]
}

// Ein Slot ist entsperrt, wenn alle vorherigen Slots belegt sind
function isUnlocked(slot) {
  for (let i = 1; i < slot; i++) {
    if (!selection[i]) return false
  }
  return true
}

// Lädt die Optionen für einen Slot vom Server
async function loadOptions(slot) {
  loadingSlot.value = slot
  delete errors[slot]
  try {
    options[slot] = await apiGetOptionen(slot)
  } catch (e) {
    errors[slot] = e.message || 'Verbindung zum Server fehlgeschlagen'
  } finally {
    loadingSlot.value = null
  }
}

// Kurs wählen oder abwählen
async function select(slot, id) {
  if (selection[slot] === id) {
    // Abwählen: diesen und alle nachfolgenden Slots leeren
    for (let i = slot; i <= 8; i++) {
      selection[i] = null
      delete options[i]
      delete errors[i]
    }
  } else {
    // Neu wählen: alle nachfolgenden Slots leeren …
    for (let i = slot + 1; i <= 8; i++) {
      selection[i] = null
      delete options[i]
      delete errors[i]
    }
    // … dann diesen Slot setzen …
    selection[slot] = id
    // … und sofort die Optionen für den nächsten Slot laden
    const nextSlot = slot + 1
    if (nextSlot <= 8) {
      await loadOptions(nextSlot)
    }
  }
}

// Kurswahl abschicken
async function submit() {
  isSubmitting.value = true
  try {
    const result = await apiSubmitKurswahl()
    alert(result.nachricht ?? 'Kurswahl erfolgreich abgeschickt!')
  } catch (e) {
    alert('Fehler beim Abschicken: ' + e.message)
  } finally {
    isSubmitting.value = false
  }
}

// Alles zurücksetzen
function reset() {
  for (let i = 1; i <= 8; i++) {
    selection[i] = null
    delete options[i]
    delete errors[i]
  }
}

// ─── Fortschritt & Zusammenfassung ────────────────────────────────────────────
const totalSelected = computed(() =>
  Object.values(selection).filter(Boolean).length
)
const progressPct = computed(() => Math.round(totalSelected.value / 8 * 100))

const summaryRows = computed(() => [
  { label: '1. LK', val: selection[1], isLK: true },
  { label: '2. LK', val: selection[2], isLK: true },
  ...CARDS.filter(c => !c.isLK).map(c => ({
    label: c.badge, val: selection[c.slot], isLK: false,
  })),
])
</script>

<style scoped>
/* ─── Design Tokens ────────────────────────────────────────────────────────── */
.kw-app {
  --c-primary:    #560D4F;
  --c-secondary:  #9B4094;
  --c-accent:     #F6F1F5;
  --c-text:       #000000;
  --c-muted:      #6b5261;
  --c-border:     #ddd3dc;
  --c-surface:    #ffffff;
  --c-dis-bg:     #ece7eb;
  --c-dis-text:   #b8adb7;
  --c-success:    #2d6a4f;
  --c-error:      #9b2335;
  --shadow-sm:    0 2px 12px rgba(86,13,79,.07);
  --shadow-md:    0 5px 24px rgba(86,13,79,.14);
  --radius:       14px;
  --radius-sm:    9px;

  font-family: 'DM Sans', 'Segoe UI', system-ui, sans-serif;
  background: var(--c-accent);
  color: var(--c-text);
  min-height: 100vh;
  padding: 2rem 1rem 5rem;
}

/* ─── Header ──────────────────────────────────────────────────────────────── */
.kw-header {
  background: var(--c-primary);
  margin: -2rem -1rem 2.5rem;
  padding: 2.8rem 1rem 2.2rem;
}
.kw-header__inner { max-width: 1060px; margin: 0 auto; text-align: center; }
.kw-header__title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2rem, 4.5vw, 3rem);
  color: #fff; letter-spacing: -.5px;
}
.kw-header__sub { color: rgba(255,255,255,.6); font-size: .95rem; margin-top: .5rem; font-weight: 300; }

.kw-progress       { max-width: 560px; margin: 1.7rem auto 0; }
.kw-progress__bar  { background: rgba(255,255,255,.18); border-radius: 99px; height: 6px; overflow: hidden; }
.kw-progress__fill { height: 100%; background: linear-gradient(90deg, var(--c-secondary), #d08ad0); border-radius: 99px; transition: width .4s ease; }
.kw-progress__labels { display: flex; justify-content: space-between; font-size: .77rem; color: rgba(255,255,255,.55); margin-top: .45rem; }

/* ─── Page / Layout ───────────────────────────────────────────────────────── */
.kw-page   { max-width: 1060px; margin: 0 auto; }
.kw-layout { display: grid; grid-template-columns: 1fr 270px; gap: 1.5rem; align-items: start; }
@media (max-width: 820px) {
  .kw-layout { grid-template-columns: 1fr; }
  .kw-sidebar { order: -1; }
}

/* ─── Banner ──────────────────────────────────────────────────────────────── */
.kw-banner {
  display: flex; align-items: center; gap: .75rem;
  background: var(--c-success); color: #fff;
  border-radius: var(--radius); padding: 1.1rem 1.4rem;
  margin-bottom: 1.5rem; font-weight: 500;
}
.kw-banner__icon {
  width: 28px; height: 28px; border-radius: 50%;
  background: rgba(255,255,255,.2);
  display: flex; align-items: center; justify-content: center;
  font-size: 1rem; flex-shrink: 0;
}
.kw-slide-enter-active, .kw-slide-leave-active { transition: opacity .3s, transform .3s; }
.kw-slide-enter-from,   .kw-slide-leave-to     { opacity: 0; transform: translateY(-10px); }

/* ─── Card ────────────────────────────────────────────────────────────────── */
.kw-card {
  background: var(--c-surface); border-radius: var(--radius);
  border: 1px solid var(--c-border); box-shadow: var(--shadow-sm);
  margin-bottom: 1.2rem; overflow: hidden;
  transition: box-shadow .2s, transform .15s, opacity .2s;
}
.kw-card:hover:not(.kw-card--locked) { box-shadow: var(--shadow-md); transform: translateY(-1px); }
.kw-card--locked { opacity: .55; }

.kw-card__head {
  display: flex; align-items: center; gap: .75rem;
  padding: .9rem 1.4rem; border-bottom: 1px solid var(--c-border);
}
.kw-card__head--lk { background: linear-gradient(135deg, #f9f0f8, var(--c-accent)); border-bottom-color: #e0c8de; }
.kw-card__head--gk { background: var(--c-accent); }

.kw-card__title { font-size: .95rem; font-weight: 600; flex: 1; }
.kw-card__hint  { font-size: .77rem; color: var(--c-muted); }
.kw-card__body  { padding: 1.1rem 1.4rem; min-height: 52px; }

/* ─── Badges ──────────────────────────────────────────────────────────────── */
.kw-badge { font-size: .67rem; font-weight: 700; letter-spacing: .09em; text-transform: uppercase; padding: .22rem .62rem; border-radius: 6px; flex-shrink: 0; }
.kw-badge--lk { background: var(--c-primary);   color: #fff; }
.kw-badge--gk { background: var(--c-secondary); color: #fff; }

/* ─── Option buttons ──────────────────────────────────────────────────────── */
.kw-opts { display: flex; flex-wrap: wrap; gap: .5rem; align-items: center; }

.kw-opt {
  display: inline-flex; align-items: center; gap: .45rem;
  padding: .5rem 1rem; border-radius: var(--radius-sm);
  border: 2px solid var(--c-border); background: var(--c-surface); color: var(--c-text);
  font-family: inherit; font-size: .875rem; font-weight: 500;
  cursor: pointer; transition: all .14s; user-select: none; line-height: 1.2;
}
.kw-opt--lk:hover:not(.kw-opt--selected)               { border-color: var(--c-primary);   background: #f4e8f3; color: var(--c-primary);   }
.kw-opt--lk.kw-opt--selected                           { background: var(--c-primary);     border-color: var(--c-primary);   color: #fff; }
.kw-opt--gk:hover:not(.kw-opt--selected)               { border-color: var(--c-secondary); background: #f5eaf5; color: var(--c-secondary); }
.kw-opt--gk.kw-opt--selected                           { background: var(--c-secondary);   border-color: var(--c-secondary); color: #fff; }

.kw-opt__dot { width: 8px; height: 8px; border-radius: 50%; border: 2px solid currentColor; flex-shrink: 0; }
.kw-opt--selected .kw-opt__dot { background: currentColor; }

/* ─── Hint & error text ───────────────────────────────────────────────────── */
.kw-hint-text        { font-size: .82rem; color: var(--c-muted); font-style: italic; display: flex; align-items: center; gap: .5rem; }
.kw-hint-text--lock  { color: var(--c-muted); }
.kw-hint-text--error { color: var(--c-error); font-style: normal; }
.kw-retry {
  margin-left: .4rem; padding: .2rem .6rem; border-radius: 6px; border: 1px solid var(--c-error);
  background: transparent; color: var(--c-error); font-size: .78rem; cursor: pointer;
  transition: all .14s;
}
.kw-retry:hover { background: var(--c-error); color: #fff; }

/* ─── Loading skeleton ────────────────────────────────────────────────────── */
.kw-skeleton { display: flex; flex-wrap: wrap; gap: .5rem; }
.kw-skeleton__btn {
  height: 36px; width: 110px; border-radius: var(--radius-sm);
  background: linear-gradient(90deg, var(--c-dis-bg) 25%, #f3eef2 50%, var(--c-dis-bg) 75%);
  background-size: 200% 100%;
  animation: kw-shimmer 1.3s infinite;
}
@keyframes kw-shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* ─── Loading dots ────────────────────────────────────────────────────────── */
.kw-loading-dot { display: inline-flex; gap: 3px; align-items: center; }
.kw-loading-dot span {
  width: 5px; height: 5px; border-radius: 50%;
  background: currentColor; opacity: .5;
  animation: kw-dot-blink .9s infinite ease-in-out;
}
.kw-loading-dot span:nth-child(2) { animation-delay: .15s; }
.kw-loading-dot span:nth-child(3) { animation-delay: .3s;  }
@keyframes kw-dot-blink { 0%, 80%, 100% { transform: scale(.7); opacity: .3; } 40% { transform: scale(1); opacity: 1; } }

/* ─── Sidebar ─────────────────────────────────────────────────────────────── */
.kw-sidebar { position: static; }
@media (min-width: 820px) { .kw-sidebar { position: sticky; top: 1.5rem; } }
.kw-summary {
  background: var(--c-surface); border-radius: var(--radius);
  border: 1px solid var(--c-border); box-shadow: var(--shadow-sm);
  padding: 1.3rem 1.3rem 1.5rem;
}
.kw-summary__title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.1rem; color: var(--c-primary);
  margin-bottom: 1rem; padding-bottom: .7rem;
  border-bottom: 2px solid var(--c-accent);
}
.kw-summary__row { display: flex; justify-content: space-between; align-items: center; padding: .38rem 0; border-bottom: 1px dashed var(--c-border); font-size: .82rem; }
.kw-summary__row:last-of-type { border-bottom: none; }
.kw-summary__label { color: var(--c-muted); }
.kw-summary__val   { font-weight: 600; text-align: right; max-width: 55%; }
.kw-summary__val--lk    { color: var(--c-primary);   }
.kw-summary__val--gk    { color: var(--c-secondary); }
.kw-summary__val--empty { color: var(--c-dis-text); font-style: italic; font-weight: 400; }

.kw-btn {
  display: flex; align-items: center; justify-content: center;
  width: 100%; padding: .72rem; border-radius: 10px;
  font-family: inherit; font-size: .88rem; font-weight: 600;
  cursor: pointer; transition: all .15s; border: none;
}
.kw-btn--submit { margin-top: 1.2rem; background: var(--c-primary); color: #fff; min-height: 42px; }
.kw-btn--submit:hover:not(:disabled) { background: #3e0939; transform: translateY(-1px); box-shadow: 0 4px 14px rgba(86,13,79,.3); }
.kw-btn--submit:disabled { background: var(--c-dis-bg); color: var(--c-dis-text); cursor: not-allowed; transform: none; box-shadow: none; }
.kw-btn--reset { margin-top: .5rem; background: transparent; color: var(--c-muted); border: 1.5px solid var(--c-border); font-weight: 400; }
.kw-btn--reset:hover { border-color: #c0392b; color: #c0392b; background: #fff5f5; }

</style>