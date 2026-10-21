// Side-panel matrix check (R-ED12): opens each left/right combination and measures the visible canvas, controls covered by an
// overlay, controls clipped by their card, and sideways page scroll. Load from the console: run __runAll() at each width.
window.__meas = async (label, setup) => {
  S.ai = false; S.ed.vh = false; S.ed.sel = null; S.ed.view = "video"; S.ed.scenes[0].layers = []; S.ed.scene = 0; edPrefs.keepcanvas = false; edPrefs.fullheight = false; S.aiView = "side"; S.ed.panel = ""; S.ed.dockTab = "left"; S.ed.lastAi = false; S.ed.lastVh = false;
  setup(); render(); await new Promise(r => setTimeout(r, 150)); document.querySelectorAll(".aipanel").forEach(a => { a.style.animation = "none"; a.classList.remove("arrive"); }); await new Promise(r => setTimeout(r, 40));
  const R = e => e && e.getBoundingClientRect(); const vis = e => { const r = R(e); return r && r.width > 0 && r.height > 0 && getComputedStyle(e).display !== "none"; };
  const overlays = [...document.querySelectorAll(".aipanel, .edvh, .edinsp, .ed.keep .edpanel")].filter(vis);
  const fr = R(document.querySelector(".edframe, .edart, .edgd"));
  let visW = 0; if (fr) { let x0 = fr.left, x1 = fr.right; for (const o of overlays.map(R)) { if (o.top < fr.bottom && o.bottom > fr.top) { if (o.left <= x0 && o.right > x0) x0 = Math.max(x0, o.right); if (o.right >= x1 && o.left < x1) x1 = Math.min(x1, o.left); } } visW = Math.max(0, Math.round(x1 - x0)); }
  const sheet = S.ed && edTier() === "phone" && (S.ai || S.ed.vh);
  const ctrls = [...document.querySelectorAll(".ed button, .ed input")].filter(vis);
  const covered = sheet ? [] : ctrls.filter(b => { if (b.closest(".edinsp")) return false; const r = R(b); return overlays.filter(o => !o.contains(b) && !(o.matches(".edpanel") && false)).some(o => { const q = R(o); if (o.matches(".edinsp") && b.closest(".edcanvas")) return false; return r.left < q.right - 1 && r.right > q.left + 1 && r.top < q.bottom - 1 && r.bottom > q.top + 1; }); }).map(b => (b.getAttribute("aria-label") || b.innerText).slice(0, 14));
  const clipped = ctrls.filter(b => { const r = R(b); const c = b.closest(".edgrp,.edbottom,.edpanel,.edrail,.edinsp"); if (!c) return false; const q = R(c); return (r.right > q.right + 1 || r.left < q.left - 1) && !b.closest(".edrail.edfmt,.edscenes,.tabs,.edrail") ; }).map(b => (b.getAttribute("aria-label") || b.innerText).slice(0, 14));
  const ap = document.querySelector(".aipanel, .edvh"); const apc = ap && vis(ap) ? [...ap.querySelectorAll("button, textarea, input")].filter(vis).filter(b => { const r = R(b), q = R(ap); return r.right > q.right + 1 || r.left < q.left - 1; }).map(b => (b.getAttribute("aria-label") || b.innerText).slice(0, 12)) : [];
  return `${label} | tier ${edTier()} panel ${S.ed.panel || "-"} ai ${S.ai ? S.aiView : "-"} vh ${S.ed.vh} tab ${S.ed.dockTab} | canvas ${visW}/${fr ? Math.round(fr.width) : 0} | covered ${covered.length}${covered.length ? " " + covered.slice(0, 4).join(",") : ""} | clipped ${clipped.length ? clipped.slice(0, 3).join(",") : 0} | rightClip ${apc.length ? apc.slice(0, 3).join(",") : 0} | hs ${document.documentElement.scrollWidth - innerWidth}${sheet ? " | sheet" : ""}`;
};
window.__states = [
  ["script+ai", () => { S.ed.panel = "script"; S.ai = true; }],
  ["script+ai tab left", () => { S.ed.panel = "script"; S.ai = true; S.ed.lastAi = true; S.ed.dockTab = "left"; }],
  ["media+ai", () => { S.ed.panel = "media"; S.ai = true; }],
  ["captions+ai", () => { S.ed.panel = "captions"; S.ai = true; }],
  ["script+float", () => { S.ed.panel = "script"; S.ai = true; S.aiView = "float"; }],
  ["script+vh", () => { S.ed.panel = "script"; S.ed.vh = true; }],
  ["ai only", () => { S.ai = true; }],
  ["script+insp", () => { S.ed.panel = "script"; S.ed.scenes[0].layers = [{ id: "z", type: "text", x: 70, y: 30, text: "Hi", shape: "" }]; S.ed.sel = "z"; }],
  ["script+ai+insp", () => { S.ed.panel = "script"; S.ai = true; S.ed.scenes[0].layers = [{ id: "z", type: "text", x: 70, y: 30, text: "Hi", shape: "" }]; S.ed.sel = "z"; }],
  ["keep+script+ai", () => { edPrefs.keepcanvas = true; S.ed.panel = "script"; S.ai = true; }],
  ["fullh+script+ai", () => { edPrefs.fullheight = true; S.ed.panel = "script"; S.ai = true; }],
  ["article+ai", () => { S.ed.view = "guide"; PROJECTS.find(p => p.id === "p1").article = true; S.ai = true; }],
];
window.__runAll = async () => { const out = []; for (const [l, f] of __states) out.push(await __meas(l, f)); S.ai = false; S.ed.panel = "script"; S.ed.sel = null; S.ed.vh = false; S.ed.view = "video"; S.ed.scenes[0].layers = []; edPrefs.keepcanvas = false; edPrefs.fullheight = false; render(); return out.join("\n"); };
