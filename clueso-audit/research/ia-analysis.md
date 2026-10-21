# Information architecture: the redesign prototype

Analysed 21 Oct 2026, prototype v=369 (`prototype/`). Live Clueso (web.clueso.io) was re-read the same day and is used only as the baseline.

**Method**
- Read the prototype's routes, sidebar, top bar, menus, search index and every page (`app.js`, `editor.js`).
- Opened each route in the browser as a signed-in account with no videos.
- Walked 12 common tasks through the structure, the way a tree test would.
- Each finding was confirmed in the code or in the running prototype. None of them are guesses.

---

## 1. The prototype's structure

```
Try screen (visitors)  ── Sign in / Sign up / SSO / Invite open as boxes over it
│
└─ App (signed in)
   ├─ Top bar: Search ⌘K · Building chip · Help & resources · Clueso AI · New project ▾
   ├─ Sidebar, top group
   │   ├─ Home ............................ /create
   │   ├─ Projects ........................ /projects            tabs: All · Deleted
   │   │   └─ Project page ................ /project/:id         Versions · Step-by-step guide · "made with" chat
   │   │       └─ Editor .................. /edit/:id            Video | Article · 9 tools
   │   ├─ Chats ........................... /chats               list + conversation
   │   ├─ Clueprints ...................... /library/styles      tabs: Community · Workspace
   │   ├─ Brand kit ....................... /library/brand
   │   └─ Analytics (lock) ................ /analytics, /analytics/:id   sample data on Free
   ├─ Sidebar, bottom: usage meter → Plan and usage · Integrations (/integrations) · Settings
   │   └─ Settings: Profile | General · Plan and usage · Members | Video defaults · Language and voice | Player and links
   └─ Workspace button: workspace · you · theme · Profile settings · Sign out
```

**Compared with live**

| | Live | Prototype |
|---|---|---|
| Primary nav items | 9, plus 4 widgets | 6, then Integrations and Settings at the bottom, plus a usage meter |
| Agent (Enterprise sales page) | In primary nav | Removed; `/agent` redirects to Chats |
| MCP, GitHub/Bitbucket | MCP in primary nav; repos in Settings > Connections | Both in Integrations |
| Settings | 10 flat pages, profile kept elsewhere | 7 pages in 4 groups, Profile included |
| Pronunciations, Transcriptions, Translations | 3 separate Settings pages | 3 tabs of one "Language and voice" page |
| Page titles | "Clueso Platform" on every page | Named per page ("Projects · Clueso") |
| Translations and AI spin-offs | Loose, unrelated projects | Grouped under their source project |

**What works and should stay**
- **Flatter, task-based primary nav.** Rare setup work (MCP, repos) is at the bottom.
- **Projects is the main object.** Language versions and videos made from a project nest under it. The project page has breadcrumbs and links both ways to the chat that made it.
- **Settings in four groups:** you, the workspace, how videos sound, how they're shared. The glossary-style dictionaries are on one page.
- **Search covers pages, projects and actions.** It has scopes, a real "no results" state, and next steps when nothing matches.

---

## 2. Weak links

Most severe first. "Broken" means a user hits a dead end; "Confusing" means the path exists but its labels or place mislead.

### Broken

> **Fixed in the prototype on 21 Oct 2026 (v=370):** W1, W2 and W3. See the prototype README.

**W1. Analytics sends new accounts to projects that don't exist.**
- *Evidence:* On Free, Analytics shows four sample "Taskly" rows, each with an Open project link. For an account with no videos, `#/project/p1` opens "This project doesn't exist" (checked in the browser).
- *Fix:* Sample rows shouldn't link anywhere. Show "Sample" in place of Open project, or link to the sample project the editor already offers.

**W2. The editor has no way back to its project page.**
- *Evidence:* The project page opens the editor, but the editor's only exit is the logo menu's "Back to Home" (`editor.js:296`). Its title has no breadcrumb. Versions, the guide, Share status and analytics are on the project page. Leaving the editor drops the user at Home, two levels above where they came from.
- *Fix:* Make the editor title a breadcrumb (`Projects › Name`), and add "Back to project" first in the logo menu.

**W3. Folders can be filled but never seen.**
- *Evidence:* The editor's "Move to folder" creates folders and moves projects into them (`editor.js:285`). The Projects page has no folder level, no folder filter and no folder column. Its "New folder" button only shows a toast. The move dialog calls the top level "Your projects", but the page is called "Projects".
- *Fix:* Either show folders in Projects (rows or a Folder filter, with a breadcrumb inside a folder), or remove folders from both places until they're designed. Rename "Your projects" to "Projects".

### Confusing

> **Fixed in the prototype on 21 Oct 2026 (v=371):** W4 (Article everywhere), W5 (Clueprints described as recipes, URL `/clueprints`; the editor keeps live's "Template" name), W6 (label-based URLs with redirects), W7 (Settings headings, search text and per-page titles). See the prototype README. W8–W10 were fixed in v=373 (one account menu, Help center as the docs name, Chats subtitle, and a working Translate door; see the README).

**W4. One object, four names: guide / step-by-step guide / article / how-to guide.**
- *Evidence:*

  | Where | Label |
  |---|---|
  | Home chip | How-to guide |
  | Projects badge | Guide |
  | Project page | Step-by-step guide |
  | Editor toggle | Article |
  | Plan and usage | Article exports |
  | Search | "All your videos and guides" |

  A user who exports an "Article" can't tell that it's the "Guide" badge in Projects.
- *Fix:* Pick one noun. Live uses "Article" in the editor, its plan and its help centre, so the cheapest consistent choice is **Article**, with "step-by-step" as the description. If "Guide" tests better, it has to change everywhere, including the plan limits.

**W5. Clueprint, template and style are used for the same idea.**
- *Evidence:*
  - The Clueprints page says a Clueprint "sets the look, pacing, voice and structure of a whole video".
  - Search describes Clueprints as "Reusable video templates" and finds them on the words "styles, blueprints, templates".
  - The URL is `/library/styles`.
  - The editor has its own "Template" tool, which is a different thing (scene layouts).

  A user who searches "template" gets Clueprints, then finds Templates in the editor that aren't Clueprints.
- *Fix:* Don't use "template" for Clueprints. Describe them as "a recipe for a whole video" in search, keep "Template" for scene layouts, and change the URL to `/clueprints`.

**W6. URLs and labels disagree, and the URLs carry concepts users never see.**
- *Evidence:*

  | Label | URL |
  |---|---|
  | Home | `/create` |
  | Clueprints | `/library/styles` |
  | Brand kit | `/library/brand` |
  | Plan and usage | `/settings/plan` |
  | Player and links | `/settings/sharing` |

  "Library" and "styles" come from an earlier plan that grouped Clueprints and Brand kit; the UI has neither word today. Shared links, browser history and support replies ("go to /library/styles") then name things the user can't find.
- *Fix:* Paths follow labels: `/home`, `/clueprints`, `/brand-kit`, `/settings/plan-and-usage`, `/settings/player-and-links`. Keep redirects from the old paths.

**W7. Settings labels don't match the pages they open.**
- *Evidence:*
  - "Player and links" opens a page headed "View-only links", plus a second card headed "Embedded player".
  - Search describes Video defaults as "voiceover, captions and clicks", but the page has no captions setting.
  - Every Settings page has the browser title "Settings", so tabs and history can't be told apart.
- *Fix:* Head the page "Player and links", with the two cards under it. Correct the search description. Use the browser title "Plan and usage · Settings".

**W8. The editor and the app have different global menus.**
- *Evidence:*

  | | App | Editor |
  |---|---|---|
  | Help menu | "Help & resources" › Knowledge base | Separate account menu: Help center, Chat with support, Sign out |
  | Workspace, theme, Profile settings | In the account menu | Not available |

  The same destination is called "Knowledge base" in one place and "Help center" in the other.
- *Fix:* One account menu everywhere (workspace, you, theme, Profile settings, Sign out). Help stays in the Help button only, with one name for the docs: **Help center**, as live's footer and URL (help.clueso.io) say.

**W9. The assistant has two names in the global navigation.**
- *Evidence:* The sidebar says **Chats**, the top bar says **Clueso AI**, and the Chats empty state says "where you and Clueso AI plan, build and change videos". The prototype already cut live's five doors down to three surfaces with one job each (Home starts, the panel helps, Chats keeps the history). The naming still makes them look like two features.
- *Fix:* Keep the structure. Label the history as the AI's: for example, sidebar "Chats" with the panel's history link reading "All chats". Never call it "Clueso AI chats" in one place and "Chats" in another.

**W10. Translate is hard to start before you have a project.**
- *Evidence:*
  - Translate isn't in the New project menu or on Home. It shows in search only once you have a video.
  - Its own description says "Upload one or pick a project", so uploading a video from elsewhere to translate is meant to work, but there's no door for it.
  - Once a project exists, the doors are good: "Add a language" on the project page, the editor's Captions panel, and the AI panel.
- *Fix:* Add "Translate a video" to the New project menu, opening upload-or-pick.

### Smaller

- **W11. Brand kit holds rare, admin-only settings but has a top-level slot.** It's set once and used through the composer's brand pill. Keep it until we have usage data (the evidence rule), but it's the first candidate to move if primary nav needs room.
- **W12. On phones, the navigation opens from a "⋯" (dots) button.** Dots usually mean "more actions", which is weak information scent for the main menu. A menu icon labelled "Menu" is clearer.
- **W13. Analytics is a locked page in primary nav.** That's acceptable: there's sample data, "Upgrade to Business" and a per-project link from the project page. Check again once real usage shows whether Free users open it.

---

## 3. Tasks walked through the structure

| # | Task | Path in the prototype | Result |
|---|---|---|---|
| 1 | Make a video from a screen recording | Home › Record your screen, or New project ▾ | Passes, 1 click |
| 2 | Find last week's video | Projects › sort by Edited, or Search | Passes |
| 3 | Share a video | Projects › project › Share (also in the editor) | Passes |
| 4 | Add a Spanish version | Project › Add a language, editor › Captions › Translate, or New project › Translate | Passes since v=373, also before the first project (was W10) |
| 5 | Find the step-by-step guide for a video | Projects (Guide badge) › project (Step-by-step guide) › editor (Article) | Passes, but the name changes three times (W4) |
| 6 | Go back from the editor to the project | Logo menu › Back to project | Passes since v=370 (was a fail: W2) |
| 7 | Put videos in a folder and find them later | Row menu or editor › Move to folder › Projects › folder | Passes since v=370 (was a fail: W3) |
| 8 | Fix how "Taskly" is pronounced | Settings › Language and voice › Pronunciations | Passes, 3 levels; good label |
| 9 | Invite a teammate | Settings › Members › Invite | Passes |
| 10 | Connect Claude via MCP | Integrations, or Search "MCP" | Passes |
| 11 | Check views for one video | Project › analytics link, or Analytics › row | Passes; on Free the sample rows dead-end (W1) |
| 12 | Find a template for a launch video | Search "template" › Clueprints, then the editor's Templates are something else | Passes, then confuses (W5) |

Before the fixes, 10 of 12 passed; with W1–W3 fixed, all 12 pass, though tasks 4, 5 and 12 still have the labelling problems below. The two failures are both about the depth below Projects (project › editor, and folders), which is the layer the prototype added.

---

## 4. What to fix, in order

1. **W1, W2, W3: the dead ends.** Each is small to fix: one link, one breadcrumb, and one decision on folders.
2. **W4, W5: naming of the two core objects (Article, Clueprint).** Fix this before testing with users, since labels are what tree tests measure.
3. **W6, W7: URLs and Settings labels follow the visible labels.** Mechanical, with redirects.
4. **W8, W9, W10: one global menu, one name for the docs, a Translate door.**
5. **W11 to W13: watch items.** Decide these from usage data, not opinion.

**Not covered here:** the IA inside the AI panel's modes, the editor's tool rail (9 tools; a separate interaction audit), and plan-gated states other than Free. A real tree test with 5 to 8 users on the tasks above would confirm W4 and W5, which are judgement calls; W1 to W3 are verified defects.
