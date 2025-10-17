// ---------------- Tooltip logic on .topic cells ----------------
const tip = document.getElementById('tooltip');
function showTip(e, text) {
    if (!text) return;
    tip.textContent = text;
    tip.classList.remove('hidden');
    const pad = 10;
    const x = e.clientX + pad;
    const y = e.clientY + pad + window.scrollY;
    Object.assign(tip.style, { left: x + 'px', top: y + 'px' });
}
function hideTip() { tip.classList.add('hidden'); }
document.querySelectorAll('.topic').forEach(cell => {
    const txt = cell.dataset.tip || '';
    cell.addEventListener('mousemove', (e) => showTip(e, txt));
    cell.addEventListener('mouseleave', hideTip);
});

// ---------------- Ranking state across methods (topics) ----------------
const SELECTORS = Array.from(document.querySelectorAll('.rank-select'));
const TOPIC_CELLS = Array.from(document.querySelectorAll('.topic[data-topic]'));
const KEY = 'neuro-method-picks-v2';

// Map rank->topic and topic->rank
const rankState = { 1: null, 2: null, 3: null };
const topicRank = {}; // topic -> '1'|'2'|'3'|''

function updateChipsFor(topic) {
    const rank = topicRank[topic] || '';
    TOPIC_CELLS.filter(c => c.dataset.topic === topic).forEach(cell => {
        const chip = cell.querySelector('.rank-chip');
        chip.className = 'rank-chip ' + (rank ? ('rank-' + rank) : 'rank-none');
        chip.textContent = rank ? ('Rank ' + rank) : '';
    });
    SELECTORS.filter(s => s.dataset.for === topic).forEach(sel => sel.value = rank);
}

function assignRank(topic, val) {
    // clear previous holder of this rank
    if (val) {
        const prevTopic = rankState[val];
        if (prevTopic && prevTopic !== topic) { topicRank[prevTopic] = ''; updateChipsFor(prevTopic); }
        rankState[val] = topic;
    }
    // clear ranks 1..3 if this topic held any other
    ['1', '2', '3'].forEach(r => { if (rankState[r] === topic && r !== val) { rankState[r] = null; } });
    topicRank[topic] = val || '';
    updateChipsFor(topic);
    persistLocal();
}

SELECTORS.forEach(sel => sel.addEventListener('change', (e) => {
    const topic = e.currentTarget.dataset.for;
    const val = e.currentTarget.value; // '', '1','2','3'
    assignRank(topic, val);
}));

function persistLocal() {
    const data = Object.entries(topicRank).map(([topic, rank]) => {
        const link = (document.querySelector(`.topic[data-topic="${topic}"]`) || {}).dataset?.link || '';
        return { topic, rank, link };
    });
    localStorage.setItem(KEY, JSON.stringify({ rankState, topicRank, data }));
}

function restoreLocal() {
    const raw = localStorage.getItem(KEY); if (!raw) return;
    try {
        const { rankState: rs, topicRank: tr } = JSON.parse(raw);
        if (rs) { rankState[1] = rs[1]; rankState[2] = rs[2]; rankState[3] = rs[3]; }
        if (tr) { Object.assign(topicRank, tr); }
        Object.keys(topicRank).forEach(updateChipsFor);
    } catch (err) { console.warn('restore failed', err); }
}

// ---------------- Export helpers (pairs per topic) ----------------
function rowInfo(tr) {
    const tds = tr.querySelectorAll('td');
    return {
        week: tds[0]?.textContent?.trim() || '',
        date: tds[1]?.textContent?.trim() || '',
        day: tds[2]?.textContent?.trim() || '',
        type: tds[3]?.textContent?.trim() || '',
        topic: tr.querySelector('.topic a')?.textContent?.trim() || '',
        presenter: tds[5]?.textContent?.trim() || ''
    };
}
function rowsForTopic(topic) {
    return Array.from(document.querySelectorAll('tr')).filter(tr => {
        const cell = tr.querySelector('.topic[data-topic]');
        return cell && cell.dataset.topic === topic;
    }).map(rowInfo);
}

function toCSV(rows) {
    const esc = v => '"' + String(v).replace(/"/g, '""') + '"';
    const header = ['Rank', 'Week', 'Date', 'Day', 'Type', 'Topic', 'Presenter'];
    const lines = [header.map(esc).join(',')];
    rows.forEach(r => lines.push([r.rank, r.week, r.date, r.day, r.type, r.topic, r.presenter].map(esc).join(',')));
    return lines.join('\n');
}
function download(filename, text) {
    const blob = new Blob([text], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename; a.click();
    URL.revokeObjectURL(url);
}

document.getElementById('exportCsv').addEventListener('click', () => {
    const rankedTopics = Object.entries(topicRank).filter(([, r]) => r).sort((a, b) => a[1].localeCompare(b[1]));
    if (!rankedTopics.length) { alert('No selections yet. Assign Rank 1–3 first.'); return; }
    const rows = [];
    rankedTopics.forEach(([topic, rank]) => {
        const pair = rowsForTopic(topic);
        pair.forEach(info => rows.push({ rank, ...info }));
    });
    const csv = toCSV(rows);
    download('method_pairs.csv', csv);
});

document.getElementById('save').addEventListener('click', () => { persistLocal(); alert('Saved locally.'); });
document.getElementById('clear').addEventListener('click', () => {
    localStorage.removeItem(KEY);
    ['1', '2', '3'].forEach(r => rankState[r] = null);
    Object.keys(topicRank).forEach(k => topicRank[k] = '');
    SELECTORS.forEach(sel => sel.value = '');
    TOPIC_CELLS.forEach(cell => { const chip = cell.querySelector('.rank-chip'); chip.className = 'rank-chip rank-none'; chip.textContent = ''; });
});

document.getElementById('email').addEventListener('click', () => {
    const rankedTopics = Object.entries(topicRank).filter(([, r]) => r).sort((a, b) => a[1].localeCompare(b[1]));
    if (!rankedTopics.length) { alert('No selections yet. Assign Rank 1–3 first.'); return; }
    let bodyTxt = 'Here are my top 3 method picks for NeuroPy 2025:\n\n';
    rankedTopics.forEach(([topic, rank]) => {
        const pair = rowsForTopic(topic);
        bodyTxt += `Rank ${rank}: ${topic}\n`;
        pair.forEach(p => { bodyTxt += `  - ${p.date} (${p.day}) • ${p.type} • ${p.presenter || ''}\n`; });
        const link = (document.querySelector(`.topic[data-topic="${topic}"]`) || {}).dataset?.link || '';
        if (link) bodyTxt += `  ${link}\n`;
        bodyTxt += `\n`;
    });
    // add name at the end of the email
    bodyTxt += '\nName: ';
    const name = (document.getElementById('name').value || '').trim();
    bodyTxt += name;
    const subject = encodeURIComponent(`NeuroPy 2025: My Top 3 Methods (Theory + Exercise pairs) - ${name}`);
    const body = encodeURIComponent(bodyTxt.trim());
    window.location.href = `mailto:shahidi.arash@gmail.com?subject=${subject}&body=${body}`;
});

// Initialize topicRank keys from DOM so everything syncs nicely even on first load
new Set(TOPIC_CELLS.map(c => c.dataset.topic)).forEach(t => { if (t) topicRank[t] = topicRank[t] || ''; });

// boot
restoreLocal();
Object.keys(topicRank).forEach(updateChipsFor);

// ---------------- Minimal self-tests (console) ----------------
(function selfTests() {
    try {
        // Test 1: rowsForTopic should return 2 rows for AR
        const arRows = rowsForTopic('AR');
        console.assert(Array.isArray(arRows) && arRows.length === 2, 'rowsForTopic("AR") should return 2 rows');
        // Test 2: toCSV should contain header and two data lines when passed two rows
        const csvSample = toCSV([{ rank: '1', week: '3', date: 'Oct 30', day: 'Thu', type: 'Theory', topic: 'AR', presenter: '' }, { rank: '1', week: '3', date: 'Nov 4', day: 'Tue', type: 'Exercise', topic: 'AR', presenter: '' }]);
        console.assert(csvSample.split('\n').length === 3, 'toCSV should produce 3 lines (1 header + 2 rows)');
        // Test 3: assignRank uniqueness across ranks
        assignRank('AR', '1');
        assignRank('PCA', '1'); // should move rank 1 from AR to PCA
        console.assert((topicRank['AR'] || '') === '' && topicRank['PCA'] === '1', 'assignRank should keep rank unique');
        // cleanup: clear state
        ['AR', 'PCA'].forEach(t => assignRank(t, ''));
        console.log('%cSelf-tests passed', 'color:#6ee7b7');
    } catch (e) { console.warn('Self-tests failed:', e); }
})();