# UX Audit Framework: Onboarding, Information Architecture & Feature Grouping

This is the method I'll follow when you hand me a product. It pulls together standard UX practice (Nielsen Norman Group heuristics, Rosenfeld & Morville's information architecture model, Jobs-to-be-Done, cognitive walkthroughs, card sorting and tree testing) into one repeatable audit.

---

## 0. What I need from you (inputs)

The more of these you give me, the less I have to guess:

| Input | Why it matters |
|---|---|
| Product access: URL, app build, Figma file, screenshots or a screen recording | I need to see the real thing |
| Who it's for: 1–3 primary user types | Every IA decision depends on who is looking |
| The core job: what users come to get done | This sets "time to value" |
| Business goal: activation, retention, conversion, expansion | Tells me which problems matter most |
| Any data: funnel drop-offs, support tickets, reviews, NPS comments | Grounds my findings in real behaviour, not just opinion |
| Competitors (optional) | For pattern benchmarking |

Without data, my findings are **expert review** (heuristic). That's valuable, but they're hypotheses to check with real users, not proof.

---

## 1. Understand the product first (before judging anything)

1. **Write down the jobs to be done.** For each user type: *"When ___, I want to ___, so I can ___."*
2. **Build a feature inventory.** List every feature, setting and screen in a spreadsheet: name, where it lives, how often it's likely used, which job it serves.
3. **Map the current sitemap.** Draw the navigation tree as it exists today, including every place you can reach the same feature from.
4. **Define the "aha moment."** This is the first point where the user gets real value (for example, sending their first invoice or seeing their first report).

The inventory and the sitemap feed every later step.

---

## 2. Onboarding audit

### 2a. Walk through it as a new user (cognitive walkthrough)
At **every step** from landing page to the aha moment, ask:
1. Will the user know what to do here?
2. Will they see the control that does it?
3. Will they connect that control to their goal?
4. After acting, will they know they made progress?

Any "no" is a finding.

### 2b. Onboarding checklist

| Area | Best practice | Red flags |
|---|---|---|
| **Time to value** | Shortest path to the aha moment; delay everything else | Long signup forms, mandatory setup before any value |
| **Signup friction** | Ask only for what's needed now; social/SSO login; ask for the rest later | Asking for company size, role, phone or card on step 1 for no clear reason |
| **Personalization** | 1–3 questions that actually change what the user sees | Survey questions that change nothing |
| **Empty states** | Every empty screen explains what goes here, why it matters and gives one clear next action | A blank table with "No data" |
| **Guidance style** | Learn by doing (checklists, sample data, templates, inline hints) | 8-step product tours that block the screen; tooltips on every button |
| **Progressive disclosure** | Show basics first; reveal advanced options when they're needed | Every feature visible on day 1 |
| **Progress & momentum** | Setup checklist with visible progress; quick early wins | No sense of "how much is left" |
| **Escape & recovery** | Skip, go back, resume later; data is kept | Losing input when going back; no way to skip |
| **Activation hooks** | Invite teammates, connect integrations or import data at the moment it's useful | Asking users to invite people before they've seen any value |
| **Re-engagement** | Emails or prompts tied to unfinished setup steps | Generic "we miss you" emails |

### 2c. Onboarding metrics to request or estimate
- Signup → activation conversion
- Time to first value (minutes or sessions)
- Drop-off by onboarding step
- Day 1, day 7 and day 30 retention for users who did vs. didn't reach the aha moment

---

## 3. Information architecture audit

Rosenfeld & Morville split IA into 4 systems. I audit each one:

### 3a. Organization system: how content is grouped
- **Organized by the user's mental model, not the org chart or the database.** If the menu mirrors internal teams or backend objects, that's a finding.
- Pick a scheme and use it consistently: by task, by object (projects, invoices, users), by audience, or by time. Mixing schemes at one level is a common problem.
- **Breadth vs. depth:** prefer broader and shallower menus. About 5–9 top-level items is a guideline, not a rule; past 3 levels deep, findability drops.
- Watch for **catch-all buckets** ("More", "Tools", "Other", "Misc") that hide important features.

### 3b. Labeling system: what things are called
- Labels use the **user's vocabulary** (check reviews, support tickets and search queries for the words people actually use).
- The same concept has the same name everywhere ("Workspace" vs. "Team" vs. "Organization" for one thing is a finding).
- Labels are **specific and predictive**: a user can guess what's behind them before clicking.
- Avoid jargon, internal codenames, and clever or cute names on core navigation.

### 3c. Navigation system: how people move around
- **Global nav** holds the core jobs; **local nav** covers sections; **contextual links** connect related items.
- The user always knows **where am I, where can I go, how do I get back** (active states, breadcrumbs, page titles).
- **High-frequency actions are 1 click away**; rarely used settings sit deeper.
- One primary place per feature. Shortcuts from other places are fine, but they should point to the same place.
- Consistent placement across screens and platforms (web vs. mobile).

### 3d. Search system
- Is there search where content volume justifies it?
- Does it cover features and settings as well as content (a command palette such as ⌘K)?
- Typo tolerance, recent items, useful "no results" states.

---

## 4. Feature grouping: what goes where

### 4a. Grouping rules
1. **Group by user task or goal**, not by technical type. "Get paid" beats "Payments module + Invoices module + Stripe settings".
2. **Things used together live together** (co-usage). If users always do A and then B, put A and B side by side.
3. **Frequency sets prominence.** Daily features go in primary nav, weekly ones in secondary, one-time setup in settings.
4. **Audience splits.** Admin/billing/team management is separated from day-to-day work.
5. **Objects vs. actions.** Nouns (Projects, Clients) usually make the navigation; verbs (Create, Export, Share) live inside the object as contextual actions.
6. **Settings hygiene.** Group settings into Personal / Workspace / Billing / Integrations / Security. A setting that changes a feature's behaviour should also be reachable from that feature.

### 4b. Prioritization matrix (for each feature in the inventory)

| | **High frequency** | **Low frequency** |
|---|---|---|
| **High importance** | Primary nav / home screen | Easy to find, but secondary (for example, export or billing) |
| **Low importance** | Contextual or inline | Settings, overflow menu, or a candidate to remove |

### 4c. Validation methods (to recommend running with real users)
- **Open card sort:** users group feature cards and name the groups. This reveals their mental model.
- **Closed card sort:** users sort features into my proposed categories. Tests whether the categories make sense.
- **Tree testing:** users find items in a text-only version of the nav. Measures findability without visual design getting in the way. Typical tools: Optimal Workshop, Maze, UXtweak, Useberry.
- **First-click testing:** whether the first click is right strongly predicts whether the task succeeds.

---

## 5. General usability heuristics (applied on every screen)

Nielsen's 10 usability heuristics:
1. Visibility of system status
2. Match between the system and the real world
3. User control and freedom (undo, cancel, back)
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency of use (shortcuts for experts)
8. Aesthetic and minimalist design
9. Help users recognize, diagnose and recover from errors
10. Help and documentation

Supporting laws I'll reference:
- **Hick's law:** more choices means slower decisions, so trim options at decision points.
- **Fitts's law:** important targets should be big and close.
- **Jakob's law:** users expect your product to work like the others they already use.
- **Gestalt proximity and similarity:** visual grouping should match logical grouping.
- **Miller / cognitive load:** chunk information and don't make users remember things across screens.

Also checked: accessibility basics (WCAG 2.2 AA contrast, keyboard access, labels, focus states) and mobile behaviour.

---

## 6. Severity rating (for every finding)

| Severity | Meaning |
|---|---|
| **4 – Critical** | Blocks the core job or activation; fix before anything else |
| **3 – Major** | Causes frequent confusion, errors or drop-off |
| **2 – Minor** | Slows users down or annoys them; there's a workaround |
| **1 – Cosmetic** | Polish |

Each finding is scored on **frequency × impact × persistence** (does it happen once, or every time?).

---

## 7. Deliverables you'll get

1. **Executive summary:** the top 5 problems and the top 5 fixes, ranked by impact vs. effort.
2. **Onboarding flow map:** current vs. proposed, with friction points marked.
3. **Current IA sitemap → proposed IA sitemap**, with the reasoning for each move.
4. **Feature grouping table:** feature → current location → proposed location → why.
5. **Findings log:** screen, issue, heuristic violated, severity, evidence, recommendation.
6. **Labeling fixes:** current label → proposed label.
7. **Validation plan:** which card sorts, tree tests and usability tests to run, with 5–8 sample tasks and success criteria.
8. **Quick wins vs. strategic changes**, as a roadmap.

---

## 8. Usability test plan template (to validate my findings)

- **Participants:** 5–8 per user type (5 usually surface most of the major issues in qualitative testing).
- **Format:** moderated think-aloud, 30–45 minutes, remote is fine.
- **Tasks:** realistic scenarios tied to the jobs, for example *"You just signed up. Get your first invoice sent to a client."* Never phrase a task with the UI's own label.
- **Measure:** task success, time on task, errors, first click, SEQ (single ease question, 1–7), and SUS at the end.
- **Synthesize:** affinity map the observations → themes → severity → fixes.
