// QA helper (not loaded by the app). Inject it, then call runQA() to check contrast, overflow and design-token consistency.
(function () {
  const cv = document.createElement("canvas"); cv.width = cv.height = 1; const cx = cv.getContext("2d", { willReadFrequently: true });
  const rgba = (c) => { cx.clearRect(0, 0, 1, 1); cx.fillStyle = "#000"; cx.fillStyle = c; cx.fillRect(0, 0, 1, 1); const d = cx.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2], d[3] / 255]; };
  const parse = (c) => { if (!c || c === "transparent") return [0, 0, 0, 0]; const m = c.match(/^rgba?\(([^)]+)\)/); if (m) { const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p[3] === undefined ? 1 : p[3]]; } return rgba(c); };
  const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const blend = (top, bot) => { const a = top[3]; return [top[0] * a + bot[0] * (1 - a), top[1] * a + bot[1] * (1 - a), top[2] * a + bot[2] * (1 - a), 1]; };
  const gradStops = (img) => (img.match(/(rgba?\([^)]+\)|oklch\([^)]+\)|#[0-9a-f]{3,8})/gi) || []).map(parse);
  function bgOf(el) {
    // Collect backgrounds from the element up to the root, then composite bottom-up.
    const layers = []; let e = el;
    while (e && e.nodeType === 1) { const s = getComputedStyle(e); const img = s.backgroundImage; let c = parse(s.backgroundColor);
      if (img && img !== "none" && /gradient/.test(img)) { const st = gradStops(img); if (st.length) layers.push({ grad: st }); }
      if (c[3] > 0) layers.push({ c });
      if (c[3] >= 1) break; e = e.parentElement; }
    // Composite bottom-up; once a gradient is painted, the layers beneath it are hidden, so only its stops (and any tints above it) count.
    let base = [255, 255, 255, 1]; let stops = null;
    for (let i = layers.length - 1; i >= 0; i--) { const L = layers[i];
      if (L.grad) stops = L.grad.map(g => blend(g, base));
      else if (stops) stops = stops.map(st => blend(L.c, st)); else base = blend(L.c, base); }
    return stops || [base];
  }
  window.runQA = function (label) {
    // Finish enter animations first so text is measured at its resting opacity, not mid-fade.
    for (const an of document.getAnimations()) { const t = an.effect && an.effect.getTiming(); if (t && t.iterations !== Infinity) try { an.finish(); } catch (e) {} }
    const issues = []; const seen = new Set();
    const nodes = [...document.querySelectorAll("body *")].filter(el => { if (el.closest("svg")) return false; if (!el.offsetParent && getComputedStyle(el).position !== "fixed") return false; const t = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()); return t; });
    for (const el of nodes) {
      const s = getComputedStyle(el); if (s.visibility === "hidden" || +s.opacity === 0) continue;
      const r = el.getBoundingClientRect(); if (r.width === 0 || r.height === 0) continue;
      let op = 1; let e = el; while (e && e.nodeType === 1) { op *= +getComputedStyle(e).opacity; e = e.parentElement; }
      const fg = parse(s.color); const bgs = bgOf(el);
      const size = parseFloat(s.fontSize); const bold = +s.fontWeight >= 600; const large = size >= 24 || (bold && size >= 18.66);
      const need = large ? 3 : 4.5;
      let worst = 99; for (const bg of bgs) { const f = blend([fg[0], fg[1], fg[2], fg[3] * op], bg); const a = lum(f), b = lum(bg); const ratio = (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05); worst = Math.min(worst, ratio); }
      const disabled = el.closest("[disabled]") || el.closest(".lock-dim");
      if (worst < need && !disabled) { const txt = el.textContent.trim().slice(0, 40); const key = txt + "|" + worst.toFixed(2); if (seen.has(key)) continue; seen.add(key); issues.push({ type: "contrast", text: txt, ratio: +worst.toFixed(2), need, size, cls: (el.className && el.className.baseVal === undefined ? el.className : "") + " < " + (el.parentElement.className || "") }); }
    }
    // Overflow: page-level horizontal scroll and elements wider than their container or clipped text
    const doc = document.documentElement; if (doc.scrollWidth > doc.clientWidth + 1) issues.push({ type: "page-hscroll", by: doc.scrollWidth - doc.clientWidth });
    // a dialog or panel whose content is wider than itself scrolls sideways and cuts content off (missed once: the video player)
    for (const box of document.querySelectorAll(".dlg, .pop, .drawer, .aipanel")) { if (box.offsetParent === null && getComputedStyle(box).position !== "fixed") continue; if (box.scrollWidth > box.clientWidth + 1) issues.push({ type: "box-hscroll", el: box.className.toString().slice(0, 30), by: box.scrollWidth - box.clientWidth }); }
    for (const el of document.querySelectorAll("body *")) { const r = el.getBoundingClientRect(); if (!r.width || el.closest("svg")) continue;
      if (r.right > innerWidth + 1 && getComputedStyle(el).position !== "fixed" && !el.closest(".tablewrap,table,svg") && !inHScroller(el)) issues.push({ type: "off-right", el: el.tagName + "." + (el.className || ""), by: Math.round(r.right - innerWidth) });
      const s = getComputedStyle(el); if ((s.overflow === "hidden" || s.textOverflow === "ellipsis" || s.whiteSpace === "nowrap") && el.scrollWidth > el.clientWidth + 1 && el.textContent.trim() && !el.matches(".trunc,.ws .t b,.ws .t span,.tw b, .sr, .psug .w, .app.phone .way > span > span")) issues.push({ type: "clipped", text: el.textContent.trim().slice(0, 40), el: el.tagName + "." + (el.className || "") });
    }
    // A horizontal scroller (scene strip, tool rail on phones) that itself fits on screen is fine; its far items are scrolled to, not off the page
    function inHScroller(e) { for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) { const o = getComputedStyle(p).overflowX; if (o === "auto" || o === "scroll") { const pr = p.getBoundingClientRect(); return pr.right <= innerWidth + 1; } } return false; }
    // Content scrolled out of a scroll container's view is clipped, not overlapping anything
    function clippedByScroller(e, r) { for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) { const o = getComputedStyle(p).overflowY; if (o === "auto" || o === "scroll" || o === "hidden") { const pr = p.getBoundingClientRect(); if (r.bottom <= pr.top + 1 || r.top >= pr.bottom - 1) return true; } } return false; }
    // The part of an element its scroll containers actually show (a tile half-scrolled out of a panel is clipped there)
    function visRect(e) { const r = e.getBoundingClientRect(); let l = r.left, t = r.top, rt = r.right, b = r.bottom; for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) { const s = getComputedStyle(p); if (s.overflowX === "visible" && s.overflowY === "visible") continue; const q = p.getBoundingClientRect(); l = Math.max(l, q.left); t = Math.max(t, q.top); rt = Math.min(rt, q.right); b = Math.min(b, q.bottom); } return { left: l, top: t, right: rt, bottom: b }; }
    // Overlap: buttons and links that sit on top of other buttons, links or headings (not nested)
    const ctl = [...document.querySelectorAll("button, a, h1, h2, h3")].filter(e => { const r = e.getBoundingClientRect(); const st = getComputedStyle(e); return r.width > 0 && r.height > 0 && st.visibility !== "hidden" && !e.closest(".fixbar,.fixlist,.toast,.coach,svg,.sr") && !clippedByScroller(e, r); });
    const SHEETS = ".scrim,.drawer,.aipanel,.edvh"; // full-screen layers: only what is on them is checked against each other
    const scoped = [...document.querySelectorAll(SHEETS)].find(s => { const r = s.getBoundingClientRect(); return !s.matches(".edvh") || (r.width >= innerWidth - 1 && r.height >= innerHeight - 1); });
    const pool = scoped ? ctl.filter(e => e.closest(SHEETS)) : ctl;
    // A pinned bar (position: sticky, e.g. the phone composer) is opaque and meant to cover content scrolling under it
    const pinnedBar = e => { for (let p = e; p && p !== document.body; p = p.parentElement) if (getComputedStyle(p).position === "sticky" || p.matches(".app.phone .create > .prompt")) return p; return null; };
    for (let i = 0; i < pool.length; i++) for (let j = i + 1; j < pool.length; j++) { const A = pool[i], B = pool[j]; if (A.contains(B) || B.contains(A)) continue; if (!!pinnedBar(A) !== !!pinnedBar(B)) continue; if (!!A.closest('.pop') !== !!B.closest('.pop')) continue; if (A.closest('.crow') && A.closest('.crow') === B.closest('.crow') && (A.matches('.crmenu') || B.matches('.crmenu'))) continue; if ((A.matches('.edflyout') && B.matches('[data-k="shapes"]')) || (B.matches('.edflyout') && A.matches('[data-k="shapes"]'))) continue; /* the shape picker is a corner trigger on the Shapes tool, as in live */ /* a row's hover menu sits over its own hidden time and dot by design */ /* an open menu sits over the page by design; menu-hidden checks it is on top */
      const a = visRect(A), b = visRect(B); const w = Math.min(a.right, b.right) - Math.max(a.left, b.left), h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (w > 4 && h > 4) issues.push({ type: "overlap", text: (A.textContent.trim() || A.getAttribute("aria-label") || A.tagName).slice(0, 24) + " × " + (B.textContent.trim() || B.getAttribute("aria-label") || B.tagName).slice(0, 24) }); }
    // Escaped: a button or link whose centre lies outside its parent's box (misplaced by positioning)
    for (const e of ctl) { if (e.matches("h1,h2,h3")) continue; const p = e.parentElement; if (!p) continue; const ps = getComputedStyle(p); if (/auto|scroll/.test(ps.overflowY + ps.overflowX) && (p.scrollHeight > p.clientHeight + 1 || p.scrollWidth > p.clientWidth + 1)) continue; /* reachable by scrolling */ const r = e.getBoundingClientRect(), q = p.getBoundingClientRect(); if (!q.width) continue;
      const cx = (r.left + r.right) / 2, cy = (r.top + r.bottom) / 2; if (cx < q.left - 2 || cx > q.right + 2 || cy < q.top - 2 || cy > q.bottom + 2) issues.push({ type: "escaped", text: (e.textContent.trim() || e.getAttribute("aria-label") || e.tagName).slice(0, 30) }); }
    // Wrapped: text inside a one-line control (button, tab, chip, nav item) that breaks onto a second line
    for (const c of document.querySelectorAll("button, a.btn, a.navitem, .pill, .chip, .navitem, [role=tab], .edchip, .seg button, .ws")) { const cr = c.getBoundingClientRect(); if (!cr.width || cr.height > 44 || c.closest(".fixbar,.fixlist,.toast,.edframe,svg") || c.matches(".madewith")) continue; /* the "Made with Clueso AI" line wraps to two lines by design */
      const tw = document.createTreeWalker(c, NodeFilter.SHOW_TEXT); let n; while ((n = tw.nextNode())) { if (!n.textContent.trim()) continue; const rg = document.createRange(); rg.selectNodeContents(n); const tops = new Set([...rg.getClientRects()].filter(q => q.width > 0).map(q => Math.round(q.top))); if (tops.size > 1) { issues.push({ type: "wrapped", text: c.textContent.trim().replace(/\s+/g, " ").slice(0, 40), cls: (c.className || c.tagName).toString().split(" ")[0] }); break; } } }
    // Spilled: content taller than its box, drawn outside it (a fixed height that the text no longer fits)
    for (const el of document.querySelectorAll("button, a, li, .ws, .usage, .pill, .chip, .navitem, .btn, .card, .box, .row, [class*=row]")) { const r = el.getBoundingClientRect(); if (!r.width || r.height > 120 || el.closest(".fixbar,.fixlist,svg,.edframe")) continue; const st = getComputedStyle(el); if (st.overflowY !== "visible" || st.display === "inline" || st.display === "contents") continue; if (el.scrollHeight > el.clientHeight + 2 && el.clientHeight > 0) issues.push({ type: "spilled", text: (el.textContent.trim() || el.getAttribute("aria-label") || el.tagName).replace(/\s+/g, " ").slice(0, 40), by: el.scrollHeight - el.clientHeight, cls: (el.className || el.tagName).toString().split(" ")[0] }); }
    // Unpinned: a row with a spacer (.grow, .spacer, flex:1) whose items after it should end at the row's right edge but don't
    // (the editor's right-hand group once drifted to the middle when a never-growing spacer collapsed to 0 px)
    for (const sp of document.querySelectorAll(".grow, .spacer, [style*='flex:1'], [style*='flex: 1']")) { const p = sp.parentElement; if (!p || sp.closest("svg,.fixbar,.fixlist,.toast")) continue; const ps = getComputedStyle(p);
      if (!/flex/.test(ps.display) || !/^row/.test(ps.flexDirection) || p.scrollWidth > p.clientWidth + 1) continue; const pr = p.getBoundingClientRect(); if (!pr.width) continue;
      const kids = [...p.children].filter(k => { const r = k.getBoundingClientRect(); const s = getComputedStyle(k); return (k === sp ? s.display !== "none" : r.width > 0) && s.position !== "absolute" && s.position !== "fixed"; });
      const i = kids.indexOf(sp); const after = kids.slice(i + 1); if (i < 0 || !after.length) continue; const sr = sp.getBoundingClientRect(), last = after[after.length - 1], lr = last.getBoundingClientRect();
      const mid = sr.top + sr.height / 2; if (mid < lr.top - 1 || mid > lr.bottom + 1) continue; /* the items after the spacer wrapped onto another line */ /* wrapped onto another line */
      const edge = ps.direction === "rtl" ? 0 : pr.right - parseFloat(ps.paddingRight) - parseFloat(ps.borderRightWidth); const gap = edge - lr.right - (parseFloat(getComputedStyle(last).marginRight) || 0); /* an item's own right margin is deliberate */
      if (gap > 2) issues.push({ type: "unpinned", text: (last.textContent.trim() || last.getAttribute("aria-label") || last.tagName).replace(/\s+/g, " ").slice(0, 30), by: Math.round(gap), cls: (p.className || p.tagName).toString().split(" ")[0] }); }
    // Backdrop: a dialog's scrim must cover the whole viewport (a class collision once shrank it to 137 px)
    for (const sc of document.querySelectorAll(".scrim")) { const r = sc.getBoundingClientRect(); if (r.top > 0 || r.left > 0 || r.width < innerWidth - 1 || r.height < innerHeight - 1) issues.push({ type: "scrim-partial", text: Math.round(r.width) + "x" + Math.round(r.height) }); }
    // Search: the input must stay pinned when the results scroll
    const sb = document.querySelector(".sbody"), sh = document.querySelector(".shd"); if (sb && sh) { const t0 = sh.getBoundingClientRect().top; sb.scrollTop = 9999; if (Math.abs(sh.getBoundingClientRect().top - t0) > 0.5) issues.push({ type: "search-header-moved" }); sb.scrollTop = 0; }
    // Layers: an open menu must be on top where it is drawn (a menu once rendered under the Clueso AI panel)
    for (const pop of document.querySelectorAll(".pop")) { const r = pop.getBoundingClientRect(); if (r.top < 0 || r.left < 0 || r.bottom > innerHeight + 1 || r.right > innerWidth + 1) issues.push({ type: "menu-offscreen", text: (pop.innerText || "").slice(0, 30) }); const x = r.left + r.width / 2, y = r.top + Math.min(r.height / 2, 20); const top = document.elementFromPoint(x, y); if (top && !pop.contains(top)) issues.push({ type: "menu-hidden", text: (pop.innerText || "").slice(0, 30) }); }
    // Token consistency
    const tally = (prop, sel = "body *") => { const m = {}; for (const el of document.querySelectorAll(sel)) { if (!el.getBoundingClientRect().width) continue; const v = getComputedStyle(el)[prop]; m[v] = (m[v] || 0) + 1; } return m; };
    const fs = tally("fontSize"); const btnH = {}; for (const b of document.querySelectorAll("button,.btn,a.btn")) { const h = Math.round(b.getBoundingClientRect().height); if (h) btnH[h] = (btnH[h] || 0) + 1; }
    const radii = tally("borderRadius", "button,.btn,.pill,.chip,.box,.pcard,.way,.job,.goal,.opt,.choice,.field input,.prompt,.dlg,.pop");
    return JSON.stringify({ label: label || location.hash, vw: innerWidth, issues: issues.slice(0, 60), issueCount: issues.length, fontSizes: fs, buttonHeights: btnH, radii });
  };
})();
// Sweep every route and layer at the current viewport; returns only screens with issues.
window.runSweep = async function (opts = {}) {
  const wait = ms => new Promise(x => setTimeout(x, ms));
  const routes = ['/signin', '/start/1', '/start/2', '/start/3', '/home', '/projects', '/project/p1', '/project/p2', '/chats', '/analytics', '/analytics/p1', '/clueprints', '/brand-kit', '/edit/p1', '/integrations', '/settings/general', '/settings/members', '/settings/plan-and-usage', '/settings/video-defaults', '/settings/language-and-voice', '/settings/player-and-links', '/settings/profile'];
  S.start.jobs = new Set(['demo']); S.start.job = 'demo'; S.start.have = S.start.have || 'idea'; S.start.brief = S.start.brief || 'A 1-minute demo'; S.firstRun = true; S.collapsed = !!opts.collapsed;
  const prevTheme = S.theme; if (opts.theme) applyTheme(opts.theme); // runSweep({ theme: 'dark' }) checks the dark theme
  const out = []; let total = 0;
  const keep = q => { if (opts.layoutOnly) q.issues = q.issues.filter(i => i.type !== 'contrast'); q.issueCount = q.issues.length; return q; };
  const fmt = (r, q) => { total += q.issueCount; return q.issueCount ? r + ' :: ' + q.issues.map(i => i.type + ':' + (i.text || i.el || '') + (i.ratio ? ' (' + i.ratio + '/' + i.need + ')' : '') + (i.by ? ' by ' + i.by : '')).join(' | ') : null; };
  for (const r of routes) { location.hash = r; await wait(280); out.push(fmt(r, keep(JSON.parse(runQA(r))))); }
  // States: build chip while building elsewhere, ready box after a build, projects search with no match
  S.generating = { id: 'p1', step: 2, cost: 250 }; location.hash = '/home'; await wait(280); out.push(fmt('state:building', keep(JSON.parse(runQA('building'))))); S.generating = null;
  S.ready = 'p1'; location.hash = '/project/p1'; await wait(280); out.push(fmt('state:ready', keep(JSON.parse(runQA('ready'))))); S.ready = null;
  S.projQ = 'zzz'; location.hash = '/projects'; await wait(280); render(); await wait(60); out.push(fmt('state:projects-none', keep(JSON.parse(runQA('pnone'))))); S.projQ = '';
  // Conversation states: a plan to approve on the Clueso AI page (options open), a finished one, the empty page, and a conversation in the panel
  { const id = 'cqa'; if (!chatById(id)) TASKS.unshift({ id, t: 'QA brief', pid: null, st: 'Waiting for you', cr: '0', w: 'just now', kind: 'Planning a video', ask: 'A 1-minute demo of inviting a teammate in Taskly', plan: true });
    S.chatId = id; S.planOpen = true; location.hash = '/chats'; await wait(280); render(); await wait(60); out.push(fmt('state:chat-plan', keep(JSON.parse(runQA('chat plan')))));
    S.chatId = 'c1'; S.planOpen = false; render(); await wait(60); out.push(fmt('state:chat-done', keep(JSON.parse(runQA('chat done')))));
    S.chatId = null; render(); await wait(60); out.push(fmt('state:chat-empty', keep(JSON.parse(runQA('chat empty')))));
    // Every seeded conversation state on the Chats page: question, plan, failed, done (long brief, checklist), polished, plus New chat and a building one
    for (const cid of ['c3', 'c4', 'c5', 'c1', 'c2', 'c6']) { if (!chatById(cid)) continue; S.chatId = cid; render(); await wait(60); out.push(fmt('state:chat-' + cid, keep(JSON.parse(runQA('chat ' + cid))))); }
    S.chatId = 'new'; render(); await wait(60); out.push(fmt('state:chat-new', keep(JSON.parse(runQA('chat new')))));
    // Focus view (one chat full width), with and without its "Made in this chat" panel
    { const pf = S.chatFocus, pp = S.chatPanel; S.chatFocus = true; for (const [cid, panel] of [['c2', true], ['c2', false], ['c3', true], ['c1', true]]) { S.chatId = cid; S.chatPanel = panel; render(); await wait(60); out.push(fmt('state:focus-' + cid + (panel ? '' : '-nopanel'), keep(JSON.parse(runQA('focus ' + cid))))); } S.chatFocus = pf; S.chatPanel = pp; render(); }
    { const c4 = chatById('c4'); if (c4) { const sv = { ...c4 }; c4.pid = 'p1'; c4.st = 'Building'; S.generating = { id: 'p1', step: 3, cost: 250 }; S.chatId = 'c4'; render(); await wait(60); out.push(fmt('state:chat-building', keep(JSON.parse(runQA('chat building'))))); S.generating = null; Object.assign(c4, sv); } }
    S.ai = true; S.pChat = 'c2'; setAiView(innerWidth <= 760 ? 'full' : 'side'); location.hash = '/project/p2'; await wait(280); render(); await wait(60); out.push(fmt('state:panel-chat', keep(JSON.parse(runQA('panel chat')))));
    TASKS.splice(TASKS.findIndex(c => c.id === id), 1); S.ai = false; S.pChat = null; render(); }
  S.start.jobs = new Set(); location.hash = '/start/1'; await wait(280); out.push(fmt('state:start-empty', keep(JSON.parse(runQA('start-empty'))))); S.start.jobs = new Set(['demo']);
  location.hash = '/home'; await wait(280);
  const layerOnly = q => { q.issues = q.issues.filter(i => [...document.querySelectorAll('.scrim *, .drawer *, .aipanel *, .pop *')].some(e => (e.textContent || '').trim().slice(0, 40) === i.text || (i.el && e.matches && e.matches((i.el.split('.')[0] || '*').toLowerCase())))); return keep(q); };
  const dl = [['share', () => shareDialog()], ['invite', () => inviteDialog()], ['record', () => openCreate('record')], ['upload', () => openCreate('upload')], ['translate-rules', () => translateDialog(true)], ['style-drawer', () => styleDrawer(2)], ['cmdk', () => cmdk()], ['cmdk-query', () => { cmdk(); const i = document.querySelector('#cq'); i.value = 'ta'; i.dispatchEvent(new Event('input')); }], ['cmdk-none', () => { cmdk(); const i = document.querySelector('#cq'); i.value = 'xyzq'; i.dispatchEvent(new Event('input')); }]];
  for (const [n, f] of dl) { closeLayers(); f(); await wait(220); out.push(fmt('layer:' + n, layerOnly(JSON.parse(runQA(n))))); }
  // Clueso AI panel in each view, on pages with different contexts (whole page checked, since side-by-side reflows it)
  closeLayers(); const views = innerWidth <= 760 ? ['full'] : ['side', 'float'];
  for (const v of views) for (const r of ['/projects', '/project/p1', '/analytics', '/clueprints', '/settings/plan-and-usage']) { S.ai = true; setAiView(v); location.hash = r; await wait(280); render(); await wait(60); out.push(fmt('ai:' + v + r, keep(JSON.parse(runQA('ai ' + v))))); }
  for (const r of ['/home', '/projects']) { S.ai = false; location.hash = r; await wait(250); render(); await wait(60); const b = document.querySelector(r === '/home' ? '.create [data-act="model"]' : '[data-act="filter"]'); if (b) { b.click(); await wait(150); out.push(fmt('menu:' + r, keep(JSON.parse(runQA('menu ' + r))))); closeLayers(); } }
  for (const m of ['aiviewmenu', 'aicheckin', 'model', 'aiadd']) { S.ai = true; setAiView(innerWidth <= 760 ? 'full' : 'side'); location.hash = '/project/p1'; await wait(250); render(); await wait(60); const b = document.querySelector('[data-act="' + m + '"]'); if (b) { b.click(); await wait(150); out.push(fmt('ai-menu:' + m, keep(JSON.parse(runQA('ai menu ' + m))))); closeLayers(); } }
  S.ai = false; setAiView(aiViewDefault()); S.collapsed = false; render();
  if (opts.theme) applyTheme(prevTheme || 'system');
  return 'viewport ' + innerWidth + 'x' + innerHeight + (opts.theme ? ' · ' + opts.theme : '') + ' · issues: ' + total + '\n' + out.filter(Boolean).join('\n');
};

// Clicks every menu button the way a user would (not by calling popover directly) and reports any that open nothing
// or throw. Added after the panel's View menu threw on click and the sweep, which opened it directly, missed it.
async function runMenuCheck() {
  const errs = []; const onErr = e => errs.push(String(e.message)); window.addEventListener("error", onErr);
  const wait = ms => new Promise(r => setTimeout(r, ms)); const res = [];
  for (const r of ["/home", "/projects", "/project/p1", "/chats", "/clueprints", "/brand-kit", "/settings/general", "/analytics", "/integrations", "/edit/p1"]) {
    for (const withAI of [false, true]) {
      S.ai = false; location.hash = "#" + r; await wait(450); render();
      if (withAI && panelAllowed()) { S.ai = true; render(); await wait(300); }
      const btns = [...document.querySelectorAll('[aria-haspopup="menu"], [data-act=help], [data-act=ws], [data-act=newmenu], [data-act=attach], [data-act=filter]')].filter(b => b.getBoundingClientRect().width > 0);
      for (const b of btns) {
        closeLayers(); const lab = (b.getAttribute("aria-label") || b.innerText || b.dataset.act).trim().slice(0, 30); const n = errs.length;
        try { b.click(); } catch (e) { errs.push(e.message); }
        await wait(120);
        if (!document.querySelector(".pop") && !document.querySelector(".scrim")) res.push(`${r}${withAI ? " +panel" : ""} :: ${lab} opened nothing`);
        if (errs.length > n) res.push(`${r} :: ${lab} threw ${errs[errs.length - 1]}`);
        closeLayers();
      }
    }
  }
  window.removeEventListener("error", onErr); S.ai = false;
  return `menus · issues: ${res.length}\n` + res.join("\n");
}

// Every editor state at the current viewport: each side panel, the article, Clueso AI, version history, an element
// selected (inspector), the detailed and collapsed timeline, find and replace, and a drawing tool on. Layout checks only.
window.runEditorStates = async function () {
  const wait = ms => new Promise(x => setTimeout(x, ms)); location.hash = '/edit/p1'; await wait(300); const e = S.ed; const keep = { panel: e.panel, view: e.view, vh: e.vh, sel: e.sel, timeline: e.timeline, collapsed: e.collapsed, replace: e.replace, mode: e.mode }, keepAi = S.ai;
  const out = []; let total = 0;
  const chk = (label) => { const q = JSON.parse(runQA(label)); const iss = q.issues.filter(i => i.type !== 'contrast'); total += iss.length; if (iss.length) out.push(label + ' :: ' + iss.map(i => i.type + ':' + (i.text || i.el || '') + (i.by ? ' by ' + i.by : '')).join(' | ')); };
  const set = async ({ ai, ...o }, label) => { Object.assign(e, keep, o); S.ai = !!ai; if (S.ai) setAiView(innerWidth <= 760 ? 'full' : 'side'); render(); await wait(120); chk(label); };
  for (const p of ['', 'script', 'media', 'effects', 'animation', 'templates', 'transitions', 'captions']) await set({ panel: p, view: 'video' }, 'panel:' + (p || 'none'));
  for (const p of ['', 'script']) await set({ panel: p, view: 'video', ai: true }, 'ai+panel:' + (p || 'none'));
  await set({ view: 'guide', panel: '' }, 'article'); await set({ view: 'guide', ai: true }, 'article+ai');
  await set({ vh: true, panel: 'script' }, 'version-history');
  { const l = e.scenes[e.scene].layers[0]; if (l) await set({ sel: l.id, panel: 'script' }, 'inspector'); }
  await set({ timeline: true, panel: 'script' }, 'detailed-timeline'); await set({ collapsed: true, panel: 'script' }, 'collapsed-timeline');
  await set({ replace: true, panel: 'script' }, 'find-replace'); await set({ mode: 'text', panel: 'script' }, 'text-tool');
  Object.assign(e, keep); S.ai = keepAi; render();
  return 'editor ' + innerWidth + 'x' + innerHeight + ' · issues: ' + total + '\n' + out.join('\n');
};
