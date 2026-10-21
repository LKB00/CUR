"""Navigation-layer audit: feature map, left-nav verdicts, entry-point matrix, core use-case paths."""
import html

E = html.escape


def refs(r):
    return " ".join(f'<a class="ref" href="#f-{x.strip()}">{E(x.strip())}</a>' for x in r.split(",") if x.strip())


ANATOMY = [
 ("Sidebar: navigation (9)", "Home · Projects · Agent · Chats | MCP | Clueprints | Brand kit · Analytics · Settings", "Four groups separated by thin rules, with no group names"),
 ("Sidebar: widgets (4)", "New in Clueso · What's new card · Get started checklist · Upgrade card", "They push the nav up and compete with it"),
 ("Sidebar: footer (1)", "Workspace switcher (\"UX's Workspace, Free trial\")", "Lists workspaces only; no link to workspace settings"),
 ("Header (5)", "Search ⌘K · Avatar menu · Help · Clueso AI · New project ▾", "Clueso AI is missing on Home; Help also appears in the avatar menu"),
 ("Page footer (3)", "Built with care · Learn about our features · More from Clueso", "Three more exits to help and YouTube"),
 ("Overlays (2)", "Promo banner · floating chat bubble", "Always on"),
]

# feature, job, entry points, leads to, issues, finding refs
FEATURE_MAP = [
 ("Home", "Start something new; see recent work", "Sidebar · logo · \"Back to Home\" in the editor menu", "Prompt → a chat page (no nav item highlighted). Four chips → upload, record or translate dialogs. Recent projects → editor", "Its four start chips differ from the New project menu and onboarding. Clueso AI disappears from the header here.", "D13, C12"),
 ("Projects", "Find and manage existing work", "Sidebar · Home \"See all\" · ⌘K · checklist \"Export a video\"", "Editor", "No link to the chat that produced a project. Translations aren't grouped with their original or labeled with a language. Names are cut at about 30 characters. The filter bar overflows.", "H6, N4"),
 ("Agent", "Enterprise automation: agents that record and update videos", "Sidebar only", "\"Book a demo\" (leaves the app) · a promo video", "A dead end for every non-Enterprise user. It has no path to anything usable and is not the \"AI agent\" the checklist means.", "D1, D2"),
 ("Chats", "History of AI conversations", "Sidebar · Home prompt · Clueprint \"Create video\" · checklist \"Chat with the AI agent\"", "A chat, which then opens a project", "Overlaps with Projects; chat and project names differ for the same work. Chats started inside the editor don't appear here.", "D3, N3"),
 ("Clueso AI (header)", "Talk to the AI from anywhere", "Header button (not on Home) · ⌘K Tab", "A side panel, or a full chat page", "A third way into the same AI, alongside the Home prompt and Chats.", "D6"),
 ("MCP", "Connect Claude, ChatGPT or Cursor to Clueso", "Sidebar · checklist · onboarding step 4", "Setup steps in external tools", "A one-time developer setup in primary nav. Code connections (GitHub, Bitbucket) are separately in Settings.", "D10"),
 ("Clueprints", "Pick a reusable video style", "Sidebar · onboarding gallery (unlabeled) · AI panel chip · prompt + menu", "Detail modal → \"Create video\" → a new chat, not the editor", "The detail view has no description or input requirements. \"Create video\" immediately starts a paid AI chat. It overlaps with editor Templates.", "D11, N5"),
 ("Brand kit", "Workspace look: logo, colors, fonts, tone", "Sidebar · Home prompt chip", "Nowhere; there's no \"use this\" path", "Configuration that's done rarely, sitting in primary nav. It was auto-filled from gmail.com.", "C7, C2"),
 ("Analytics", "Video performance", "Sidebar", "Upgrade wall on Free", "A paywall in primary nav. Its data is about projects but it lives apart from them.", "D7"),
 ("Settings", "Workspace configuration (10 pages)", "Sidebar · translator's \"Customize translation rules\" · checklist \"Invite a collaborator\"", "Settings pages", "Profile settings lives elsewhere (avatar modal). Jumping in from the translator throws away the user's setup.", "D14, N6"),
 ("Get started checklist", "First-run guidance", "Sidebar widget, collapsed", "Mixed: a chat page, Projects, MCP, Settings > Users, an install modal", "Each item lands somewhere different with no guidance. \"Export a video\" just opens the Projects list.", "C4, N7"),
]

# item, frequency, audience, verdict, new place, why
NAV_VERDICT = [
 ("Home", "Daily", "Everyone", "keep", "1st, rename \"Create\"", "The primary job; it's where creation starts"),
 ("Projects", "Daily", "Everyone", "keep", "2nd", "The object users come back to (Brown: objects)"),
 ("Agent", "Weekly", "Everyone, including Free", "move", "3rd, renamed Clueso AI: the full home of conversations, a list beside the open conversation, where you reply, approve plans and see what was built. New videos start in Create; the panel helps on other pages. Enterprise automations are named Automations and listed once here.", "Today the same assistant hides behind five doors and four names, while Agent is an Enterprise sales page. Three surfaces with one job each remove the guesswork"),
 ("Chats", "Weekly", "Everyone", "merge", "Into Clueso AI as the conversation list; the three most recent also appear in the panel", "The same conversations are reached from Chats, Home and the panel, under different names"),
 ("MCP", "Once", "Developers", "move", "Integrations, pinned at the bottom", "Setup that's done once doesn't belong in primary nav"),
 ("Clueprints", "Weekly", "Everyone", "move", "Library > Video styles; also a \"Start from a style\" option in Create", "A reusable asset, not a destination; an unfamiliar name gives weak information scent"),
 ("Brand kit", "Monthly", "Admins", "move", "Library > Brand kit (also offered at first export)", "Rare configuration; it should reach users where it's used"),
 ("Analytics", "Weekly (paid)", "Business and Enterprise", "keep", "4th, with a lock badge on Free and a labeled sample dashboard; each project page links to its filtered view", "Clueso's Analytics is a workspace-wide dashboard across all videos (overview, trend, top content, locations, help-center searches), so it needs its own place"),
 ("Settings", "Rare", "Admins", "keep", "Pinned last; merge in Profile settings", "Microsoft's guidance: Settings goes last and holds everything configurable"),
 ("New in Clueso + What's new card", "Rare", "Everyone", "move", "Inside the Help menu as \"What's new\"", "Frees sidebar space"),
 ("Get started checklist", "First week", "New users", "move", "A card on Create (Home) until done, 3 to 5 items", "Onboarding must be seen to work (Appcues)"),
 ("Upgrade card", "Always", "Free users", "merge", "A slim usage meter (minutes and credits) with an Upgrade link", "Shows the limits that matter, in place of a static ad"),
]

ACTIONS = ["Create from prompt", "Record screen", "Upload video", "Slides or PDF", "Translate", "Blank project", "From a Clueprint", "Connect AI tools (MCP)"]
SURFACES = [
 ("Home chips and prompt", ["Prompt", "Record your screen", "Upload videos", "Upload slide decks", "Translate", "", "+ menu", ""]),
 ("New project menu", ["", "Record screen", "Upload videos", "Upload PPT/PDF", "", "Start blank project", "", ""]),
 ("Onboarding step 4", ["Create with a prompt", "Record screen", "Upload screen recording", "Upload slide decks", "Translate an existing video", "", "Unlabeled gallery", "Create from Claude, ChatGPT, or Gemini"]),
 ("Clueso AI panel", ["Ask anything", "", "", "", "", "", "Create a Clueprint", ""]),
 ("Clueprints page", ["", "", "", "", "", "", "Create video", ""]),
 ("Checklist", ["", "Install screen recorder", "", "", "", "", "", "Connect our MCP"]),
]

# use case, best path today, steps, ends in, issues, refs, proposed
USE_CASES = [
 ("Product demo or walkthrough", "Home → Record your screen → install modal → Chrome Web Store", "3 steps, then it leaves the app", "Blocked until the extension is installed", "The recommended path in onboarding and Home leads out of the product. The working alternative (prompt) is presented as equal, not as a fallback.", "B13, B17", "Home → Record (in-browser tab capture), with the extension offered after the first video"),
 ("SOP or step-by-step guide", "No direct entry. Make a video first → Article tab → \"Step-by-step help article\" → Prompt hub → Confirm → type a request", "6+ steps", "A raw AI instruction screen before anything happens", "Clueso's second headline product has no start option of its own; it's hidden as a tab inside the video editor.", "F14, N8", "A \"Create guide\" option in Create, and an \"Article\" toggle on every upload"),
 ("Training video", "Home → Upload slide decks → attach → Create → editor → AI ideas → \"Train the team on it\"", "6 steps", "New, separate projects (not the one you're in)", "It works, but the user starts in one project and the results land as new projects with different names.", "N9", "Ask \"Training, explainer or teaser?\" in the upload dialog, before Create"),
 ("Marketing video", "Clueprints → card → Create video → chat asks for a brief", "4 steps", "A chat, not the editor; 13 credits for a clarifying question", "The style is chosen first and the content after, through chat.", "N5", "Clueprint detail opens a short form (product, audience, call to action) with a cost estimate"),
 ("Slides or PDF to video", "Home → Upload slide decks → attach → Create", "3 steps", "Editor with a script", "Smooth. The dialog title (\"Upload files\") differs from the button (\"Upload slide decks\").", "D13", "Keep; align the labels"),
 ("Translate a video", "Home → Translate → choose existing project → Translate", "4 steps", "A new project with a translated title", "\"Customize translation rules\" jumps to Settings and loses the setup. The copy isn't linked to its original.", "N6, N4", "Open the rules in a side panel; group language versions under one project"),
 ("Motion graphics or animation", "No entry. Only the AI panel chip \"Create an animation\" or a rotating Home placeholder", "Hidden", "A chat", "Offered as a goal in onboarding but has no start option anywhere.", "N10", "An \"Animation\" option in Create"),
 ("Measure performance", "Sidebar → Analytics", "1 step", "Paywall on Free", "Can't preview what you would get.", "D7", "Keep Analytics as a workspace-wide dashboard; show a labeled sample on Free and link each project to its filtered view"),
 ("Bring the team", "Checklist → Settings > Users → Invite", "3 steps", "Invite dialog with a role picker", "No seat limit or role explanation in the dialog.", "E4, N11", "Invite from the Share dialog, with roles explained inline"),
]

NEW_FINDINGS = [
 ("N1", "major", "86-sidebar-collapsed.jpg", "The collapsed sidebar is an unlabeled icon rail", "Agent, Chats and Clueso AI use similar sparkle and pointer icons, and MCP's icon is unrecognizable. NN/g advises keeping text labels on vertical nav.", "Show labels on hover as a fly-out, and use distinct icons for each item.", "NN/g vertical navigation"),
 ("N2", "major", "81-checklist-chat-orphan.jpg", "The AI chat page is an orphan in the navigation", "Opened from the checklist or the Home prompt, it is titled \"Clueso AI\" while no sidebar item is highlighted. Users lose \"where am I\".", "Highlight the parent item (Chats, or Create in the proposed nav) and add a breadcrumb.", "Brown: front doors"),
 ("N3", "major", "80-chats-list.jpg", "Chats and Projects list the same work under different names",
  "\"Taskly Project Management Demo Video\" (chat) produced \"Taskly – Track Tasks Together (Product Demo)\" (project), and neither links to the other. Chats started inside the editor (the PDF ideas chat) don't appear in Chats at all.", "Make the project the object, with its chats inside it; show the chat in the project's AI panel.", "Brown: objects; Rosenfeld and Morville: organization"),
 ("N4", "major", "87-projects-six.jpg", "Language versions and AI spin-offs are loose projects",
  "The Spanish copy (\"Taskly – Seguimiento de T...\") sits as an unrelated project with no language badge. The two videos generated from the PDF are separate projects with new names.", "Group versions under their source with language and type badges.", "Brown: multiple classification"),
 ("N5", "major", "84-clueprint-detail.jpg", "Clueprint detail doesn't say what you need or what happens next",
  "No description (onboarding showed one), no required inputs (recording? script?), no cost. \"Create video\" sends a chat message at once. The help docs say you describe your video first.", "Show the description, the inputs needed and a cost estimate, then a short brief form.", "Brown: disclosure"),
 ("N6", "major", "83-translate-rules-jump.jpg", "\"Customize translation rules\" throws away the translator setup",
  "It navigates to Settings > Translations; going back shows Home with the dialog closed and the selection lost.", "Open rules in a side sheet over the translator.", "User control and freedom"),
 ("N7", "minor", "82-translator.jpg", "Checklist and dialogs send people to scattered places",
  "\"Export a video\" opens the Projects list with no hint of what to do next. The translator's rules link opens Settings. \"Invite a collaborator\" opens Settings > Users.", "Each checklist item should open the exact action with a coach mark.", "Match between system and real world"),
 ("N8", "major", "76-article-prompt-hub.jpg", "The SOP use case has no start option",
  "\"Step-by-step help article\" opens a \"Prompt hub\" showing a raw AI instruction, then needs a typed request.", "Add \"Create guide\" to the creation menu and generate the article automatically from every recording.", "Time to value"),
 ("N9", "minor", "77-pdf-ideas-cost.jpg", "AI ideas create new projects away from where you are",
  "Picking ideas in the PDF project made two new projects; the current project stayed a plain slide video. This version shows a cost estimate, unlike the Home prompt.", "Say \"This will create 2 new projects\" and link to them; use the same estimate everywhere.", "Visibility of system status"),
 ("N10", "major", "14-onb-first-video.jpg", "Motion graphics is a goal with no door",
  "Onboarding offers \"Motion graphics\" as a goal, but no menu has an Animation start option.", "Add it to Create, or drop it from onboarding goals.", "Brown: choices"),
 ("N12", "major", "89-search-padded.jpg", "Search pads results and never says \"no results\"",
  "Searching \"on\" lists \"Untitled (1)\" and \"Taskly — Product Teaser\" (1) with nothing highlighted; \"xyzq\" still returns 5 projects and \"brand\" returns Home. Navigation (2) is always listed first, even when a project is the better match. The empty panel is blank (screenshot 90). The frame itself is good: fixed 680 × 480, input pinned, scopes with p; f; n; a; prefixes, Tab to ask AI.", "Show only real matches, ranked and highlighted, at most 5 per group with \"Show all\"; order groups by best match; show recent projects and quick actions when empty; an honest no-results state that offers Ask AI and Create.", "Nielsen #6 recognition over recall; NN/g search results and no-results pages; Hick's law"),
 ("N13", "minor", "38-account-menu.jpg", "Theme icons have no names",
  "Light, Dark and System sit in the account menu as three icon-only buttons. They use role=tab with no aria-label or text, so screen readers announce three unnamed tabs, and sighted users must guess the third (a monitor) means System.", "Label each option (or at least give it an accessible name) and treat the set as a radio group.", "NN/g: icons need text labels; WCAG 4.1.2 name, role, value"),
 ("N14", "major", "91-ai-sidebar-hides-actions.jpg", "Clueso AI's view modes each break something",
  "Floating (the default) covers the page's own controls: on Projects it hides the date filters and sort (screenshot 92). Sidebar docks the panel but pushes Help, the account menu and New project off screen (1) and drops the page's filters (2). Full screen navigates to /home/chat, so the page you were asking about is gone and no nav item is highlighted (screenshot 93). The chosen view resets every time the panel reopens.", "Keep the three views but make side-by-side keep the top bar, expand full width in place, and remember the choice.", "Nielsen #3 user control; Nielsen #1 visibility; NN/g: don't hide primary actions"),
 ("N15", "major", "92-ai-floating-covers.jpg", "Clueso AI ignores where you are and what a reply costs",
  "The same three chips (Create a video, Create an animation, Create a Clueprint) appear on every page, and none mention the project open behind the panel. Cost appears only as a \"Running low on AI credits\" banner (2) after the fact; a clarifying reply cost 13 credits. Escape on a menu inside the panel also closes the panel, and focus stays on the header button when it opens. The model menu lists nine vendor models (Opus, Sonnet, Astra, Sol, Luna, Terra, Kimi, GLM, DeepSeek) with no cost, and the default differs by surface (Sonnet 5.5 here, Opus 5.5 on Home). Screen readers hear the controls as \"Director autonomy mode\" and \"Director model\". View descriptions live only in hover tooltips.", "Context line and page-specific chips; run button-able tasks directly without credits; show credits per reply before sending; Escape closes one layer at a time; move focus to the composer.", "HAX G3 and G4 (time services to context, show relevant information); Shape of AI cost estimates; WAI-ARIA focus management"),
 ("N16", "minor", "94-projects-live.jpg", "Projects toolbar has nine controls and still hides one",
  "Five filter dropdowns plus a sort menu push New folder off the edge (1); titles are cut to about 30 characters (2); sort exists twice, as a menu and as column headers (3). Row actions appear only on mouse hover, so keyboard and touch users can't see them. A one-person workspace still gets a Creator filter and column.", "Sort on the headers only; one Filter button with chips; show the row menu on hover and keyboard focus; drop Creator for solo workspaces; keep Deleted (30 days), which works well.", "Hick's law; Jakob's law (sortable headers); WCAG 2.1.1 keyboard"),
 ("N17", "critical", "96-chat-page-is-agent.jpg", "One assistant, five doors, four names",
  "The Home prompt, the Clueso AI panel, the Chats list and a full-page chat (1) are all the same agent, whose chats are titled \"Getting Started With Director\" and whose controls read \"Director model\". The Agent nav item is something else: an Enterprise sales page for automations. Inside a chat no nav item is highlighted (2) and the Clueso AI button disappears (3); it also disappears on Home. Switching an open chat to Floating drops you on Home with two composers, Home's prompt and the chat's (screenshot 97).", "Give each surface one job: Create starts something new and hands off to the conversation; a Clueso AI page (replacing Agent and Chats) holds conversations in full, list beside conversation; the panel only helps with what is on screen on other pages, and hides on Create and the Clueso AI page, as Clueso already does. Call it Clueso AI everywhere and name the Enterprise automations Automations.", "Nielsen #4 consistency; Dan Brown, objects and front doors; cognitive load"),
 ("N11", "major", "88-invite-modal.jpg", "Invite dialog hides seat limits and role meaning",
  "An email field, an Editor dropdown and Send invite. Nothing says Free has 1 seat or explains Editor vs Reviewer.", "Show seats left and a one-line description of each role.", "Visibility of system status"),
]

STATUS = {"keep": "Keep up front", "move": "Move", "merge": "Merge", "remove": "Remove or hide by plan"}


def nav_html():
    anatomy = "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in ANATOMY)
    fmap = "".join(f"<tr><td><b>{E(f)}</b></td><td>{E(j)}</td><td>{E(en)}</td><td>{E(l)}</td><td>{E(i)}</td><td>{refs(r)}</td></tr>" for f, j, en, l, i, r in FEATURE_MAP)
    verdict = "".join(f'<tr><td><b>{E(i)}</b></td><td>{E(fq)}</td><td>{E(a)}</td><td><span class="vd vd-{v}">{STATUS[v]}</span></td><td>{E(p)}</td><td>{E(w)}</td></tr>' for i, fq, a, v, p, w in NAV_VERDICT)
    head = "".join(f"<th>{E(a)}</th>" for a in ACTIONS)
    rows = ""
    for s, cells in SURFACES:
        rows += f"<tr><td><b>{E(s)}</b></td>" + "".join(f'<td class="{"has" if c else "none"}">{E(c) if c else "—"}</td>' for c in cells) + "</tr>"
    uc = "".join(f"<tr><td><b>{E(u)}</b></td><td>{E(p)}</td><td>{E(s)}</td><td>{E(e)}</td><td>{E(i)}</td><td>{refs(r)}</td><td>{E(pr)}</td></tr>" for u, p, s, e, i, r, pr in USE_CASES)
    nf = []
    for fid, sev, img, title, ev, fix, heur in NEW_FINDINGS:
        nf.append(f'<figure class="finding-fig"><a class="shot" href="img/{img}" target="_blank" rel="noopener"><img src="img/{img}" alt="{E(title)}" loading="lazy"></a>'
                  f'<figcaption><ol class="flist"><li class="f f-{sev}" id="f-{fid}"><span class="badge badge-{sev}">1</span><div class="fbody"><div class="fhead"><span class="fid">{fid}</span>'
                  f'<span class="chip chip-{sev}">{sev.title()}</span><h3>{E(title)}</h3></div><p>{E(ev)}</p><p class="fix"><b>Fix:</b> {E(fix)}</p><p class="heur">{E(heur)}</p></div></li></ol></figcaption></figure>')
    return f"""
<section id="navigation" class="block">
  <h2>Navigation layer audit</h2>
  <p class="lede">This is the scope you asked for: the layout people move through after signing in, how each feature is reached, what it's for, where it leads, and whether the left navigation is structured well. It does not cover what happens inside video creation or the AI chat. Those notes are kept as an appendix further down.</p>

  <h3>What's on screen at all times</h3>
  <p class="lede">Every page carries about 24 clickable ways out. That is the main reason the product feels busy before the user has done anything.</p>
  <div class="tablewrap"><table><thead><tr><th>Area</th><th>Items</th><th>Problem</th></tr></thead><tbody>{anatomy}</tbody></table></div>

  <h3>Feature map: how each feature is reached, and where it leads</h3>
  <div class="tablewrap"><table class="wide"><thead><tr><th>Feature</th><th>User job</th><th>Entry points</th><th>Leads to</th><th>Navigation problems</th><th>Findings</th></tr></thead><tbody>{fmap}</tbody></table></div>

  <h3>Left navigation: what should be up front, moved, merged or hidden</h3>
  <p class="lede">Each item is rated on how often people need it and who it's for. The rule (NN/g, Dan Brown, Microsoft's settings guidance) is that frequent jobs go up front, one-time setup goes to the bottom, and nothing appears that the plan can't use. Of the 9 nav items and 4 widgets, Home, Projects, Agent, Analytics and Settings stay; the rest move, merge or go.</p>
  <div class="tablewrap"><table class="wide"><thead><tr><th>Item</th><th>How often</th><th>Who</th><th>Verdict</th><th>New place</th><th>Why</th></tr></thead><tbody>{verdict}</tbody></table></div>

  <h3>The same actions, offered differently in six places</h3>
  <p class="lede">Each row is a surface where users start something. A dash means the action isn't offered there; the text shows the exact label used. No two surfaces offer the same set with the same names.</p>
  <div class="tablewrap"><table class="matrix"><thead><tr><th>Surface</th>{head}</tr></thead><tbody>{rows}</tbody></table></div>

  <h3>Core use cases: the path through the layout</h3>
  <p class="lede">These are the use cases Clueso offers in onboarding, plus three supporting ones. Each was traced from Home to the point where the feature takes over.</p>
  <div class="tablewrap"><table class="wide"><thead><tr><th>Use case</th><th>Best path today</th><th>Steps</th><th>Ends in</th><th>Navigation problem</th><th>Findings</th><th>Proposed path</th></tr></thead><tbody>{uc}</tbody></table></div>

  <h3>How the features connect today</h3>
  <div class="chartwrap mer"><pre class="mermaid">
flowchart LR
  SI([Sign in]) --> ON[Onboarding, 4 steps]
  ON --> HOME[Home]
  HOME -->|prompt| CHAT[AI chat page]
  HOME -->|chips| DLG[Upload or translate dialogs]
  DLG --> ED[Editor]
  CHAT --> ED
  HOME --> PROJ[Projects]
  PROJ --> ED
  NAV{{Sidebar}} --> AG[Agent]
  AG -->|Book a demo| OUT([Leaves app])
  NAV --> CHATS[Chats]
  CHATS --> CHAT
  NAV --> MCP[MCP]
  MCP --> OUT
  NAV --> CP[Clueprints]
  CP -->|Create video| CHAT
  NAV --> BK[Brand kit]
  BK -.->|no exit| BK
  NAV --> AN[Analytics]
  AN -->|Free plan| PAY([Upgrade wall])
  NAV --> SET[Settings]
  DLG -->|translation rules| SET
  ED -->|Article tab| ART[Article and Prompt hub]
  CHK[Checklist] --> CHAT
  CHK --> PROJ
  CHK --> SET
  CHK --> MCP
  </pre></div>

  <h3>Proposed structure</h3>
  <div class="chartwrap mer"><pre class="mermaid">
flowchart TB
  subgraph Main
    CREATE[Create: prompt, record, upload, slides, guide, animation, Clueprint]
    PROJECTS[Projects: all, folders, versions]
    AGENT[Agent: tasks and chat history, open on Free]
    ANALYTICS[Analytics: all videos, drill into one]
    LIB[Library: Clueprints, clip templates, components, brand kit, media]
  end
  subgraph Pinned at bottom
    USAGE[Usage meter and upgrade]
    INT[Integrations: Chrome extension, MCP, GitHub, Bitbucket]
    SETTINGS[Settings: profile, workspace, members, plan, language, sharing]
    HELP[Help: docs, chat, what's new]
  end
  AI[[Clueso AI panel, same on every page, recent agent tasks]]
  CREATE --> PROJECTS
  LIB --> CREATE
  AI --- AGENT
  PROJECTS --> ANALYTICS
  AGENT --> PROJECTS
  </pre></div>

  <h3>New findings at the navigation layer</h3>
  {''.join(nf)}
</section>
"""


CSS = """
table.wide td { min-width: 140px; }
table.matrix td.has { color: var(--ink); font-size: 0.82rem; }
table.matrix td.none { color: var(--muted); text-align: center; }
.vd { font: 600 0.7rem var(--body); text-transform: uppercase; letter-spacing: 0.05em; padding: 2px 8px; border-radius: 999px; white-space: nowrap; }
.vd-keep { color: var(--good); background: var(--good-soft); } .vd-move { color: var(--accent); background: var(--accent-soft); }
.vd-merge { color: var(--minor); background: var(--minor-soft); } .vd-remove { color: var(--crit); background: var(--crit-soft); }
.chartwrap.mer pre { margin: 0; background: transparent; font: 13px var(--body); }
.appendix-note { background: var(--minor-soft); border-radius: 10px; padding: 12px 16px; font-size: 0.92rem; }
"""
