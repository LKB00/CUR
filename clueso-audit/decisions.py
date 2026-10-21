"""Decision log for the redesign prototype: every change with its evidence, plus open proposals."""
import html, json, os
E = html.escape
HERE = os.path.dirname(__file__)
SCREENS = [("signin", "Sign-in"), ("s1", "Get started: one question"), ("s2", "Get started: what Clueso does"), ("create", "Create"), ("agent", "Agent"), ("analytics", "Analytics"), ("projects", "Projects"), ("project", "Project page"), ("library", "Library"), ("integrations", "Integrations"), ("settings", "Settings")]
PROPOSALS = [
 ("Record a browser tab without installing the extension", "Clueso requires the Chrome extension today. Browsers can capture a tab natively (the Screen Capture API), so this is technically plausible, but engineering must confirm the editor can work with it without click data.", "Engineering spike; compare activation with and without the install step"),
 ("\"Quality: Fast / Best\" instead of a list of six models", "Based on Clueso's own note that a smaller model costs about half per message. The quality difference between models hasn't been measured.", "Internal benchmark of output quality and cost per model"),
 ("Make the role question optional", "Nothing visible changes with role today, but Clueso may use it for sales routing.", "Ask the growth team; check whether role predicts activation"),
 ("Merge Chats into Agent, and group Clueprints, templates, components and brand kit as Library", "The grouping follows Clueso's own pricing groups and help-center wording, not tested user mental models.", "Open card sort (15+ participants), then tree test of old vs new nav"),
 ("Show a labeled sample Analytics dashboard on Free", "It should reduce the blank-paywall problem, but its effect on upgrades is unknown.", "A/B test: sample dashboard vs current paywall, measuring upgrade clicks"),
 ("One \"what to make\" question (4 jobs) in place of Clueso's 7-goal survey", "The 4 jobs cover Clueso's goals, but Clueso may use the 7 goals for segmentation or sales.", "Check with growth; compare activation between the two flows"),
 ("Show a before-and-after example instead of building in onboarding", "Should make onboarding faster and clearer, but users may still want to try with their own content right away.", "Compare time to first build and activation: example-first vs build-first"),
 ("A finished sample project in onboarding", "Clueso doesn't offer one today. It follows NN/g's empty-state advice and Loom's \"get inspired\" fork.", "Usability test: do sample-first users go on to make their own video?"),
 ("Notify people when a build finishes", "Clueso shows only elapsed time today. Notifications are a common pattern for long jobs (Nielsen, \"Slow AI\") but aren't built.", "Engineering scope; measure how many builds are abandoned"),
 ("Group language versions and AI spin-offs under their source project", "Observed as loose projects; grouping is a design inference.", "Usability test task: \"find the Spanish version\""),
]
BEFORE_AFTER = [
 ("Things competing for attention on first view", "7 (sale banner, What's new card, checklist, upgrade card, survey, work-email toast, chat bubble)", "2 (the prompt and one next step)"),
 ("Controls on the prompt", "5 (attach, record, mode, model, brand)", "3 (add, quality, brand), with mode moved to the confirm step"),
 ("AI model choices", "6 vendor models, no costs", "2 quality levels with credit estimates"),
 ("Ways to start shown", "4 chips + prompt, and different sets on 5 other surfaces", "Prompt + 3, the same everywhere (Clueso's own four, minus the Enterprise-only agent recorder)"),
 ("Prompt suggestions", "Generic (\"Facts about Lewis Hamilton\")", "3, from the user's goals"),
 ("Getting-started guidance", "6-item checklist collapsed in the sidebar", "One next step with progress, on the page"),
 ("Onboarding side panel", "Decorative (\"Make something beautiful\")", "A live preview of how your answers change Create, then \"what happens next\""),
 ("Cost shown before building", "None on the Home prompt", "Estimate next to Send and in the confirm step"),
]

def decisions_html():
    F = json.load(open(os.path.join(HERE, "fixes.json")))
    rows = []
    for key, name in SCREENS:
        for t, ids, ev in F.get(key, []):
            kinds = [k for k in ("Clueso", "Observed", "Research") if k in ev]
            tag = "".join(f'<span class="bdgk k-{k.lower()}">{k}</span>' for k in kinds)
            rows.append(f"<tr><td class=\"mono\">{E(name)}</td><td><b>{E(t)}</b></td><td>{tag}<div class=\"evt\">{E(ev)}</div></td><td class=\"mono\">{E(ids)}</td></tr>")
    ba = "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in BEFORE_AFTER)
    pr = "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in PROPOSALS)
    return f"""<section id="decisions" class="block">
  <h2>Redesign decision log</h2>
  <p class="lede">Every change in the redesign prototype, with the evidence behind it. <b>Clueso</b> means Clueso's own website, pricing table, help center or app copy. <b>Observed</b> means seen during this audit, with a screenshot. <b>Research</b> means a cited UX source. Decisions that rest only on inference are listed separately below as proposals to validate.</p>
  <h3>Create page: cognitive load, before and after</h3>
  <div class="tablewrap"><table><thead><tr><th>What</th><th>Clueso today</th><th>Redesign</th></tr></thead><tbody>{ba}</tbody></table></div>
  <h3>All decisions</h3>
  <div class="tablewrap"><table class="wide"><thead><tr><th>Screen</th><th>Decision</th><th>Evidence</th><th>Findings</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
  <h3>Proposals that still need validation</h3>
  <div class="tablewrap"><table><thead><tr><th>Proposal</th><th>Why it isn't proven yet</th><th>How to validate</th></tr></thead><tbody>{pr}</tbody></table></div>
</section>"""

CSS = """
.bdgk { font: 600 0.62rem var(--body); text-transform: uppercase; letter-spacing: .05em; padding: 1px 6px; border-radius: 999px; margin-right: 4px; }
.k-clueso { color: var(--accent); background: var(--accent-soft); } .k-observed { color: var(--major); background: var(--major-soft); } .k-research { color: var(--good); background: var(--good-soft); }
.evt { color: var(--muted); font-size: 0.85rem; margin-top: 4px; }
"""
