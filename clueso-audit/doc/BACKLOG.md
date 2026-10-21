# Before/after doc: updates still to make

The doc (https://claude.ai/artifact/YMG2Q8yU9v7G8KigJnr1ap, version 2) was last published on 17 Oct 2026, before the changes below. The user asked to apply these later, in one pass. To apply them, re-capture the affected screens (see "Screens to re-capture"), update `PAIRS` in `doc/build_doc.py`, run `python3 doc/build_doc.py`, and publish to the same URL.

## Design changes since version 2

| # | Change | Affects pair | Evidence |
|---|---|---|---|
| 1 | One identity menu. The top-bar avatar is gone; the sidebar's workspace button opens workspace, then you (name, email), theme, profile, sign out. Workspace = square, person = circle | Every after-screen (top bar); add a new pair | Live shows two identical blue squares ("UW", "UA") for different things. Gestalt similarity, Nielsen #4 |
| 2 | Composer controls follow live: + (now holds Record your screen first, then Attach files, Add a project, Add a Clueprint), Ask/Plan/Auto, model, brand | `create` | Record and mode had been removed without evidence. Record folded into + because "Choose recording" duplicated "Attach files" and Record is also a card below |
| 3 | Auto builds on send, with the cost shown first; Ask and Plan stop at the plan card | `build` | Hiding the mode had removed Auto (Nielsen #7) |
| 4 | Getting started: one quiet line under the composer ("2 of 4 done · Next: …"), not a card. Hidden until the first video exists. The brand pill isn't highlighted. Progress survives reload | `create` (decision 6) | The card duplicated the prompt (two primary buttons, Nielsen #8). An interim sidebar placement was rejected as low-attention |
| 5 | Brand is shown, not named: swatch on the composer pill, a picker previewing each kit (logo, four colours, font), "Clueso default" when no kit, the same preview in the plan card, live's Brand kit layout with a Preview card | `create` (decision 3), `build`, add a Brand kit pair | Live: toggle with no default; preview only on the Brand kit page; the agent appends "Use our brand kit." to the brief |
| 6 | Clueso AI panel view menu works again; third option named "Full screen" again | `agent` or a new panel pair | The menu threw on click; the rename had no evidence |
| 7 | Phone composer: Send on the right, cost on its own line | Mobile note | Visual fix |
| 8 | Onboarding: the selected card's tick is white (was invisible grey) | `questions` | CSS bug |
| 9 | Nav item renamed to live's "Chats" (speech-bubble icon); the top-bar button stays "Clueso AI" (R2) | `agent`, `sidebar` (icons), every screen's nav | Two controls had the same name and did different things (Nielsen #4) |
| 10 | Floating panel is a smaller draggable window below the page toolbar (R3) | New panel pair, or `agent` | It covered Share and Open editor |
| 11 | Cancel build, Remove from queue, Build again (R4) | `progress` | Nielsen #3. Credits-on-cancel policy needs Clueso to confirm |
| 12 | New user / Returning scenarios in the review bar (R1) | Capture the new-user empty states for an onboarding-to-first-video pair | The demo mixed first-run and returning states |
| 13 | Chats redesigned: one two-line list with status dots at the right edge (yellow needs you, blue unopened result, grey pulsing running, red failed), sort, row menu (Rename, Delete with Undo), New chat restored, a thread body per state (question choices, plan, building, failed with Continue or Start over, done with checklist and follow-ups) | `agent` (replace), add pairs for failed and done states | Live: table with no status; failures only reported; New chat removed without evidence |
| 14 | Chats filters: Status with counts, one Date filter (Last active / Created), Created by only for teams (default Anyone), chips and Clear all | `agent`, new filter pair | Live: no status filter, two 7-option date filters, creator preset to you |
| 15 | Chats Browse / Focus views; Focus is Clueso's full-width chat with a "Made in this chat" panel; sort beside Filter; count line removed, dot on the Chats nav item | `agent`, new Focus pair | Live: full-width chat with a Projects panel |
| 16 | Brand picker on the chat and panel composers; the plan card's Options panel replaced by one "Uses …" line; Record first in every + menu; Focus view drawn as one surface | `build`, `agent` | User review; live chat composer lacks brand; Options duplicated the composer |
| 17 | Editor designed and built: canvas first, scene strip, script that follows the scene with voice states, one Update all, labelled grouped tools, detailed timeline on demand, labelled top bar, Clueso AI with scene context | New pair: live editor (screenshot from 17 Oct) vs `#/edit/p1` | Live: 194 × 110 px canvas, 11 unlabeled tools, blue text, duplicate Generate speech, ~60 unnamed controls |
| 18 | Editor cross-checked against live: live's look (floating cards, compact controls), its playback (skip, previous, next, 1x, Loop, High res), Split, Add, Undo, Redo, a voice per scene, Add pause, Search script, media filters, guide toolbar; the project menu moves to the title | Same editor pair (re-capture `#/edit/p1`) | Live editor, 17 Oct 2026; the first version had dropped these without evidence |
| 19 | Editor back to live's design: icon-only rail in live's order with names on hover (no labels or groups), logo project menu, cloud save icon, icon-only Clueso AI, "Voiceover script" with live's footer and one Generate speech, full-width bottom panel with the scene track | Same editor pair (re-capture `#/edit/p1`) | Review on 18 Oct: the redesign looked too different from live; labels weren't needed up front |
| 20 | Editor flows: every control works as in live (project menu and dialogs, rename, Text and Shapes tools, selection, panels, size, zoom, speed, full-screen preview, timeline settings, Article formatting rail and article AI); AI Rewrite asks first and can be undone | Editor pair; maybe a flows appendix | Live editor, 18 Oct 2026; live's AI Rewrite has no undo |
| 21 | Editor second pass: timeline ruler and playhead, live timecode, inspector, "/" commands, remaining editor preferences; one size scale measured from live (16/8 spacing, 6 px cards, 28 px controls, 24 px chips, 12/14 px text) | Editor pair (re-capture) | Live editor, measured 18 Oct 2026 |
| 22 | Editor side panels at every width: 360/300 px docks, a shared tabbed column at 901–1015, a full-screen sheet on phones; Floating AI above the timeline; the inspector beside or under the canvas | Add a small-screen pair (live at 1024 px with the AI panel off-screen vs the prototype at 1024 and 960 px) | Live resized on 18 Oct 2026 |
| 23 | Script back to live's look: blue for words not yet voiced, banner explains it, Sync Point and pause chips, dashed dividers, editable scene names, menu on hover; status lines, dots and count removed; AI panel Chat history and New chat in the editor | Editor pair (re-capture) | Live page code, 18 Oct 2026 |
| 24 | One type and size scale across the app, from live: 12 px interface, 14 px titles and content, 11 px badges, 28 px controls, 8 px cards, main surface 8 px from the sidebar. Work also survives a reload | Every after-screen (type size changes) | Live, measured 18 Oct 2026 |
| 25 | Pixel audit: whole-pixel line heights (no blurred borders), icons at 12/14/16, one secondary grey, spacing on the 2/4/8 grid | Every after-screen | Audit script, 18 Oct 2026 |
| 26 | One Help menu (Get help · Learn · What's new) replaces live's Help panel, Home footer links and the "New in Clueso" sidebar card; unread dot for new updates. Also: responsive and hover audit fixes | New pair: live footer and sidebar card vs Help menu | Live, 18 Oct 2026 |

## Edge cases found and fixed (17 Oct 2026)

| # | Edge case | Before | After |
|---|---|---|---|
| E1 | Not enough credits for a video (100 left, 150–250 needed) | No warning; Build enabled | Cost line says "Needs about 150–250 · only 100 left" in amber; the plan card explains and suggests the cost-efficient models; Build is disabled |
| E2 | Auto mode with too few credits | Built anyway | Stops at the plan card with the warning |
| E3 | Out of credits (fewer than one reply's worth) | Send enabled | "Out of credits · See plans"; Send disabled in the composer and the Clueso AI reply box |
| E4 | All 10 export minutes used | Share said "uses about 1 of your 10" and allowed it | Says the minutes are used, when they reset, that shared links keep working; Create link disabled |
| E5 | Starting a second build while one runs | The second took over; the first stayed "Building" forever | The second is queued ("Queued" on its page and in the conversation) and starts on its own when the first finishes |
| E6 | Opening a project that doesn't exist | Silently opened a different project | "This project doesn't exist", or "This project is in Deleted" with Open Deleted |
| E7 | Unknown settings page | Empty card, nothing selected | Falls back to General |
| E8 | Unknown address | Showed Home but titled the tab "Welcome" | Titled "Home" |
| E9 | Every project deleted | Projects said "No projects match these filters"; Home showed an empty Recent header; getting started said "share your video" and its Share would crash | "No projects yet" with Make a video (and how many are in Deleted); Recent hidden; the share step hidden; Share is guarded |
| E10 | Corrupted or unknown saved values (panel view, theme, model, progress) | An unknown panel view crashed the page; an unknown theme was applied | Each value is validated and falls back to its default |
| E11 | Brand preview note in dark mode | "No logo" at 1.86:1 on the white preview card | Fixed grey, readable in both themes |

Checked and already fine: HTML in a brief is escaped; a 1,500-character brief doesn't overflow; whitespace-only can't be sent; double-clicking Send makes one conversation; special characters in both searches; renaming a conversation to blank keeps the old title; Escape closes one layer at a time; ⌘K works from inside the prompt; Tab accepts the suggestion.

Known and left as is: a reload during a build loses the build (the prototype keeps no server state); Analytics sample data lists sample projects even after they're deleted (it's labelled sample data).

## Screens to re-capture

`create`, `build`, `agent`, `project`, `projects`, `analytics`, `library` (and a new Brand kit screen), `integrations`, `plan`, `share`, `invite`, `translate`, `search`, `search-empty`, `sidebar`. Every after-screen shows the top bar, which lost its avatar (change 1).

## After the outside Home review (18 Oct 2026)

| # | Change | Affects pair | Evidence |
|---|---|---|---|
| 27 | Getting-started next step is a link (Brand kit / Share); hiding keeps progress with Undo; fainter grid; 32 px section rhythm; video frame thumbnails on Recent; Recent first for returning users; usage bar only when credits are low; cost tooltip | `create` (both scenarios), `sidebar` | Two outside reviews, 18 Oct 2026 |
| 28 | Editor Clueso AI: suggestions grouped (Ask / Suggest / Edit, Enterprise), two shown then More; scope "Scene 4 only" / "the whole video" with put-back chip; resizable panel kept for the session; credits labelled an estimate, not-enough state | Editor pair with AI panel | Outside review, 18 Oct 2026 |
| 29 | Editor cross-check with live: per-scene speech button, live's blue mic and solid V4, bordered footer with AI Rewrite split, "Text active · Exit Esc" mode bar over the canvas, icons matched (Fx, Animation, Collapse, New chat, Prompt hub) | Editor pair (re-capture) | Live screenshots from the user, 18 Oct 2026 |
| 30 | Script rows, second pass: joined scene header (white name, grey voice, AI-voice mic), faint edges, + between scenes, live's Sync Point card (status, frame, Edit, Remove) | Editor pair (re-capture) | User review with live screenshots, 18 Oct 2026 |
| 31 | Project page: status row above both columns (tops aligned), ready banner reworded and wraps, one pink at a time, details under the video on two lines, locked analytics tooltip, chat names without a dangling word | `project` | Outside review, 18 Oct 2026 |
| 32 | Analytics: preview card with Explore Business plan, Clueso's metric definitions with ⓘ, working date ranges and Custom, chart readout by hover and keyboard, previous-period change, sortable right-aligned table, empty state, location "by impressions", searches with dates | `analytics` | Outside review + Clueso help center, 18 Oct 2026 |
