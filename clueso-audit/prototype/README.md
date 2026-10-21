# Clueso redesign prototype

A clickable prototype of Clueso's web app with the audit's navigation and onboarding improvements applied. It reuses Clueso's measured colors, spacing, radii, the Geist font, the logo mark and the sidebar and header icons taken from the live app.

## Run it

```bash
python3 -m http.server 4317 --directory clueso-audit/prototype
```

Then open http://localhost:4317 (start at `#/signin`).

## Click path

1. Sign in → Google
2. Onboarding (3 steps): goals and optional role → brand (optional) → first video
3. Create: prompt with quality, brand and cost; unified start options; checklist
4. Send → "Ready to build" → project hub with scene-by-scene progress
5. Projects (grouped versions and spin-offs), Library (Clueprints drawer, brand kit), Integrations, Settings (one area), ⌘K search, Clueso AI panel, collapsed sidebar

Use **Show improvements** (bottom right) to see numbered markers on each screen, and **List** for what changed and which audit findings it addresses.

## Notes

- The heading font is Outfit, standing in for Clueso's commercial Nohemi font.
- Thumbnails are CSS placeholders, not Clueso's assets.
- The video editor and AI chat internals are out of scope, matching the audit's navigation-layer focus.
- This reproduces another company's branding, so it is kept as local files and not published.

## QA

`qa.js` is a checker that isn't loaded by the app. In the browser console, inject it and run `await runSweep()` to check every screen and layer at the current viewport for:

- Text contrast against WCAG AA (4.5:1 for normal text, 3:1 for large text), measured against the real background, including gradients
- Horizontal page scroll and elements running off the right edge
- Clipped text
- Buttons and links overlapping each other, or rendering outside their own container

Last run (16 Oct 2026): 0 issues at 375×812, 1024×768 (sidebar open and collapsed), 1440×900 and 1920×1080, across 23 screens, 8 dialogs and drawers, and the Clueso AI panel. The 1440 run predates the overlap and escaped-element checks.

Deliberate changes from Clueso's measured values, all to pass AA contrast:
- Button gradient `rgb(247,112,227) → rgb(221,65,198)` became `rgb(200,48,178) → rgb(168,30,150)`. Clueso's white-on-pink buttons measure 2.5–3.7:1.
- The faint grey went from oklch 0.60 to 0.49, and the muted grey from 0.50 to 0.46.
- Badge text colors (pink, green, amber) were darkened to at least 4.5:1 on their tints.

Design scale used everywhere:
- Type: 10 / 11 / 12 / 13 / 14 / 16 / 18 / 24 px
- Control heights: 24 / 28 / 32 px
- Corner radii: 4 / 6 / 8 / 10 px, or a full pill

Below 760 px the sidebar becomes a drawer opened from the top bar.

Prompt suggestion motion and focus, matched to values measured on web.clueso.io:
- Old suggestion: each character runs `promptCharVanish` (400 ms ease-out, blur 0→4px, translateX 0→6px) with scattered delays of (i×13) mod 50 ms. The Tab key fades out over 200 ms.
- 500 ms later the new suggestion runs `promptCharMaterialize` (450 ms ease-out, blur 10px→0, translateX 6px→0), staggered 20 ms per character from left to right. The Tab key fades back in once the last character lands, and the suggestion holds for 4 s.
- Focused prompt: border turns brand pink `oklch(0.67 0.2 333.8)`, glow `0 0 10px 2px rgb(218 92 199 / .25)`, fill deepens from 4% to 6% black, over 150 ms. The caret is pink too. The border measures 3.3:1 on white, above the 3:1 needed for UI.
- Under reduced motion the suggestion stays still.
- Characters sit inside per-word wrappers, so long suggestions wrap between words, not mid-word.

Motion between features:
- Sidebar: the hover pill matches Clueso's measured hover (fades in over 100 ms, scales 0.96 → 1 over 200 ms, ease-out). The active item settles the same way when you change page.
- Menus: they match Clueso's measured enter (150 ms, opacity 0 → 1, scale 0.95 → 1, 7.5 px drop). Dialogs get the same fade and scale, and the dimmed backdrop behind them fades in.
- Drawers and the Clueso AI panel slide 16 px in from the right over 200 ms. Toasts rise in and fade out.
- Pages: Clueso swaps page content with no transition. Here the new page fades and rises 4 px over 180 ms, and only when the route changes, never on re-renders.
- Under reduced motion all of this is off. `qa.js` finishes running animations before it measures contrast.

Create page spacing (8 px rhythm): prompt to "Or start another way" is 32 px, matching Clueso's Home. Then 16 px to the cards, 32 px to the next step, and 48 px before Recent projects, so the three sections read as separate groups. The cards' padding grew to 14 × 16 px, with a 12 px gap.

Search (⌘K), compared with Clueso's (measured on web.clueso.io, 16 Oct 2026):

| | Clueso | Redesign |
|---|---|---|
| Frame | 680 × 480 px, 15vh from top, input pinned in a 48 px header | Same. Results scroll inside, header and footer stay put. On phones it fills the screen above the bar |
| Empty query | Blank panel | 3 recent projects and 4 quick actions (recognition over recall) |
| Matching | Fuzzy or semantic. "xyzq" returns 5 projects, "brand" returns Home | Only real matches. Ranked title start, then word start, then mid-word (3+ letters). Every query word must match |
| Highlight | Bold matched letters, but padded results show nothing | Bold on every match, in titles and subtitles |
| Volume | About 5 per group, Navigation always first | At most 5 per group with "Show all N". Groups ordered by best match |
| Scopes | Dropdown: All, Projects, Folders, Navigation, Actions; prefixes p; f; n; a; | Visible tabs with counts: All, Projects, Pages, Actions; prefixes p; n; a;. Backspace in an empty box returns to All. The prototype has no folders |
| No results | Never shown | States it, suggests a fix, and offers Ask Clueso AI (Tab) or Create a video about the query |
| Old names | — | "chats" finds Agent, "mcp" finds Integrations, "styles" finds Clueprints |
| Keyboard | ↑↓, Enter, Tab, Esc | Same, built as an ARIA combobox and listbox with a live result count |

The QA sweep now also opens search empty, with a query and with no results. It checks that the dialog backdrop covers the viewport (a `.top` class collision once shrank it) and that the search input stays pinned while results scroll.

Round 5 (17 Oct 2026), from a pass over the whole prototype:
- **Build status follows you.** While a video builds, the top bar shows "Building · 2 of 6" on every page (just "2/6" on phones), linking back to the project. The finish toast has an Open button and stays 6 s, pausing on hover. The project page then leads with "Your video is ready" and Share link, since sharing is the activation step.
- **Dialogs follow the WAI-ARIA dialog pattern.** `aria-modal` and a label are set, focus moves inside, Tab wraps, and Esc or a backdrop click returns focus to the button that opened it. The style drawer does the same.
- **Toasts are announced.** One persistent `aria-live` region carries every toast (WCAG 4.1.3).
- **Onboarding's Continue says why it is disabled.** This was a flaw the audit found in Clueso, and the prototype repeated it.
- **Projects search works.** It matches names, including language versions and spin-offs, bolds the match, and shows a no-results state with Clear and Search everything.
- **Fixes.** The collapsed sidebar's hover labels were hidden under the page (a side effect of the hover-pill isolation). Short windows let the sidebar scroll. The search placeholder shortens to "Search" on phones.
- **QA.** The sweep now covers the building, ready, no-match and empty-onboarding states. It skips controls that are reachable by scrolling. 0 issues at 375, 1024 (open and collapsed), 1440, 1920 and a 340 px-tall window.

Dark theme (17 Oct 2026), from Clueso's own `.dark` tokens on web.clueso.io:

| Prototype token | Light | Dark (Clueso token) |
|---|---|---|
| `--page` | grey-10, oklch 0.94 | grey-90, oklch 0.16 (bg-canvas) |
| `--main` | grey-5, 0.97 | grey-80, 0.24 (bg-surface) |
| `--surface` / `--raised` | 0.985 / white | 0.255 / 0.27 (surface + 2% and 4% white, elevated-1 and -2) |
| `--ink` | grey-80, 0.24 | grey-0, white (fg-text-strong) |
| `--muted` / `--faint` | 0.46 / 0.49 | 0.80 / 0.70 (Clueso: grey-30 0.88 and grey-40 0.60; see below) |
| `--hover` / `--active` | black 4% / 6% | white 6% / 8% (interaction hover-subtle and selected-subtle) |
| `--line` / `--ring` | black 8% / 5% | white 10% / 7% (stroke) |
| `--field` | black 4% | black 16% (depth-inset-1) |
| `--pink` (brand text) | deepened rgb(168,30,140) | pink-40, oklch 0.719 0.168 335.8 |
| `--pink-soft`, `--green-soft`, `--amber-soft` | 5-step tints | pink-90, green-90, yellow-90 |
| `--inv-bg` / `--inv-fg` | grey-80 / white | grey-5 / grey-80 (bg-inverted, fg-text-inverted) |

Deliberate deviations, all for WCAG AA contrast in dark:
- Clueso's weak text (grey-40, 0.60) measures 3.9:1 on its dark surface, so `--faint` is 0.70.
- `--muted` is 0.80 rather than grey-30 (0.88), so it stays visibly different from white body text.

Other rules:
- Pink buttons keep the deepened gradient in both themes so white text passes.
- Fills that carry white text or checkmarks use fixed `--pink-fill` and `--green-fill`.
- Hover and selected surfaces use `--raised`, not white.
- Toasts and tooltips use the inverted pair.
- Video thumbnails and the onboarding art panels look the same in both themes.

Switching: Clueso offers Light, Dark and System as three unlabeled icon tabs in the account menu. They have no accessible names, so screen readers announce them as unnamed tabs. The prototype keeps Clueso's icons (copied from its DOM) and the location, adds labels, makes the set a radio group with arrow keys, and repeats it in Settings › Profile. System follows `prefers-color-scheme`. The choice is saved in this browser.

QA: `runSweep({ theme: 'dark' })` sweeps the dark theme. 0 issues in both themes at 375, 1155 (open and collapsed) and 1920.

Improvements bar: drag it by the grip on its left (or focus the grip and use the arrow keys), or click the chevron to shrink it to a small "Improvements N" pill. Position and minimized state are saved in this browser. Double-click the grip to put it back in the corner. The list opens next to wherever the bar is.

Collapsed sidebar header, matched to web.clueso.io:
- The header row keeps its height when collapsed, so nav items don't jump down. Before, the logo and the toggle stacked.
- The expand button sits over the logo at opacity 0. Hovering the row cross-fades them (200 ms, cubic-bezier(0, 0, .2, 1)).
- The sidebar width animates 198 → 52 px over 350 ms with the same easing. The wordmark shrinks and fades as it does in Clueso.
- The toggle no longer re-renders the page, so focus stays on it. Its label switches between "Collapse sidebar" and "Expand sidebar".
- One deliberate difference: the button also appears on keyboard focus. In Clueso it is invisible to anyone who tabs to it.

## Projects and Clueso AI, checked against the live app (17 Oct 2026)

**Projects: what Clueso has → what the prototype does**

| Clueso (live) | Prototype | Why |
|---|---|---|
| Tabs: All, Deleted (kept 30 days) | All, Folders, Deleted (30 days, with a removal date and Restore) | Keeps Clueso's safety net |
| Sort menu with 8 options, plus sortable headers | Sortable Name, Length and Edited headers only, with `aria-sort` | One control, not two (Jakob's law) |
| 5 filter dropdowns (type, creator, tags, created, modified) | One Filter (type, edited) with removable chips and a count | Hick's law; Clueso's dropdowns clip New folder. Creator is dropped for one-person workspaces. Tags wait until tags exist |
| Row menu on hover only: open in new tab, edit title, tags, duplicate, copy link, pin, move, copy to workspace, delete | Row menu on hover and keyboard focus: copy link, rename, duplicate, pin, move, delete | Titles are real links, so new tab is the browser's. Copy to workspace is pointless with one workspace |
| Delete (to Deleted) | Delete with an Undo toast | Undo beats confirmation (NN/g) |
| Titles cut to about 30 characters | Full titles | Recognition |

**Clueso AI: live behavior → redesign**

| Clueso (live) | Prototype |
|---|---|
| Floating 378 px panel over the page (default) covers page controls | Over the page is still offered, but side by side is the default from 1100 px |
| Sidebar mode pushes New project, Help and the account menu off screen | Side by side narrows the page column. The top bar keeps every action |
| Full screen navigates to /home/chat and loses the page | Full width expands over the main area in place. Esc steps back to the previous view |
| View choice resets on reopen | Remembered in this browser |
| Same 3 chips everywhere | A context line ("On: Projects" or the video's name) and chips for that page |
| Chips start AI chats | Chips a button can do run directly, marked "No credits". Question chips fill the composer to edit |
| + menu: Attach files, Add Project, Add Clueprint | Same three. Attachments and the current video show as removable chips |
| Mode and model pickers in the composer | Quality (Best or Fast, with credits per reply). Mode stays in the build step |
| "Running low on AI credits" banner after the fact | "10–15 a reply · N left" before sending (observed: 13 credits for one reply) |
| Escape on a menu also closes the panel | Escape closes one layer at a time |
| Focus stays on the header button; no landmark | Focus moves to the composer. The panel is a labelled complementary region (a dialog when full width). Closing returns focus to the button, which shows `aria-expanded` and keeps its label |
| No history in the panel | Recent conversations, linking to their projects |
| Editing by chat (Enterprise) not mentioned | Stated once on project pages, with its plan |

Replies are out of scope. Sending shows your message, a "thinking" row with the cost, and a note that answers aren't part of this prototype.

QA: `runSweep` now opens the panel in all three views on five pages. 0 issues at 375, 1155 (light and dark, collapsed) and 1920.

### Clueso AI, element by element (second pass, 17 Oct 2026)

| Visible in Clueso | Decision | Why |
|---|---|---|
| View menu: Sidebar, Floating, Full screen, each with an icon and a check | **Adopted.** Same names and Clueso's own icons | Consistency with the product |
| Option descriptions only in hover tooltips ("Tall panel inset from the screen edge", "Compact floating window", "Open AI chat on the full page") | **Changed:** shown as a second line, rewritten to say what actually happens | Tooltips don't work on touch or keyboard. Don't hide essential information (NN/g) |
| Header button icon shows the current view | **Adopted** | Visibility of state |
| One hover highlight that slides between menu items (200 ms transform, 100 ms fade) | **Adopted for every menu** | Matches Clueso's sidebar and menus |
| Title is an input, disabled until a conversation exists | **Adopted.** After the first message it takes the first words; click to rename (Enter saves, Esc cancels) | Conversations become findable |
| Dashed 1 px, 5% line under the header | **Adopted** | Fidelity |
| Greeting and chips at the bottom, next to the composer; empty space above | **Adopted the bottom anchoring.** The top now shows "Pick up where you left off" | Proximity between starters and the input. The empty top becomes useful |
| Filled pink sparkle above the greeting | **Adopted** | Fidelity |
| "How can I help you today?" on every page | **Kept ours:** "How can I help with this video?" or the page name | Context |
| Chips as a row of short pills | **Adopted the pills.** Direct actions get an arrow and a one-line legend ("Opens directly, no credits") | Same look; tells actions from questions |
| "Running low on AI credits · Upgrade plan" banner | **Adopted, conditional.** Only under 150 credits (about one video), and it says the number | Show status when it changes a decision (Google PAIR) |
| + (Add): Attach files, Add Project, Add Clueprint | **Kept** | |
| "Director autonomy mode": Ask, Plan, Auto | **Kept** as Ask, Plan and Auto with Clueso's descriptions. Labelled "Check in" for screen readers, and synced with the build step's setting | It decides whether the agent spends credits without asking, so it belongs where you ask. No "Director" jargon |
| "Director model": 9 vendor models with no costs (6 during the audit); Sonnet 5.5 here but Opus 5.5 on Home | **Replaced** by Best or Fast, with credits per reply. Same control and default as Create | Match with the real world (Nielsen #2); one default everywhere |
| Send (pink, disabled until text) | **Kept** | |

Bug found while doing this: menus opened from the panel rendered underneath it (layer 40 against 45, and 95 for the phone sheet). Menus now sit on layer 100. The QA sweep now checks that every open menu is topmost, and opens the panel's four menus on every run.

## One Clueso AI (17 Oct 2026)

**What live Clueso does, checked end to end.** One agent (internally "Director") sits behind five doors with four names:

| Door | Name shown | What it is |
|---|---|---|
| Home prompt | (none) | Starts a chat |
| Header button | Clueso AI | The same chat in a panel. The button is hidden on Home and inside a chat |
| Chats (nav) | Chats | The list of those chats, with its own New chat |
| /home/chat/… | the chat's title | The panel in Full screen. No nav item is active |
| Agent (nav) | Agent | Not the chat at all: an Enterprise sales page for automations |

Chat titles and controls say "Director". Switching an open chat to Floating drops you on Home with two composers, Home's prompt and the chat's.

**The prototype before this pass was no better.** The Create prompt, the Clueso AI panel and the Agent page each had their own composer for the same assistant.

**The model now.** One assistant, one name, one place to talk.
- It is called **Clueso AI** everywhere. The words agent, Director and chat no longer compete in the interface.
- **The Clueso AI panel is the only place a conversation lives.** Sidebar, Floating and Full screen are sizes of it, never routes.
- **Every door opens that panel:**
  - **Create prompt:** sends the first message. The panel opens with a plan card showing cost, time and Options, plus Change brief and Build video. This replaces the separate "Ready to build" dialog. Nothing is built or charged until you press Build.
  - **Header button:** on every page, always in the same place.
  - **Nav "Clueso AI"** (was Agent): the list of conversations, with what each made, its status and the credits it used. It has no composer. New chat and every row open the panel without leaving the page.
  - **Project page:** "Made with Clueso AI: …" opens the conversation that made it.
- **Never two composers at once.** While the panel is open, Create's prompt is replaced by "You're in Clueso AI… Go to the panel". Closing the panel brings the prompt back.
- **Building happens in the conversation.** Build takes you to the project page. The thread shows "Building scene n of 6", then a card linking to what it made, and the list updates from Building to Done.
- **Enterprise "agents" are called Automations** (record for you, keep videos up to date). They are listed once on the Clueso AI page and where they act (Integrations).
- **`#/agent` redirects to `#/chats`.**

Basis:
- **Consistency (Nielsen #4):** the same thing gets the same name.
- **Dan Brown, objects and front doors:** a conversation is one object with one home, and you can enter from any page.
- **Jakob's law:** a persistent assistant button in a fixed place.
- **Cognitive load:** one composer at a time.

**QA.** The sweep now covers a plan awaiting approval (options open), a finished conversation on its project, and Create with the panel open. 0 issues at 375, 1280 (light and dark, collapsed) and 1920.

### Revised: three jobs, three places (17 Oct 2026, after review)

The first version put the panel everywhere, including on Create and on the Clueso AI page. There it was redundant: Create's prompt already *is* Clueso AI, and the Clueso AI page already shows conversations. Clueso hides its button in exactly those two places, and that was the better call. The revised model gives each surface one job:

| Surface | Its one job | What happens |
|---|---|---|
| **Create** | Start something new | The prompt is the only composer, with no AI button. Sending opens the conversation on the Clueso AI page, with the nav showing where you are (Clueso shows no active item) and the plan card focused |
| **Clueso AI page** (nav, was Agent) | Your conversations, in full | A list beside the open conversation. Reply, approve a plan (cost, options, Build), see what was built. No AI button and no "new chat" composer. "New video" and the empty state point to Create. "Change brief" takes the brief back to Create. On phones it shows the list or the conversation, with Back |
| **Clueso AI panel** | Help with what's on screen, while you work elsewhere | Only on Projects, a video, Analytics, Library, Integrations and Settings. It knows the page or video. Questions asked here are saved as conversations ("Asked on …"). Views: Sidebar or Floating, plus **Open in Clueso AI**, which takes the conversation to its page. It replaces Full screen, so no third mode pretends to be a page |

Rules that follow from the jobs:
- **Leaving closes the panel.** Going to Create or the Clueso AI page closes it. On the Clueso AI page, the conversation you had in the panel is already selected.
- **Separate memories.** The panel and the page each remember their own open conversation, so the panel never opens on something unrelated you were reading.
- **Where you are is always shown.** The nav highlights Clueso AI while you read a conversation.

So "where do I talk to the AI?" always has one answer: **start in Create, continue in Clueso AI, ask about what you're looking at in the panel.**

QA: the sweep covers a plan on the Clueso AI page, a finished conversation, the empty page, and a conversation in the panel. It runs panel views on the five pages that have one. 0 issues at 375, 1280 (light and dark, collapsed) and 1920.

### Model picker (17 Oct 2026, after review)

An earlier pass replaced Clueso's model menu with Best/Fast. That took away a choice people actually use (Nielsen #3, user control), so it is reverted. Now:

- **One control on every composer:** Create, the Clueso AI panel, the Clueso AI page and the plan card's Options. The pill shows the vendor mark and model name, as Clueso's does. Vendor marks are copied from Clueso's menu.
- **Clueso's nine models, grouped by vendor** so nine options scan as three chunks:
  - **Anthropic:** Opus 5.5, Sonnet 5.5
  - **OpenAI:** Astra 6, Sol 6.1, Luna 6, Terra 5.6
  - **Open models · hosted by Baseten:** Kimi K3, GLM 5.3, DeepSeek V4.1 Flash

  Each shows Clueso's own description.
- **Costs follow the model, using only Clueso's numbers.** The two models Clueso calls "fast, cost-efficient" (Luna 6, DeepSeek V4.1 Flash) are tagged Cost-efficient and estimated at about half: 75–125 credits a video and about 7 a reply. The others are estimated at 150–250 a video and about 13 a reply, from the observed 250 and 13. The Create cost, the plan card and the per-reply line all update when you switch.
- **One remembered default:** Sonnet 5.5, Clueso's current default, everywhere. Clueso itself shows Sonnet in chat and Opus on Home.

Bug fixed along the way: tall menus opened off screen. The model menu's top sat at -361 px on Create. Menus now open below if they fit, else above, else on the roomier side with a scrollable maximum height, and they're kept inside the screen horizontally. QA now flags any menu outside the viewport and opens Create's model menu and the Projects filter on every run. 0 issues at 375, 1280 (light and dark, collapsed) and 1920.

### Clueso AI page hierarchy (17 Oct 2026, after review)

Problems in the first layout, and what changed:

| Problem | Change | Why |
|---|---|---|
| A full row of plan information ("Included on Free… Automations on Enterprise") sat between the title and the content | Moved to a footnote under the list | Reference information shouldn't outrank the work (NN/g visual hierarchy) |
| Two buttons for the same thing: "New video" in the header and a pink "Start in Create" in the empty state | One button, New video, in the header. The empty state has a button only when there are no conversations at all | One primary action (Nielsen #8) |
| The page opened on an empty "Pick a conversation" card filling most of the screen | On wide screens the most relevant conversation opens automatically: the one that needs you, otherwise the most recent. Phones open on the list | The list–detail convention (Gmail, Slack) |
| "Needs your reply" was last, and green "Done" badges drew as much attention | A "Needs you" group with a count comes first, then "Recent". Only items that need action, or are building, get a coloured badge | Colour signals priority, not completion |
| No list header, count or search; the list floated while the detail was a card | Title with a count. The list is a framed column with search at the top, as in Clueso's Chats | Proximity and common region (Gestalt) |

QA: 0 issues at 375, 1280 (light and dark, collapsed) and 1920. The sweep now runs in the background on the page because it covers more states than a single 45-second tool call allows.

## Cross-check against live Clueso (17 Oct 2026)

Every page, menu and dialog in the prototype was compared with web.clueso.io on the same account (Free plan), plus the 92 screenshots from the audit. Each difference is one of four things:

- **Same:** matches live.
- **Improved:** the same feature, changed for a stated reason.
- **New:** not in Clueso, kept only because there is evidence for it.
- **Corrected now:** the prototype had drifted from live with no evidence, so it was put back.

### Corrected now (prototype had drifted with no evidence)

| Area | Live Clueso | Prototype before | Now |
|---|---|---|---|
| Nav | Clueprints and Brand kit are two top-level items | A "Library" group with Clip templates, Components and Media pages | Two top-level items, as live. Templates, components and media are managed in Clueso's editor, which the prototype doesn't cover |
| Nav label | Home | Create | Home |
| Help | Top bar, opens a widget: start a chat, knowledge base, feature request | Sidebar, with a "Keyboard shortcuts" item that has nowhere to go | Top bar. Knowledge base, Chat with support, Request a feature, and What's new (moved from the sidebar card) |
| Home start options | Record your screen, Upload videos, Upload slide decks, Translate | Record, Upload, Start from a Clueprint; Translate dropped as "needs an existing video" | Record, Upload videos or slides, Translate a video. Clueso's Translator takes an upload, so the old reason was wrong |
| New project menu | Start blank project, Record screen, Upload videos, Upload PPT/PDF | Blank last, plus a Clueprint item | Blank first, then record and upload, as live |
| Upload dialog | Drop zone, Google Drive, optional instructions, input language; always makes a video and an article | Four made-up "What should the video do?" presets and a guide on/off switch | Live's fields. It says you get a video and an article |
| Translate dialog | Input → Output, upload or "choose from an existing project", Customize translation rules | Existing project only; rules locked as Enterprise | Live's fields; rules open |
| Plan locks | On Free, only the embedded player and analytics are locked | Pronunciations, transcription keywords, translation glossary, clip templates, components and your own Clueprints locked | Only the player and analytics are locked |
| Clueprints | Workspace and Community tabs, search, New clueprint | Community grid only, with "Your own Clueprints: Enterprise" | Community and Workspace tabs, search, New Clueprint |
| Brand kit | Pull again from website, logo variants, Text / Backgrounds / Accent / Accent 2, title and body font, tone of voice, Save changes | Logo, 3 unnamed colors, one font line | Every live field |
| Video defaults | Auto-rewrite script, Auto-generate speech, Auto-add elements, Default voices, legacy color export | Reworded toggles, no default voices | Live names, descriptions and Default voices |
| View-only links | Domain, appearance (theme, colors, logo, header links, feedback, author), authentication | One "Edit appearance" button | Domain, appearance and authentication |
| Projects | All and Deleted tabs | Added a Folders tab | All and Deleted. New folder stays |
| Account menu | Name, email, Help Center, Profile Settings, Chat with Support, Sign out, theme | Email, theme, Profile, Settings, Sign out | Name and email, theme, Profile settings, Sign out. Help items live in Help, so they aren't repeated |
| Workspace switcher | The workspace list with the current one checked | Added "Workspace settings" and "Create workspace" | The list only |
| Dead code | — | A five-screen onboarding (welcome 1–3) that redirected away, plus its handlers and decision entries | Removed |

### Improved, with the reason (kept)

| Area | Live | Prototype | Basis |
|---|---|---|---|
| Nav items | `div`s with click handlers: no keyboard access, no links | Real links | WCAG 2.1.1 keyboard |
| Agent + Chats | Two items: Chats is the list, Agent is an Enterprise sales page | One "Clueso AI" item, the conversation list; automations named and listed there | Nielsen #4, one name per thing (see One Clueso AI) |
| MCP + Connections | MCP page; GitHub and Bitbucket under Settings › Connections | One Integrations page with the extension too | Things set up once, in one place |
| Settings | 11 sections under "Workspace settings", plus a separate Profile modal | 7 sections in 5 groups, profile included | Fewer places to look |
| Billing | Overview, Usage and AI Credits tabs | One Plan and usage page | Same numbers on one screen |
| Upgrade card | Two meters, "Get more out of Clueso" and Upgrade | One usage line linking to Plan and usage | Cognitive load |
| Getting-started checklist | 6 items, hidden in the sidebar | One next step on Home | Appcues 3 to 5 items; endowed progress |
| Promo banner, survey, footer links | Shown on every page | Not shown | Seven competing elements on first load (audit) |
| Onboarding | 5 screens: name twice, 13 roles, workspace, extension gate | 2 screens: one question, then what Clueso makes for it | Audit issues 1 to 6 |
| Projects | 5 filters, 8-option sort, hover-only row menu, flat language copies | One Filter, sortable headers, row menu on focus too, versions grouped | See Projects table above |
| Search, Clueso AI panel, model picker, sidebar collapse, dark theme | See their sections above | | |
| Analytics | "Not available on your current plan" | A labelled sample of the dashboard Clueso's help center describes | Show the value before the paywall |

### New, kept because there is evidence

| Element | Evidence |
|---|---|
| Project page (live opens straight into the editor) | One home per object (Dan Brown); it holds what Clueso already makes for a video: the guide, language versions, analytics |
| Build progress with an estimate and a status chip in the top bar | A 9 min 37 s build showed only elapsed time (audit issue 10); Nielsen #1 |
| Cost before sending, per model | A free user can't see what a model costs (audit issue 9); only Clueso's own numbers are used |
| Recording in the browser, no extension | Audit issue 6: the recommended path ended in an install. Needs engineering validation |
| Sample project in onboarding | Marked as a proposal; Clueso has no sample today |

QA after the cross-check: 0 issues at 1155 × 811 (light and dark) and 375 × 812. The sweep no longer visits the removed Library pages.

### One identity menu (17 Oct 2026, after review)

Live Clueso shows two identical blue initial squares: "UW" at the bottom of the sidebar (the workspace switcher) and "UA" in the top bar (the account menu). Same shape, same color, same size, different things. The prototype had copied this as "A" and "AR".

| Before | Now | Why |
|---|---|---|
| Workspace button (bottom left) and account avatar (top right), each with a menu | One button at the bottom of the sidebar: "Alex's workspace", with "Alex Rivera · Free plan" under it. Its menu shows the workspace, then you (name, email), theme, Profile settings and Sign out. No avatar in the top bar | One place to answer "who am I and where am I" (Linear, Notion and Slack do this). Fewer things in the top bar |
| Both avatars are blue squares | A workspace is always a square, a person always a circle, here and in Profile and Members | Gestalt similarity: things that look the same are read as the same thing (Nielsen #4) |

Checked at 1155 × 811 (open and collapsed, light and dark) and 375 × 812, where the menu opens from the drawer. QA sweep: 0 issues.

### Composer controls restored (17 Oct 2026, after review)

Rule: a live control is removed only if there is evidence for removing it.

| Live control | Earlier prototype | Now | Why |
|---|---|---|---|
| Record (Record screen, Choose recording) | Removed; a "Record your screen" card started a separate flow | Restored next to +, with Clueso's two items | No evidence for removing it, and the card can't attach a recording to the brief you're typing |
| Mode: Ask, Plan, Auto | Hidden until the plan card, and the first message always stopped at a plan, so Auto never applied | Restored on the composer with Clueso's descriptions. Ask and Plan stop at the plan card; Auto builds on send. The default stays Ask | Hiding it removed Auto, a real capability (Nielsen #7, flexibility for experts). The cost is still shown beside Send before anything runs |
| Brand kit, on by default | Off until you set one | Unchanged | Backed: Clueso built a kit from gmail.com and added "Use our brand kit" to the brief (audit issue 8) |

**Follow-up, same day:** Record is folded into the + menu, listed first: Record your screen, Attach files, Add a project, Add a Clueprint. This removal is backed. Both buttons add source material to the brief, "Choose recording" was "Attach files" for videos only, and "Record your screen" is also a full card right under the composer. Live's record icon (a dot in a ring) also reads as a radio button. Mode and model stay separate from +, because they control how Clueso works, not what you give it.

### Getting started: one line under the composer (17 Oct 2026, after review)

An earlier pass moved the Home card into the sidebar. That was the wrong call. The sidebar's bottom is the lowest-attention spot on the screen, and the remaining step that matters on Home, adding a brand, changes the next video you describe, so it belongs at the input.

| Before | Now | Why |
|---|---|---|
| A full-width "Next step" card below the start options, with its own Start button | Nothing while you have no video: the prompt is that step | The card described the page it sat on, and Start only focused the prompt: two primary buttons for one action (Nielsen #8) |
| — | After the first build, one line right under the composer: "2 of 4 done · Next: add your brand, so your videos look like yours." The composer's "Add your brand" pill stays in its normal style (an earlier pink outline was removed: pink marks Send, the primary action, and brand is optional) and is described by the line for screen readers | Proximity: the reminder sits next to the control it's about. No second button for the same action |
| — | When brand is done: "3 of 4 done · Next: share your video with a link. It uses about 1 of your 10 free minutes." with one Share button | Home has no other share control, so this one earns a button. The cost is stated before you commit |
| Building never marked "Make your first video" done | Starting a build marks it | Bug: progress could never pass 1 of 4 |
| Dismissing marked every step done | Dismissing hides the line; progress is kept | Honest state |

QA: 0 issues at 375 × 812 (dark) with the line showing. Checked: line hidden with no video, brand step, share step (opens Share), hidden at 4 of 4.

### Brand pill: a picker with Clueso's default (17 Oct 2026, after review)

| Before | Now | Why |
|---|---|---|
| "Add your brand" when no brand existed, "Acme brand ×" when one was on | The pill always names the brand the video will use: "Clueso default" or "Acme", with a menu like the model pill's | Visibility of system status (Nielsen #1): "no brand" is still a look, so name it. One pattern for every composer setting (Nielsen #4) |
| — | Menu with no brand: Clueso default (neutral colors and fonts, no logo), then Add your brand (pull from your website) | The way to add one stays one click away, without a separate button |
| — | Menu with a brand: Clueso default, Acme (from acme.io), Edit brand kit | Switching per video, as before, plus a way to edit |
| "Clueso's neutral style" in the plan card | "Clueso default" everywhere: pill, menu, plan card, Brand kit page | One name for one thing |

Unchanged: Clueso never builds a brand from an email domain (audit issue 8). QA: 0 issues.

### Brand, shown wherever it's used (17 Oct 2026, after review)

What live Clueso does (checked 17 Oct 2026):
- **Composer:** a toggle pill with the kit's logo. "Brand kit ×" when on, "Use brand kit" when off. No menu, no preview, and no word on what "off" means.
- **Brand kit page:** logo variants, four labelled colour tiles, title and body font, tone of voice, and a Preview card (logo, the font set large, the four colours with hex codes).
- **Agent chat:** the brand appears only as text appended to your brief ("Use our brand kit."). You never see which colours or logo it will use.

Live's preview is good, but it appears only on a settings page, not where the decision is made. The redesign keeps Clueso's visual language and shows it everywhere the brand matters:

| Where | Redesign | Why |
|---|---|---|
| Composer pill | A four-colour swatch of the active kit plus its name: "Clueso default" or "Acme" | Visibility of system status (Nielsen #1). "Off" is still a look, so it gets a name and a face |
| Pill menu | Each option shows a mini preview (logo, four colours, font). "Add your brand" or "Edit brand kit" sits below | Recognition over recall (Nielsen #6): you see what you're choosing |
| Plan card in Clueso AI | The Brand row shows the same preview and opens the same picker. Nothing is added to your brief | Fixes live's hidden "Use our brand kit." line (audit issue 8) |
| Brand kit page | Clueso's layout: logo tile, four colour tiles, font pickers, tone, Preview card. With no kit, it previews the Clueso default you'd be replacing | Consistency with the product (Jakob's law). The empty state teaches what a kit changes |

Colour tiles choose black or white text by WCAG contrast, so any brand colour stays readable. QA: 0 issues at 1155 × 811 and 375 × 812 (dark), with a brand set.

### Clueso AI panel: View menu fixed (17 Oct 2026, after review)

- **Bug:** the panel's view button did nothing. Its menu code called `.join()` on a string and threw, so Sidebar, Floating and the full-page option never appeared. The QA sweep missed it because it opened menus by calling them directly, not by clicking.
- **Name:** the third option is called **Full screen** again, as in Clueso. It still opens the conversation on the Clueso AI page, as before, and its description now says so. The behaviour has evidence behind it; the rename didn't.
- **QA:** `runMenuCheck()` in `qa.js` clicks every menu button on nine pages, with and without the panel, and reports any that open nothing or throw. Result: 0 issues.

### Edge-case pass (17 Oct 2026)

Eleven edge cases were found and fixed: not enough credits, Auto with too few credits, out of credits, no export minutes left, a second build while one runs (now queued), missing projects, unknown settings pages and addresses, every project deleted, corrupted saved values, and a dark-mode contrast miss in the brand preview. The full list, with before and after, is in `doc/BACKLOG.md`, which also lists the before/after doc updates still to make.

QA after the fixes: 0 issues at 1155 × 811 (light and dark) and 375 × 812; `runMenuCheck()` 0 issues at both sizes.

### High-severity review findings built (17 Oct 2026)

From `UX-REVIEW.md`, R1 to R4:

| # | Before | Now |
|---|---|---|
| R1 | A new user finished onboarding and landed on a workspace with projects, chats and "2 of 4 done" | The review bar has a **New user / Returning** switch, remembered in this browser. New user: no projects or conversations, the first-run strip and every empty state. Signing in with Google starts a new user. Returning: the seeded workspace |
| R2 | The nav item and the top-bar button were both "Clueso AI" but did different things | Nav item: **Chats** (Clueso's own name for the list, with a speech-bubble icon). Top-bar button: **Clueso AI** (the assistant). Both names are live's |
| R3 | Floating was a full-height column over the page, covering the project page's Share and Open editor | Floating is a 360 × up to 560 px window at the bottom right, below the page toolbar. Drag it by its header (kept on screen, remembered); double-click to reset. It opens scrolled to the starters next to the composer and keeps your place when the page updates |
| R4 | No way to stop a build | **Cancel build** on the project page and in the conversation, with a confirmation that says how many credits are already used. **Remove from queue** for a queued build, at no cost. A cancelled build shows **Build again**. The credits charged on cancel are an assumption; Clueso's real policy needs confirming |

Also fixed while testing: with no conversations, Chats said "No conversations match “undefined”"; it now says "No conversations yet". The QA overlap check now ignores content scrolled out of view inside a scroll area, which had produced a false positive in the shorter Floating window.

QA: 0 issues at 1155 × 811 (light and dark) and 375 × 812, in both scenarios; `runMenuCheck()` 0 issues.

### Chats redesign (17 Oct 2026, after review)

Live Clueso's Chats (checked 17 Oct 2026): a table of Name, Date created, Last updated and Creator; Created and Modified filters; a creator filter; search; New chat; a row menu with Open chat and Delete. Inside a chat it has numbered choices, "Show more" for long briefs, "Ran n steps", explicit failures, caveats, thumbs and copy, and per-message credits.

**Scenarios designed for:** a question waiting, a plan waiting, a build running, a build failed, a video done, finding an old chat, a new user with none, and 40+ chats.

| Part | Design | Kept / improved / new |
|---|---|---|
| List rows | Two lines: the title with its time ("8m", "Yesterday"), then whatever helps you choose. A question shows the question itself, a plan its cost, a build its scene, a failure where it stopped, a finished chat "▷ video title". A badge appears only for Needs reply, Plan or Failed | Improved (live shows name and dates) |
| Groups | Needs you · In progress · Today · Yesterday · Earlier | New; scales to many chats with what needs you pinned |
| Search | Unchanged | Kept |
| Sort | One menu: Last activity or Date created | Kept (live's Created and Modified), as one control. Creator filter left out for a one-person workspace, as on Projects |
| Row menu | Rename, Delete with Undo; on hover, focus, and always on touch | Delete kept; Rename added |
| Plan footer | Removed from the list; now in the empty state | Removed: noise for returning users |
| Thread header | Title (rename in place); one line of status · where it started · when · credits; ⋯ menu | Improved |
| Question | Clueso's numbered choices plus "Something else…". Picking one charges a reply and leads to a plan | Kept from live |
| Plan | Cost, time, options, Build; Build disabled when credits are short | Kept |
| Building | Scene n of 6, time left, meter, "you can leave", Open project, Cancel build; you can keep chatting | Improved |
| Failed | Which scene failed and why, what's kept and what it cost, then Continue from that scene (with its estimate) or Start over (with its estimate) | New (live only reports it) |
| Done | Result card (Open video, Share), "check before sharing" checklist, thumbs and copy with the credits, then follow-ups: shorten, translate, make the guide | Improved |
| Long brief | Collapsed to 3 lines with Show more | Kept from live |
| Agent steps | "Ran n steps", collapsed | Kept from live |
| New chat | A blank thread here with Home's composer; still one composer on screen | Kept from live (restored) |
| Empty | One centered state: what Chats is, what Free includes, New chat. No empty list column | Improved |

Bugs found while building: a sent New chat didn't open (the page didn't re-render on the same route); a build didn't refresh the chat's time; a missing timestamp showed "NaN". All fixed.

QA: `runSweep` now opens every conversation state (question, plan, failed, two done, polished, new chat, building). 0 issues at 1155 × 811 and 375 × 812, light and dark; `runMenuCheck()` 0 issues. Truncated rows carry the full text as a tooltip and are marked intentional for the clipping check.

Assumptions to confirm with Clueso: what's charged when a build fails or is continued (the prototype prorates by scene), and the follow-up suggestions.

**Revision, same day (after review): status dots instead of groups**

| Before | Now | Why |
|---|---|---|
| Group headings: Needs you, In progress, Today, Yesterday, Earlier | One list, newest activity first. The title reads "6 conversations · 2 need you" | The headings repeated what each row already said |
| Text badges: Needs reply, Plan, Failed | A 6 px dot at the right edge, after the time: yellow needs you, blue a result you haven't opened (clears when opened), grey pulsing while running or queued, red failed. No dot otherwise, and no reserved space | Subtle, scannable down one edge (as in Slack, Linear, Gmail). Never colour alone (WCAG 1.4.1): line 2 says the same in words, and each dot has a name for screen readers and on hover. Each dot is at least 3:1 against the row (WCAG 1.4.11). The pulse stops under reduced motion |
| Row menu took its own 24 px column | It takes no space: it replaces the time and dot on hover or keyboard focus; on touch it stays visible | No dead space at the right either |

Also fixed: on phones the Translate dialog with rules open kept two columns and ran 200 px off screen; it now stacks. QA: 0 issues at 1155 × 811 (light and dark) and 375 × 812; `runMenuCheck()` 0 issues.

### Chats filters (17 Oct 2026, after review)

Live Clueso (checked 17 Oct 2026): **Created** and **Modified** dropdowns, each with All time, Today, Yesterday, Last 7, 30 or 90 days, and Custom; and a **creator** dropdown that is preset to the signed-in user.

| Live problem | Redesign |
|---|---|
| No way to filter by status, although "what needs me?" and "what failed?" are why people open Chats | **Status** first: All, Needs you, Running, Failed, Finished, each with its count |
| Two date filters with 14 options for one question, "when?" | **Date**: one list of Clueso's own options with a **Last active / Created** switch above it. Custom range shows two date fields in the menu |
| The creator filter defaults to you without saying so, hiding teammates' chats; on a one-person workspace it does nothing | **Created by** only when the workspace has more than one member, defaulting to **Anyone** (hidden on this Free workspace) |
| No summary of what's applied, no quick clear | One **Filter** button with a count, next to search (the Projects pattern); removable chips ("Needs you", "Active: since 14 Oct") with Clear all; a no-results message that names the filters |
| — | "2 need you" in the page title is a shortcut that applies the Needs you filter |

The menu stays open while you pick, so you can combine Status and Date. QA: 0 issues at 1155 wide (light and dark) and 375 × 812; `runMenuCheck()` 0 issues.

**Sort moved next to Filter (after review):** sort was in the page toolbar while Filter sat by the search box, though both act on the list. It's now a 28 px icon button between search and Filter, highlighted when not on the default order, named "Sort: Last activity" for screen readers and on hover. Focus returns to it after choosing. The toolbar keeps only New chat. Basis: Gestalt proximity (controls that act on the same thing sit together).

**Count line removed (after review):** "6 conversations · 3 need you" left the Chats title. The total supports no decision, and "need you" repeated the row dots and the Filter's Status counts, behind a link that didn't look clickable. Its one useful job, saying something needs you, moved to a 6 px dot on the **Chats** item in the sidebar: yellow when something needs you, red when something failed and nothing needs you. It's visible from every page and on the collapsed sidebar, and is named for screen readers ("Chats, 2 need you").

### Chats: Browse and Focus (17 Oct 2026, after review)

Live Clueso opens a chat across the whole content area: a back arrow, the conversation, and a **Projects** panel on the right listing what the chat made, each with Open and a copy-link button.

| View | What it is | How to get there |
|---|---|---|
| **Browse** (default) | List beside the conversation, for triage across chats | The default; the list button or Escape from Focus |
| **Focus** (Clueso's view) | One conversation fills the area. Messages and the composer stay at a readable 720 px, centred. A **Made in this chat** panel lists everything the chat produced (for example all three videos from the onboarding deck), each with Open and Copy link, toggled from the header and shown only when the chat made something | The expand button in the conversation header, or double-click a row. Back arrow, the list button or Escape returns |

Both the view and the panel are remembered in this browser. Below 1100 px the panel and its toggle step aside; phones show the list or one chat, as before.

Why not copy live outright: with no list, moving from one chat that needs you to the next means going back, scanning and opening again. Browse stays the default; Focus gives live's full-width reading when one chat deserves it.

QA: the sweep now includes Focus for four chats, with and without the panel. 0 issues at 1155 (light and dark), 1000 × 760 and 375 × 812; `runMenuCheck()` 0 issues.

**Focus is one surface (after review):** in Focus the conversation was a card inside the main area, leaving the page's 20 to 32 px padding plus a second border around it. It now fills the main area edge to edge, as in Clueso, and "Made in this chat" is a column separated by a 1 px divider instead of a second card.

**Chat composer checked against live (after review):** live's chat composer is + · Record · Ask · model, with no brand control; brand is only on Home, where a video starts. The prototype keeps brand out of replies and in the plan card's Brand row (same picker and preview). The gap was Record: it's now the first item in the + menu of the Chats composer and the Clueso AI panel, as on Home.

**Brand on the chat composer (after review):** live's chat composer has no brand, but anything a chat builds uses one, so the Chats and panel composers now end with the same brand picker as Home (+ · Ask · model · brand · Send). The plan card's Options panel, which repeated model, check-in and brand right above that composer, is replaced by one line: "Uses Sonnet 5.5 · Ask · Clueso default — change these in the box below". One control per setting. QA: 0 issues at 1155 (light and dark) and 375 × 812.

## Editor (17 Oct 2026, after review)

**Live Clueso's editor (checked 17 Oct 2026):**
- **Top bar:** a project menu behind the logo, Video / Article, a centre banner "Click on 'Generate Speech' to update the voiceover" with its own button, six icon buttons (avatar, help, comments, translate, Clueso AI) and Share.
- **Left rail:** 11 unlabeled icons that mix canvas modes (Select, Hand), panels (Voiceover script, Media, Effects, Animation, Template, Transition, Captions) and insert actions (Text, Shapes).
- **Script:** 20+ clips with "CLIP NAME", a voice per clip, blue text and "Sync Point" chips; AI Rewrite and a second Generate speech.
- **Canvas:** 194 × 110 px, about 3% of the screen.
- **Timeline:** collapsed.
- **Controls with no accessible name:** about 60.

**Jobs, in order of frequency:** watch what Clueso made; fix the words in a scene and hear the new voice; fix what's on screen in a scene; change something across the video; ask Clueso AI for a change; share, or switch to the guide. Detailed timeline work is the minority case.

**Redesign: one idea, the scene.** Open it from a project's **Open editor** (`#/edit/p1`).

| Part | Design | Why |
|---|---|---|
| Canvas | The largest element, sized to the space (727 × 409 px at 1155 × 811). Select / Hand, aspect ratio and zoom sit above it; labelled playback below, with "Scene 4 of 6 · Track progress" | Hierarchy follows importance |
| Scene strip | Numbered thumbnails with names and durations, always visible; the current scene is marked; a dot marks a scene whose voice is out of date. Arrow keys move between scenes | You always know where you are; Clueso's script, canvas and timeline weren't linked |
| Script | Follows the selected scene (and focusing a scene's text selects it). Each scene says its state: "Voice out of date · Update voice" or "Voice matches the script". Editing marks it out of date and saves ("Saving…", then "Saved") | Replaces unexplained blue text and Sync Point chips |
| Updating the voice | One summary at the strip: "3 scenes need a new voice · Update all", plus per-scene Update voice | Replaces the banner that repeated Generate speech |
| Tools | All 11 of Clueso's tools, each labelled, grouped as Content (Script, Captions), Add (Media, Text, Elements, Animation, Templates) and Polish (Effects, Transitions), each panel scoped to the selected scene ("Adds to scene 4") | Labels and grouping cut learning time; modes moved to the canvas |
| Detailed timeline | Video, Voice (out-of-date blocks marked), Captions and Music tracks with a playhead; clicking a block selects its scene | Kept from Clueso, one click away |
| Top bar | Two cards, as live: back · the title (opens Clueso's project menu: Back to projects, Duplicate, Move to folder, Save, View original media, Keyboard shortcuts, Editor preferences, Version history, Delete) · "Saved" · Video \| Guide; then who's here · Help · Comments · Translate this video · Clueso AI · Share | Live's controls and order; the menu moves from the logo to the title, where people look for it, and the icons get names |
| Clueso AI | The app's panel; it knows the scene ("On: Scene 4: Track progress") and the canvas makes room | One assistant, aware of context |
| Guide | The same scenes as written steps; Make the guide when there isn't one yet | Live's "Article", named as elsewhere in the prototype |

Scope: a working mock with scene data. Selection, linking, script states, voice updates, playback, the timeline, every panel and Clueso AI context work; placing media or effects on the canvas doesn't.

QA: the sweep and `runMenuCheck()` include the editor. 0 issues at 1155 × 811 (light and dark) and 375 × 812. On phones the tool rail and the scene strip scroll sideways; the overflow check now ignores content inside a horizontal scroller that itself fits on screen.

**Cross-checked against live (17 Oct 2026, after review).** The first version looked like a different product and had dropped controls live has. Now:

| | What changed | Why |
|---|---|---|
| Adopted from live | Floating rounded cards on a grey ground, dark selected tool, compact 28 px controls, live's grey and blue badges | It should look like Clueso |
| Adopted from live | Playback: skip to start, previous, play, next, skip to end, time, 1x, Loop, High res. Strip: Split at the playhead, Add a scene, Undo, Redo (⌘Z, ⇧⌘Z) | Live has them; removing them had no evidence |
| Adopted from live | A voice per scene (picker with each voice described, "Use … for every scene", V4 badge), Add pause, Search script | Live's per-clip voice, Sync Point and script search |
| Adopted from live | Media tabs and filters (sources, types, ratio), "Photos and videos provided by Pexels"; Captions and Transitions with their tabs; the guide's formatting toolbar | Live's panels |
| Kept different | Canvas first, the scene strip, one "Update all" instead of the banner, labelled and grouped tools, timeline on demand, no banner | Each backed above (hierarchy, Nielsen #1, #2, #8, NN/g labels) |
| Kept different | "Sync Point" is "Add pause", with Clueso's name in the tooltip | Says what it does (Nielsen #2) |
| Adopted from live (18 Oct, after review) | "Article", live's name for the written version, replaces "Guide" in the editor | Keep live's names |

QA after the cross-check: 0 issues at 1155 × 811 (light and dark) and 375 × 812 (light and dark); `runMenuCheck()` 0. On phones the canvas tools and playback wrap instead of widening the page.

**Narrow editor (18 Oct 2026, after review).** With the Script panel and the Clueso AI sidebar both open at 1155 px, the canvas column was 343 px: the time wrapped onto three lines, the scene label and zoom were cut off, and Share stuck out of its card. Now:
- The playbar and canvas tools follow the column's width, not the window's (container queries). Below 640 px the scene label (already marked in the strip) and "(1920×1080)" go; below 480 px the time, speed, Loop and High res move to a second row under the transport controls.
- Between 900 and 1260 px, a tool panel and the Clueso AI sidebar don't open side by side: opening one closes the other, so the canvas never drops below about 440 px (it was 108 px at 920). Floating view is unaffected. Canva and Figma swap side panels the same way.
- The actions card in the top bar never shrinks. In a narrow top bar the title truncates, "Saved" keeps its tick, Video | Guide drop their icons, and Clueso AI shows its icon (its panel is open beside it, named).
- The Clueso AI panel's "Pick up where you left off" showed "undefined" for chats added by a scenario switch; it now works out the time itself.

QA: no overflow at 1440, 1280, 1155, 1024 and 920 with both panels open; sweep 0 at 1155 × 811 and 375 × 812; `runMenuCheck()` 0.

**Back to live's design (18 Oct 2026, after review).** Review: "looks too much different from the live"; the rail's categories and names weren't needed up front. The editor now uses live's layout and visual design, and keeps only the improvements that change what people can do:

| Part | Now (as live) | Kept from the redesign, and why |
|---|---|---|
| Rail | Icons only, live's order and names: Select, Hand tool, Voiceover script, Media, Text, Shapes, Effects, Animation, Template, Transition, Captions. Names on hover and focus | Accessible names on every icon (WCAG 4.1.2) |
| Top bar | Logo opens the project menu; title; cloud for saved; Video \| Article; avatar, Help, Comments, Translate, Clueso AI (icon), Share | Clueso AI knows the scene |
| Script | "Voiceover script": number and name chip, voice chip with V4, sync (Add pause) button; footer with more, add, AI Rewrite, voice settings, Generate speech | A scene shows a line only when its voice is out of date; Generate speech shows the count; no duplicate banner |
| Canvas | "Original (1920×1080)" on the canvas, zoom at the bottom right | The canvas takes the free space |
| Bottom | Full-width panel: live's playback bar (skip, previous, play, next, skip, time, 1x, Loop, High res, Split, Add, Undo, Redo) over the timeline | The track is the scenes (blue headers with names, thumbnails, durations, an out-of-date dot); the detailed tracks are one click away |

Dropped: the rail labels and Content / Add / Polish groups, the "Scene 4 of 6" line, "Saved" in words, the panel's intro sentence, "Voice matches the script" on every scene, the separate canvas toolbar.

## Editor flows: what every control does (18 Oct 2026)

Checked in live's editor first (menus, panels and tools opened and closed). "As live" means the same options; changes have a reason.

**Top bar**

| Control | Flow |
|---|---|
| Logo ▾ | Project menu, as live: Back to Home · Duplicate project (toast with Open copy) · Move to folder (dialog: folders, Create folder, Cancel, Move here) · Save · View original media (dialog with the original recording player) · Keyboard shortcuts (dialog, tabs Playback / Tools / Editing / Comments / Navigation) · Editor preferences (dialog of switches, saved on this device) · Version history (right panel) · Delete project (confirm, then Deleted with Undo) |
| Title | Click to rename in place. Enter or leaving saves; Esc cancels; an empty name keeps the old one |
| Cloud | "All changes saved · just now", with a link to Version history. Shows "Saving…" while a change saves |
| Video \| Article | Switches view. In Article the rail becomes the formatting toolbar and the timeline hides, as live |
| Avatar | Workspace, email, Help center, Chat with support, Sign out (live's menu) |
| Help | Knowledge base, Chat with support, Request a feature, What's new |
| Comments | Free plan: "Unlock video comments" with what they do and See Business plan (live shows the same upgrade) |
| Translate | The translate dialog (live: Magic translate) |
| Clueso AI | Opens the panel. In Article: "How would you like to improve this article?" with live's three areas, and "Ask AI to improve your article" |
| Share | The share dialog |

**Rail (Video)**

| Control | Flow |
|---|---|
| Select (V) | Click an element to select it (blue box and handles); drag to move; arrows nudge (⇧ by 4); ⌫ deletes with Undo; Esc deselects |
| Hand tool (H) | Drag the canvas to move around; double-click resets |
| Text (T) | A tool, as live: the cursor becomes a crosshair; click the canvas to add a text box, already selected for typing; back to Select after |
| Shapes (R) | A tool with live's shapes behind the corner: Rectangle, Arrow, Ellipse, Polygon, Line, Star (with live's keys). Click the canvas to add one |
| Voiceover script | Panel: search (highlights matches), Find and replace (Replace, Replace all, with Undo); per scene: go to scene, voice menu, scene actions (AI rewrite, Generate speech, Duplicate scene, Delete scene with Undo); footer: More (Download / Copy transcript), Insert (Add a pause, at the cursor), AI Rewrite (This scene / Every scene), Prompt hub (base prompt), Generate speech |
| Media | Tabs In this project / Saved in workspace (empty state) / Stock; filters for source, type and ratio; See more; music sets the background track; a background applies to the current scene (with Undo); Pexels credit |
| Effects | Blur, Callout, Spotlight, Zoom: toggle on the current scene, shown on the canvas and tagged |
| Animation | Library / Recents; adds an animation element to the scene; New animation with Clueso AI opens the panel with the request started |
| Template | Templates (default intro and outro, Find a template), Components (add an element), Saved, Library (add as a scene, or pick as default); Save current clip as template (dialog) |
| Transition | Live's nine; applies between this scene and the next, marked on the timeline; select again to remove |
| Captions | Style / Library (live's eight styles; choosing one turns captions on), Content (edit each scene's line), Saved; Download .srt / .vtt / .txt; Translate; Visibility |

**Canvas and timeline**

| Control | Flow |
|---|---|
| Original (1920×1080) ▾ | Live's seven sizes; the canvas changes shape |
| Zoom ▾ | Fit, 50%, 100%, 200%; use the Hand tool to move around |
| Playback | Skip to start, previous, play / pause (Space), next, skip to end; time |
| 1x | Live's speeds, 0.5x to 3x; playback follows |
| Loop · High res | Toggles |
| Split (X) · Add · Undo · Redo | Edit the scenes; every change can be undone |
| Detailed timeline · Skimming (S) · Full-screen preview · Timeline settings · Collapse | Live's right-hand controls: the detailed tracks; hover a scene to preview it; a full-screen preview (Esc to exit); Click to seek, Skimming, Show clip frames; hide the track |
| Scene clips | Select a scene; arrow keys move between them |

**Article**

| Control | Flow |
|---|---|
| Formatting rail | Live's 15: Block type (Heading 1, Heading 2, Paragraph), Bold, Italic, Underline, Strikethrough, Link (address field), Text alignment, Numbered list, Bullet list, Horizontal rule, Code block, Blockquote, Add image (a frame from any scene), Undo, Redo |
| Article | One editable document: title, a heading, text and screenshot per scene; edits are kept when you switch views |
| Screenshot | Replace screenshot: a frame from any scene, or upload |
| Make the article | When there's none yet, writes it from the scenes |

**Changed from live, with the reason:** AI Rewrite asks what to rewrite (this scene or every scene) and can be undone. In live it rewrites the whole transcript at once with no undo, which happened on the test project during this check (Nielsen #3, user control). Deleting a scene, an element or the project offers Undo for the same reason.

## Editor: second check against live, and one size scale (18 Oct 2026)

**Built because live has it:**
- **Timeline ruler and playhead.** Seconds along the top of the track, a playhead with the time, clips sized by length; click the ruler or track to seek (live's "Click to seek").
- **Live's timecode,** minutes, seconds and frames: `00:14:00f / 00:57:00f`.
- **Inspector** for a selected element (live's "Inspector expanded" preference): X and Y, text size, colour and bold, shape colour and fill, Duplicate, Delete. It collapses to its header.
- **"/" commands,** which live's placeholder promises ("press / for commands"). In the script: Add a pause, AI rewrite this scene, Generate speech, Change voice. In the article: Heading 1, Heading 2, Bullet list, Numbered list, Quote, Code block, Image from a scene.
- **Live's other Editor preferences:** Inspector expanded; "When a left panel opens": Keep canvas in place (the panel opens over the canvas) or Make room for the canvas; Full-height script (the panel runs down beside the timeline).

**One scale, measured from live** (1440 × 900):

| | Live | Prototype before | Now |
|---|---|---|---|
| Page margin, gap between cards | 16, 8 | 8, 8 | 16, 8 |
| Card radius, border | 6, none | 10, 1 px ring | 6, none |
| Control height, radius | 28, 4 | 22–32, 4–10 | 28, 4 |
| Chip height (script, canvas, tabs, filters) | 24 | 24–26 | 24 |
| Top bar, rail | 40 high, 40 wide | 44, 44 | 40, 40 |
| Text | 12 UI, 14 titles and script | 9–14 and 21 | 10 labels, 11 meta, 12 UI, 14 titles and content |
| Side panels | left 387, right 320 | left 340, right 368 | both 360, 16 from the edges, 8 from the canvas |

An audit script measured every control, card and text node in each panel, the inspector, version history, the detailed timeline and the Article view. Nothing is now off the scale. The exceptions are on the canvas, which scales with the video, and the article's headings.

Not adopted: live's banner repeating Generate speech (decision R-ED3).

## Editor: side panels on every screen size (18 Oct 2026)

**Live, resized with the Voiceover script and Clueso AI open (no clicks):** both panels keep full width at every size. At 1180 px the top bar overlaps the script panel and the canvas is about 350 px. At 1024 px the AI panel runs off the right edge. At 900 px the canvas is about 80 px. At 768 px the canvas is gone.

**Rules here.** A panel you opened is never closed by opening another, and no panel covers the top bar or the canvas:

| Width | Left panel + right dock (Clueso AI or Version history) |
|---|---|
| 1280 and up | Both docked at 360 px |
| 1016–1279 | Both docked at 300 px; the canvas keeps at least 304 px (388 at 1100) |
| 901–1015 | Left and right share one 320 px column with two tabs ("Voiceover script" / "Clueso AI"); the panel opened last is in front. One panel alone docks on its own side. The canvas stays 477–591 px |
| 900 and below | Clueso AI and Version history open as a full-screen sheet with their close button; the rest stacks |

- **Floating Clueso AI** opens over the top right of the canvas and stops above the zoom control and the timeline. It's still draggable. Below 1016 px it docks like the sidebar, and the view menu is hidden there because it would have no effect.
- **Inspector** reserves 228 px beside the canvas instead of covering it. When the canvas column is under 720 px, it becomes a strip under the canvas. This also fixes a sideways page scroll on phones.
- **Keep canvas in place:** the panel opens over the canvas by design, and the canvas-size control moves just right of it.
- **Playback bar** wraps between groups (transport, timing, editing, view), never inside one.

**Checked:** `qa-panels.js` opens 12 combinations at 1440, 1280, 1180, 1100, 1016, 1015, 960, 901, 768 and 390 px. The combinations are: script, media or captions with AI; script with Floating AI; script with version history; AI alone; the inspector, with and without AI; Keep canvas in place; Full-height script; and Article with AI. At every width it reports no control covered or clipped and no sideways scroll. The QA sweep reports 0 at 1155 × 811 (light and dark) and 375 × 812, and `runMenuCheck()` reports 0.

## Editor script: back to live's look (18 Oct 2026, after review)

Review: "in the live this UI is in bluish text… why it's made grayish"; the build looked opposite to live. Checked in live's page code (read-only): the script text is ink (`oklch(.24 0 0)`), the same as here. Only words added since the voice was generated are blue (`<ins>`, `oklch(.546 .215 263)`), and sync points are light-blue chips with a frame.

| Was | Now (as live) | Why |
|---|---|---|
| "Voice out of date · Generate" line on each scene, amber dots on cards and timeline, a count on Generate speech | New words in blue, as live; live's top banner, reworded to explain the blue: "Blue text needs new speech · Generate speech" | Live's blue shows exactly which words changed. Three extra signals were noise. The banner keeps live's one global prompt and fixes its missing explanation |
| `[pause 0.5s]` typed into the text | Pause and Sync Point chips in the text (click: change the pause length, or remove) | Live's chips |
| Boxed cards, black outline on the current one | No boxes, dashed dividers, the current scene shaded | Live |
| Scene name as a button | Number, then an editable name ("CLIP NAME" in live) | Live |
| Scene menu always visible | On hover, keyboard focus and the current scene (always on touch screens) | Live |
| Sliders icon for find and replace, gear for the prompt hub | Replace icon, sliders icon | Live's icons |
| Generate speech without an icon | With a waveform icon | Live |
| Effect labels drawn on the video | Removed; the canvas is the preview | The output has no labels |
| Clueso AI in the editor listed unrelated chats | Chat history and New chat in the header, as live | Live; closes R7 |

Changing a scene's voice makes its whole text blue, since none of it is in the new voice yet. Generate speech clears the blue, and Undo brings it back.

## Work survives a reload (18 Oct 2026)

A reload used to wipe the session: a project built from a chat was lost twice in review. Projects, chats, Deleted, folders, credits, a build in progress, the Chats filters and the editor (scenes, panels, article) are now kept in the tab's sessionStorage and restored on reload. A build carries on from its step without charging again. A new tab, or switching scenario in the review bar, starts fresh, so a demo can still be reset.

## One type and size scale across the app (18 Oct 2026)

Measured in live Clueso (Home, Projects, Agent, the editor) with computed styles at 1024 px. Live's interface text (nav, buttons, labels, dates) is 12 px; row names, card titles, messages and the script are 14 px; badges are about 11 px; headings are 16, 18, 20 or 24 px. Controls are 28 px (24 and 32 for small and large) with 4 px corners, cards have 8 px corners, and the main surface sits 8 px from the sidebar and the window edges.

The prototype had mixed 10, 11, 12, 13 and 17 px text. Now:
- Body and interface text is 12 px; the 13 px used in 66 places is gone.
- Titles in rows and cards, chat messages and question options are 14 px.
- Badges and durations are 11 px.
- Table sort headers are 24 px controls; the chat panels have 8 px corners.
- The main surface is 8 px from the sidebar.

An audit of 10 pages finds no text or control off the scale. The exceptions are thumbnails, the brand preview and the wordmark, which follow their content. QA: 0 issues at 1155 (light and dark), 1024 and 375 px; `runMenuCheck()` 0.

## Editor: pixel pass (18 Oct 2026)

`qa-pixel.js` checks 11 editor states for: boxes on fractional pixels, items in a row off a shared centre line, icons off-centre in their buttons, mixed icon sizes, left edges inside panels, text cut off without an ellipsis, and text contrast (with a probe confirming the contrast check catches a 1.76:1 sample).

**Found and fixed:**
- **Half-pixel edges.** 47–91 boxes per state sat on fractional pixels: widths came from text (title 304.09 px, Video \| Article 108.3 px), and default line heights were fractional (16.8 px). Each text size now has a whole-pixel line height (12/16, 14/20, 10–11/14). After each render, text-sized controls round up to whole pixels, the two tile columns and 16:9 thumbnails snap to whole pixels, and timeline clips sit on whole-pixel boundaries. What's left is the other session's scene-name chips (their width follows the text as you type) and the centred banner.
- **Icon sizes:** icon-only buttons use 16 px icons, text buttons 14 px.
- **Placeholder contrast** measured 3.88:1 light and 3.78:1 dark, under the 4.5:1 WCAG asks for; now 6.0–9.3:1.
- **Script footer:** at 300 px, Generate speech wrapped onto its own line. AI Rewrite now shows as its icon in panels under 340 px, with its name on hover and for screen readers.
- **Top bar:** the Generate speech banner couldn't shrink and clipped Article at 960 px with Clueso AI docked. It now gives way first and hides under 640 px of top bar; Generate speech stays in the script footer.

Rows share a centre line, icons sit centred in their buttons, and no text is cut off without an ellipsis, in light and dark.

## Pixel audit (18 Oct 2026)

An audit script measured every element on 11 pages for half-pixel edges, line heights, icon sizes, greys and spacing off the grid.

| Found | Fix | After |
|---|---|---|
| Text line heights of 1.4 × size (12 px → 16.8 px) put elements below on half pixels, so 1 px borders and rings blurred (22 editor buttons, Clueprint cards, page buttons). `font:` shorthands without a line height fell back to "normal" (18 px → 22.68 px) | Whole-pixel line heights on a 4 px rhythm: 10–12 → 16, 14 → 20, 16–18 → 24, 20 → 28, 24 → 32; aspect-ratio thumbnails round down to a whole pixel | No fractional line heights; one element left on a half pixel (an inline text link with no border) |
| Icons in 10 sizes (10–20 px) | 12 (chevrons, inline), 14 (in chips), 16 (default), 20 (empty states) | 12, 14, 16 |
| Two secondary greys almost alike (L 0.46 and 0.49) | One, 0.46 (passes 4.5:1 on every surface). Dark mode keeps its two distinct greys | One |
| Off-grid spacing: badges (1 px padding, 3 px gap), keyboard hints (1 / 5 px), clip names (3 px), a chat button (7 px), the canvas size chip (5 px gap) | 18 px badges with 6 px padding and 4 px gap; 2 / 6 px; 2 px; 8 px; 4 px | On the 2 / 4 / 8 grid (the brand swatch cluster keeps its 1 px hairlines) |

Icons and labels were already centred within 1 px in every button. Live itself sits on half pixels (24 of 25 buttons on its Projects page), so this is crisper than live. QA after the changes: 0 issues at 1024 and 1155 (light and dark) and 375 px; `runMenuCheck()` 0.

**Tooltips no longer clipped (18 Oct 2026, after review).** The "Scene actions" tooltip was cut off at the script panel's edge, because the CSS tooltips sat inside scrolling panels. Every editor tooltip is now drawn in one fixed layer above the page and kept 8 px inside the window: right of the rail, above the timeline and panel footers, below everything else, flipping when there's no room. It follows the control when a panel scrolls, hides when the control scrolls out of sight, and closes on click or Esc. Checked at the panel edge, the rail, the bottom bar's right end, the script footer and the top-right corner.

**Canvas size shows its shape (18 Oct 2026, after review).** Live's size menu is text only (Original, Landscape 16:9, Portrait 9:16, Square 1:1, Standard 4:3, Portrait 3:4, Portrait 4:5), with the tick on the right. Each option now starts with a small frame drawn in its ratio, and the size button shows the current one, so a size is recognised by its shape before its name is read (recognition over recall; video editors such as Canva and CapCut do the same). The tick stays on the right, as in live.

**Ratio frames drawn like the product's icons; one tick style (18 Oct 2026, after review).** The canvas-size frames had a heavier line (1.2 on a 16-unit grid) and ink colour, so they didn't match the other icons. They now use the icon set's own drawing rules: 24-unit grid, 1-unit line on half-unit edges, round joins, 1-unit corners, the same size and muted colour as the other menu icons. Checking them side by side also showed two tick styles: pink ticks on the left in most menus, an ink tick on the right in the size menu. Every menu now uses live's style, an ink tick 8 px from the right edge, which also keeps pink for the primary action.

## Responsive and hover audit (18 Oct 2026, after review)

Review found the workspace button breaking: "Free plan" wrapped onto a second line and spilled out of a fixed 40 px box after body text moved from 11 to 12 px. QA had missed it, so QA now has two more checks: **wrapped** (text breaking inside a one-line control: buttons, tabs, chips, nav items, pills) and **spilled** (content taller than its box). Every page and state was swept at 1440, 1280, 1155 (light and dark), 1024, 768, 390 and 320 px, plus the collapsed sidebar.

| Found | Fix |
|---|---|
| Workspace button: second line wrapped and spilled at its fixed height | No fixed height (`min-height`); each line stays on one line and truncates. The second line shows the plan only, as live ("Free plan"); your name is in the menu it opens |
| "Made with Clueso AI: <chat>" wrapped on the project page with the AI panel open | One line, truncates, full name on hover |
| Editor banner clipped at 1024 px | As live, the project title truncates first; when the bar itself is narrow (container query on the bar, not the window) the banner keeps only Generate speech, then hides |
| Composer pill "Clueso default" wrapped | Pills never wrap; their row does |
| Tabs (language settings) and segment switches (Share dialog) wrapped at 390 px | One line; a row that doesn't fit scrolls sideways; dialog switches drop their icons on phones |
| Chats at 320 px: a column floor of 326 px pushed rows off screen | The single column can shrink (`minmax(0, 1fr)`) |

**Hover states.** All 301 clickable elements on 11 pages were checked against the stylesheet. 23 had no hover. Every clickable element now responds, using one system: quiet controls (icons, tabs, segments, rows) get `--hover`; raised controls (buttons, pills, chips, the workspace button) get `--raised`; fields get a stronger 1 px edge; dark buttons get a lighter dark; pink (primary) gets slightly deeper; text links turn ink.

Result: 0 issues at every width above, in light and dark, collapsed and expanded; `runMenuCheck()` 0.

## Help, learning and what's new in one place (18 Oct 2026, after review)

**Live (checked 18 Oct 2026)** spreads these over four places:
- a Help button in the top bar that opens a support panel (start a chat, Knowledge Base, Feature request);
- a footer under Home ("Make something beautiful", "Built with care", "Learn about our features" → help.clueso.io, "More from Clueso" → YouTube). At 1155 × 811 it starts at 964 px, below the fold, and "Built with care" isn't a link;
- a "New in Clueso" card in the sidebar (Multi-Video Layering, Media Panel, Voice Library, View changelog);
- help links in the account menu.

**Now:** one Help menu in the top bar, where live already puts Help, on every page and in the editor, grouped:

| Group | Items |
|---|---|
| Get help | Chat with support (a message form: "We're offline right now…"), Request a feature (what and why) |
| Learn | Knowledge base (help.clueso.io), Video tutorials (Clueso's YouTube), Keyboard shortcuts (also `?` anywhere) |
| What's new | Live's three updates, each opening its note, and View changelog |

A small blue dot on Help (not pink, which is kept for the primary action) means there are updates you haven't seen. It clears once you open the menu, and screen readers hear "Help, 3 new updates". The footer tagline and the sidebar card are not carried over: the footer sat below the fold with decorative text, and the card used navigation space for occasional news (Nielsen #4 consistency, #10 help in one findable place). The update notes describe only what is visible in the product; no dates are invented.

QA: 0 issues at 1155 (light and dark) and 390 px; `runMenuCheck()` 0; the menu fits on screen at 390 px.

**Named "Help & resources" (18 Oct 2026, after review).** "Help" with a headset said "support" only, but the menu also holds learning and product updates. It's now **Help & resources** with a question-mark icon, the label Figma uses for the same grouping. "Help" stays first because it's the word people scan for when they're stuck. The editor's icon button carries the same name in its tooltip. On phones (≤ 600 px) the button shows only the icon, keeping the name for screen readers, so the search field keeps its room.
The button has live's filled style (surface fill, 1 px faint edge, 4 px corners, ink text and icon), the same as Clueso AI beside it; it had been a borderless button.
**Icon: lifebuoy.** Compared at real size beside the product's icons: a question mark (generic, and its curve reads thin at 16 px), an open book (says "learning" only), a compass (suggests "explore") and a lifebuoy. The lifebuoy says "help and support" without its label, as in many help centres. It is drawn in the icon set's style (24-unit grid, 1-unit line, round joins) and stays distinct from Clueso AI's sparkle beside it. Used on the top-bar button and the editor's icon button.
**Icon, final: book with a question mark (chosen in review).** The lifebuoy read as a tyre or steering wheel at 16 px. Four options were compared large, at real size and beside nearby icons: a redrawn question mark, a book with a question mark, live's headset and the lifebuoy. The book with a question mark was chosen: it says "help you can read and learn from" (knowledge base, tutorials, shortcuts, what's new) and is drawn in the icon set's style. Used on the top-bar button and the editor's icon button.

**Settings nav without category headings (18 Oct 2026, after review).** The nav had headings Account, Workspace, Billing, Content and Sharing. Three of them headed one item and repeated it ("Account" over "Profile", "Billing" over "Plan and usage", "Sharing" over "Player and links"), so they read as more settings, not categories. Live's Workspace settings has no headings: items with icons, grouped by hairline dividers (Admin, Billing, Users · Video defaults, Pronunciations, Translations, Transcriptions · Video player, View only links · Connections). The nav now does the same: Profile · General, Plan and usage, Members (live's order) · Video defaults, Language and voice · Player and links. Each item has an icon, and the current page is marked for screen readers (`aria-current`). On phones the items wrap as chips without dividers. QA: 0 issues at 1155 and 375 px.
Follow-up review: the divider lines were removed; the groups are kept by a small gap only.
**Link icon redrawn (follow-up review).** In the settings menu the link icon looked small and light beside the others: its drawing filled about 13 of 24 units while the rest fill 15–20. It is now a two-link chain filling 17 × 18 units, in the same 1-unit line, so it carries the same visual weight. It changes everywhere the link icon appears (Share buttons, link fields).

## Clueprint preview, centred (18 Oct 2026, after review)

Review asked for a more intuitive way to open a Clueprint than the side drawer. **Live (checked 18 Oct 2026)** opens a centred window over a blurred grid: title and "by Clueso", a video player (play, time, speed, volume, download, full screen), arrows to the previous and next Clueprint, a strip of scene thumbnails, the created date, Edit this Clueprint and Create video.

The drawer here had a small still image, a description, a needs list, a three-field "Quick brief" form and an info box. Choosing a template is a watch-and-compare job, and the video needs room; the brief duplicated the Home composer, where Clueso already asks its questions and shows the plan.

**Now:**
- A centred window, 760 px wide, built around a large 16:9 preview. Play from the corner button or the bar; the progress bar and time follow; the caption changes with the scene.
- A scene strip taken from the template ("Hook on the pain", "Reveal the product", "Show it working", "Name who it's for"); click a scene to jump to it.
- Previous and next Clueprint arrows, plus ← and →, to compare without closing. Space plays.
- One line of description and one line "You'll need …".
- Footer: "Free on every plan. You'll see the plan and credit cost before anything is built." · Edit this Clueprint (saves a copy to Workspace) · Create video.
- **Create video** goes to Home with the Clueprint attached as a removable chip above the brief, the cursor in the brief and the prompt "Your product, who it's for, and what viewers should do". Sending starts the chat with that Clueprint. The brief is written once, in the one place briefs are written.

Not shown: live's "Created on" date (the prototype has no real dates for these templates). On phones the arrows hide (← → and the scene strip still work) and the footer wraps.

QA: 0 issues at 1155 and 390 px for the open preview and for Home with a Clueprint attached; `runMenuCheck()` 0.

**Dropdowns styled like the other controls (18 Oct 2026, after review).** The browser's own select styling was showing through: a grey 1 px border, the native arrow and its own focus ring (the Analytics project picker; also the upload, translate and Brand kit fields). Every `<select>` now has no native chrome, the faint 1 px edge, 4 px corners (form fields keep their 6 px), the product's chevron in muted grey (a lighter one in dark mode), ellipsis for long project names, and the same hover and keyboard-focus states as buttons and fields. QA: 0 issues at 1155 in light and dark.
Follow-up: a clicked dropdown showed a heavy dark ring, because Chrome treats a focused select like a text field. Focus now matches every other field: a thin 1 px pink edge.
**Dropdowns are the app's own (follow-up review: "on hover it breaks and on click what kind of UI is that").** Restyling the native select wasn't enough: the button hover style reset the background and wiped the chevron, and a click opened the operating system's own list, unlike every other menu here. Every select is now shown as the app's dropdown: a button with the current value and a chevron (a toolbar button on Analytics, a field inside forms), opening the same menu as the canvas size or zoom, with the tick on the right, the menu at least as wide as the button, and focus on the current choice. The real select stays underneath, hidden; picking sets it and fires `change`, so existing behaviour holds (choosing a project on Analytics opens that project's analytics). Inside a dialog (Translate, upload) the menu now closes on its own instead of taking the dialog with it, and Esc closes only the menu. QA: 0 issues at 1155 (light and dark) and 375 px; `runMenuCheck()` 0.

## Home: outside review (18 Oct 2026)

Two outside reviews of Home (8/10 and 8.4/10) asked for targeted fixes, not another redesign. What was taken, and why:

- **The next setup step is a link.** "add your brand" (or "share your video") in the getting-started line is now an underlined link that opens Brand kit (or Share). Both reviewers read the line as information only. The earlier choice to point at the composer's brand pill instead of linking is reversed: the evidence is that people didn't see what to click.
- **Hiding getting started keeps progress.** The × says so on hover, and the toast offers Undo. Progress (2 of 4) is unchanged.
- **Quieter grid.** Live's grid texture stays (it's live's look), with fainter lines (`--gridline`, 4.5% instead of 8%) that fade out by the lower half, so the cards and project thumbnails sit on a plain surface.
- **Section rhythm.** Recent projects sits 32 px below the cards, the same as the gap above "Or start another way"; 12 px inside, as in the cards row; heading at the 14 px title size in ink.
- **A frame in the thumbnail.** Recent project cards show a frame of the video (the product screen it shows, with its title card and duration) instead of a plain colour tile. A real build would use the video's own frame; here it's drawn. The whole card is the link, with a focus ring and a name read out with its length and last edit.
- **Returning users see their work first.** Once setup is done (or hidden) and there's more than one project, Recent projects moves above "Or start another way". New users keep the first-video path on top.
- **Usage bar only when it means something.** The sidebar's pink bar had no scale for two numbers (minutes and credits). It's gone; the line keeps both numbers, and hovering gives "x of y" for each. When credits drop to 20% or less, an amber bar of credits left appears.
- **When credits are taken, on hover.** The composer's cost line explains it on hover: an estimate, taken as Clueso builds, approved first in Ask and Plan.

Not taken: a project-card actions menu and sorting on Home (the reviewer advised waiting until there's a need; Projects has both); contrast and focus states were already checked by the QA sweep and hover audit.

**Shapes menu matches the other editor menus (18 Oct 2026, after review: "not matching with the rest of the UI").** It had no icons, an uppercase heading, taller two-line rows, and the tick after the shortcut. Now each row is like the project and size menus: a shape icon (drawn in the same 1 px stroke), the name, the shortcut as a small quiet key, and the tick at the right edge; 30 px rows; no heading (the button's tooltip already says "Choose a shape"). The rail tooltip now shows the chosen shape's own shortcut (it said "Star (R)").

## Editor's Clueso AI: outside review (18 Oct 2026)

The review kept the direction and flagged one main risk: the panel's chips read as if they change the video, then a note says editing by chat is Enterprise. What was taken:

- **Suggestions grouped by what happens.** Ask about this video (Clueso AI answers), Suggest improvements (nothing changes until you make the change), Edit this video (Enterprise: "Chat edits are on Enterprise. On Free, make the change here", with *What Enterprise adds*). Each group's meaning is on hover. Two chips show at first; *More suggestions* shows the rest, including Translate this video, which opens directly on Free.
- **Scope is stated.** The header says "On: Scene 4 only" while the scene chip is attached, and "On: the whole video" once it's removed; the chips change wording to match ("Summarize this scene" / "this video"). The scene chip explains its scope on hover, and a dashed "+ Scene 4" chip puts it back.
- **Resizable panel.** Drag the panel's left edge (or focus it and use ←/→, Home/End; double-click resets). Wide screens: 300 to 520 px, default 360. Mid: 280 to 360 px, default 300. It won't grow if the canvas would drop below 320 px; the canvas keeps its ratio and scales. The width and whether the panel is open are kept for the session. Narrow and phone layouts keep their shared column and sheet.
- **Credits are an estimate.** "About 13 credits a reply, estimated · 750 left"; on hover: longer answers and attachments use more, shorter ones less, and credits are taken only when Clueso AI replies (Clueso's own threads show per-message credits that vary). With too few credits: "Not enough credits for a reply · See plans", and Send is off.

Already in place: the selected scene is the same in script, canvas and timeline; Delete project asks first and says it can be restored for 30 days; the cloud icon shows save status.

Bug found on the way: a call at load time in `editor.js` ran before `app.js` had defined the app state and stopped the rest of the file from loading; it now runs on each editor render.

## Editor cross-checked against live, control by control (18 Oct 2026, after review)

Checked against the user's live screenshots ("Taskly — Product Teaser", web.clueso.io). Every live control, and where it is here:

| Area | Live | Here | Status |
|---|---|---|---|
| Top bar | Logo menu, title, cloud save, Video / Article | Same | Kept |
| Top bar | "Generate Speech to update the voiceover" banner with Generate speech | "Blue text needs new speech" with Generate speech (shrinks to the button at narrow widths) | Kept, clearer wording |
| Top bar | "Text active · Exit Esc" pill, laid over the speech banner (it covers it) | **New:** a mode bar over the canvas while Text or a shape is on: tool icon, "Text active" or "Star active", Exit · Esc. It no longer covers the banner; it replaces the old "Click the canvas…" toast, which vanished after 3 seconds | Added, improved |
| Top bar | Avatar, Support (headset), Comments, Translate, Clueso AI, Share | Same; Support became the Help & resources menu (book icon, chosen in review) | Kept |
| Rail | Select, Hand, Voiceover script, Media, Text, Shapes (with corner flyout), Fx, Animation, Template, Transition, Captions | Same, same order | Kept; icons redrawn: Fx upright like live's, Animation a dotted motion path ending in a dot (was a wave) |
| Script | Header and close; Search script; options icon | Same; the icon is Find and replace | Kept |
| Script row | Number and name chip; voice chip with blue mic and solid **V4**; a speech button (waveform with sparkle), greyed when nothing to voice | Number and editable name; voice chip now with live's blue mic and solid V4; **new** per-scene speech button, enabled only when the scene has words not yet voiced ("Speech is up to date" otherwise); scene menu on hover | Added |
| Script row | "Start typing or press "/" for commands…" | Same, and "/" opens commands | Kept |
| Script footer | ⋯, +, AI Rewrite and its settings as one split button, Generate speech (dark, waveform) | Same, now bordered as live and AI Rewrite with Prompt hub joined as one split control; the label hides in a narrow panel | Matched |
| Canvas | Size menu "Original (1920x1080)" with frame icon; zoom "100%" | Same menus (default zoom Fit) | Kept |
| Clueso AI | Title, Chat history, New chat (plus in a circle), close; Show more; answer choices; "Running low on AI credits · Upgrade plan"; +, Ask, model | Same, plus panel view and brand; New chat now uses live's circled plus so it isn't confused with the composer's + | Kept, icon matched |
| Timeline bar | Start, previous, play, next, end; timecode with frames; 1x; Loop; High res; Split; Add; Undo; Redo | Same | Kept |
| Timeline bar right | Detailed timeline (diamond), Skimming (green when on), Full screen, Timeline settings (sliders), Collapse | Same; Collapse now uses live's "down to the tray" icon instead of a chevron; Prompt hub sliders redrawn to match the settings sliders | Icons matched |
| Track | Ruler with playhead label; scene clips with a header and frames; transition marks between clips; scrolls sideways | Same; the clip header shows the scene number (as in the script) instead of a play icon; the whole video fits the width, so there is no sideways scroll for short videos | Kept; the scroll is a deliberate change: fit-to-width shows every scene at once |

Removed or changed on purpose: nothing from live is gone. Live's clip-header play icon became the scene number so a clip, its script and its canvas read as the same scene.
QA: 0 issues at 1155 and 375 px, light and dark, in every scene and with the mode bar on; `runMenuCheck()` 0. Small fix found on the way: the sample blue scene's subtitle was just under 4.5:1, so that blue is slightly darker.

**Script rows matched to live, second pass (18 Oct 2026, after review).** The review pointed at live's details the first pass missed, and at styling that conflicted with live:
- **Scene header is one control, as live.** Number, name and voice are joined: the name sits on white (it's a text field), the voice on grey (it opens a menu), split by a hairline. Live's colours say what's typed into and what's picked from, which reads better than two identical outlined chips. Faint 1 px edge (was the stronger line colour), live's 4 px corners, regular weight in grey (was medium in ink). The voice uses live's AI-voice mic (a mic with a sparkle) in blue, and the solid blue V4 with 2 px corners.
- **Per-scene speech button** on white with the faint edge; greyed when the scene is up to date, dark when it has words to voice.
- **+ between scenes.** As in live, a + sits on the dashed line between two scenes and adds a scene there (with Undo). It shows on hover or keyboard focus; always on touch screens.
- **Sync Point card.** Clicking a Sync Point chip opens live's card: "Sync Point", its status (Pending while the scene has words not yet voiced, Synced otherwise; live shows only Pending), the frame it waits for, a line saying what it does, **Edit** (moves the playhead to that frame) and **Remove**. It replaces a two-line menu.
- Footer and speech-button edges toned down to the same faint edge.
QA: 0 issues in light and dark, with the card open, and at 375 px; full sweep and `runMenuCheck()` 0.

**Editor top bar: right group back on the right edge (18 Oct 2026, after review).** With no speech banner showing, the spacer between the groups had shrunk to nothing (the "title truncates first" fix had set it to never grow), so avatar, Help, Comments, Translate, Clueso AI and Share sat in the middle of the bar. The spacer grows again (it still never shrinks, so the title truncates first), and the right group is pinned to the right edge, as live, even when the banner is hidden at narrow widths. Checked at 1360, 1155, 960 and 375 px, with and without the banner and the AI panel: 0 px from the edge, QA 0.

## Alignment and layout sweep (18 Oct 2026, after review: "check all such possible issues")

The editor's right-hand group drifting to the middle had one root cause: `.grow` spacers only grew where a page set them to, so any spacer elsewhere collapsed to 0 px. QA had no check for this. Added:

- **`unpinned` check (qa.js):** in any row with a spacer (`.grow`, `.spacer`, `flex: 1`), the items after it must end at the row's right edge, unless they wrapped onto another line or carry their own deliberate right margin. Verified it catches the original bug.
- **`runEditorStates()` (qa.js):** every editor state at the current width: each side panel, the article, Clueso AI, version history, the inspector, the detailed and collapsed timeline, find and replace, a drawing tool on.
- **Overlap check fixes:** it now uses only the part of an element its scroll containers show (a half-scrolled tile was reported over the timeline), and treats the editor's full-screen version history sheet like the other sheets.

Found and fixed:

| Where | Problem | Fix |
|---|---|---|
| Every row using `.grow` without its own rule | Spacer collapsed; right groups drifted | `:where(.grow) { flex: 1 1 0% }` as a zero-specificity default |
| Editor timeline bar | Detailed timeline, Skimming, Full screen, Settings and Collapse sat mid-bar, 413 px from the right | Same default |
| Script footer | Generate speech 30 px short of the right edge | Same default |
| Chats, New chat at 960 px | The composer row couldn't wrap in the 386 px column: Send squeezed to 16 px and pushed out of the box | Composer controls now wrap by the composer's own width (container query), not the window's: Send at the right, cost below, as on phones |
| Top bar at 768 px while a video builds | Search label wrapped onto two lines; the bar ran 7 px off screen and pushed New project out | Search label stays on one line and truncates; the search box gives way first (300 px down to 96 px) |

Checked clean afterwards: every page and state (`runSweep`) and every editor state (`runEditorStates`) at 1360, 1155, 960, 768, 375 and 320 px, sidebar open and collapsed at 1155 and 768, light and dark at 1155, `runMenuCheck()` 0.

## Project page: outside review (18 Oct 2026)

The review (8.5/10) asked to keep the structure and refine details. Taken:

- **Columns start on one line.** The status boxes (ready, queued, building, cancelled) moved from the top of the video column to a full-width row above both columns, so the video and the Step-by-step guide card share a top edge. Both columns keep 12 px between items.
- **Ready banner: status, explanation, action.** "Your video is ready to share · Share a link with your team. It uses about 1 export minute; 10 of 10 are left this month. · Share link". When the banner is narrow, Share link moves under the text instead of squeezing it.
- **One pink at a time.** While the banner offers Share link, the top Share is the plain button; after you dismiss the banner, the top Share is pink again. Two pink buttons for the same action broke the "pink is the one primary action" rule.
- **Details under the video on two lines.** "AI video · ~1:00 · Edited just now", then "Made with Clueso AI from “…”" on its own line, wrapping to two lines instead of cutting off. Both in the muted grey (passes contrast).
- **Locked analytics explains itself on hover:** "Who watched and where they stopped. On the Business plan; opens a sample of the dashboard." It stays a compact row.
- **Chat names don't end mid-phrase.** New chats drop a dangling last word ("Walk through our sign-up flow", not "… flow in"). Existing chats keep their names; they can be renamed.

Not taken: filler for the space below the content (the review itself advised against it); Versions already lists translations and made-from videos once they exist; Make guide already shows as the dark button when there's no guide.
QA: the page in each state (ready, building, queued, cancelled, none) at 1360, 1155, 960 and 375 px: 0 issues, tops aligned, one pink button. Full sweep in light and dark.

## Analytics: outside review (18 Oct 2026)

The review (8.3/10) asked for clearer metrics, a more useful chart and a clearer sample/upgrade split. Checked against Clueso's help center (help.clueso.io/home/analytics, read 18 Oct 2026), which defines the metrics, the presets, sorting by any header, location by impressions, and help-center searches with a date.

| Was | Now | Why |
|---|---|---|
| Pink "Sample data. This is what Analytics shows…" + See plans | "Analytics preview" on a quiet card: "This is sample data. On the Business plan, Analytics tracks…" + **Explore Business plan** (the one pink button) | Preview and upgrade said separately; the banner no longer competes with the data |
| "Times opened, played or not", "Unique plays per session", "Impressions that led to a play" | Clueso's definitions: "Times your content was opened, watched or not", "Unique plays per viewing session", "Plays ÷ impressions"; an ⓘ on each gives the full rule on hover (rewatches in a session don't count; the exact play-rate sum and rounding) | Help center; review asked for precise definitions without more text on the cards |
| 7d/14d/30d/90d/Custom did nothing | They work. A line says what's shown: "Last 30 days · 19 Sept – 18 Oct, including today · All projects". Custom opens From/To dates (up to today) | Review: date coverage must be clear |
| Chart: two lines, no values | Hover, or focus and use ←/→ (Home/End): a cursor, dots and a readout with date, impressions, plays and play rate. Plays is dashed, so the lines differ by more than colour. A hidden table carries every value for screen readers | Review: tooltips, keyboard, not colour alone |
| No comparison | "▲ 23% vs previous 30 days" under each number (play rate in points; "No change" at 0) | Review, medium priority. Not in Clueso's help center: the sample shows it; it needs real previous-period data before shipping |
| Table: plain headers, numbers left | Sort by any header (buttons, `aria-sort`), numbers right-aligned in tabular figures, average play as time then % in grey, titles are links (to that video's analytics) with "Open project" under each; totals add up to the cards; on phones the table scrolls instead of dropping Impressions | Help center (sortable headers); review |
| — | No views in the chosen dates: "No views in this period" with "Show the last 30 days"; Download CSV is off | Review: empty state |
| "Breakdown by location" | "Breakdown by location · by impressions"; Other says "14 more countries, each under 3%" on hover; bars scaled to the largest country | Help center: by impressions |
| Help center searches: query, clicked | Date, search, clicked guide ("None" when nothing was clicked) | Help center columns |

Sample data fixes on the way: the sample videos now have created dates before their views (12 Jun to 9 Sep); there are no views before the first one; the table and the cards agree. Layout bug found: at 768 to 1000 px the table spilled into the location card (an inline column rule beat the stacking rule); it now stacks below 1000 px.
QA: /analytics and /analytics/p1, light and dark, with and without Clueso AI, at 1360, 1155, 960, 768 and 375 px: 0 issues; the chart readout stays inside the chart at both ends; the Custom picker 0. The full sweep caught a class clash on the way (the chart legend reused `lg`, the large-button class, and shrank onboarding's Continue to 24 px); the legend is now `anlg`. Full sweep light and dark 0, `runMenuCheck()` 0.

**Analytics sample is visible without reading (18 Oct 2026, after review: "if I miss that, it would look like real data").** The preview card said it in words only. Now the page looks like a sample at a glance: a "Sample data" tag beside the Analytics title, the data cards hatched with a faint amber stripe and edge (the placeholder pattern), the big numbers tinted towards amber, and SAMPLE DATA written faintly across the chart. Amber, not pink: it's a notice, and pink stays for Explore Business plan. QA: 0 issues (contrast included) in light and dark, with and without Clueso AI, at 1155, 960 and 375 px.

Follow-up review: the "Sample" tag on every card was too much; one tag by the title is enough. Removed from the cards; the hatching, tint and chart watermark stay.

**Analytics: the banner is an upgrade offer (18 Oct 2026, after review: "same icon… this is enabling the paid feature").** The preview card repeated the Analytics icon from the title and read as a notice. It's now an offer: the amber lock "Business" badge used everywhere a feature is on a paid plan (so it reads the same as the project page's "Views and drop-off · Business"), the headline "See how your real videos perform", what Business adds as three ticks (every published video, link and embed; where viewers stop watching; where they're from and what they search for), **Upgrade to Business** as the one pink button and Compare plans beside it. "Sample data" is said once, by the title. On phones the actions sit under the text. QA: 0 issues, light and dark, with and without Clueso AI, at 1155, 960 and 375 px.

Follow-up review ("who suggested a dark background?"): nobody did; the pink wash was my addition and read as a muddy, darker card next to the white ones. The card now uses the same surface and faint edge as every other card; the badge, headline and the one pink button carry the offer.

**Home composer with a Clueprint: no overlapping hints (19 Oct 2026, after review).** Attaching a Clueprint added a placeholder ("Your product, who it's for, and what viewers should do") under the Tab suggestion, and the two were drawn on top of each other. Now there is one hint, the Tab suggestion; the Clueprint guidance is on the chip's hover and in the box's accessible name.

## Onboarding, redesigned from the goal (19 Oct 2026)

Research and the decisions agreed with the user: `research/onboarding-research.md`. In short: the goal is the user watching a finished video of their own product in the first session; every question must change what happens next; no tutorial.

| Screen | What it asks or does | Why |
|---|---|---|
| 1 · What video do you need right now? | Product demo, Training video, How-to guide, Launch teaser (single choice, a tap moves on). "Just exploring?" opens a sample project. Skip goes to Home | Picks the structure, Clueprint, example brief and Home's suggestions |
| 2 · What do you have to start with? | Record my screen now / I have a recording / I have slides or a doc / Just an idea, with the usual choice for that video marked | Decides the whole first step: the biggest branch in Clueso |
| 3 · Make your first … | The first video itself: record (live timer, Stop, Record again), choose a file, or edit a brief written for that video type. Optional website pulls logo and colours. What you'll get (example and style), the cost, Make my video (says why it's off). "I'll do this later" goes to Home | Ends at value, not at setup; nothing runs before the cost is shown |
| Sample project | The editor with real scenes and a lasting "Sample project to explore · Make my own" notice in the top bar | A toast disappeared after 6 s; the label has to stay |

Removed: the "Here's what Clueso does with…" screen (a tutorial: NN/g found these don't help) and the 3-step strip on Home (the same tutorial again). Not asked any more: role, workspace name, multiple goals.
Also fixed: a project made with a Clueprint was named after the instruction ("Use the “…” Clueprint. …"); the instruction stays in the brief, not the name (new projects).
QA: every path and state (record idle, recording, done; file before and after; idea with an empty and a filled brief; sample) at 1155, 768, 375 and 320 px in light and dark: 0 issues. The sweep now includes /start/3.

## Onboarding, second design: no wizard (19 Oct 2026, after review)

The three-screen version was rejected after a walkthrough as the user (made-up name, a question for us not them, first-option bias, the hardest start on top, credits before value, too much on one screen, an unplanned wait, explorers dropped into the editor). Full reasoning: `research/onboarding-research.md` §7.

Now the first Home visit is the onboarding. Sign-up (Google or email) lands on Home; /start redirects there. First-run Home: a greeting only when the name is known, a compact 40-second before/after (Watch with sound, Open this sample in the editor), the composer with "Start from an example" chips (Product demo, Training video, How-to guide, Launch teaser) that fill an editable brief, then Upload (or drop a file anywhere) and Record ("about 2 minutes, open your product first"; on phones "Record on your computer" emails a link). Translate is hidden until there's a video.
The first video is on us: "Your first video is on us" replaces every cost line (composer, plan, build dialog, upload), canBuild allows it, and no credits are taken (proposal: Clueso to confirm). The plan states "Clueso will make a how-to guide with a short video · Change", inferred from the brief. The build says what it's doing and that it emails when ready. The result offers the company's logo and colours only for a work email. "What will you mostly make?" appears once, after the first share.
Removed: the onboarding screens, their progress dots and Skip, and the old wizard's state and actions.
QA: first-run Home, plan, build, ready, second video, the question after sharing, drop, explore and phone at 1155 and 375 px: 0 issues; full sweep light and dark, `runMenuCheck()`.

**First-run focus mode (19 Oct 2026, decided with the user).** On the first screen nothing competes with making the first video: no side menu (empty Projects and Chats, set-up pages, a locked Analytics, a credits line that doesn't apply), no search, no New project. Kept: the Clueso logo, Help (for someone who feels stuck) and the account button (sign out, settings). The full app returns when the first video starts building, the moment it's needed; one tip then points at Projects ("Your video is building. Find it here, along with every video you make." · Got it, which moves focus to Projects; on phones it points at the menu button). No "Explore Clueso first" link: with the menu gone it made no sense; the tip teaches where things are instead. QA: focus mode and the tip at 1155 and 375 px in light and dark: 0 issues.

**First-run Home, by information hierarchy (19 Oct 2026, after review: "no information or visual hierarchy").** Before: two headings, the before/after card between the heading and the composer, "example" meaning three things (the demo card, the grey Tab suggestion, the starters), the reassurance tiny in a corner, and Upload and Record as cards as heavy as the composer. Now it follows a new user's questions in order:
1. *Where am I, what do I do?* One heading, "Welcome, Alex. Let's make your first video" (name only when known), and one line: "Describe it, or start from a file or a screen recording. **Your first video is on us.**"
2. *The main action:* the composer, the strongest element (raised, the only shadow on the page), with one plain placeholder ("What's the video about, and who is it for?") and a "Try:" row of starters attached. No Tab suggestion in the first run: it duplicated the starters.
3. *Other ways:* a light row under a divider, "Or start from · A file · A screen recording (about 2 min)", the compact button row live Clueso uses for "Or start directly"; descriptions on hover; dropping a file anywhere still works.
4. *Not ready yet:* a quiet line at the bottom, "Not sure yet? See a rough 2-minute recording become a 1-minute video… · Watch it · 0:40 · Open the sample in the editor".
QA: light and dark at 1155 and 375 px: 0 issues; Tab on an empty first-run box no longer inserts a hidden suggestion.
Reverted the same day at the user's request: the hierarchy version felt less convincing and less personal. The previous first-run Home is back (Welcome line, "What are we creating today?", the visible "See what Clueso does" example above the composer, the Tab suggestion, "Your first video is on us" in the composer, Start from an example, and the Upload and Record cards). Kept from that pass: Tab on an empty box only fills a suggestion that's visible.
Moved the "See what Clueso does" example to the bottom of first-run Home, under the ways to start (19 Oct 2026, user request).
**No pill shapes (19 Oct 2026, after review).** Example starters, suggestion chips, search scopes, the build chip and filter chips had fully round corners; live uses 4 px on every control. All are 4 px now; starters at the 24 px chip height.

## First-run controls and edge cases (19 Oct 2026, decided with the user)

Every control on the first screen was judged by whether a first-time user needs it. Until the first video starts, and back to normal after:

| Control | First run | Why |
|---|---|---|
| Help (now labelled "Help", not just the book icon) | Chat with support ("We usually reply within a few hours"), How to make your first video, Knowledge base | Request a feature, shortcuts and What's new mean nothing on day one; updates are marked read at sign-up, so no dot |
| Account | Who you're signed in as (email only for an email sign-up, initials from it), theme, **Use a different account**, Sign out | Spotting a wrong Google account is a real day-one problem; one workspace and Profile settings aren't |
| + | Record your screen, Attach a file | "Add a project" had nothing to add; Clueprints are for later |
| Ask / model / brand | Hidden | Jargon; an accidental Auto skipped the plan; a cheaper model makes the first video worse; brand is offered on the result |

Edge cases handled:
- **Brief too short** ("demo", "hi", "asdf", fewer than four words): one question with three example answers and Something else; nothing is built or charged, even in Auto. The video is built from the answer, and its type is read from it.
- **A link in the brief:** the plan offers "Use the logo and colours from taskly.io?".
- **Not in a Latin script:** the plan says it's made "in the language you wrote in".
- **Offline when sending:** "You're offline. Your brief is kept; send it when you're back".
- **Wrong file type dropped:** says which types work; over 2 GB says to trim (Free takes videos up to 10 minutes).
- **Cancelled or failed build:** nothing charged, and the first video is still on us (the cancel dialog says so). The full app stays, since there's now a project.
- **Replies before the first video** (answering Clueso's question) are free too.
- **Several free videos via new accounts:** a policy for Clueso (one per workspace, after email verification), noted not built.
Also fixed: a new-user reset kept the previous user's tip, starters and goals (the reset sat in the page-load code, not the scenario switch).
QA: every first-run menu, the question, the plan, cancel, offline and drop, in light and dark at 1155 and 375 px: 0 issues.
Chat names also drop the Clueprint instruction ("Use the “…” Clueprint."), like project names.

## The whole first-run journey, sign-in to first video (19 Oct 2026)

| Step | Screen | Edge cases handled |
|---|---|---|
| Sign in | Live's layout. Google, SSO, email and password, Forgot password (a reset dialog), "Don't have an account? Sign up" | Not an email: says so. No account for that email: "Create one". Empty password |
| Sign up (new, live's layout) | "Welcome to Clueso · Create your free account": Google, SSO, first and last name, email, live's work-email tip (only while the email is a personal one), password (8+), Create account | Bad email; an email that already has an account ("Sign in instead"); short password with the count so far; errors beside the field, focus on the first one |
| Google | "Choose an account" with the account and "Use another account"; says what Google shares | From sign-in: signs in. From sign-up: a new, verified account with the name |
| SSO | "Continue with SSO · Enter your work email" | Personal email: SSO needs a company address. A company without SSO: "We couldn't find SSO for … Ask your IT team, or sign up with email". A company with SSO: signs in, verified, name from the address |
| Verify (email sign-ups) | Doesn't block: a quiet "Check your inbox to verify … You can start now · Resend" in the first-run top bar | Only sharing needs it: "Verify your email to share" with Change email, Resend, I've verified |
| First-run Home | As decided earlier (focus mode, starters, free first video) | |
| The plan | **Stays on the focused Home** ("Change the brief" goes back with the text kept) instead of jumping into the full Chats page. A brief too short gets Clueso's question with answers in place | Reply box without mode, model or brand |
| Building | The full app returns; one tip points at Projects and closes when you leave that page | |
| Ready | "Your video is ready · Watch it first: it takes a minute" → a player (pause, progress, captions) → at the end "That's your video": Open editor, Share link. Then the banner becomes "ready to share" | Share asks to verify first if needed |

A new account starts clean: the previous account's watched state, plan, tip, starters and goals don't carry over (found while testing: "Watch it" was skipped for a second account). Sign-up and SSO pages have their own tab titles.
QA: every step above in light and dark at 1155 and 375 px: 0 issues; full sweep and `runMenuCheck()`.

## Try before an account (19 Oct 2026, gap 1 from "How to Win at Onboarding")

The doc's strongest finding: value before commitment (Duolingo lets people finish a lesson before signing up). Before, Clueso needed an account before anything happened. Now:
- **Try it first.** "try it first" on Sign in and "Try it without an account" on Sign up open the first-run Home as a guest (/try): focus mode with Help, Sign in and Sign up instead of the account button.
- **A guest can do everything up to Build:** starters, writing the brief, Clueso's question, the plan (which says "Free. You'll create an account to build it, so you can keep and share it. Your brief is kept.").
- **The account is asked at Build, when there's something to keep:** "Create your free account to build your video", Google or email and password (names wait; the shortened form the doc recommends). After it, the build starts at once and the brief, plan and chat carry over. Same at Start recording, and at "Record on your computer" on a phone (there's no email to send the link to until there's an account).
- **Edge cases:** an email that already has an account ("Sign in instead; your brief is kept") switches the same box to Sign in; Sign in with no account ("Create one"); short password with a count; signing in from the Sign in page keeps what the guest started; a guest who reloads keeps the brief and plan; switching scenario ends guest mode.
QA: guest Home, plan, the box (sign up, errors, sign in), Sign in and Sign up pages, light and dark at 1155 and 375 px: 0 issues.

## Gap 2: see it while it builds · Gap 3: the return visit (19 Oct 2026)

From "How to Win at Onboarding": shorten time to value; plan the return visit with behaviour-triggered messages.

**Gap 2 · time to value.** The first look used to wait for the whole 10-minute build. Now the build card shows the work as it happens:
- "Writing the script" first, then **Read the script** (each scene's line, with Watch on the scenes already built).
- Six scene tiles: built ones play (an 8-second scene player with its caption, then "Next scene" or "Back to the build"), the current one shows it's building, the rest say "Up next". The first "that's my product" comes after the first scene, not the last.
- While building, the big player plays the ready scenes, and **Share is off** ("Share when it's ready"); it used to be possible to share an unfinished video.

**Gap 3 · the return visit.**
- **Home picks up where they left off:** "Your video is building · 2 of 6 scenes ready · Watch what's ready", or "Your video is ready · Watch it". It goes once watched. (A plan not yet built already reopens on the first-run Home.)
- **Follow-up emails** (review page at #/emails, also from the review bar's Emails button): five, each triggered by what the person did or didn't do and stopped by the step it asks for: no brief after a day; plan not built after a day; video ready (reminder after 2 hours unwatched); watched but not shared after 2 days; shared but no second video after 5 days. Never more than one a day. Clueso's lifecycle tool would send them; the page specifies them.
QA: build card (script, scenes, scene player), Home resume (building, ready), emails page, light and dark at 1155 and 375 px: 0 issues.

**First screen: Try for new visitors, Sign in for returning ones (19 Oct 2026, the user's idea).** Live opens on Sign in. Now the bare app URL picks by browser: one that has never signed in gets the try screen (value before commitment; ChatGPT has allowed use without an account since 2024); one that has signed in before gets Sign in, so a signed-out customer never lands on an empty workspace and thinks their videos are gone. Every way of getting an account (sign up, Google, SSO, the Build box, sign in) marks the browser. The try screen says "Have an account? Sign in to see your videos" above the heading. Website links: "Get started" → Try, "Log in" → Sign in. The review bar has a **Visitor** scenario (a browser that has never signed in). Worth asking Clueso: the share of new vs returning visitors on its sign-in page.
Sign-up box and Google's account picker fit their content (400 px, form full width); they were 520 px with a 380 px form, leaving dead space on the right (19 Oct 2026, review).

**Sign in from the try screen opens a box, not a page (19 Oct 2026, the user's idea, with its limits).** Why: what the person typed stays visible behind it, so it doesn't feel like leaving, and it matches Sign up, which was already a box (two neighbouring buttons behaving differently broke consistency). Limits kept: the full Sign in page stays for direct entry (a returning browser, email links, bookmarks), where there's nothing to keep; SSO still has to hand off to the company's sign-in ("Use SSO" in the box says so). The box has what the page has: Google, email and password, Forgot password, Use SSO. It says "What you started here comes with you" when there's a brief or plan, "Welcome back" when there isn't, and after signing in the brief and plan carry over. Fixed on the way: SSO from a guest session created a fresh workspace and dropped the brief despite saying it was kept; it now carries over too.

**Sign in and Sign up: same layout, different words (19 Oct 2026, review).** They share a layout on purpose (people switch between them; Google, Notion, Slack and live do the same), but should be told apart at a glance. Now: the Terms line only where an account is created (it was on Sign in too); Sign up says what you get ("Your first video is on us, and your brief stays where it is"); Use SSO in both modes (live offers SSO at sign-up); Forgot password only on Sign in. The wrong-form safety net stays: "There's already an account… Sign in instead" and "No account… Create one".

**First run: Clueprints instead of one example (19 Oct 2026, the user's idea).** The "See what Clueso does" card is replaced by "Start from a Clueprint": four finished styles (Chapter-based Product Tutorial, Narrated Product Teaser, Product Marketing Teaser, Product Tutorial – Customer Education), each with what it needs. Live's own first-video step shows Clueprints too. Presented as "Video styles made with Clueso", not as what other users made, because they're Clueso's. A card opens the centred preview (plays scene by scene); Create video there attaches it to the box. "Browse all 8" opens the same preview to step through every Clueprint (← →), so a first-time user or guest never leaves the focused screen for the full Clueprints page. Fixed on the way: Create video from Home didn't redraw when already on Home, so the chip didn't appear.
**First-run Home: two sections by proximity (19 Oct 2026, review).** "Make a video" (box, examples, Or start another way, Upload and Record) is grouped tightly: 10 px box → examples, 20 px → divider, 12 px → the two ways. "Start from a Clueprint" is its own section: 72 px away (space only, no line), with a 16 px section heading. Before, everything was 16–32 px apart, so the Clueprints read as part of the creation area.
**Guest sign-up names what they chose (19 Oct 2026, review).** "Browse all" stays open to guests: Clueprints are inspiration, and locking them would cut the chance a guest finds one that fits. The sign-up box comes when they commit, and names the Clueprint: building with one says "Create your free account to build with “Chapter-based Product Tutorial”"; "Edit this Clueprint" as a guest (which used to claim a copy was saved to a Workspace they did not have) now opens "Create your free account to save a copy of “…”" with "Create account and save", and lands the copy after sign-up. Sign-in wording follows ("Sign in to build with “…”").
**Section "see all" buttons (19 Oct 2026, review).** "Browse all 8" (Clueprints) and "See all" (Recent projects) now copy live's own "See all": the outlined xsmall Button (24 px, 4 px corners, raised fill, 1 px faint stroke, 12 px label, 14 px chevron), as `.btn.xs`. Label measured on live: "See all", Geist 12/12, weight 400, −1.5% tracking, 6 px to the chevron; width 71.72 px on both. The Clueprints one was "Browse all 8"; it is now "See all" like live, with the count in the hover text. An earlier pass had turned them into 14 px text links, a style live doesn't use; reverted.
**Video card corners (19 Oct 2026, review; measured on live Home).** Live cards are 8 px with the thumbnail inset 7 px on three sides and its own 4 px corners (211 → 197 × 111). Ours ran the image to the card edge, so the 8 px curve showed on the image and looked rounder. Now inset like live, on Recent projects and Clueprints. The input box was already live's 6 px. Card text now matches live too: Geist 13/13, −1.5%, title 500 ink on one line (full name on hover), meta 400 muted; 11 px below the image, 6 px between lines, 12 px at the bottom. The Recent projects type tag (AI video, Slides) is ours and stays.
**Sign-up box: SSO beside Google (19 Oct 2026, review).** The box had demoted SSO to a small grey "Use SSO" link under the password, with no evidence for it. Live, and our Sign in and Sign up pages, put Google and SSO side by side as equal buttons; the box now does too ("Google" | "SSO", live's labels). "Forgot password?" (sign in only) sits right, under the password, like the Sign in page.
**Onboarding recheck (19 Oct 2026).** Walked the journey against the research (research/onboarding-research.md §10). Fixed: the first-run plan no longer shows "Uses Sonnet 5.5 · Ask · … Change these in the box below" (there is no box below in focus mode); "Your first video is on us" once on the plan, not three times; the Projects tip says "Your video is ready" once it is; Home shows one next step (Watch it, then brand); new projects get a short name from the brief (`shortTitle`, e.g. "How to create your first project") instead of the whole brief.
**Verify-email strip in the full app (19 Oct 2026).** Before, the "verify your email" note lived only in the focus-mode top bar, so once the full app appeared the user learned about verification only when Share asked for it. Now `vStrip()` uses live's announcement strip, measured on live: full width above the app, inverted background (oklch 0.24 in light), 41 px (`--strip-h`), centred 14 px/500 white text with a 17 px icon (new `mail` icon), the whole strip one button, no close (like live). It opens the verify box (Change email, Resend, I've verified), and verifying removes it. When: from the moment there is a finished video to share until verified; not while the first video builds, and not while the Projects tip is showing (one hint at a time; it appears after "Got it" or leaving the page). Copy: "Verify sam@taskly.io to share your videos. Check your inbox, or open this to resend."; phones: "Verify your email to share". The Clueso AI panel moves down by the strip. Checked at 1155, 768 and 375, light and dark.
**Plan cost row neutral (19 Oct 2026).** The plan's cost row ("Your first video is on us" and "About 150–250 credits") had a pink wash, with no live evidence; pink is for the primary action only, so Build video was competing with it. Now a neutral tint (`--hover`) with a muted icon, in both themes. The amber "not enough credits" row keeps its colour (a warning).

**Hover and pressed states from Clueso's component library (19 Oct 2026, review: "different type of hover states").** Read from live's Button classes and interaction tokens, then measured on our elements with a real pointer. Before, the prototype mixed five styles: background swaps to white (`--raised`, nearly invisible in light), 4% on icon buttons, a hard-coded grey on the dark button, a brightness filter on pink, a stroke and shadow on cards, 22% white on dark surfaces, and no pressed states at all. Live uses one method: a translucent overlay laid on top, 150 ms.

| Component (ours) | Live variant | Hover | Pressed |
|---|---|---|---|
| `.btn`, chips, pills, way cards, job/have cards, See all, select buttons, search | Outlined | 4% overlay, stroke → 4% | 8% overlay, stroke → 10% |
| `.btn.ghost`, `.iconbtn` | Ghost | 8% | 14% |
| `.btn.dark` (New project, Sign up) | Inverted | 10% white overlay | 18% white |
| `.btn.pink`, `.sendbtn` | Brand | 8% black overlay on the gradient | 14% |
| Buttons on the tip and the editor mode bar | Inverted surface | 10% white | 18% white |
| Menu items, rows, nav | Subtle | 4% (nav pill already matched) | 8% |
| Video cards | Project card | Card still; thumbnail darkens 30%, play appears (200 ms) | |
| Example chips (`.choice`) | Outlined | Had no hover; now 4% | 8% |

Tokens: `--ix-hover-subtle`, `--ix-pressed-subtle`, `--ix-hover`, `--ix-pressed`, `--ix-hover-inv`, `--ix-pressed-inv`, `--ix-brand-*`, `--stroke-normal`, `--ix-t`. The overlay is an inset box-shadow, so it sits on gradients and select chevrons, and doesn't need ::before. **Estimated:** dark-mode pressed, standard and inverted values (live's dark theme couldn't be read without changing its setting); dark hover-subtle (6%) was measured earlier. Not changed: text links (underline), colour-only hovers on text, media controls (play buttons), the editor's canvas and layer outlines, the prototype's own review bar. Found by the sweep: Clueprints page cards now carry the full name on hover (titles are one line, like live).
**One "Change brief" (19 Oct 2026, review: "same CTA twice").** The first-run plan showed a "Change the brief" link at the top and a "Change brief" button on the plan card, both doing the same thing. Now one per state: with a plan, only the plan card's button (next to Build video, as on live's plan card), and in first run it returns to the box with the brief (`frback`); while Clueso asks a question (no plan card), only the top link.

**Clueprint preview, redesigned (19 Oct 2026, review: "think a better design solution").** Kept from live (screenshot 84): the window, title and "by Clueso", the video, a frame strip with the current frame outlined in pink, Edit this Clueprint, Create video (the only pink). Changed, and why:
- **It plays on open, muted** (not with reduced motion). Before, a flat colour block and two play buttons; the point of a preview is seeing the result without effort.
- **The preview looks like a video of this style**: an opening card in the Clueprint's own type and colours, product shots per chapter with a zoom on the key moment, and an end card with a call to action. Chapter captions sit on the video.
- **One timeline: the chapter strip.** Each tile shows its own frame and a progress line; click to jump. Replaces a separate progress bar plus empty black scene boxes. The player keeps only controls that work (play/pause, time); "Muted preview" says why there's no sound.
- **Previous / next by the title, with "1 of 8"** (and ← →), instead of arrows floating outside the video. A typed brief is kept while you compare.
- **"Will this fit?" answered at a glance**: You'll get, You'll need, Good for (`CLUE_META`), beside the video; stacked on phones.
- **Create video attaches the Clueprint to Home's box**, where the brief is written, as before. An inline "What's it about?" field beside Create video was tried and removed (19 Oct 2026, review: "I am not able to understand"): it had only a placeholder for a label, didn't look optional, didn't visibly connect to Create video, and duplicated the box. Guests: Edit this Clueprint opens the sign-up box.
Checked: guest, both themes, 1155 and 375 px, pager keeps focus, Create video.
**Clueprint preview, layout pass (19 Oct 2026, review).** (1) The side column is the decision panel: You'll get / need / Good for at the top, then Create video (pink, full width) and Edit this Clueprint at its foot, aligned with the bottom of the chapter strip. The separate footer row and the empty space under the info are gone (dialog 487 px tall at 1155). On phones it stacks: video, chapters, info, buttons last. (2) The key-moment zoom stays inside the frame (1.12× from the window's centre; was 1.35× and clipped the window's title bar). (3) The caption is a sample voiceover line ("Invite your team and assign the first task."), showing "AI voice and captions" instead of repeating the chapter name; the product window sits clear of it. (4) Lighter progress: a faint 2 px line for finished chapters, only the current one in ink.

**Credits from the first video, as on live (20 Oct 2026, the user's call).** "Your first video is on us" was our proposal, not Clueso's pricing, so it is off: `FREE_FIRST_VIDEO = false` (one switch restores every "on us" path if Clueso adopts it). The credit anxiety it addressed is handled by putting credits in videos: with nothing typed the box says "1,000 credits · about 5 videos" (`credWords`; a video is about 150–250 credits on the default model, so ~200 each); typed, "About 150–250 credits · 1,000 left", as before. The plan shows the cost row; the sign-up box says "The free plan includes 1,000 credits, about 5 videos"; the day-1 email is "Your 1,000 free credits are waiting"; cancelling shows credits used. The first build still gets the Projects tip. Credit numbers are formatted the same everywhere (1,000).

**Workspace name from the account, not "Alex" (20 Oct 2026, review: "an edge case … workspace").** "Alex's workspace" and an "A" avatar were hard-coded (sidebar, account menu, editor menu, Settings), so every new account showed Alex's. The name isn't asked for (it changes nothing on day one); `wsName()` defaults from what we know: a known name → "Sam's workspace"; no name but a work email → the company ("Taskly"); a personal email → "My workspace" with your own initial. Settings → General renames it (saved with the session). Follow-up emails say "Hi Sam," or "Hi there,".

**Workspaces in onboarding (20 Oct 2026, review: "how will the workspace be created").** No workspace step (it changed nothing on day one). Three cases:
- **Signing up alone:** a workspace is created silently with the account, named by `wsName()` (Sam's workspace / the company / My workspace); Settings renames it.
- **Invited (`#/invite`, from the new invite email):** the sign-up page says "Join Taskly on Clueso · Priya Shah invited you. 5 teammates and their videos are already there." Email, Google, SSO or signing in all join the team's workspace (`takeInvite`); no workspace is created, no first-run focus mode, the team's videos are on Home.
- **Company already on Clueso (a work email matching `TEAMS`, e.g. taskly.io):** nothing interrupts the first video; it builds in their own workspace, which is never named "Taskly" (no duplicate). When it's ready, the project page offers "Your team at Taskly uses Clueso (6 people). Move this video to their workspace?" with Move and join / Keep my own. This offer replaces the brand offer (joining brings the team's brand); keeping their own shows the brand offer next, and Settings → General keeps "Join Taskly". Asked after value, like the brand offer; Slack and Notion ask at sign-up instead, which avoids duplicates but adds a decision before value.
Also fixed: the "plan not built" email still said "It's free"; it now says it uses about 150–250 of 1,000 credits.

**SSO "Go back" returns to where you came from (20 Oct 2026, review: "why is this screen").** It was a fixed link to Sign in, so from the sign-up box on the try screen (or Sign up, or an invite) it dropped people on a page they never chose, and hid their brief. Now: from the sign-up box it returns to the try screen with the brief and plan, and reopens the box; from Sign in, Sign up or an invite it returns there; opened directly, it falls back to Sign in.

**Sign in knows the accounts you make (20 Oct 2026, review).** Sign-in only knew the demo account, so signing up as someone else, signing out and back in said "There's no account". Accounts made in the prototype (sign-up page, the sign-up box, Google, SSO) are now remembered in this browser (`clueso-proto-accounts`), and sign-up says "There's already an account" for them too. The prototype keeps one workspace's work at a time, so signing in as a different account you made opens its workspace fresh. Errors sit under their own field: the email error under Email, "Enter your password." under Password, with focus on that field.

**Google: "Use another account" works (20 Oct 2026, review: "why this here if I haven't logged in before").** The chooser stands in for Google's own screen, which lists the Google accounts signed in to the browser (Clueso history doesn't matter), so Alex Rivera is "the browser's Google account". "Use another account" now opens a Google-style step (email, name; name defaults from the address) and signs in as that person, verified; an account already made here signs back in. The sign-up box's Google button now opens the same chooser (it used to sign in as Alex straight away), and a build waiting in the box still goes to its project page.

**One entry screen: the try screen (20 Oct 2026, decided with the user; supersedes "Try for new browsers, Sign in for returning ones").** Everyone lands on the try screen, signed in before or not. There are no separate Sign in, Sign up or SSO pages: they are boxes over it, and the old links (`#/signin`, `#/signup`, `#/sso`, `#/invite`) open the matching box. A link that needs an account (a project, Settings, Chats…) opens "Sign in to continue" over the try screen and then goes to that link. Sign out (and "Use a different account", "Change email") lands on the try screen; the account's work is kept aside and comes back when it signs in again (the demo account gets its seeded videos). A visitor's typed brief survives opening a box. Signed in, the box links just go to Home.
- "Have an account? Sign in to see your videos" shows only to a browser that has signed in before (it reassures someone who signed out that their videos are there); a first-time visitor sees just the top-right Sign in. The old rule that treated any used browser as "returning" is gone; the review bar's Visitor resets it.

**Onboarding visual communication (20 Oct 2026; in Clueso's own visual language, no new art style).** One still per scene (`sceneArt` / `sceneThumb`: an opening title card with the video's own title, product-window shots like the Clueprint previews, an end card with a call to action) is used at every step, so the person watches the same video take shape:
- **Show, don't tell. The plan is a storyboard:** six scene stills (Hook … Outro) instead of a three-line list, then what's included (AI voiceover, zooms and captions, a step-by-step guide) with icons. Phones: two rows of three.
- **The sign-up box shows what you're about to build:** the video's opening still, title, and "a 1-minute product demo · 6 scenes · about 10 min" above Google/SSO. You're signing up for something you've already seen.
- **The build continues the storyboard:** finished scenes are the same stills (hover to play); the one being built shimmers; the newest one "develops" once.
- **Motion, only where it explains a change:** the storyboard lays out once (staggered, the first time the plan appears), a finished scene develops, the ready check pops once. All off with reduced motion; none replays on redraws.
- **Hierarchy pass, one primary per screen:** try screen (Send, pink only once there's a brief), plan (Build video), sign-up box (Create account and build), building (no pink: nothing to do but wait), ready (Watch it), after watching (Share link). Make guide drops from dark to outlined while the first video builds or is unwatched, so it doesn't compete.
Checked in light and dark, desktop and phone.

**Selected choice in live's accent blue (20 Oct 2026, review: "is this selection style Clueso's?").** It wasn't: a picked example chip had a 1.5 px pink outline. Live marks a picked option (its onboarding goal cards, screenshot 08) with a 1 px blue outline on white, `--color-fg-stroke-accent-normal` = oklch(0.623 0.188 259.8), measured on live. Now `.choice.on` (and `.have.on`) use `--stroke-accent`; dark mode uses a lighter blue (estimate). Pink stays for the primary action, and for the Clueprint player's current frame, which live outlines in pink.
- **Every sign-up box shows what it's for (20 Oct 2026, review: "did you miss visual communication here?").** The card was only on "build"; now each reason has one in the same language: build (the video's still, type, Clueprint if any, scenes, time), save a Clueprint (its opening still, name, chapters, what it needs), join a team (a stack of the team's videos, name, people, videos, who invited you), record (record tile, "About 2 minutes…"), record on your computer (mail tile). Plain Sign up / Sign in have no card (nothing chosen). Titles got shorter because the card carries the name ("Create your free account to save this Clueprint", not the full Clueprint name in a two-line heading).

**Learned from ChatGPT and Gemini, signed out vs signed in (20 Oct 2026).** (1) Visitors use Clueso AI before an account, so the try screen now states the terms quietly at the bottom, as both do: "By using Clueso, you agree to the Terms and Privacy Policy. Clueso is AI and can make mistakes." Signed in it goes (agreed at sign-up). (2) A visitor heading that says what Clueso does and how: "Describe a video, and Clueso makes it" (Gemini introduces itself signed out, then just prompts signed in). Signed in keeps live's "What are we creating today?". Not adopted: the full sidebar for visitors (fine for a chat app's tiny sidebar, not Clueso's), and making Sign in heavier than Sign up (depends on Clueso's new-vs-returning mix). Open, the user's call: both products strip the signed-out screen down; ours offers five ways to start.
- Decided (20 Oct 2026, the user): the visitor screen keeps all five ways to start (box, examples, Upload, Record, Clueprints). Watch "time to first send" in Clueso's data before revisiting.

**Onboarding edge-case sweep (20 Oct 2026).** 46 cases run in the prototype as a fresh visitor, scripted and checked by state and on screen. All pass after the fixes below.
- **Entry, composer, plan (14):** bare URL → try screen; unknown route → try screen; empty and spaces-only brief (Send disabled); 5,000-character brief; HTML in a brief (shown as text, not run); short brief → question → option, and "Something else" → focus on the reply; non-Latin brief ("in the language you wrote in"); a website in the brief (brand offer); offline (brief kept); example chip on/off; change the video type; Change brief (brief back, cursor in the box).
- **Sign-up box (12):** bad email; short password (live count); existing email → "Sign in instead" with the build still waiting; sign-in unknown email / no password; Google another account with a bad email; closing Google keeps the plan; SSO personal / unknown company / Back / "sign up with email"; forgot password with an empty email; Escape keeps the plan; email sign-up builds, unverified.
- **Build, ready, credits, files (13):** cancel (a third charged) → Build again; a second video queues; low and no credits; leaving mid-build (Home line, top-bar chip); Share unverified → verify box; wrong file type; over 2 GB; a good file → upload → plan; record and record-later as a guest.
- **Accounts and links (7):** a visitor with a plan signs in (plan kept); reload with a plan (kept) and mid-build (carries on); a project link signed out → sign in → that project; the same link → a new account; an invite while signed in; the invite again once joined.
**Fixed:**
1. **Change email** signed you out and opened a new sign-up, losing the video. It now changes this account's email in place (checks format and duplicates), re-sends the link, and keeps everything.
2. **An invite opened while signed in** was ignored. It now offers "Join Taskly on Clueso" with the team card (Not now / Join Taskly); opened again after joining: "You're already in Taskly's workspace".
3. **A project link, then a new account**, landed on "This project doesn't exist". A new account goes to Home: "That link is in someone else's workspace: ask them to invite you."
4. **Names cut mid-phrase** ("A product demo for new customers on setting"). `shortTitle` now takes the topic after on/about/showing: "Setting up a project", "Running the weekly review", "How to export a report".
**Not testable here:** real email delivery, real Google/SSO, real file upload and processing, a build that fails partway (the seeded failed chat shows the state), payment.

**Video player dialog cut off (20 Oct 2026, review: "why this looks like broken").** The player was a fixed 720 px inside the standard 520 px dialog, so it overflowed and the dialog scrolled sideways, cutting off the title and progress bar. The dialog now sizes to the player (`min(744px, 100%)`) and the player fills it: 744 px desktop, 736 px tablet, 343 px phone, no sideways scroll. QA missed it because it only checked the page for sideways scroll; `runQA` now also flags any dialog, menu, drawer or panel whose content is wider than itself (`box-hscroll`), and caught the old bug when it was simulated. 13 other dialogs checked with it: none overflow.

**Menu and dialog corners and shadows from live (20 Oct 2026, review).** Measured on live: the Ask/Plan/Auto menu is 6 px with a 1 px stroke at 5% and a soft shadow (0 6 6 4% + 0 2 4 4%), items 4 px; the Clueprint preview dialog is 12 px with the same stroke and 0 24 24 6% + 0 6 13 7%, over a 30% black backdrop. Ours were menus 8 px with a heavier 12% shadow, dialogs (and search) 10 px with a 20% shadow, backdrop 18%. Now tokens `--r-menu`, `--r-dialog`, `--sh-menu`, `--sh-dialog`, `--backdrop` carry live's values; every menu (app and editor) and dialog uses them. Not changed (live not measured): the Clueso AI panel (8 px), the coach tip, toasts, and the backdrop blur.

**Dialog header, close button and edges from live (20 Oct 2026, review: live's Upload videos dialog vs ours).** Measured on live: text block 16 px padding, 4 px gap; title Geist 18/18 500 −1.5%; subtitle 14/20 muted; close is live's outlined Button, 32 px, 6 px corners, 16 px icon, 9 px from the top and right; body and footer 12 px at the sides and bottom; the dialog and menu outline is a real 1 px border. Ours had a borderless 24 px close, an Outfit 16/24 title, a 12/16 subtitle, 14/16/6 header padding, 16 px body sides and a shadow outline. All dialogs share `dh()`, so every dialog now matches: title at 17,17, subtitle at 39, close 32 px at 9/9, body edge at 13, the same as live. QA clean on 10 dialogs (light, dark) and 4 on a phone.

**Storyboard tidy-up (20 Oct 2026, review: "this looks messy").** (1) Six equal tiles that fill the card edge to edge (it left a gap on the right); three per row where the card is narrow (Clueso AI panel, phones). (2) One-line labels on one baseline, full name on hover (two-line labels made a ragged edge). (3) The scenes follow the video type (`SCENE_SETS`): a teaser is Hook, The problem, The reveal, See it work, Who it's for, Call to action; a demo, a training video, a how-to guide and a general video each have their own. Before, every plan showed the Taskly demo's scenes ("Create and assign" in a dashboard teaser). The build keeps the plan's type, so its scenes match. (4) The title card drops the duration and "teaser for": "Our new dashboard", not "30-second teaser for our new dashboard".
- **What the video includes, as one sentence (20 Oct 2026, review: "isn't it confusing?").** The icon row under the storyboard (AI voiceover, Zooms and captions, A step-by-step guide) read as clickable controls, had no label, and was the same for every video, even a teaser, which live makes without a voiceover. Now one plain muted line that follows the type (`includesFor`): demo, how-to and training "Includes an AI voiceover, captions and zooms, plus a step-by-step guide." (the guide part drops if the guide is turned off); teaser "Includes music, captions and animated text."; general video "Includes an AI voiceover and captions."
- **First-video cost, quiet and in videos (20 Oct 2026, review: "a potential hurdle in the aha moment").** Before the first video, the plan no longer shows the grey credits box (the heaviest thing on the card, in a unit the person has never used). It shows one muted line beside Change brief / Build video: "Uses about 1 of your 5 free videos · about 10 minutes", with the exact range on hover ("About 150–250 credits of your 1,000"). Still visible and honest; framed as part of the allowance they already have. After the first video the credits box returns; with too few credits the amber warning and a disabled Build are unchanged. Phones: the line takes its own row above the buttons.

**Plan card hierarchy (20 Oct 2026, review: "still an issue of visual and information hierarchy"; and "note not required").** (1) One header line says what you'll get: "Here's the plan: a how-to guide with a short video" (14/500), Change beside it, instead of a small "Here's the plan" plus a separate "Clueso will make…" sentence. (2) Content: storyboard, then what's included. (3) The decision, set apart by space: cost (and, for visitors, "You'll create an account to build it. Your brief is kept.", aligned under the cost text) on the left, Change brief / Build video on the right; three loose grey lines became one group. The "Nothing is built or charged until you press Build." footnote is gone (the cost line and the Build button already say it); Auto mode keeps its note. (4) End cards follow the type: a teaser "Try it free · Start free", a demo "Try it today · Get started", a how-to "You're all set", training "That's a wrap", a general video "Thanks for watching". Narrow cards and phones stack the decision group above the buttons.

**The sidebar after sign-in (20 Oct 2026, the user's call).** Focus mode (logo, Help, Sign in; no sidebar or top bar) is now for visitors only. Anyone signed in gets the full app from the first moment, sidebar and top bar included, as signed-in ChatGPT and Gemini do; Home still shows the first-run content (examples, other ways to start, Clueprints) until the first video, and the Projects tip still appears when it starts building. Why the change: the try screen now does the job focus mode was for (a clean first screen for someone who hasn't committed); hiding a signed-in customer's navigation made the product look smaller and delayed finding Projects, Clueprints and Brand kit.
- **What changes now that new accounts see the sidebar (20 Oct 2026, review).** Checked every first-run special case and walked a new account through all eight sidebar pages and the top-bar menus. Fixed: the account menu was a focus-mode stub ("Use a different account", "Sign out") and is now the full menu (workspace, Profile settings, Sign out); Help & resources was trimmed to 3 items and is now the full menu, with "How to make your first video" first under Learn until the first video. Visitors keep the trimmed Help. Unchanged on purpose: the composer stays trimmed until the first video (no mode/model/brand pills; the + menu has Record and Attach); a short brief still gets one question; the first plan stays on Home. Fine as is: every page has a sensible empty state for a new account (Projects "No projects yet… Make a video", Chats, Brand kit, Clueprints, Integrations, Settings), QA clean on all; Analytics shows labelled sample data behind Business; the sidebar shows "10 export min · 1000 credits" from the start, as live does.

**Deep check: a new account with the sidebar visible (20 Oct 2026, review: "you need to do a deep check").** Everything a new account can now reach before its first video, used, not just opened; fresh test account per case.
- **Top bar (6):** search for a word (nothing from other workspaces), empty search, New project → Start blank / Record / Upload, the Clueso AI panel (from Projects; Home has the composer instead), a brief from the panel → plan (three columns, quiet cost) → Build → project page with the Projects tip.
- **Pages (9):** Projects (Make a video, New folder, Deleted, Filter), Chats (empty, New chat), Clueprints (preview → Create video; Workspace tab; New Clueprint), Brand kit (Pull from website), Analytics (labelled sample data), seven Settings pages, Integrations. QA clean on all.
- **First video from the new places (5):** Chats → New chat, a Clueprint from the library, Brand kit first then Home (no brand offer twice), New project → Upload, the panel.
- **Moving around (4):** leave a plan and come back; the same plan in Chats; build from Chats then Home (resume line); a second brief while the first builds (normal credits row, as it's the second video).
- **Layout sweep:** every page for a new account, desktop, phone and dark: 0 issues.
**Fixed:**
1. **Start blank project** opened "This project doesn't exist" (it jumped to a seeded demo project). It now creates your own "Untitled project"; its page and editor open.
2. **Clueso AI panel** showed "Pick up where you left off" and suggestions about videos you don't have ("Which videos don't have a guide yet?", "Translate a video"). With no videos it now offers "Help me write a brief for a product demo", "Record your screen", "Which Clueprint fits my first video?", and no empty history.
3. **Search quick actions** offered "Translate a video" with nothing to translate; hidden until there's a video.
4. **The Clueprints tab leaked across accounts** (a new account could open on an empty Workspace tab); each new account starts on Community.

## IA fixes: three dead ends (21 Oct 2026, v=370)

From the information-architecture analysis (`research/ia-analysis.md`, W1–W3).

- **W1. Analytics sample rows no longer lead to missing projects.** "Open project" shows only when that project exists in the workspace; otherwise the row says "Sample video". Before, an account with no videos landed on "This project doesn't exist".
- **W2. The editor links back to its project.** "Back to project" is now first in the editor's logo menu, above live's "Back to Home". Before, the only way back to the project page (versions, guide, share, analytics) was the browser's Back button. The header itself is unchanged, to keep live's look.
- **W3. Folders are visible in Projects.**
  - Folders are one level deep. They show as rows above the projects (with a neutral folder tile), and open at `#/projects/<name>` with a `Projects › Folder` breadcrumb.
  - **New folder** opens a naming dialog. Empty names, a duplicate name, or the name "Projects" (the top level) are refused with an inline error.
  - A folder's ⋯ menu renames it or deletes it. Deleting moves its projects back to Projects.
  - The project row menu's **Move to folder** now works; before, it only showed a toast. The editor's Move to folder uses the same dialog, whose top level is now called "Projects" (it was "Your projects").
  - Searching or filtering at the top level also looks inside folders. Folders appear in ⌘K search.
  - A folder link that no longer exists says so and links back to all projects.
- **Tested:** all of the above in the browser with a returning account, and the no-videos case for W1. QA layout check: 0 issues on desktop and phone (folder rows, folder page, the naming dialog). The user's session was restored afterwards.

## IA fixes: naming and URLs (21 Oct 2026, v=371)

From the information-architecture analysis (`research/ia-analysis.md`, W4–W7).

- **W4. One name for the written step-by-step output: Article.** Live uses "Article" (its editor toggle, its plan's "Article exports" and its help center), so every label now matches:

  | Where | Was | Now |
  |---|---|---|
  | Home chip | How-to guide | How-to article |
  | Projects badge | Guide | Article |
  | Project page section | Step-by-step guide | Article |
  | Project page button | Make guide | Make article |
  | Plan card, emails, AI panel, toasts | guide | article |
  | Analytics, help-center searches column | Clicked guide | Clicked article |

  Search still matches "guide", "SOP" and "how-to" as keywords. Live's own onboarding goal text ("SOPs or step-by-step guides") is quoted as it is.
- **W5. Clueprints are no longer called templates.** Search now describes them as "Recipes for a whole video: look, pacing, voice and structure", matching the Clueprints page. The URL is `/clueprints`, not `/library/styles`. The editor's "Template" tool keeps live's name; it's for scene layouts, a different thing.
- **W6. URLs follow the labels.**

  | Label | Was | Now |
  |---|---|---|
  | Home | `/create` | `/home` |
  | Clueprints | `/library/styles` | `/clueprints` |
  | Brand kit | `/library/brand` | `/brand-kit` |
  | Plan and usage | `/settings/plan` | `/settings/plan-and-usage` |
  | Player and links | `/settings/sharing` | `/settings/player-and-links` |
  | Video defaults | `/settings/defaults` | `/settings/video-defaults` |
  | Language and voice | `/settings/language` | `/settings/language-and-voice` |

  Old links redirect without leaving an extra history entry, and links that need an account return to the new path after sign-in. `route()` maps the new paths to the same internal page keys, so nothing else changed.
- **W7. Settings labels match their pages.** "Player and links" now opens a page headed "Player and links", with View-only links and Embedded player as its two sections (it was headed "View-only links"). Search describes Video defaults by what's on it (AI script, voiceover, click highlights, default voices; there's no captions setting). Settings pages and folders get their own browser titles, for example "Plan and usage · Settings · Clueso (redesign)".
- **Tested:**
  - All 9 old paths redirect to the right page, with the right sidebar item and title.
  - Back after a redirect skips the old URL.
  - A visitor opening `/clueprints` or the old `/library/brand` gets Sign in to continue, then lands on the new path.
  - Searching "template" finds Clueprints with the new description, and the new labels show on Home, Projects and the project page.
  - Layout sweep of every page: 0 issues on desktop, phone, and phone in dark mode.
  - The user's session was restored afterwards.

## IA fixes: one account menu, one name for the docs, Translate (21 Oct 2026, v=373)

From the information-architecture analysis (`research/ia-analysis.md`, W8–W10).

- **W8. One account menu.**
  - The editor's avatar opens the same menu as the app's workspace button: workspace, you, theme, Profile settings, Sign out (`accountMenu()` in app.js). Before, it had Help center, Chat with support and Sign out only.
  - Help now lives only in the Help button, in both places.
  - The docs link is called **Help center** everywhere, as live's help.clueso.io is. It was "Knowledge base" in the app's Help menu.
- **W9. Chats is tied to Clueso AI by name.** The Chats page title reads "Chats · Your conversations with Clueso AI", in the same style as the Clueprints subtitle. The panel already linked its history to Chats ("All chats", and Full screen "opens this conversation on the Chats page"), so no other change was needed.
- **W10. Translate has a door before your first project, and it works.**
  - "Translate a video" is in the New project menu and in search's quick actions for everyone.
  - The dialog takes an upload or one of your projects. The project you're on is preselected when you open it from a project page or the editor.
  - With no projects, the picker is hidden and the subtitle says to upload.
  - **Bug fixed while doing this:** Translate always sent people to the demo project `p1` with a fixed "Spanish version added" toast. That was a dead end for new accounts. It now adds the chosen language under the right project. An upload becomes a new project with the language version under it.
  - It refuses a language the project already has, and it says what's missing if nothing is chosen.
  - The output language and the chosen project are kept when the rules panel opens or closes.
- **Tested:**
  - The account menu in the app and the editor is identical, theme works in both, and Profile settings from the editor opens Settings › Profile.
  - Help center is in both Help menus. New project shows Translate.
  - Translate was tested from a project page (preselected, French added), a duplicate language (refused), and a new account (no picker, error, upload, new project with its Spanish version, shown nested in Projects).
  - Layout: 0 issues on desktop, phone and phone dark, including the dialog and the editor menu on a phone.
  - The user's session was restored afterwards.

## Phone experience (21 Oct 2026, v=378)

The phone layout (≤760px) was rebuilt as a phone experience modelled on the mobile apps of Claude, ChatGPT and Gemini, not a squeezed desktop. The user chose two things: the editor becomes **review and quick edits**, and navigation is a **drawer**.

**Evidence and limits**
- Live Clueso's phone layout couldn't be checked. The original audit left mobile out, and the live tab had signed out (it redirects to sign-up). Nothing here is copied from live.
- The patterns come from the three AI apps:
  - a ☰ drawer with recent chats;
  - a short top bar (menu, title, new);
  - the composer pinned to the bottom;
  - full-screen conversations;
  - bottom sheets for menus;
  - artifacts shown as previews, not editors.
- Sizes follow Apple's HIG: 44pt touch targets, and 16px inputs so iOS doesn't zoom on focus.

**What was wrong on a phone before**
- The Home composer sat at the top, with a "Tab" key hint that phones don't have.
- A conversation was a card inside a page, under the page header.
- Projects was a desktop table running off the right edge, with no reachable row actions.
- The editor was the full desktop editor stacked about four screens tall.
- Menus were small popovers, and the menu button was "⋯".

**What's built**
- **Top bar:** ☰, the page name (the logo on Home), Clueso AI (where the panel applies), and New project as ＋. Search and Help move into the drawer.
- **Drawer:** Search, the six sections, the 5 most recent chats (with a dot when one needs you), the usage meter, Help & resources, Integrations, Settings and the account.
- **Bottom sheets:** every menu and picker (`popover()` on phones) opens as a full-width sheet with a grab handle; tapping outside closes it. Dialogs rise from the bottom, and search fills the screen.
- **Home:**
  - The greeting comes first, then the examples (first run), then the other ways to start and recent projects.
  - The composer is pinned to the bottom.
  - Recent projects swipe sideways.
  - The composer's controls fit one row: the brand pill shows its colour dots only, and the cost sits on its own line.
  - The typed-out suggestion and its Tab hint are replaced by a normal placeholder.
  - The visitor's screen (focus mode) gets the same layout.
- **Chats:**
  - The list is one screen.
  - An open conversation replaces the top bar with its own header (back, title, ⋯), and its reply box is pinned to the bottom.
- **Clueso AI:** a full-screen sheet with the same compact composer.
- **Projects:**
  - A single-column list: thumbnail, name, badges, then length and edited time underneath.
  - The ⋯ row menu always shows, and versions stay nested.
  - Search spans the full width.
- **Clueprints:** two compact columns.
- **Editor (phone):**
  - Back to the project, the title, and the project menu.
  - The player, with a play button and progress.
  - **Script / Article** tabs. Each scene's words are editable, tapping a scene plays from it, and changed scenes are marked with a "Generate speech" banner.
  - **Ask Clueso AI for a change**, with the scene as context, and **Share**.
  - A note says the timeline, layers and design tools are on a computer.
  - Playback keeps the reader's scroll position.
- **Buttons** on phones are 40px tall with 14px labels.
- **Rotating or resizing** across 760px re-renders the page.

**Fixed along the way**
- At 320px, recent-chat names, a scene header and the Clueprint preview caption were cut off or wrapped. They now truncate cleanly or wrap to two lines.

**QA**
- `qa.js` now accepts a pinned (sticky) bar covering content that scrolls under it.
- Layout sweep of every page and state: 0 issues at 375 (light and dark), 320, 768 (tablet keeps the desktop layout) and 1280.
- Tested by hand at 375: drawer, recent chat, New project sheet, Home composer, starters and the first plan as a visitor, conversation, AI panel, Projects, Clueprints, project page, and the editor (play, edit text, scene jump, Article, menu sheet, Share, Ask AI).
- **Not tested:** a real phone. The on-screen keyboard pushing the composer up, safe-area insets on a notched phone, and touch gestures (swipe to close the drawer, long-press) need a device.

## Deployed on GitHub Pages (21 Oct 2026, v=379)

Live at https://lkb00.github.io/Clueso-Redesign/, served from the `main` branch of LKB00/Clueso-Redesign. The repo holds only the five files the prototype runs on.

**Fix for Pages:** the demo-account sign-in reloaded the page at `/?s=…`, which on Pages is the account's root site, not the prototype. It now reloads at the current path (`location.pathname`).

**Checked on the live site:**
- The visitor Home loads.
- A starter builds a plan.
- A link that needs an account opens Sign in.
- The demo sign-in reloads under `/Clueso-Redesign/` with its 3 projects.
- No console errors.

**Keep in mind:**
- The site is public.
- Each visitor's work is kept only in their own browser storage.
- Pushing to `main` redeploys the site.

## Live site shows only the product (21 Oct 2026, v=381)

Decided with the user: the deployed site keeps only a scenario switcher.

**Where review mode shows.** It's on at localhost and on any URL with `?review=1`; it's off on GitHub Pages (`REVIEW` in app.js). Review mode covers:
- the improvements bar;
- its numbered markers and list;
- the follow-up emails page (`#/emails`).

**On the live site:**
- One small **"Viewing as: …"** button. Its sheet switches between Visitor, New user and Returning user.
- On phones it sits under the top bar, clear of the pinned composer.
- `#/emails` goes to Home.

**Fixed:** switching from Visitor to a user state left the account blank, with no name or email. It now signs in as the demo account (Alex Rivera). This applies locally too.

**Checked on the live site:**
- No review bar, markers or list, and no emails page.
- All four switches work: Visitor → Returning (3 projects) → New user (empty) → Visitor.
- No console errors.

**Checked locally:** the full review bar is unchanged.

## Test-email suggestions (21 Oct 2026, v=383)

Asked for by the user: since this is a prototype, focusing an email field lists emails to try, like a browser's autofill list. Each email leads down one path. The list appears in the sign-up and sign-in box, on the SSO screen, and in Google's "Use another account" form.

| Where | Emails | What each shows |
|---|---|---|
| Sign up | `new.userN@gmail.com` | A new account with a personal email |
| | `samN@taskly.io` | A work email whose team is already on Clueso (team offer) |
| | `leeN@northwind.com` | A work email, with the brand pulled from the company website |
| | `alex.rivera@gmail.com` | An existing account (shows the error) |
| Sign in | `alex.rivera@gmail.com` | The demo account, with videos |
| | up to 2 accounts made in this browser | Signing back in to them |
| | `nobody@gmail.com` | No account (shows the error) |
| SSO | `jo@acme.io` | A company with SSO |
| | `sam@taskly.io` | Taskly: SSO, and the team is on Clueso |
| | `pat@northwind.com` | A company without SSO |
| | `you@gmail.com` | A personal email, so no SSO |

**How it behaves**
- **New-account emails** take the next unused number (N), so they always make a new account.
- **Picking one** fills the email and the test password `prototype-123`, then moves focus to the submit button.
- **Typing** filters the list. **Keyboard:** ↑↓ move, Enter picks, and Escape closes the list only (not the dialog).
- **Accessibility:** the field is a combobox and the list is a listbox.
- **Layout:** the list sits in the flow under the field, pushing the form down. That way a dialog's edge, a bottom sheet or the phone keyboard can't cut it off.

**Tested:**
- The Taskly sign-up creates the account and gets the team offer.
- The sign-in and SSO lists show the right emails.
- Keyboard picking and filtering work.
- Phone and desktop layouts: no clipping, and the dialog doesn't scroll.
- On the live site: the list shows, with no console errors.

## Phone Home tidy-up (21 Oct 2026, v=384)

- **The four examples** form an even 2 × 2 grid of 40px buttons. Before, they wrapped 3 + 1, leaving "Launch teaser" alone on a row.
- **The Clueprint section** sits 28px below the ways to start. Desktop's 72px margin had left an empty band on phones.
- **Checked:** 0 layout issues at 375 and 320, for both the visitor and the new-user Home.

## Email suggestions reworked as native autofill (21 Oct 2026, v=387)

The user rejected the v=383 version. It was an inline panel inside the form, headed "Test emails · prototype", with a description under each email. That made it look like part of the product. The user asked for what the browser's own autofill does.

**What it is now**
- A small floating list of previously used emails under the field, just the addresses, with no header or descriptions.
- It's attached to the page body (`position: fixed`), so a dialog's edge doesn't cut it off.
- It matches the field's left edge and width, 4px below it.
- It stays below the field and scrolls when there isn't room. It only flips above when there's almost no room below.
- It follows scrolling, resizing and the dialog's opening animation, and closes with the dialog.
- Typing filters by prefix, as autofill does.

**Which emails appear**
- **Sign-up:** `new.userN@gmail.com`, `samN@taskly.io`, `leeN@northwind.com` and `alex.rivera@gmail.com`.
- **Sign-in:** the demo account, plus up to 2 accounts made in this browser.
- **SSO:** `jo@acme.io`, `sam@taskly.io` and `pat@northwind.com`.

**Kept from v=383:** picking an email fills the saved password, keyboard ↑↓ Enter Esc work, and the field is a combobox for screen readers.

**Checked:** on desktop and phone, the list lines up with the field and the dialog doesn't scroll. Keyboard picking works, and the list closes with the dialog.

## Live site keeps itself current (21 Oct 2026, v=388)

**The problem.** The user saw the improvements list ("What changed on this screen, and why") on the live site after v=380 had removed it. A fresh load of the live site showed none of it. The page they were looking at was an older copy: either a tab opened before v=380, or a page the browser reused (GitHub Pages allows browsers to cache it for 10 minutes).

**The fix.** The deployed site (not localhost) checks for a newer deploy:
- 1.5 seconds after loading;
- whenever its tab is focused or shown again.

It fetches `index.html` without the cache and compares the `app.js?v=` number with the one it's running. If they differ, it saves the work in progress and switches to `?v=<new>`, a new address that skips the cache.

**Tested on the live site:** a simulated newer deploy made the page switch on focus. After switching, it ran the current version with no review bar or list, and didn't loop.

## "One question" row fixed (21 Oct 2026, v=389)

**The problem.** The question, its four answers and the × shared one flex row. At around 900px the answers squeezed between the text and the × and wrapped 3 + 1.

**The fix.**
- **Desktop:** the question and × sit on the first line, with the four answers together on the line below. At 900px all four fit in one row.
- **Phones:** the answers form a 2 × 2 grid of 40px buttons, and the row moves up under the greeting.

**Checked:** 900px and 375px with 0 layout issues; live on GitHub Pages.

## Phone, second pass: fixed bars, calmer Home (21 Oct 2026, v=390)

From the user: making it responsive isn't enough. The top bar and the bottom should be fixed, nothing should be cropped, and it shouldn't feel overwhelming.

**Fixed bars**
- **Screen height:** on phones the app is exactly the visible screen (`100dvh`). With `100vh`, mobile browsers' toolbars could hide the bottom.
- **What scrolls:** only the content between the top bar and the composer.
- **The composer** is a fixed bar at the bottom: a solid strip in the page colour with a soft upward shadow, no rule, above the safe area.
- **Nothing hidden behind it:** the page reserves the composer's measured height (`--dock`, kept current with a ResizeObserver as the box grows while typing).
- **Checked:** scrolled to the end at 320 × 640, the last content sits above the bar for both a visitor and a returning user.

**A calmer Home** (every way to start is kept, as decided earlier with the user)
- The second logo above the greeting is gone; the top bar already has one.
- The ways to start are compact rows (56px tall), with a one-line description that ends in "…".
- The Clueprints row is one swipeable row of smaller cards, and its subtitle is hidden.
- The recent-project cards are smaller (62% of the width).
- **Result:** the visitor, new-user and returning Home each fit on one 375 × 812 screen, apart from about 10px.

**QA:** `qa.js` now treats the phone composer as a pinned bar and accepts the deliberate one-line descriptions. Layout sweep: 0 issues at 375 and 320. Live on GitHub Pages.
