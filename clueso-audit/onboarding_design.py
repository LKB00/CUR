"""Onboarding from first principles, the information policy, and per-screen information budgets."""
import html
E = html.escape

MINDSET = [
 ("Just signed up", "High motivation, low patience", "\"Can this make the video I need?\"", "Is it hard? Do I have to install something? Will it cost me?"),
 ("First question", "Willing to answer one or two things", "\"Why are you asking me this?\"", "Is this a sales survey?"),
 ("Seeing the example", "Curious", "\"So that's what it does. Will mine look like that?\"", "Will it work with my product?"),
 ("Waiting for the build", "Motivation decays with each minute", "\"How long? Can I leave?\"", "Is it stuck? Am I spending credits for nothing?"),
 ("First video ready", "Peak moment", "\"Is this good enough to share?\"", "Will sharing cost me, or show a watermark?"),
 ("Next day", "Low; needs a reason to come back", "\"What do I do now?\"", "Forgot where things are"),
]

FUNNEL = [
 ("Sign up", "Google or form; then \"Complete your profile\" asks for a name Google already gave", "Asking twice feels broken; extra fields cost conversion", "Name from Google; no profile screen", "signup_completed", "NN/g forms: derive data instead of asking; 78% vs 42% error-free first tries with good forms"),
 ("First screen", "About 20 s of blank screen and logo", "Users assume it's broken (Doherty threshold); 40–60% of sign-ups never return after the first experience (ProductLed)", "Skeleton screen with the first question immediately", "first_screen_rendered (ms)", "Laws of UX, Doherty threshold; ProductLed"),
 ("Questions", "4 screens: goals, name + role, workspace, first-video method", "Each screen is a chance to quit; none of the answers visibly changes anything", "1 question with its reason on screen; the answer changes the next screen and Create", "job_selected", "NN/g onboarding: skip it where you can; Canva asks 1 question (Userpilot)"),
 ("Understanding", "No explanation of what Clueso does; the recommended option needs an extension install", "Users don't yet know what they'll get, and leaving to install loses them", "A before-and-after example (video and guide) and how it works in 3 lines; then Create, where the prompt needs no install", "example_viewed, first_action_started", "Fogg B=MAP: ability must be high when motivation peaks"),
 ("Approval", "Agent asks questions in chat (13 credits each); no cost shown", "Surprise costs erode trust; chat back-and-forth is slow", "Storyline to approve with cost and time beside the button", "storyline_approved", "Shape of AI: cost estimates; Smashing: intent preview"),
 ("Build wait", "\"Working for 9 min 37 s\" with no estimate", "Long, opaque waits get abandoned", "On the project page: scene progress, time left, and \"leave and we'll notify you\"", "build_started, build_completed, tab_closed_during_build", "NN/g response times; Nielsen \"Slow AI\"; Hook model investment"),
 ("Aha", "Lands in a dense editor with failure logs", "The peak is buried, and the end of the session is unclear", "A project page that leads with the video, its guide and Share; no failure logs", "first_video_played", "Peak-end rule"),
 ("Activation", "Share dialog hides minute cost and watermark", "Hesitation at the final step", "Share a link with its cost stated up front", "first_link_shared (activation)", "Lenny's Newsletter: activation = earliest milestone that predicts retention"),
 ("Return", "Checklist hidden in the sidebar; nothing pulls users back", "No reason to return", "Email when the build is done; one \"next step\" on Create; an unfinished storyline is kept", "day7_return", "Zeigarnik effect; Appcues checklists: 3 to 5 items"),
 ("Upgrade", "Sale banner and upgrade card before any value", "Pricing before value is the most criticised onboarding pattern in the competitor benchmark", "Upgrade appears only at real limits: minutes running low, a locked feature clicked, the Analytics sample", "upgrade_viewed_from_limit", "Competitor benchmark; Guidde and Loom upsell after the first creation"),
]

DISTRACTIONS = [
 ("Series A sale banner", "Every page, first load", "Remove before activation; show plan offers at limits instead"),
 ("Work-email toast", "Every onboarding step", "Remove; mention the benefit once, in the brand step"),
 ("Auto-scrolling testimonial wall", "Sign-in and sign-up", "Replace with one static quote"),
 ("How did you hear about us? survey", "Seconds after the first Home view", "Move to after the first share, or to email"),
 ("What's new card", "Sidebar, day one", "Move into the Help menu"),
 ("Upgrade card", "Sidebar, day one", "Replace with a one-line usage meter"),
 ("Floating chat bubble", "Every page", "Keep inside Help; don't overlay content"),
 ("\"We've simplified the editor\" modal", "First editor open", "Don't show to new users"),
 ("Raw agent log (\"2 failed\", \"plan.md\")", "During the first build", "Show scene progress; hide recovered retries"),
]

RULES = [
 ("One primary action per screen", "Everything else on the screen supports it or waits.", "Fogg (a clear prompt); NN/g visual hierarchy"),
 ("No more than 4 choices at a decision", "More options go behind \"More\".", "Hick's law; NN/g progressive disclosure (at most 2 levels)"),
 ("Ask only what changes the next screen", "And show the change, live if possible.", "Userpilot welcome surveys; NN/g onboarding"),
 ("Show cost and limits at the point of action, and only there", "Not as a permanent banner.", "HAX G4; Shape of AI cost estimates"),
 ("Show status only when it changes a decision", "Progress during waits; no permanent log noise.", "Google PAIR: show confidence only when it changes a decision"),
 ("Defer setup until it's needed", "Brand, team, integrations and settings appear in context.", "NN/g: contextual help beats front-loaded tutorials"),
 ("No promotions before value", "Upgrades appear at limits, after the first success.", "ProductLed; competitor benchmark"),
 ("Name things by what users recognize", "Explain a coined name (Clueprints) once, inline.", "NN/g information scent"),
 ("Empty states teach and offer one next step", "Never a blank canvas or a blank list.", "NN/g empty states"),
 ("Show a locked feature once, with its plan", "Not as repeated nags.", "Dan Brown: disclosure"),
]

BUDGET = [
 ("Onboarding: one question", "Say what you'll make", "4 jobs, the reason for asking", "—", "Profile, role, workspace, survey, decorative panel, toasts", "4 screens and 9+ inputs → 1 screen, 4 options"),
 ("Onboarding: what Clueso does", "Understand the product", "Before-and-after for your answer, video plus guide, how it works in 3 lines", "Other examples (if several jobs picked)", "Building, spending, waiting, settings", "—"),
 ("Create", "Start a video", "Prompt, quality, brand, cost; 3 suggestions; 3 other ways; 1 next step; 3 recent", "Mode, model, attachments", "Banner, survey, footer links, 6-item checklist", "Prompt controls 5 → 3; ways to start 8 → 4"),
 ("Projects", "Find and open work", "Name, type, guide, versions count, length, edited", "Filters, folders", "Owner column (solo), versions column", "Columns 5 → 3"),
 ("Project page", "See and share one video", "Video, Share, guide status, versions, analytics link", "Editor", "Separate boxes for chats, performance and spin-offs", "Boxes 6 → 3"),
 ("Agent", "Give the agent a task; review tasks", "Prompt, one line of Free abilities, tasks with status and credits", "Enterprise abilities (menu)", "Three locked capability cards", "Cards 5 → 1 line"),
 ("Analytics", "See how videos perform", "Totals, trend, top content, locations", "One video's retention (filter)", "—", "—"),
 ("Sidebar", "Move between areas", "5 areas, compact usage line, Integrations, Settings, Help", "Library sub-items (on the Library page)", "Upgrade card, What's new card, checklist", "Items and widgets 13 → 9"),
]


def onboarding_html():
    mind = "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td></tr>" for a, b, c, d in MINDSET)
    fun = "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td><td class=\"mono\">{E(e)}</td><td class=\"evt\">{E(f)}</td></tr>" for a, b, c, d, e, f in FUNNEL)
    dis = "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in DISTRACTIONS)
    rules = "".join(f"<li><b>{E(a)}.</b> {E(b)} <span class=\"evt\">{E(c)}</span></li>" for a, b, c in RULES)
    bud = "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td><td>{E(e)}</td><td class=\"mono\">{E(f)}</td></tr>" for a, b, c, d, e, f in BUDGET)
    return f"""<section id="onboard-first" class="block">
  <h2>Onboarding from the user's side</h2>
  <p class="lede">This doesn't copy Clueso's steps. It starts from what a new user wants and worries about, then removes everything that stands between them and a first video they can share. The prototype's "Get started" flow implements it in two light screens: one question with a visible reason, then a before-and-after of what Clueso does for that answer, then a personalized Create page. Onboarding should feel downhill, so nothing is built, spent or waited for during it; the first build happens in the product, when the user chooses.</p>
  <h3>What's on the new user's mind</h3>
  <div class="tablewrap"><table><thead><tr><th>Moment</th><th>Mood</th><th>Question in their head</th><th>Worry</th></tr></thead><tbody>{mind}</tbody></table></div>
  <h3>Funnel: where people drop off, and what fixes it</h3>
  <p class="lede">Each stage lists what Clueso does today (observed), the drop-off risk, the redesign, and the event to instrument so the drop-off can be measured. Activation is the first shared link: the earliest milestone that shows value was received.</p>
  <div class="tablewrap"><table class="wide"><thead><tr><th>Stage</th><th>Clueso today</th><th>Drop-off risk</th><th>Redesign</th><th>Measure</th><th>Basis</th></tr></thead><tbody>{fun}</tbody></table></div>
  <h3>Distractions in the first session</h3>
  <div class="tablewrap"><table><thead><tr><th>Element</th><th>When it appears</th><th>Verdict</th></tr></thead><tbody>{dis}</tbody></table></div>
  <h3>Information policy, applied to every screen</h3>
  <ol class="plain">{rules}</ol>
  <h3>Information budget per screen</h3>
  <p class="lede">For each screen: its one job, what it shows, what waits until asked for, and what's removed. The last column counts choices or elements, Clueso today against the redesign.</p>
  <div class="tablewrap"><table class="wide"><thead><tr><th>Screen</th><th>Job</th><th>Show</th><th>On demand</th><th>Removed</th><th>Load</th></tr></thead><tbody>{bud}</tbody></table></div>
</section>"""
