"""Before/after design doc: Clueso's screen with the issue highlighted and its basis, then the redesign with its decisions.

Before images are the audit's annotated screenshots (report/img). After images are prototype screenshots in doc/raw,
annotated here with green numbered boxes. Run: python3 doc/build_doc.py
"""
import html
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import build_report as B  # noqa: E402
import nav_sections as N  # noqa: E402
from annotate import annotate  # noqa: E402

E = html.escape

# Findings from the audit, keyed by (image, number) -> (severity, title, observation, basis)
FIND = {}
for sec in B.SECTIONS:
    for img, cap, items in sec[3]:
        for num, sev, title, obs, fix, basis in items:
            FIND[(img, num)] = (sev, title, obs, basis)
NF = {f[2]: f for f in N.NEW_FINDINGS}


def nf(img, num="1"):
    _id, sev, _img, title, obs, fix, basis = NF[img]
    return (sev, title, obs, basis)


# Each pair: stage, title, one-line summary, before image, issues [(num, override or None)],
# after image, after boxes [(x0, y0, x1, y1, label)], decisions [(label, decision, why)]
PAIRS = [
 dict(id="signin", stage="Sign in", title="Sign-in page",
  gist="The form works, but keyboard order and an auto-scrolling wall get in the way of a 10-second task.",
  before="01-login.jpg", issues=["1", "3"],
  after="signin", boxes=[(79, 253, 321, 360, "1"), (405, 5, 795, 556, "2"), (79, 401, 321, 417, "3")],
  decisions=[("1", "Visible labels tied to each input, and Forgot password moved below the field, so Tab goes email → password → Sign in.", "WCAG 1.3.1 (info and relationships) and 2.4.3 (focus order)."),
             ("2", "One static customer quote replaces the moving wall of testimonials and unrelated showcase tiles.", "Cognitive load (Laws of UX): motion beside a form competes for attention while the user is typing."),
             ("3", "A one-line terms and privacy notice under the button.", "Nielsen #10, help and documentation: consent is stated where it happens.")]),

 dict(id="questions", stage="Onboarding", title="Setup questions",
  gist="Clueso asks for a name Google already gave, then role and workspace, across 4 screens before Home.",
  before="09-onb-profile.jpg", issues=["1", "2", "3"],
  after="start1", boxes=[(200, 52, 600, 97, "1"), (203, 104, 598, 262, "2"), (204, 276, 263, 297, "3")],
  decisions=[("1", "One screen, one question, and the reason is written under it: \"so we can show you a relevant example and set up your Home page\".", "NN/g onboarding: skip what you can and explain why you ask. Canva asks one question (Userpilot)."),
             ("2", "Four jobs in Clueso's own terms. The answer changes the next screen and the Home page, so answering visibly pays off.", "Userpilot welcome surveys: ask only what changes the experience. Hick's law: 4 options instead of 13 roles."),
             ("3", "\"Not sure yet\" and Skip are always there. Name, role and workspace are never asked; the name comes from Google.", "Nielsen #3, user control and freedom. NN/g forms: derive data instead of asking for it.")]),

 dict(id="firstvalue", stage="Onboarding", title="The end of onboarding",
  gist="The recommended option ends in an install wall, at the moment motivation is highest.",
  before="15-onb-extension-gate.jpg", issues=["1"], extra=[("14-onb-first-video.jpg", "1"), ("14-onb-first-video.jpg", "3")],
  after="start2", boxes=[(145, 52, 655, 79, "1"), (145, 102, 655, 309, "2"), (145, 317, 655, 386, "3")],
  decisions=[("1", "Show, don't ask: the last onboarding screen shows what Clueso does for the job you picked. Nothing is built, spent, installed or waited for.", "Fogg behavior model (B = MAP): keep ability high while motivation peaks. HAX G1: make clear what the system can do."),
             ("2", "A before-and-after of a rough recording becoming a polished video, plus the written guide, because that pair is Clueso's core promise.", "Clueso homepage: \"Your video is ready. So is your documentation.\""),
             ("3", "How it works in three plain steps, so nothing later is a surprise. Then \"Start creating\" goes to a Home page already set up for that job.", "Google PAIR, mental models: set expectations early. Downhill onboarding: every step should be easier than the last.")]),

 dict(id="create", stage="Home", title="Home",
  gist="Seven things compete for attention on the first view, and the prompt carries controls a new user can't judge.",
  before="18-home-checklist-survey.jpg", issues=["1", "2", "3", "4", "5", "6"],
  after="create", boxes=[(238, 123, 694, 178, "1"), (266, 180, 349, 204, "2"), (349, 180, 432, 204, "3"), (600, 184, 665, 199, "4"), (236, 248, 696, 337, "5"), (237, 355, 695, 407, "6"), (4, 443, 133, 474, "7")],
  decisions=[("1", "A suggestion sits in the empty prompt with a Tab key to accept it, built from the onboarding answer. It uses Clueso's own pattern and animation.", "Recognition over recall (Nielsen #6). Clueso's own RotatingPlaceholder, measured in the live app."),
             ("2", "Clueso's nine models stay, grouped by vendor, and the pill shows the one in use. Every estimate follows the chosen model.", "User control and freedom (Nielsen #3). Clueso's help center: a smaller model costs about half per message."),
             ("3", "Brand stays off until you set one up, so the AI never invents a brand kit from gmail.com.", "Error prevention (Nielsen #5)."),
             ("4", "Credits left, and the estimate once you type, sit next to Send.", "HAX G4 and Shape of AI cost estimates: show the cost before the action."),
             ("5", "Clueso's own start options, each with one line on what it does: record, upload videos or slides, translate.", "Clueso Home's \"Or start directly\". Hick's law for merging its two upload buttons into one."),
             ("6", "One next step with progress, replacing a 6-item checklist hidden under a promo card.", "Goal-gradient effect and endowed progress (Nunes and Drèze, 2006): showing 1 of 4 done raises completion."),
             ("7", "One compact usage line instead of a two-meter card and an upgrade ad. No sale banner, survey or chat bubble. What's new moves into Help, which stays in the top bar where Clueso has it.", "Aesthetic and minimalist design (Nielsen #8). ProductLed: no pricing before value.")]),

 dict(id="build", stage="Home", title="Before the build",
  gist="The default model is the most expensive one, and nothing says what the video will cost.",
  before="46-model-picker.jpg", issues=["1"], extra=[("60-chat-plan.jpg", "1")],
  after="build", boxes=[(387, 251, 761, 279, "1"), (387, 281, 761, 348, "2"), (387, 351, 761, 374, "3")],
  decisions=[("1", "Sending opens the conversation with a plan card: the cost range, credits left, about how long it takes, and that a guide is included.", "Shape of AI: cost estimates. Clueso's own idea picker shows \"about 150 credits\"; a 57-second video used 250."),
             ("2", "Model, how often to check in, and brand sit in the card, using Clueso's own names. The brief is shown exactly as typed; nothing is added to it.", "Progressive disclosure (NN/g). User control and freedom (Nielsen #3)."),
             ("3", "Nothing is built or charged until you press Build video. Change brief takes it back to Home.", "Error prevention (Nielsen #5): a costly action needs an explicit go.")]),

 dict(id="progress", stage="Project", title="While it builds",
  gist="A 9 min 37 s build showed only elapsed time and raw agent logs.",
  before="63-ai-video-building.jpg", issues=["1"],
  after="project", boxes=[(152, 123, 533, 184, "1"), (152, 48, 780, 65, "2"), (540, 123, 780, 311, "3")],
  decisions=[("1", "Scene-by-scene progress with time left and \"you can leave; we'll notify you\".", "Nielsen's \"Slow AI\": show progress, stage and estimate. NN/g response times: waits over 10 s need percent done."),
             ("2", "A breadcrumb shows where this project lives.", "Dan Brown, principle of front doors: people arrive deep and need to know where they are."),
             ("3", "The project page leads with the video, then three things only: its guide, its versions and its analytics.", "Peak-end rule: the finished video is the peak, so it gets the stage. Dan Brown, objects: one home per object.")]),

 dict(id="projects", stage="Projects", title="Projects list",
  gist="Seven filters for two projects push New folder off screen, and copies made from a video float loose.",
  before="65-projects-list.jpg", issues=["1", "2", "3"], extra=[("87-projects-six.jpg", "nf")],
  after="projects", boxes=[(656, 71, 705, 95, "1"), (152, 99, 779, 347, "2")],
  decisions=[("1", "One Filter button replaces seven filters, so New folder always fits.", "Hick's law and progressive disclosure: filters appear when there is something to filter."),
             ("2", "Language versions and AI spin-offs sit under the video they came from, with badges. Columns show only what helps you pick.", "Dan Brown, multiple classification and objects. Cognitive load: show information when it supports a decision.")]),

 dict(id="agent", stage="Clueso AI", title="Agent and Chats",
  gist="On Free, a primary nav item opens a sales page whose only action is Book a demo, while the real assistant sits under Chats.",
  before="20-agent-upsell.jpg", issues=["1", "2"],
  after="agent", boxes=[(5, 80, 132, 100, "1"), (158, 125, 357, 477, "2"), (158, 480, 357, 530, "3"), (368, 437, 779, 535, "4")],
  decisions=[("1", "Agent and Chats become one item, Clueso AI: one name for the one assistant.", "Consistency (Nielsen #4). Clueso shows the same assistant as Agent, Chats, Clueso AI and Director."),
             ("2", "The page lists your conversations, with what needs you first, each with its status and the credits it used.", "List and detail pattern (Gmail, Slack). NN/g: colour signals priority. Clueso chats already show per-message credits."),
             ("3", "What Free includes is stated once, and Enterprise agents are called Automations, listed once.", "Clueso pricing: creating a video from chat and MCP are on Free; agents for auto-recording are Enterprise."),
             ("4", "Reply in place, with the model and the cost per reply shown before you send.", "Shape of AI cost estimates. Observed: 13 credits for one reply.")]),

 dict(id="analytics", stage="Analytics", title="Analytics",
  gist="Analytics is a locked page with no preview of what you'd get.",
  before="25-analytics-locked.jpg", issues=["1", "2"],
  after="analytics", boxes=[(152, 75, 780, 107, "1"), (152, 113, 780, 368, "2"), (5, 146, 132, 167, "3")],
  decisions=[("1", "On Free, a clearly labeled sample of the real dashboard, with one \"See plans\" button.", "Show value before asking for it. Clueso pricing: viewership analytics is Business and Enterprise."),
             ("2", "One workspace-wide dashboard across all videos, built from Clueso's help center description.", "Clueso help center (Analytics): filters, impressions, plays, play rate, top content, locations."),
             ("3", "A lock on the sidebar item, so the paywall is never a surprise.", "Dan Brown, principle of disclosure.")]),

 dict(id="library", stage="Clueprints", title="Clueprints",
  gist="\"Reusable video templates\" collides with the editor's Templates, and the coined name is never explained.",
  before="23-clueprints.jpg", issues=["1", "2"],
  after="library", boxes=[(152, 70, 271, 93, "1"), (222, 48, 503, 65, "2")],
  decisions=[("1", "Clueso's Community and Workspace tabs, search and New Clueprint stay, with nothing locked that Clueso leaves open.", "Consistency with the product (Jakob's law). Clueso: New clueprint is available on Free."),
             ("2", "The subtitle explains the coined name: a Clueprint sets the look, pacing, voice and structure of a whole video.", "NN/g information scent: explain a coined name once, inline, instead of a label that collides with Templates.")]),

 dict(id="integrations", stage="Integrations", title="MCP and connections",
  gist="MCP takes a top-level nav slot while GitHub and Bitbucket hide in Settings.",
  before="22-mcp.jpg", issues=["1", "2"],
  after="integrations", boxes=[(152, 89, 780, 219, "1"), (5, 479, 132, 500, "2")],
  decisions=[("1", "Everything you connect once (Chrome extension, MCP, code connections) is on one page, each saying which plan includes it.", "Gestalt proximity and Dan Brown's objects: set-once tools belong together."),
             ("2", "Integrations moves to the bottom of the sidebar, next to Settings.", "Microsoft settings guidance: rarely changed items go last. Serial position effect: keep the ends for what matters.")]),

 dict(id="plan", stage="Settings", title="Plan, usage and credits",
  gist="Credits are shown with no explanation of what costs them, in a team table built for one person.",
  before="30-ai-credits.jpg", issues=["1", "2"],
  after="plan", boxes=[(318, 107, 743, 165, "1"), (318, 170, 743, 296, "2"), (318, 302, 743, 331, "3")],
  decisions=[("1", "Three meters that match the Free plan exactly: export minutes, article exports, AI credits.", "Consistency (Nielsen #4): Clueso's pricing table says 10 minutes, 10 articles and 1,000 credits."),
             ("2", "What credits go on, using only Clueso's own numbers.", "Help and documentation (Nielsen #10). Observed: 250 credits for a 57-second video, 13 for one question."),
             ("3", "How export minutes count, in one sentence, next to See plans.", "Visibility of system status (Nielsen #1).")]),

 dict(id="share", stage="Share", title="Sharing a video",
  gist="Share opens on Export and says nothing about the 10 free minutes, the watermark or the 1080p cap.",
  before="57-share-export.jpg", issues=["1", "2"],
  after="share", boxes=[(229, 211, 571, 235, "1"), (229, 239, 571, 277, "2"), (229, 281, 571, 322, "3")],
  decisions=[("1", "Share opens on a view-only link, which is what most people want.", "Jakob's law: Share means a link in the tools people already use."),
             ("2", "The cost is stated before you commit: about 1 of your 10 free export minutes, with a watermark on Free.", "Visibility of system status (Nielsen #1). Activation happens at this step, so hesitation here costs the most."),
             ("3", "Higher resolutions show their plan instead of failing later.", "Error prevention (Nielsen #5).")]),

 dict(id="invite", stage="Team", title="Inviting a teammate",
  gist="An email field, a role dropdown and Send, with nothing about seat limits or what roles mean.",
  before="88-invite-modal.jpg", issues=["nf"],
  after="invite", boxes=[(228, 212, 330, 230, "1"), (228, 280, 572, 332, "2"), (372, 340, 482, 365, "3")],
  decisions=[("1", "The subtitle states the limit: Free includes 1 editor, you.", "Visibility of system status (Nielsen #1)."),
             ("2", "Seats and roles per plan in one sentence: Business adds 2 editors and roles; reviewer seats are Enterprise.", "Clueso pricing table. Help users recognize, not guess (Nielsen #6)."),
             ("3", "\"Share a link instead\" meets the real need (feedback) without a seat.", "Jobs to be done: the job is feedback, not membership.")]),

 dict(id="translate", stage="Translate", title="Translating a video",
  gist="\"Customize translation rules\" jumps to Settings and throws away the setup.",
  before="83-translate-rules-jump.jpg", issues=["nf"],
  after="translate", boxes=[(402, 180, 654, 321, "1"), (146, 348, 398, 386, "2"), (146, 225, 398, 344, "3")],
  decisions=[("1", "Translation rules open inside the dialog, beside the setup, and save to Settings for every translation. Nothing is lost.", "User control and freedom (Nielsen #3)."),
             ("2", "One line says how translations count against export minutes.", "Visibility of system status (Nielsen #1)."),
             ("3", "Upload a video or pick one of your projects, as Clueso's Translator allows.", "Consistency with Clueso: its Translator takes either.")]),

 dict(id="search", stage="Search", title="Search results",
  gist="Search pads every query with projects that don't match, and never says \"no results\".",
  before="89-search-padded.jpg", issues=["nf"],
  after="search", boxes=[(167, 145, 633, 316, "1"), (167, 119, 633, 141, "2"), (167, 86, 633, 117, "3"), (167, 393, 633, 415, "4")],
  decisions=[("1", "The same query, \"on\", lists only real matches, ranked, with the match bolded and at most 5 per group.", "NN/g search results: relevance first, highlight the query. Hick's law caps each group."),
             ("2", "Scopes are visible tabs with result counts, so you can see where matches are before you click.", "Visibility of options; recognition over recall (Nielsen #6)."),
             ("3", "Clueso's fixed 680 × 480 frame is kept: the input stays pinned while results scroll.", "Consistency and stability: the panel never resizes while you type."),
             ("4", "Every keyboard hint in the footer works, and Clueso's p; n; a; prefixes still narrow the search.", "Flexibility and efficiency of use (Nielsen #7). WAI-ARIA combobox pattern.")]),

 dict(id="search-empty", stage="Search", title="Search before you type",
  gist="The panel is blank until you type.",
  before="90-search-empty.jpg", issues=[("1", ("major", "The empty panel is blank", "Opening search shows only the input and the footer. Nothing suggests what you can find or do.", "Recognition rather than recall"))],
  after="search-empty", boxes=[(165, 140, 635, 392, "1")],
  decisions=[("1", "Three recent projects and four quick actions fill the panel before you type.", "Recognition over recall (Nielsen #6): most searches are for something you just worked on.")]),

 dict(id="sidebar", stage="Navigation", title="Collapsed sidebar",
  gist="Collapsed, the sidebar is a rail of similar icons with no labels.",
  before="86-sidebar-collapsed.jpg", issues=["nf"],
  after="sidebar", boxes=[(3, 34, 33, 169, "1"), (32, 59, 74, 78, "2")],
  decisions=[("1", "Six distinct icons for six areas: Home, Projects, Clueso AI, Clueprints, Brand kit, Analytics.", "Recognition over recall. Agent and Chats are one item and MCP moved into Integrations, so no two icons mean nearly the same thing."),
             ("2", "Every icon shows its name on hover.", "NN/g vertical navigation: icons need text labels.")]),
]

PRINCIPLES = [
 ("Nielsen's 10 usability heuristics", "Ten rules of thumb for interface design, from Jakob Nielsen (NN/g). Cited here by number: #1 visibility of system status, #2 match with the real world, #3 user control and freedom, #4 consistency, #5 error prevention, #6 recognition rather than recall, #7 flexibility and efficiency, #8 aesthetic and minimalist design, #10 help and documentation."),
 ("Hick's law", "Decision time grows with the number and complexity of choices. Used to cap options at a decision point."),
 ("Fogg behavior model", "Behavior happens when motivation, ability and a prompt meet. New users are most motivated right after sign-up, so that is when the first step must be easiest."),
 ("Goal-gradient effect and endowed progress", "People speed up as they near a goal, and are more likely to finish when given a head start (Nunes and Drèze, 2006)."),
 ("Peak-end rule", "People judge an experience by its most intense moment and its end. The finished video is the peak, so it gets the stage."),
 ("Jakob's law", "Users spend most of their time on other products and expect yours to work the same way."),
 ("Progressive disclosure", "Show what most people need; reveal advanced options on request (NN/g)."),
 ("Cognitive load", "Every element on screen costs attention. Remove what doesn't support the current task."),
 ("Microsoft HAX guidelines", "18 guidelines for human-AI interaction. G1: make clear what the system can do. G2: make clear how well it can do it. G4: show contextually relevant information."),
 ("Shape of AI and Nielsen's \"Slow AI\"", "Patterns for AI products: show cost before an action, and show progress, stage and an estimate during long AI work."),
 ("Google PAIR", "People + AI guidebook. Mental models: set expectations about what the AI does before it does it."),
 ("Dan Brown's 8 principles of information architecture", "Objects, choices, disclosure, exemplars, front doors, multiple classification, focused navigation, growth. Cited where content is grouped or found."),
 ("WCAG 2.2", "Web accessibility guidelines. 1.3.1: structure conveyed in code (labels tied to inputs). 2.4.3: a logical focus order."),
]

SEV = {"critical": "Critical", "major": "Major", "minor": "Minor", "good": "Works well"}


def issue_rows(p):
    rows = []
    for item in p["issues"]:
        if isinstance(item, tuple):
            num, data = item
        elif item == "nf":
            num, data = "1", nf(p["before"])
        else:
            num, data = item, FIND[(p["before"], item)]
        rows.append((num, *data))
    return rows


def extra_rows(p):
    out = []
    for img, num in p.get("extra", []):
        data = nf(img) if num == "nf" else FIND[(img, num)]
        out.append((img, num, *data))
    return out


def build():
    img_dir = os.path.join(HERE, "img")
    os.makedirs(img_dir, exist_ok=True)
    for p in PAIRS:
        shutil.copy(os.path.join(ROOT, "report", "img", p["before"]), os.path.join(img_dir, "before-" + p["before"]))
        boxes = [[x0, y0, x1, y1, lab, "good"] for x0, y0, x1, y1, lab in p["boxes"]]
        annotate(os.path.join(HERE, "raw", p["after"] + ".jpg"), os.path.join(img_dir, "after-" + p["after"] + ".jpg"), boxes)

    toc = []
    secs = []
    last_stage = None
    for i, p in enumerate(PAIRS, 1):
        if p["stage"] != last_stage:
            toc.append(f'<li class="tstage">{E(p["stage"])}</li>')
            last_stage = p["stage"]
        toc.append(f'<li><a href="#{p["id"]}">{E(p["title"])}</a></li>')
        iss = "".join(
            f'<li><span class="chip {sev}">{E(num)}</span><div><b>{E(title)}</b> <span class="sev {sev}">{SEV[sev]}</span><p>{E(obs)}</p><p class="basis"><span>Basis</span>{E(basis)}</p></div></li>'
            for num, sev, title, obs, basis in issue_rows(p))
        ext = extra_rows(p)
        ext_html = ""
        if ext:
            ext_html = '<div class="also"><span>Also seen</span>' + "".join(
                f'<p><b>{E(title)}.</b> {E(obs)} <span class="basis-inline">Basis: {E(basis)}</span></p>' for img, num, sev, title, obs, basis in ext) + "</div>"
        dec = "".join(
            f'<li><span class="chip good">{E(lab)}</span><div><b>{E(d)}</b><p class="basis"><span>Why</span>{E(why)}</p></div></li>'
            for lab, d, why in p["decisions"])
        secs.append(f'''<section class="pair" id="{p["id"]}">
  <header class="phead"><span class="pnum">{i:02d}</span><div><span class="stage">{E(p["stage"])}</span><h2>{E(p["title"])}</h2><p class="gist">{E(p["gist"])}</p></div></header>
  <div class="cols">
    <div class="col before">
      <div class="label"><span class="dot bad"></span>Clueso today</div>
      <a class="shot" href="img/before-{p["before"]}" target="_blank" rel="noopener"><img src="img/before-{p["before"]}" alt="Clueso: {E(p["title"])}, issues highlighted" loading="lazy"></a>
      <ol class="items">{iss}</ol>{ext_html}
    </div>
    <div class="col after">
      <div class="label"><span class="dot ok"></span>Redesign</div>
      <a class="shot" href="img/after-{p["after"]}.jpg" target="_blank" rel="noopener"><img src="img/after-{p["after"]}.jpg" alt="Redesign: {E(p["title"])}, decisions highlighted" loading="lazy"></a>
      <ol class="items">{dec}</ol>
    </div>
  </div>
</section>''')

    pr = "".join(f"<dt>{E(a)}</dt><dd>{E(b)}</dd>" for a, b in PRINCIPLES)
    n_issues = sum(len(p["issues"]) + len(p.get("extra", [])) for p in PAIRS)
    n_dec = sum(len(p["decisions"]) for p in PAIRS)
    page = TEMPLATE.replace("{{TOC}}", "".join(toc)).replace("{{SECTIONS}}", "\n".join(secs)).replace("{{PRINCIPLES}}", pr) \
        .replace("{{NPAIRS}}", str(len(PAIRS))).replace("{{NISSUES}}", str(n_issues)).replace("{{NDEC}}", str(n_dec))
    open(os.path.join(HERE, "index.html"), "w").write(page)
    print("wrote doc/index.html:", len(PAIRS), "pairs,", n_issues, "issues,", n_dec, "decisions")


TEMPLATE = """<title>Clueso Before and After</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&family=Outfit:wght@400;500&display=swap">
<style>
/* Layout: a reading column for the intro, then full-width before/after pairs side by side, stacking below 980px. */
:root {
  --bg: oklch(0.985 0.003 330); --surface: #fff; --ink: oklch(0.22 0.01 330); --muted: oklch(0.46 0.01 330); --line: oklch(0.9 0.006 330);
  --accent: oklch(0.45 0.16 340); --accent-soft: oklch(0.95 0.03 340);
  --critical: oklch(0.52 0.2 27); --critical-soft: oklch(0.95 0.03 27);
  --major: oklch(0.55 0.16 50); --major-soft: oklch(0.95 0.04 60);
  --minor: oklch(0.5 0.1 85); --minor-soft: oklch(0.95 0.05 95);
  --good: oklch(0.48 0.12 150); --good-soft: oklch(0.95 0.04 150);
  --display: "Outfit", "Geist", system-ui, sans-serif; --body: "Geist", system-ui, -apple-system, sans-serif; --mono: "Geist Mono", ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: oklch(0.17 0.006 330); --surface: oklch(0.21 0.008 330); --ink: oklch(0.94 0.005 330); --muted: oklch(0.72 0.01 330); --line: oklch(0.32 0.01 330);
  --accent: oklch(0.78 0.12 340); --accent-soft: oklch(0.3 0.06 340);
  --critical: oklch(0.74 0.15 27); --critical-soft: oklch(0.3 0.06 27); --major: oklch(0.78 0.13 60); --major-soft: oklch(0.3 0.05 60);
  --minor: oklch(0.82 0.11 95); --minor-soft: oklch(0.3 0.04 95); --good: oklch(0.78 0.12 150); --good-soft: oklch(0.28 0.05 150); color-scheme: dark; } }
:root[data-theme="dark"] {
  --bg: oklch(0.17 0.006 330); --surface: oklch(0.21 0.008 330); --ink: oklch(0.94 0.005 330); --muted: oklch(0.72 0.01 330); --line: oklch(0.32 0.01 330);
  --accent: oklch(0.78 0.12 340); --accent-soft: oklch(0.3 0.06 340);
  --critical: oklch(0.74 0.15 27); --critical-soft: oklch(0.3 0.06 27); --major: oklch(0.78 0.13 60); --major-soft: oklch(0.3 0.05 60);
  --minor: oklch(0.82 0.11 95); --minor-soft: oklch(0.3 0.04 95); --good: oklch(0.78 0.12 150); --good-soft: oklch(0.28 0.05 150); color-scheme: dark; }
* { box-sizing: border-box; }
body { background: var(--bg); color: var(--ink); font: 15px/1.55 var(--body); margin: 0; }
.wrap { max-width: 1320px; margin: 0 auto; padding-inline: 24px; padding-block: 48px 80px; }
.intro { max-width: 720px; display: grid; gap: 16px; }
.eyebrow { font: 500 12px var(--mono); letter-spacing: .06em; text-transform: uppercase; color: var(--accent); }
h1 { font: 400 clamp(32px, 5vw, 48px)/1.1 var(--display); margin: 0; text-wrap: balance; letter-spacing: -0.01em; }
.lede { font-size: 17px; color: var(--muted); margin: 0; }
.facts { display: flex; flex-wrap: wrap; gap: 8px 24px; font: 13px var(--mono); color: var(--muted); margin: 0; padding: 0; list-style: none; }
.facts b { color: var(--ink); font-weight: 500; }
.legend { display: flex; flex-wrap: wrap; gap: 8px 16px; font-size: 13px; color: var(--muted); align-items: center; }
.legend span { display: inline-flex; gap: 6px; align-items: center; }
.howto { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 16px 18px; display: grid; gap: 10px; font-size: 14px; }
.howto p { margin: 0; }
nav.toc { margin-top: 32px; border-top: 1px solid var(--line); padding-top: 20px; }
nav.toc ol { list-style: none; padding: 0; margin: 0; columns: 3 220px; column-gap: 24px; font-size: 14px; }
nav.toc li { break-inside: avoid; padding: 2px 0; }
nav.toc .tstage { font: 500 11px var(--mono); text-transform: uppercase; letter-spacing: .06em; color: var(--muted); padding-top: 10px; }
nav.toc .tstage:first-child { padding-top: 0; }
a { color: var(--accent); text-underline-offset: 2px; }
a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 4px; }
.pair { margin-top: 64px; padding-top: 32px; border-top: 1px solid var(--line); scroll-margin-top: 16px; }
.phead { display: flex; gap: 16px; align-items: flex-start; max-width: 900px; }
.pnum { font: 500 13px var(--mono); color: var(--muted); padding-top: 6px; font-variant-numeric: tabular-nums; }
.stage { font: 500 11px var(--mono); text-transform: uppercase; letter-spacing: .06em; color: var(--accent); }
h2 { font: 400 26px/1.2 var(--display); margin: 2px 0 6px; text-wrap: balance; }
.gist { margin: 0; color: var(--muted); max-width: 68ch; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; margin-top: 24px; }
.col { min-width: 0; display: grid; gap: 14px; align-content: start; }
.label { font: 500 12px var(--mono); text-transform: uppercase; letter-spacing: .06em; display: flex; gap: 8px; align-items: center; }
.dot { width: 8px; height: 8px; border-radius: 50%; } .dot.bad { background: var(--major); } .dot.ok { background: var(--good); }
.shot { display: block; border-radius: 8px; overflow: hidden; border: 1px solid var(--line); background: var(--surface); }
.shot img { display: block; width: 100%; height: auto; }
.shot:hover { border-color: var(--muted); }
.items { list-style: none; margin: 0; padding: 0; display: grid; gap: 12px; }
.items li { display: grid; grid-template-columns: 22px 1fr; gap: 10px; align-items: start; }
.items b { font-weight: 500; }
.items p { margin: 3px 0 0; font-size: 14px; color: var(--muted); }
.chip { width: 22px; height: 22px; border-radius: 50%; display: grid; place-items: center; font: 600 11px var(--body); color: #fff; margin-top: 1px; font-variant-numeric: tabular-nums; }
.chip.critical { background: oklch(0.55 0.21 27); } .chip.major { background: oklch(0.6 0.17 50); } .chip.minor { background: oklch(0.6 0.12 85); } .chip.good { background: oklch(0.52 0.13 150); }
.sev { font: 500 10px var(--mono); text-transform: uppercase; letter-spacing: .05em; padding: 1px 6px; border-radius: 999px; margin-left: 4px; white-space: nowrap; }
.sev.critical { color: var(--critical); background: var(--critical-soft); } .sev.major { color: var(--major); background: var(--major-soft); } .sev.minor { color: var(--minor); background: var(--minor-soft); } .sev.good { color: var(--good); background: var(--good-soft); }
.basis { color: var(--ink) !important; }
.basis span { font: 500 10px var(--mono); text-transform: uppercase; letter-spacing: .06em; color: var(--muted); margin-right: 8px; }
.also { border-left: 2px solid var(--line); padding-left: 12px; font-size: 14px; color: var(--muted); display: grid; gap: 6px; }
.also > span { font: 500 10px var(--mono); text-transform: uppercase; letter-spacing: .06em; }
.also p { margin: 0; } .also b { color: var(--ink); font-weight: 500; }
.basis-inline { color: var(--ink); }
.principles { margin-top: 72px; padding-top: 32px; border-top: 1px solid var(--line); max-width: 860px; }
.principles dl { display: grid; grid-template-columns: minmax(180px, 260px) 1fr; gap: 12px 24px; margin: 20px 0 0; }
.principles dt { font-weight: 500; } .principles dd { margin: 0; color: var(--muted); font-size: 14px; }
.foot { margin-top: 48px; font-size: 13px; color: var(--muted); max-width: 760px; }
@media (max-width: 980px) { .cols { grid-template-columns: 1fr; gap: 28px; } }
@media (max-width: 640px) { .wrap { padding-inline: 16px; padding-block: 32px 56px; } .principles dl { grid-template-columns: 1fr; gap: 4px; } .principles dd { margin-bottom: 10px; } .phead { gap: 10px; } h2 { font-size: 22px; } }
</style>
<div class="wrap">
  <header class="intro">
    <span class="eyebrow">UX audit · web.clueso.io · October 2026</span>
    <h1>Clueso, before and after</h1>
    <p class="lede">Each section puts a screen from Clueso's live app next to the redesign prototype. On the left, what's wrong, highlighted, and the principle it breaks. On the right, what changed and why.</p>
    <ul class="facts"><li><b>{{NPAIRS}}</b> screens</li><li><b>{{NISSUES}}</b> issues</li><li><b>{{NDEC}}</b> design decisions</li><li>Free plan, observed 15–17 Oct 2026</li></ul>
    <div class="howto">
      <p><b>How to read it.</b> Numbers on a screenshot match the numbered notes under it. Click any screenshot to open it full size.</p>
      <div class="legend"><span><span class="chip critical">1</span>Critical</span><span><span class="chip major">1</span>Major</span><span><span class="chip minor">1</span>Minor</span><span><span class="chip good">1</span>Redesign decision</span></div>
      <p><b>Basis</b> names the principle, law or research behind an issue. <b>Why</b> names what a decision rests on: Clueso's own pricing, help center or app (\"Clueso\"), something observed during the audit, or cited research. Nothing is assumed.</p>
    </div>
  </header>
  <nav class="toc" aria-label="Screens"><ol>{{TOC}}</ol></nav>
  {{SECTIONS}}
  <section class="principles" id="principles">
    <span class="eyebrow">Reference</span>
    <h2>Principles and laws cited</h2>
    <p class="gist">What each \"Basis\" and \"Why\" line refers to.</p>
    <dl>{{PRINCIPLES}}</dl>
  </section>
  <p class="foot">The redesign is a prototype that reuses Clueso's icons, typeface substitute and measured design tokens so the comparison is like for like. It is a concept for discussion, not Clueso's product. Pink in the prototype is deepened from Clueso's so white text passes WCAG AA contrast.</p>
</div>
"""

if __name__ == "__main__":
    build()
