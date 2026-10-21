"""Framework scorecards, competitor benchmark, onboarding rubric, journey map and sources for the Clueso audit."""
import html

E = html.escape

# status: meets | partial | fails | nt (not tested)
SCORECARDS = [
 ("hax", "Microsoft Guidelines for Human-AI Interaction",
  "18 guidelines from Amershi et al., CHI 2019, grouped by when they apply. This is the most widely used checklist for AI product UX.",
  "https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/Guidelines-for-Human-AI-Interaction-camera-ready.pdf", [
  ("G1", "Initially", "Make clear what the system can do", "partial", "Home asks \"What are we creating today?\" and the AI panel offers Create a video, an animation or a Clueprint. The suggestions are generic, though, and nothing states limits such as length, languages or styles.", "B19"),
  ("G2", "Initially", "Make clear how well the system can do it", "fails", "There are no quality caveats, and the model picker shows vendor names with no quality or speed labels.", "C10"),
  ("G3", "During", "Time services based on context", "partial", "The plan approval comes at a natural break, which is good. The survey pop-up and the work-email toast interrupt mid-task.", "C3, B4"),
  ("G4", "During", "Show contextually relevant information", "fails", "No credit cost is shown at the point of action, and the AI offers \"Polish this video\" for an empty project.", "B20, E5, F5"),
  ("G5", "During", "Match relevant social norms", "partial", "The tone is professional, but raw voice tags like [curious] and [excited] show up in user-facing scripts.", ""),
  ("G6", "During", "Mitigate social biases", "nt", "Voices and avatars weren't sampled across prompts.", ""),
  ("G7", "When wrong", "Support efficient invocation", "partial", "AI is reachable from Home, the header, the editor and ⌘K (Tab). It is split over six surfaces, though.", "D3"),
  ("G8", "When wrong", "Support efficient dismissal", "fails", "The brand kit is applied by default and written into the prompt as text. It can only be removed with a small chip after it has already shaped the request.", "C2, G1"),
  ("G9", "When wrong", "Support efficient correction", "partial", "Scripts are editable per clip, speech can be regenerated per clip, and Version History exists, but it sits below Delete.", "F17"),
  ("G10", "When wrong", "Scope services when in doubt", "meets", "Ask mode proposed a plan, flagged \"Taskly\" as a stand-in name, and offered Looks good, Try another option, or Something else.", ""),
  ("G11", "When wrong", "Make clear why the system did what it did", "partial", "The plan explains the scene structure. The run log shows \"2 failed\" with no explanation.", "G2"),
  ("G12", "Over time", "Remember recent interactions", "nt", "Follow-up edits weren't tested in the same chat.", ""),
  ("G13", "Over time", "Learn from user behavior", "nt", "This needs repeated use.", ""),
  ("G14", "Over time", "Update and adapt cautiously", "nt", "This needs repeated use.", ""),
  ("G15", "Over time", "Encourage granular feedback", "partial", "Thumbs up and down appear on each AI message, but not per scene.", ""),
  ("G16", "Over time", "Convey the consequences of user actions", "fails", "Switching model or mode shows no effect on cost, time or quality.", "C10"),
  ("G17", "Over time", "Provide global controls", "partial", "Video defaults has AI toggles (auto-rewrite, auto-speech, auto-elements), but there is no default model or autonomy setting.", "E11"),
  ("G18", "Over time", "Notify users about changes", "meets", "A \"New in Clueso\" card and the What's new feed announce features.", ""),
 ]),
 ("agentic", "Agentic UX patterns",
  "Patterns for agents that act on the user's behalf over long runs, from Smashing Magazine (Yocco, 2026), The Shape of AI (Campbell) and Jakob Nielsen's \"Slow AI\" (2025).",
  "https://www.uxtigers.com/post/slow-ai", [
  ("A1", "Smashing", "Intent preview, or plan summary, before acting", "meets", "A six-scene plan with timings and voiceover lines appears for approval before anything is built.", ""),
  ("A2", "Smashing", "Autonomy dial", "meets", "Ask, Plan and Auto modes each have a one-line description. Internally they're labeled \"Director autonomy mode\".", "D6"),
  ("A3", "Shape of AI", "Cost estimate before running", "partial", "The Home prompt shows nothing before the run (the video then cost 250 credits). The PDF ideas picker does show \"about 150 credits\" per video, and chats show each message's cost afterwards.", "B20, E5, N9"),
  ("A4", "Slow AI", "Run contract: time window, cost cap and definition of done", "fails", "No duration, cost cap or finish condition was shown before approving.", ""),
  ("A5", "Slow AI", "Three-layer progress (overall, current step, ETA)", "fails", "Only \"Working for 4m 54s\" and \"Thinking for 8m 14s\". There's no scene count or ETA.", "G5"),
  ("A6", "Slow AI", "Progressive partial results", "meets", "Scenes appeared in the editor as they were built.", "G6"),
  ("A7", "Smashing", "Action audit and undo", "partial", "A step log and Version History exist. The log shows internal file names and failed retries.", "G2, G3"),
  ("A8", "Smashing", "Escalation pathway: ask rather than guess", "meets", "\"How would you like to proceed?\" with three options.", ""),
  ("A9", "Slow AI", "Stop-and-keep salvage points", "partial", "A stop button is present. Whether partial work is kept wasn't tested.", ""),
  ("A10", "Slow AI", "Resumption summary and completion notification", "nt", "I didn't leave and come back during a run.", ""),
  ("A11", "Shape of AI", "Draft mode to explore cheaply", "fails", "There is no low-cost preview before a full build, and the default model is the most expensive.", "C10"),
 ]),
 ("psych", "User psychology principles",
  "How Clueso's first session uses or works against well-known behavioral principles. Sources: BJ Fogg, Laws of UX, Nunes and Drèze (2006), Norton et al. (2012), Kahneman, NN/g.",
  "https://lawsofux.com/", [
  ("P1", "Fogg B=MAP", "Ask when motivation is high and keep ability high", "fails", "Motivation peaks at the end of onboarding, which is exactly when the recommended path makes the user install an extension.", "B13, B17"),
  ("P2", "Hick's law", "Fewer choices mean faster decisions", "fails", "There are 6 start options, 6 AI models, 13 roles and 7 project filters.", "B15, C10, B8, H7"),
  ("P3", "Jakob's law", "Work the way familiar tools do", "meets", "The left sidebar, the ⌘K search and the stepper all follow conventions.", ""),
  ("P4", "Cognitive load", "Remove effort that doesn't help the user", "fails", "Seven competing attention elements on the first Home view, and decorative panels on onboarding.", "C6, B5"),
  ("P5", "Goal-gradient", "Visible progress speeds completion", "partial", "There is a progress bar, but the \"Step 1 of 4\" text is for screen readers only.", "B6"),
  ("P6", "Endowed progress", "A head start raises completion", "fails", "The checklist starts at 0 of 6. \"Account created\" could be pre-ticked.", "C4"),
  ("P7", "Zeigarnik effect", "Unfinished tasks pull people back", "partial", "The checklist exists but sits collapsed at the bottom of the sidebar.", "C4"),
  ("P8", "IKEA effect", "People value what they help build, if they finish it", "partial", "The user shapes the plan and can edit scripts, but the build ran over 8 minutes and was still unfinished.", "G5"),
  ("P9", "Foot-in-the-door", "Small first commitment, larger asks later", "meets", "Step 1 is a one-tap goal choice.", ""),
  ("P10", "Peak-end rule", "Experiences are judged by the peak and the end", "fails", "The peak (polished AI visuals) came after a 5-minute wait, and the session ended on an open-ended \"Thinking...\" status.", "G5"),
  ("P11", "Default effect", "Most people keep defaults, so defaults must be safe", "fails", "Risky defaults: brand kit on, the most expensive model, the Classic editor, and Show article on for an empty article.", "C2, C10, F2, H5"),
  ("P12", "Doherty threshold", "Respond within 400 ms", "fails", "A 20-second first load, a role list empty for about 2 seconds, and a preview stuck for over 60 seconds.", "B3, B10, F8"),
  ("P13", "Labor illusion", "Showing the work raises perceived value", "partial", "The step log shows work happening, but leads with failures and internal files.", "G2, G3"),
  ("P14", "Progressive disclosure", "Core options first, advanced later", "fails", "MCP and Agent are top-level, Settings shows team tables to a solo user, and broadcast color jargon is a default setting.", "D10, E7, E11"),
  ("P15", "Social proof", "Show what others choose at decision points", "partial", "Testimonials sit on the login page, but none appear at decisions such as which start option is most popular.", "A3"),
  ("P16", "Aesthetic-usability effect", "Attractive output buys tolerance", "meets", "The visuals are strong. That tolerance can hide the friction above in usability tests.", "G6"),
 ]),
 ("ia-score", "Information architecture principles",
  "Dan Brown's eight principles (2010), the four systems from Rosenfeld and Morville, and NN/g's research on information scent and navigation.",
  "https://www.nngroup.com/articles/information-scent/", [
  ("I1", "Brown: Objects", "Each object has one clear home and lifecycle", "partial", "A project is called \"guide\" in URLs, and chats are a separate object from the project they create.", "D3"),
  ("I2", "Brown: Choices", "Offer only the choices that serve the task", "fails", "Each entry point offers a different set of creation options.", "D13"),
  ("I3", "Brown: Disclosure", "Show enough to predict what's inside", "fails", "\"Agent\" opens a sales page and \"Analytics\" opens a paywall, with no hint beforehand.", "D1, D7"),
  ("I4", "Brown: Exemplars", "Show examples of a category's contents", "meets", "Clueprints and the onboarding gallery use thumbnails.", ""),
  ("I5", "Brown: Front doors", "Every page tells you where you are", "partial", "Deep links work, but the browser tab title stays \"Clueso Platform\" or shows a stale project name.", "C12"),
  ("I6", "Brown: Multiple classification", "Several ways to find things", "meets", "Folders, filters, sorting and ⌘K search.", ""),
  ("I7", "Brown: Focused navigation", "Don't mix kinds of things in one menu", "fails", "One flat list mixes objects (Projects), AI modes (Agent, Chats), integrations (MCP), assets (Brand kit) and admin (Settings).", "D2, D10"),
  ("I8", "Brown: Growth", "The structure must absorb new features", "fails", "There are already 9 nav items plus 4 widgets; every new AI feature has become a new top-level item.", ""),
  ("I9", "R&M: Organization system", "One clear organization scheme per level", "fails", "A hybrid of task, object, brand metaphor (Clueprints) and technology (MCP). Rosenfeld and Morville warn that mixing schemes almost guarantees confusion.", ""),
  ("I10", "R&M: Labeling system", "Consistent, user-language labels", "fails", "One page has four names, and there are three labels each for upload and record.", "D16, D13"),
  ("I11", "R&M: Navigation system", "Global, local and contextual navigation work together", "partial", "The active state is clear, but settings are split across three places.", "D14"),
  ("I12", "R&M: Search system", "Search reaches content, features and settings", "partial", "⌘K finds settings and projects but not actions, and it doesn't filter non-matching results.", "D17"),
  ("I13", "NN/g: Information scent", "Labels predict their destination", "fails", "\"Clueprints\", \"MCP\" and \"Agent\" don't tell a new user what's behind them.", "D11"),
  ("I14", "Microsoft: Settings guidance", "Settings holds rarely changed options and is pinned last", "partial", "Settings is near the bottom, but configuration such as Brand kit and MCP sits in the main nav.", ""),
 ]),
 ("onb-score", "Onboarding best practices",
  "From NN/g (onboarding, empty states, forms), ProductLed's Bowling Alley framework, the Appcues checklist guide and Userpilot's welcome-survey research.",
  "https://www.nngroup.com/articles/mobile-app-onboarding/", [
  ("O1", "NN/g, ProductLed", "3 or fewer questions before the first action", "fails", "Goals, name, role and workspace name, plus a separate profile screen: 5 screens.", "B1, B7, B12"),
  ("O2", "Userpilot", "Every answer visibly changes what comes next", "partial", "Goals moved the \"Recommended\" tag, but prompt suggestions and the brand kit ignored them.", "B19, C7"),
  ("O3", "NN/g", "Explain why each question is asked", "partial", "There's one generic line: \"The more we know, the more Clueso feels made for you.\"", ""),
  ("O4", "NN/g", "Questions are skippable", "partial", "\"I'm just exploring\" works at step 1, but role is required at step 2.", "B9"),
  ("O5", "NN/g forms", "Derive data instead of asking for it", "fails", "The name is asked for even though Google already supplied it.", "B1"),
  ("O6", "ProductLed", "End onboarding on doing, not a dashboard", "fails", "The recommended last step ends in an extension install.", "B17"),
  ("O7", "NN/g empty states", "Empty states teach and offer a next step", "fails", "A blank canvas, a blank article, and Projects leading with New folder.", "F4, F14, C11"),
  ("O8", "Appcues", "Checklist has 3 to 5 items and completes on real events", "fails", "6 items; \"Make your first video\" was ticked by a blank project.", "C4"),
  ("O9", "ProductLed", "No pricing or promotions before value", "fails", "A sale banner and an upgrade card on day one.", "C6"),
  ("O10", "NN/g latency", "Waits over 10 s get percent-done and a way to cancel", "fails", "The 20-second app load and the 8-minute build show no percentage; speech generation has a cancel option.", "B3, G5"),
  ("O11", "Userpilot", "\"How did you hear about us\" stays out of onboarding", "fails", "It pops up on the first Home view.", "C3"),
 ]),
]

COMPETITORS = [
 ("Clueso", "No", "Goals, name, role, workspace, plus a profile screen (5)", "Extension for the recommended path", "Prompt on Home, a hidden checklist", "Minutes in the sidebar; credits only in Billing"),
 ("Loom", "Free plan; card unverified", "Use case, role, workspace, invite, recorder (3 to 4); \"record now\" lets users skip", "Extension or desktop app, with a skip option", "4-item checklist and role videos", "Video counter next to search"),
 ("Descript", "No", "Role, use case, content type, invite (4)", "None (web)", "\"Generate video\" call to action, no tour", "Credits on the dashboard before any output"),
 ("Synthesia", "No", "Department, video type, audience, invite (about 8 screens to value)", "None", "Video type becomes a pre-filled prompt", "Pricing screen before the product"),
 ("HeyGen", "No", "Plan, personalize, avatar, voice (4); \"just exploring\" skip", "None (webcam)", "Setup strip; first video locked behind face recording", "Crown icons, upgrade walls"),
 ("Guidde", "No", "Unverified; create or join a workspace", "Extension; sign-up starts from it", "Capture from the extension", "25 editable videos after the trial"),
 ("Scribe", "Unverified", "Unverified", "Extension", "Record, then an auto-generated guide", "Gates on export, not on creating"),
 ("VEED", "No", "Use case, role, how-heard, email preferences", "None", "Two actions: Generate, Upload", "Pricing before the dashboard"),
]

PATTERNS = [
 ("Pick a type, get a pre-filled prompt", "Synthesia, Descript and VEED turn the use-case answer into the first prompt.", "Clueso asks for goals but then shows generic chips (\"Facts about Lewis Hamilton\")."),
 ("Capture tools gate first value on an extension", "Guidde, Scribe, Tango and Loom all need one. Only Loom offers a skip, and Guidde and Scribe start sign-up from the extension.", "Clueso is browser-first, so it can beat these tools by not requiring the extension for a first video."),
 ("Visible progress during generation", "Synthesia and VEED show a percentage; reviewers criticise its absence elsewhere.", "Clueso shows elapsed time only."),
 ("Pricing before value is the most criticised pattern", "Synthesia, VEED and Descript are faulted for it; Loom and Guidde upsell after the first creation.", "Clueso shows a sale banner and an upgrade card on the first Home view."),
 ("Free limits shown as simple counters", "Loom counts videos and Tango counts workflows. Soft walls (draft but can't publish) are rated better than hard ones.", "Clueso splits limits into minutes, articles and credits, and shows the credits only in Billing."),
 ("Conflicting public limits erode trust", "Guidde and Tango publish different caps in different places.", "Clueso does the same: 10 vs 15 articles, 1 vs 4 seats, 40+, 80+ and 150+ languages."),
 ("Light checklists, tours after activation", "Loom has 4 items and HeyGen 4 steps; Synthesia's tour comes after the first video.", "Clueso has 6 items, hidden, ticked by a blank project."),
]

QUESTIONS = [
 ("Goal or use case", "Onboarding, step 1", "Start options, prompt suggestions, Clueprint picks and checklist items", "Asked first (good), but only changes the \"Recommended\" tag"),
 ("First-video method", "Last step, and it should start the action", "Opens the recorder, the uploader or a pre-filled prompt", "Asked, but the recommended option needs an extension"),
 ("Name", "Never; take it from Google or SSO", "Avatar, workspace default name", "Asked twice"),
 ("Role", "Optional, only if it changes content", "Example prompts, sample project, checklist variant", "Required; changes nothing visible"),
 ("Workspace name", "Default it silently; rename when inviting", "Nothing on day one", "A full step"),
 ("Company website / brand", "When the user opens Brand kit or before the first export", "Logo, colors and fonts scraped from the real site", "Never asked; auto-built from gmail.com"),
 ("Team size", "At invite or upgrade time", "Plan recommendation", "Not asked (good)"),
 ("Invite teammates", "After the first video, at share time", "Reviewer or editor seat offer", "Checklist item on day one"),
 ("How did you hear about us", "After activation, by email or a micro-survey", "Nothing in the product", "A pop-up on the first Home view"),
 ("Experience level", "Infer it from behavior", "How much guidance to show", "Not asked (good)"),
]

# phase, x-label, doing, thinking, feeling (-2..2), pains, opportunities
JOURNEY = [
 ("Sign up", "Signs in with Google", "\"Easy, one click.\"", 1, "Personal-email warning", "Keep it as is; drop the work-email nag"),
 ("Profile", "Types a name Google already has", "\"Didn't I just do this?\"", -1, "B1", "Prefill from Google"),
 ("Load", "Waits for a blank screen", "\"Is it broken?\"", -1, "B3", "Skeleton screen with a status line"),
 ("Goals", "Picks Product demos and SOPs", "\"OK, it's asking what I need.\"", 1, "", "Use the answers visibly"),
 ("Profile again", "Retypes name, waits for the role list", "\"Again?\"", -1, "B7, B10", "Merge or remove"),
 ("First video", "Clicks the recommended option and gets an install wall", "\"I have to install something now?\"", -2, "B13, B17", "Pre-filled prompt or sample project"),
 ("Home", "Survey pop-up, banners, model menu", "\"Too much going on.\"", -1, "C3, C6, C10", "One clear next step"),
 ("Editor", "Blank canvas, unlabeled icons", "\"Where do I start?\"", -1, "F1, F3, F4", "Empty-state call to action, simplified editor"),
 ("Voiceover", "Types a script; speech is generated", "\"Nice, that was quick.\"", 1, "", "Celebrate it"),
 ("Preview stuck", "Can't play until reload", "\"It froze.\"", -2, "F8, F9", "Auto-reconnect"),
 ("AI plan", "Reads a good 6-scene plan", "\"This is impressive.\"", 2, "G1", "Show the cost before approving"),
 ("Waiting", "Watches \"Working for 8 min\"", "\"How long will this take?\"", -1, "G2, G5", "Scene progress and ETA, notify on finish"),
 ("Result", "Sees polished scenes forming", "\"Looks professional.\"", 1, "", "Make this the peak, sooner"),
 ("Share", "Opens Share; limits are hidden", "\"Will this cost me?\"", -1, "H1, H3", "State the minutes and watermark up front"),
]

SOURCES = [
 ("AI and agents", [
  ("Amershi et al., Guidelines for Human-AI Interaction (CHI 2019)", "https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/Guidelines-for-Human-AI-Interaction-camera-ready.pdf"),
  ("Microsoft HAX Toolkit", "https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/"),
  ("Google PAIR, People + AI Guidebook", "https://pair.withgoogle.com/guidebook-v2/chapters"),
  ("NN/g, A Concrete Definition of an AI Agent (2026)", "https://www.nngroup.com/articles/definition-ai-agent/"),
  ("NN/g, Adding UI Controls to Prompting (2024)", "https://www.nngroup.com/articles/prompt-controls-genai/"),
  ("NN/g, Prompt Suggestions (2025)", "https://www.nngroup.com/articles/prompt-suggestions/"),
  ("NN/g, Humanizing AI Is a Trap (2026)", "https://www.nngroup.com/articles/humanizing-ai/"),
  ("Smashing Magazine, Designing for Agentic AI (2026)", "https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/"),
  ("The Shape of AI (Emily Campbell)", "https://www.shapeof.ai/"),
  ("Jakob Nielsen, Slow AI: Designing User Control for Long Tasks (2025)", "https://www.uxtigers.com/post/slow-ai"),
  ("NN/g, Response Times: The 3 Important Limits", "https://www.nngroup.com/articles/response-times-3-important-limits/"),
  ("NN/g, Progress Indicators Make a Slow System Less Insufferable", "https://www.nngroup.com/articles/progress-indicators/"),
 ]),
 ("Onboarding and psychology", [
  ("BJ Fogg, Behavior Model", "https://behaviormodel.org/"),
  ("Laws of UX (Hick, Jakob, goal-gradient, Zeigarnik, peak-end, Doherty...)", "https://lawsofux.com/"),
  ("Nir Eyal, Hook Model", "https://www.nirandfar.com/how-to-manufacture-desire/"),
  ("Endowed progress (Nunes and Drèze 2006), summary", "https://coglode.com/nuggets/endowed-progress-effect"),
  ("NN/g, Mobile-App Onboarding", "https://www.nngroup.com/articles/mobile-app-onboarding/"),
  ("NN/g, Onboarding Tutorials vs. Contextual Help", "https://www.nngroup.com/articles/onboarding-tutorials/"),
  ("NN/g, Designing Empty States", "https://www.nngroup.com/articles/empty-state-interface-design/"),
  ("NN/g, Website Forms Usability", "https://www.nngroup.com/articles/web-form-design/"),
  ("NN/g, Progressive Disclosure", "https://www.nngroup.com/articles/progressive-disclosure/"),
  ("ProductLed, Bowling Alley framework", "https://productled.com/blog/product-led-user-onboarding-experience"),
  ("Appcues, Checklist best practices", "https://docs.appcues.com/checklist-best-practices"),
  ("Userpilot, Welcome surveys", "https://userpilot.com/blog/welcome-survey/"),
 ]),
 ("Information architecture and journeys", [
  ("Dan Brown, Eight Principles of IA (summary)", "https://principles.design/examples/eight-principles-of-information-architecture"),
  ("Rosenfeld and Morville, organization schemes (1st ed. text)", "https://files.znu.edu.ua/files/comp.books/books/information_architecture_for_WWW/infoarch/ch03_02.htm"),
  ("NN/g, IA vs. Navigation", "https://www.nngroup.com/articles/ia-vs-navigation/"),
  ("NN/g, Information Scent", "https://www.nngroup.com/articles/information-scent/"),
  ("NN/g, Left-Side Vertical Navigation", "https://www.nngroup.com/articles/vertical-nav/"),
  ("NN/g, Flat vs. Deep Hierarchies", "https://www.nngroup.com/articles/flat-vs-deep-hierarchy/"),
  ("NN/g, Card Sorting", "https://www.nngroup.com/articles/card-sorting-definition/"),
  ("NN/g, Tree Testing", "https://www.nngroup.com/articles/tree-testing/"),
  ("NN/g, Journey Mapping 101", "https://www.nngroup.com/articles/journey-mapping-101/"),
  ("NN/g, 10 Usability Heuristics", "https://www.nngroup.com/articles/ten-usability-heuristics/"),
  ("Microsoft, Guidelines for app settings", "https://learn.microsoft.com/en-us/windows/apps/design/app-settings/guidelines-for-app-settings"),
  ("Christensen Institute, Jobs to Be Done", "https://www.christenseninstitute.org/theory/jobs-to-be-done/"),
 ]),
 ("Competitor benchmark (public sources, no sign-ups)", [
  ("Supademo flow examples: Loom", "https://supademo.com/user-flow-examples/loom"),
  ("Supademo flow examples: Descript", "https://supademo.com/user-flow-examples/descript"),
  ("Supademo flow examples: Synthesia", "https://supademo.com/user-flow-examples/synthesia"),
  ("Supademo flow examples: VEED", "https://supademo.com/user-flow-examples/veed"),
  ("Vero, Loom onboarding teardown (2023)", "https://www.getvero.com/resources/user-onboarding-example-loom-2023"),
  ("B2B Growth Insights, Synthesia onboarding (2025)", "https://b2bgrowthinsights.beehiiv.com/p/what-synthesia-s-onboarding-teaches-us-about-ai-product-conversion"),
  ("HeyGen review, Marc Andrews (2026)", "https://marcandrews.com/heygen-review-2026-ai-avatar-videos-without-filming/"),
  ("Guidde pricing", "https://guidde.com/pricing"),
  ("Tango help center", "https://help.tango.us/en/articles/5971659"),
 ]),
]

STATUS = {"meets": "Meets", "partial": "Partial", "fails": "Fails", "nt": "Not tested"}


def _refs(r):
    if not r:
        return ""
    return " ".join(f'<a class="ref" href="#f-{x.strip()}">{E(x.strip())}</a>' for x in r.split(","))


def scorecards_html():
    out = ['<section id="scorecards" class="block"><h2>Framework scorecards</h2>'
           '<p class="lede">Each principle is scored against what I observed in the session: <b>Meets</b>, <b>Partial</b>, <b>Fails</b> or <b>Not tested</b>. Finding IDs link to the evidence above.</p>']
    out.append('<div class="scoretabs">')
    for key, title, intro, url, rows in SCORECARDS:
        c = {k: sum(1 for r in rows if r[3] == k) for k in STATUS}
        bar = "".join(f'<span class="seg seg-{k}" style="flex:{c[k]}" title="{STATUS[k]}: {c[k]}"></span>' for k in STATUS if c[k])
        out.append(f'<a class="scoretab" href="#sc-{key}"><b>{E(title)}</b><span class="segbar">{bar}</span>'
                   f'<span class="sccount">{c["meets"]} meets · {c["partial"]} partial · {c["fails"]} fail</span></a>')
    out.append('</div>')
    for key, title, intro, url, rows in SCORECARDS:
        out.append(f'<div class="card-block" id="sc-{key}"><h3>{E(title)}</h3><p class="lede">{E(intro)} <a href="{url}" target="_blank" rel="noopener">Source</a></p>'
                   '<div class="tablewrap"><table class="sc"><thead><tr><th>ID</th><th>Group</th><th>Principle</th><th>Clueso</th><th>Evidence</th><th>Findings</th></tr></thead><tbody>')
        for rid, grp, name, st, ev, refs in rows:
            out.append(f'<tr><td class="mono">{rid}</td><td>{E(grp)}</td><td><b>{E(name)}</b></td>'
                       f'<td><span class="st st-{st}">{STATUS[st]}</span></td><td>{E(ev)}</td><td>{_refs(refs)}</td></tr>')
        out.append('</tbody></table></div></div>')
    out.append('</section>')
    return "\n".join(out)


SELF = ' class="self"'


def competitors_html():
    rows = "".join(
        f'<tr{SELF if n == "Clueso" else ""}><td><b>{E(n)}</b></td><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td><td>{E(e)}</td></tr>'
        for n, a, b, c, d, e in COMPETITORS)
    pats = "".join(f'<li><h3>{E(t)}</h3><p>{E(m)}</p><p class="vs"><b>Clueso:</b> {E(c)}</p></li>' for t, m, c in PATTERNS)
    return f"""<section id="competitors" class="block"><h2>Competitor onboarding benchmark</h2>
<p class="lede">Built from public help centers, pricing pages and published teardowns. I didn't sign up for any competitor; unverified items are marked as such.</p>
<div class="tablewrap"><table><thead><tr><th>Product</th><th>Card needed</th><th>Questions (screens)</th><th>Install before first value</th><th>First run</th><th>How limits are shown</th></tr></thead><tbody>{rows}</tbody></table></div>
<ul class="patterns">{pats}</ul></section>"""


def questions_html():
    rows = "".join(f"<tr><td><b>{E(q)}</b></td><td>{E(w)}</td><td>{E(c)}</td><td>{E(t)}</td></tr>" for q, w, c, t in QUESTIONS)
    return f"""<section id="questions" class="block"><h2>What to ask in onboarding, and when</h2>
<p class="lede">The rule, from NN/g, ProductLed and Userpilot: ask a question only if its answer changes what the user sees next, and say how it will be used. Otherwise derive it, defer it or drop it. Canva asks 1 question, Loom 1 plus an optional follow-up, and Airtable 3.</p>
<div class="tablewrap"><table><thead><tr><th>Question</th><th>When to ask</th><th>What the answer should change</th><th>Clueso today</th></tr></thead><tbody>{rows}</tbody></table></div></section>"""


def journey_html():
    n = len(JOURNEY)
    W, H, padL, padR, padT, padB = 1000, 260, 70, 20, 20, 70
    step = (W - padL - padR) / (n - 1)
    y = lambda v: padT + (2 - v) * (H - padT - padB) / 4
    pts = [(padL + i * step, y(j[3])) for i, j in enumerate(JOURNEY)]
    grid = "".join(f'<line x1="{padL}" x2="{W - padR}" y1="{y(v):.1f}" y2="{y(v):.1f}" class="{"zero" if v == 0 else "grid"}"/>'
                   f'<text x="{padL - 10}" y="{y(v) + 4:.1f}" text-anchor="end" class="axis">{["Very bad", "Bad", "Neutral", "Good", "Great"][v + 2]}</text>' for v in range(-2, 3))
    path = "M" + " L".join(f"{x:.1f},{yy:.1f}" for x, yy in pts)
    dots = "".join(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="6" class="dot dot-{"good" if j[3] > 0 else "bad" if j[3] < 0 else "neutral"}"><title>{E(j[0])}: {E(j[2])}</title></circle>' for (x, yy), j in zip(pts, JOURNEY))
    labels = "".join(f'<text x="{x:.1f}" y="{H - padB + 18}" text-anchor="end" transform="rotate(-35 {x:.1f} {H - padB + 18})" class="axis">{E(j[0])}</text>' for (x, _), j in zip(pts, JOURNEY))
    svg = f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Emotion curve across the first session"><g>{grid}</g><path d="{path}" class="curve"/>{dots}{labels}</svg>'
    rows = "".join(
        f'<tr><td><b>{E(p)}</b></td><td>{E(d)}</td><td><i>{E(t)}</i></td><td><span class="feel feel-{"good" if f > 0 else "bad"}">{"+" if f > 0 else ""}{f}</span></td><td>{_refs(pn) if pn and pn[0] in "ABCDEFGH" and pn[1].isdigit() else E(pn)}</td><td>{E(o)}</td></tr>'
        for p, d, t, f, pn, o in JOURNEY)
    return f"""<section id="journey-map" class="block"><h2>Journey map: first session</h2>
<p class="lede">The person: a product or customer-education manager, new to Clueso, on the Free plan, who wants a product demo and an SOP. The scenario: sign up and get one shareable video in the first session. The structure follows NN/g's journey-mapping components: phases, actions, thoughts, emotions and opportunities.</p>
<div class="chartwrap">{svg}</div>
<div class="tablewrap"><table><thead><tr><th>Phase</th><th>Doing</th><th>Thinking</th><th>Feeling</th><th>Pain points</th><th>Opportunity</th></tr></thead><tbody>{rows}</tbody></table></div></section>"""


def sources_html():
    groups = "".join(
        f'<div class="srcgroup"><h3>{E(g)}</h3><ul>' + "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{E(t)}</a></li>' for t, u in items) + "</ul></div>"
        for g, items in SOURCES)
    return f"""<section id="sources" class="block"><h2>Sources</h2>
<p class="lede">Research agents fetched each page and checked the claims against it. Exceptions: Dan Brown's original PDF returned a 404, so the summary page is used. The Rosenfeld and Morville text is the 1st edition. Some competitor details came only from search snippets and are marked unverified in the benchmark.</p>
<div class="srcgrid">{groups}</div></section>"""


CSS = """
.scoretabs { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
.scoretab { display: grid; gap: 8px; background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 12px 14px; text-decoration: none; color: var(--ink); }
.scoretab:hover { border-color: var(--accent); }
.segbar { display: flex; height: 8px; border-radius: 4px; overflow: hidden; background: var(--line); }
.seg-meets { background: var(--good); } .seg-partial { background: var(--minor); } .seg-fails { background: var(--crit); } .seg-nt { background: var(--line); }
.sccount { font: 500 0.72rem var(--mono); color: var(--muted); }
.card-block { display: grid; gap: 10px; padding-top: 16px; }
.st { font: 600 0.7rem var(--body); text-transform: uppercase; letter-spacing: 0.05em; padding: 2px 8px; border-radius: 999px; white-space: nowrap; }
.st-meets { color: var(--good); background: var(--good-soft); } .st-partial { color: var(--minor); background: var(--minor-soft); }
.st-fails { color: var(--crit); background: var(--crit-soft); } .st-nt { color: var(--muted); background: var(--bg); border: 1px solid var(--line); }
.mono { font: 500 0.78rem var(--mono); color: var(--muted); }
.ref { font: 500 0.75rem var(--mono); margin-right: 4px; white-space: nowrap; }
table.sc td:nth-child(5) { color: var(--muted); min-width: 260px; }
tr.self td { background: var(--accent-soft); }
.patterns { list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }
.patterns li { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; display: grid; gap: 6px; font-size: 0.92rem; }
.patterns li p { color: var(--muted); } .patterns .vs { color: var(--ink); }
.chartwrap { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 12px; overflow-x: auto; }
.chartwrap svg { display: block; width: 100%; min-width: 640px; height: auto; }
.chartwrap .grid { stroke: var(--line); stroke-width: 1; } .chartwrap .zero { stroke: var(--muted); stroke-width: 1; stroke-dasharray: 4 4; }
.chartwrap .axis { fill: var(--muted); font: 11px var(--body); }
.chartwrap .curve { fill: none; stroke: var(--accent); stroke-width: 2.5; stroke-linejoin: round; }
.chartwrap .dot { stroke: var(--surface); stroke-width: 2; } .dot-good { fill: var(--good); } .dot-bad { fill: var(--crit); } .dot-neutral { fill: var(--muted); }
.feel { font: 700 0.85rem var(--mono); } .feel-good { color: var(--good); } .feel-bad { color: var(--crit); }
.srcgrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }
.srcgroup { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; min-width: 0; }
.srcgroup ul { margin: 8px 0 0; padding-left: 1.1rem; display: grid; gap: 4px; font-size: 0.88rem; overflow-wrap: anywhere; }
"""
