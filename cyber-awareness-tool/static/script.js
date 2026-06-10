// ── STATE ────────────────────────────────────────────
let currentIndex = 0;
const answers = {};

// ── SCREEN HELPERS ───────────────────────────────────
function showScreen(id) {
    ['screenLanding', 'screenQuiz', 'screenLoading', 'screenResult']
        .forEach(s => {
            const el = document.getElementById(s);
            if (el) el.style.display = (s === id) ? 'block' : 'none';
        });
}

function showLanding() {
    // Reset quiz state when going back
    currentIndex = 0;
    Object.keys(answers).forEach(k => delete answers[k]);
    document.querySelectorAll('.option-btn').forEach(b => {
        b.classList.remove('selected-yes', 'selected-no');
    });
    document.querySelectorAll('.q-card').forEach((c, i) => {
        c.classList.remove('active', 'exit');
        c.style.position = 'absolute';
        if (i === 0) { c.classList.add('active'); c.style.position = ''; }
    });
    updateProgress();
    showScreen('screenLanding');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showQuiz() {
    showScreen('screenQuiz');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}


// ── DOM REFS ─────────────────────────────────────────
function refs() {
    return {
        cards:     document.querySelectorAll('.q-card'),
        btnPrev:   document.getElementById('btnPrev'),
        btnNext:   document.getElementById('btnNext'),
        btnSubmit: document.getElementById('btnSubmit'),
        skipNote:  document.getElementById('skipNote'),
        fillEl:    document.getElementById('progressFill'),
        labelEl:   document.getElementById('progressLabel'),
        pctEl:     document.getElementById('progressPct'),
    };
}


// ── PROGRESS ─────────────────────────────────────────
function updateProgress() {
    const { fillEl, pctEl, labelEl } = refs();
    const answered = Object.keys(answers).length;
    const pct = TOTAL > 0 ? Math.round((answered / TOTAL) * 100) : 0;
    if (fillEl)  fillEl.style.width  = pct + '%';
    if (pctEl)   pctEl.textContent   = pct + '%';
    if (labelEl) labelEl.textContent = `QUESTION ${currentIndex + 1} OF ${TOTAL}`;
}


// ── SELECT ANSWER ─────────────────────────────────────
function selectAnswer(btn, qid, value) {
    const { btnNext, btnSubmit, skipNote } = refs();
    const card = btn.closest('.q-card');

    card.querySelectorAll('.option-btn').forEach(b =>
        b.classList.remove('selected-yes', 'selected-no')
    );
    btn.classList.add(value === 'Yes' ? 'selected-yes' : 'selected-no');
    answers[qid] = value;

    if (skipNote)  skipNote.textContent = '';
    if (btnNext)   btnNext.disabled     = false;
    if (btnSubmit) btnSubmit.disabled   = false;

    updateProgress();

    setTimeout(() => {
        if (currentIndex < TOTAL - 1) navigate(1);
    }, 420);
}


// ── NAVIGATE ─────────────────────────────────────────
function navigate(dir) {
    const { cards, btnPrev, btnNext, btnSubmit, skipNote } = refs();
    const current = cards[currentIndex];
    const next    = cards[currentIndex + dir];
    if (!next) return;

    current.classList.add('exit');
    setTimeout(() => {
        current.classList.remove('active', 'exit');
        current.style.position = 'absolute';
    }, 350);

    currentIndex += dir;

    setTimeout(() => {
        next.style.position = '';
        next.classList.add('active');
    }, 20);

    const qid       = next.dataset.id;
    const hasAnswer = answers.hasOwnProperty(qid);
    const isLast    = currentIndex === TOTAL - 1;

    btnPrev.disabled = currentIndex === 0;
    skipNote.textContent = hasAnswer ? '' : 'Select an answer to continue';

    btnNext.style.display   = isLast ? 'none' : '';
    btnSubmit.style.display = isLast ? ''     : 'none';
    btnNext.disabled        = !hasAnswer;
    btnSubmit.disabled      = !hasAnswer;

    updateProgress();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}


// ── SUBMIT ────────────────────────────────────────────
async function submitQuiz() {
    showScreen('screenLoading');
    window.scrollTo({ top: 0, behavior: 'smooth' });

    try {
        const res = await fetch('/submit', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({ answers })
        });

        if (!res.ok) throw new Error('Server error');

        const data = await res.json();
        renderResults(data);

    } catch (e) {
        showScreen('screenResult');
        document.getElementById('screenResult').innerHTML = `
            <div style="text-align:center; padding:60px 0;">
                <p style="color:var(--danger); font-family:var(--mono); font-size:13px; letter-spacing:1px;">
                    ⚠ ERROR — Could not reach server.<br><br>Please refresh the page and try again.
                </p>
            </div>`;
    }
}


// ── RENDER RESULTS ────────────────────────────────────
function renderResults(data) {
    showScreen('screenResult');
    window.scrollTo({ top: 0, behavior: 'smooth' });

    const riskClass = data.level === 'Low Risk'    ? 'risk-low'
                    : data.level === 'Medium Risk'  ? 'risk-med'
                    : 'risk-high';

    let feedbackHTML = '';

    if (!data.feedback || data.feedback.length === 0) {
        feedbackHTML = `
            <div class="all-clear">
                <div style="font-size:32px; margin-bottom:12px;">✓</div>
                <strong>No risky behaviours detected.</strong><br>
                You demonstrated strong cybersecurity awareness across every scenario.
                Keep these habits up — scammers evolve constantly.
            </div>`;
    } else {
        feedbackHTML = `<div class="feedback-header">// ${data.feedback.length} Risk${data.feedback.length > 1 ? 's' : ''} Identified — Review Below</div>`;

        data.feedback.forEach((fb, i) => {
            feedbackHTML += `
            <div class="fb-card" style="animation-delay:${i * 0.07}s">

                <div class="fb-question">⚠ ${fb.question}</div>

                <div class="fb-row">
                    <div class="fb-block unsafe">
                        <div class="fb-block-label">✗ &nbsp;What You're Doing</div>
                        <p>${fb.unsafe_practice}</p>
                    </div>
                    <div class="fb-block safe">
                        <div class="fb-block-label">✓ &nbsp;What You Should Do</div>
                        <p>${fb.safe_practice}</p>
                    </div>
                </div>

                <div class="fb-consequence">
                    <div class="fb-consequence-label">⚡ &nbsp;Potential Consequence</div>
                    <p>${fb.consequence}</p>
                </div>

                <div class="fb-tip">
                    <span class="tip-icon">💡</span>
                    <p>${fb.tip}</p>
                </div>

            </div>`;
        });
    }

    document.getElementById('screenResult').innerHTML = `
        <div class="result-hero">
            <div class="risk-label ${riskClass}">${data.level_emoji} &nbsp;${data.level}</div>
            <div class="risk-score ${riskClass}">${data.percentage}%</div>
            <div class="risk-desc">${data.score} of ${data.max_score} answers reflected safe behaviour</div>
            <div class="risk-message">${data.level_message}</div>
        </div>

        ${feedbackHTML}

        <button class="btn-retake" onclick="showLanding()">↺ &nbsp; Retake Assessment</button>
    `;
}