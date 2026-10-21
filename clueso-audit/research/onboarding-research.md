# Onboarding: what it's for, how to target it, and where Clueso and our prototype stand

19 Oct 2026. Sources at the end; vendor claims without primary data are marked as such.

## 1. What onboarding is for

Onboarding has one job: get a new person to the product's core value for themselves, as fast as possible. Everything else (tours, profile fields, checklists) is only useful if it shortens that path.

Three moments, each with its own measure (Reforge's setup / aha / habit framing, attributed to Shaun Clowes):

| Moment | What it is | For Clueso | Measure |
|---|---|---|---|
| Setup | The minimum the user must do before value is possible | Give Clueso something to work from: a recording, slides or a doc, or a brief | % who complete setup |
| Aha | The first time the user experiences the core value | Watching a polished video of **their own** product that they didn't have to edit | Activation rate (aha ÷ setup) and time to value (minutes) |
| Habit | Value repeats | Sharing it, then making a second video | 2nd video within 7 days |

Watching a tour or finishing a form is not an aha (Appcues, Kvaliotti). Most onboarding designs only the setup and stops too early.

## 2. What the research says

1. **Tours and "how it works" screens don't help.** NN/g tested deck-of-cards tutorials (70 users, 4 apps): task success 91% with the tutorial vs 94% without (not significant); perceived difficulty was significantly *worse* with it (SEQ 4.92 vs 5.49). Their advice: think twice before building a tutorial; if you need help, make it contextual and interactive.
2. **Teach in context, not up front.** Help that appears where and when it's needed (pull) beats information shown at login (push), which most people skip. One tip at a time, dismissible at no cost.
3. **Target by the job, not the job title.** People adopt software to get a job done; segment the first steps by what the user is trying to accomplish. Role and company size are secondary (Appcues). A single use-case question is enough to branch the flow; 2–3 data points that predict the right path are plenty (Appcues; Donux, vendor).
4. **Answers must change something visible.** Asking and then showing the same experience costs effort and trust. Canva and Notion ask "what will you use it for?" and route to relevant templates (descriptions of their flows; no published lift figures).
5. **Keep questions few and skippable.** No rigorous per-question drop-off benchmark exists; anecdotes report gains from cutting 8 → 4 questions, Dropbox cut signup from 7 fields to 2 and completion rose (Appcues). Ask only what changes the path; let people skip.
6. **AI products: don't open on a blank box.** Users facing an empty prompt freeze and conclude the product is weak. Offer a narrow first success: examples, templates or a guided first run that teaches what a good input looks like (AI UX pattern libraries; SAP's AI onboarding pattern).
7. **Empty states are onboarding.** One primary next step, say what will appear, or offer sample content to explore (NN/g empty-state guidance; Smashing).
8. **Progress helps finish.** A head start raises completion (endowed progress, Nunes & Drèze 2006). Use it for a short checklist tied to real events, not as decoration; check that later quality doesn't drop.
9. **Trigger later help by behaviour, not the calendar** (Appcues).

## 3. Live Clueso, scored

Flow: goals (7, multi-select, "I'm just exploring") → profile (name prefilled, role from 13) → workspace name → "Let's make your first video" (6 ways, Record screen "Recommended for you", Clueprint examples) → extension install gate → prompt modal → Home with a 6-item checklist **and** a "How did you hear about us?" survey.

| Principle | Live | Verdict |
|---|---|---|
| Ends at value | Ends at the first-video picker: close, good | ✔ |
| Targeted by job | Goals drive the "Recommended" tag, but the prompt modal's examples are generic ("Facts about Lewis Hamilton") | Partly |
| Few questions | Goals, role, name, workspace: 4 screens before anything happens; role doesn't visibly change anything | ✘ |
| No surprises | Choosing Record hits an extension install gate with no warning | ✘ |
| Contextual help | 6-item checklist plus an attribution survey on the first Home view, both pushed at once | ✘ |

## 4. Our prototype, scored (honestly)

Flow: "What will you mostly make?" (4 jobs, multi-select, Skip / Not sure yet) → "Here's what Clueso does with product demos" (a before/after example and a 3-step "how it works") → Home with the same 3-step strip again, job-based suggestions in the prompt, and a 4-step getting-started line after the first video.

| Principle | Ours | Verdict |
|---|---|---|
| Few questions, skippable | One question, Skip on both screens | ✔ |
| Answers change something | Only the example and the prompt suggestions | Weak |
| No tutorial | **Screen 2 is a tutorial** (show, don't do) and Home repeats its 3 steps | ✘ (the NN/g finding) |
| Ends at value | Ends on Home with an empty box; the user still has to choose how to start | ✘ (live does this better) |
| Targets the real branch | Asks *what* they make, but Clueso's path depends on *what they have*: a recording, slides, or just an idea | ✘ Missing |
| No surprises | The recording path and its extension aren't mentioned before Home | ✘ |
| Progress | 4-step line, real events, starts at 1 of 4 | ✔ |

Why you're not confident: our onboarding asks a good question and then doesn't use it. It explains the product instead of starting the first video, and it dropped the one thing live does well (ending on a recommended first video).

## 5. Proposal: targeted onboarding for Clueso

Principle: two questions that decide the path, then the first video itself. No tour.

**Screen 1 · "What do you want to make first?"** (single choice, reason stated, Skip)
Product demo · Training video · Step-by-step guide · Launch teaser · Just exploring

**Screen 2 · "What do you have to start from?"** (this is the branch that matters for Clueso)
- *I can record my screen now* → install the recorder here, with the reason ("Clueso records your screen and voice; 1 minute"), then record
- *A recording I already made* → upload, straight away
- *Slides or a document* → upload
- *Just an idea* → the brief, pre-filled with a template for their job and the matching Clueprint attached (e.g. demo → "Chapter-based Product Tutorial")

**Screen 3 is the first action itself**, targeted by both answers, with the cost and time shown before anything runs. *Just exploring* skips to a labelled sample project in the editor (lowest-effort aha).

**After that, nothing is pushed.** Home shows the build progress; the aha is the "Your video is ready" moment. Then one quiet next step at a time (share, add brand, make the guide), triggered by what they've done. Attribution survey: later, after the first share, or never on day one.

**What we'd remove:** the "Here's what Clueso does" screen, the 3-step strip on Home, multi-select on the first question (the path needs one answer; others can come later), and any question that doesn't change the path (role, workspace name: default them, editable in Settings).

**How we'd know it works:** setup completion, activation (first video watched to the end), time to first video, share within 24 h, second video within 7 days; compare by path.

## Sources

- NN/g, Mobile-app onboarding tutorials (70 users, 4 apps): https://www.nngroup.com/articles/mobile-tutorials/
- NN/g, Empty states in application design: https://www.nngroup.com/videos/empty-states-in-application-design-guidelines/
- Appcues, What is user onboarding: https://www.appcues.com/product-adoption-academy/user-onboarding-101/what-is-user-onboarding
- Appcues, Aha moment examples: https://www.appcues.com/blog/aha-moment-examples
- Appcues, Personalize the experience (signals, branching, what to avoid): https://www.appcues.com/product-adoption-academy/value-first-onboarding/personalize-the-experience-with-custom-recipes
- Kvaliotti, User activation, the data-driven approach: https://kvaliotti.substack.com/p/user-activation-the-data-driven-approach
- Setup / aha / habit summaries (Reforge, Shaun Clowes): https://innertrends.com/data-analyses/identify-the-habit-moment-the-key-to-long-term-retention , https://www.news.aakashg.com/p/how-to-measure-onboarding-advanced
- Donux, SaaS onboarding personalisation (vendor; its % figures are unverified): https://donux.com/blog/saas-onboarding-personalization-guide
- Candu, onboarding survey questions (vendor): https://docs.candu.ai/en/articles/8420914-questions-to-include-in-your-onboarding-flow-survey
- Canva onboarding teardowns (no published lift figures): https://uxdesign.cc/onboarding-personalisation-lessons-from-canva-b65e83f06cae , https://clearbit.com/books/data-driven-marketing/onboarding
- Nunes & Drèze (2006), The endowed progress effect: https://ideas.repec.org/a/oup/jconrs/v32y2006i4p504-512.html
- AI onboarding patterns (blank prompt, narrow first success): https://www.aiuxplayground.com/guides/ai-onboarding , https://www.sap.com/design-system/btp/patterns/generative-ai/ai-onboarding/style
- Smashing Magazine, empty states in onboarding (2017): https://smashingmagazine.com/2017/02/user-onboarding-empty-states-mobile-apps

## 6. Decided with the user (19 Oct 2026) and built

Designed from zero, not from live Clueso or our earlier version.

**Goal:** a new person watches a finished video of their own product, made by Clueso, in their first session. Second goal: they share it.

**Learn now (each changes what happens next):** what video they need right now; what they have to start with; optionally their website (logo and colours). **Learn later:** role, team size, workspace name, how they heard of Clueso.

**Show:** one example of the result for their video type, the cost and time before anything runs, progress while it builds, then their own video and one next step. **Don't show:** a tour, every way to create, a long checklist, plans.

**Metrics:** activation (watched their own finished video within 24 h), time to first video, drop-off per screen, activation by starting point, shared within 7 days, second video within 7 days; guardrails: failed builds, credits spent before the first video, skip rate.

Built in the prototype as three screens: *What video do you need right now?* → *What do you have to start with?* → *Make your first …* (record with a live timer / choose a file / edit a brief written for that video type, optional website, what you'll get, cost, Make my video). *Just exploring* opens a sample project marked "Sample project to explore · Make my own". The "Here's what Clueso does" screen and Home's 3-step strip are gone.

## 7. Second design: no wizard (19 Oct 2026, after the user's walkthrough)

The three-screen version expected too much. Walking it as the user: a greeting with a name we didn't have; a video-type question asked before the user knows Clueso's categories, which mostly served us; first-option bias locking in "Product demo"; the hardest start (recording yourself) at the top; no recording on phones; a file that may not be on this device; a third screen with six things at once; a credit cost before any value (loss aversion); an unexplained website field; an unplanned wait; explorers dropped into the densest screen.

What was missed: what users know on day one; effort and emotional cost; choice bias and reversibility; credit anxiety; device and file availability; the wait; that explorers want to watch, not edit; data we don't have; who the questions serve.

Built instead, **the first Home visit is the onboarding**:
1. Sign-up lands on Home. "Welcome, Alex" only when Google gave us the name.
2. A 40-second before/after plays muted (compact on phones), with "Watch with sound" and "Open this sample in the editor" for explorers.
3. The composer is ready, with optional "Start from an example" chips that fill an editable brief: the video-type question as a suggestion, not a gate.
4. Other starts in order of effort: upload (or drop a file anywhere on the page), then record ("about 2 minutes, open your product first"); on phones, "Record on your computer" emails a link.
5. **Your first video is on us**: no cost shown or taken before it (proposal for Clueso to confirm). Cost appears from the second video. *Changed 20 Oct 2026 (user's call): credits work as on live from the first video; the box puts them in videos ("1,000 credits · about 5 videos"). The free first video stays a switch for Clueso to decide. Before the first video the plan shows the cost as one quiet line in videos ("Uses about 1 of your 5 free videos"), not a credits box, to avoid a price pause right before the aha.*
6. The plan says what Clueso will make, inferred from the brief, with **Change** (one click, no going back).
7. The wait says what's happening ("Adding zooms and captions…") and that they can close it and get an email.
8. The result: "Your video is ready to share" and Share link; with a work email, "Use Taskly's logo and colours?" is offered here, not before.
9. One optional question only after the first share: "What will you mostly make?" (changes the suggestions); never on day one.

Metrics unchanged, plus chip use vs free typing, and record starts vs record finishes.

**Focus mode (decided with the user; since 20 Oct 2026 for visitors only, signed-in users get the full app with the sidebar):** the first screen shows only the logo, Help and the account button around the first video. The full app appears when the first video starts building, with one tip pointing at Projects. No "Explore first" escape: the tip teaches where things live once they matter.

## 8. The complete journey built (19 Oct 2026)

One entry screen, the try screen, with Sign in / Sign up / SSO as boxes over it (since 20 Oct 2026; Google, SSO, email) → non-blocking email verification (only sharing needs it) → first-run Home in focus mode → the plan on the same screen → build (full app returns, one tip) → **watch your video** (the aha) → share. Edge cases at each step are listed in prototype/README.md.

## 9. Checked against "How to Win at Onboarding" and built (19 Oct 2026)

Met: teach by doing, no tours, setup deferred, asks after value, empty states, no manipulation, activation over completion. Built from the gaps: (1) try before an account, asked at Build; (2) see the script and each scene while the video builds; (3) Home resumes a stalled first video, and five behaviour-triggered follow-up emails. Still open, and Clueso's to do with real data: (4) an event plan and dashboard for activation, time to value, step drop-off and D7 retention; (5) confirming "watched their own video" predicts who stays.

## 10. Recheck of the built journey (19 Oct 2026)

Walked end to end in the prototype as a new visitor: bare URL → try screen → "Product demo" example → plan → Build → sign-up box → Google → build → ready → watch → share. Then a second run with email sign-up (sam@taskly.io) for verification and the brand offer. Each item below was checked in the running prototype, not read from code.

**Research principles (§2)**

| # | Principle | Result | Evidence |
|---|---|---|---|
| 1 | No tours | ✔ | No tutorial screen anywhere; the first screen is the composer |
| 2 | Help in context, one at a time | ✔ after fix | One Projects tip, on the page where it matters. **Was broken:** it still said "Your video is building" once the video was ready. Fixed |
| 3 | Target by the job | Partly | Example chips (Product demo, Training, How-to, Launch teaser) fill a brief written for that job. The Clueprint row is the same for everyone, not matched to the job |
| 4 | Answers change something visible | ✔ | Chip → brief; the plan names the inferred type ("a 1-minute product demo") with Change |
| 5 | Few, skippable questions | ✔ | No questions before value. A short brief gets one question; the type question waits until later |
| 6 | No blank box | ✔ | Ghost suggestion (Tab), four example chips, Clueprints |
| 7 | Empty states | ✔ | Home with no projects is the onboarding itself |
| 8 | Progress tied to real events | ✔ | Build: script, then 6 scenes, minutes left. Home: "2 of 4 done" from real events |
| 9 | Help triggered by behaviour | ✔ | Resume line (building or ready, not watched), brand offer at ready, follow-up emails triggered by behaviour |

**Decisions (§6, §7)**

| Item | Result | Evidence |
|---|---|---|
| Goal: watch your own video in the first session | ✔ | Ready → "Watch it" on the project page and Home → player → Share link |
| Learn later: role, team, workspace, attribution | ✔ | None of these is asked |
| Show cost and time before anything runs | ✔ | "About 150–250 credits · 1,000 left · about 10 minutes" (since 20 Oct; before, "Your first video is on us") |
| Don't show: tour, long checklist, plans | ✔ | |
| Don't show: every way to create | **Tension** | The first screen has the box, examples, Upload, Record **and** Clueprints (added at the user's request, replacing the before/after). Five starts is more than §6 planned. Watch "time to first send" |
| §7.1 "Welcome, Alex" only with a known name | ✔ | |
| §7.2 a 40-second before/after | Replaced | Swapped for the Clueprint row (user's call). §2.6 is still met; "see the result first" now depends on opening a Clueprint |
| §7.4 starts in order of effort; phone emails a link | ✔ | Upload, then Record ("about 2 minutes"); phone: "Record on your computer" |
| §7.5 first video free; cost from the second | ✔ | "1000 credits left" appears only after the first build |
| §7.6 plan says what it'll make, with Change | ✔ after fix | **Was broken:** "Uses Sonnet 5.5 · Ask · Clueso default · Change these in the box below", but focus mode has no box below, and model names are jargon on day one. Hidden in first run |
| §7.7 the wait explains itself, can close, email | ✔ | "You can close this; we'll email … when it's done" |
| §7.8 brand offer at the result, for work emails | ✔ | "Use Taskly's logo and colours from taskly.io?" next to "Your video is ready" |
| §7.9 one question after the first share | Later than planned | Shows after Getting started is complete (one line at a time), not right after the share. Keep it (only one line at a time), but the doc said "after the first share" |
| Focus mode, then the full app with one tip | ✔ | 0 nav items in focus; 11 after the build |

**Journey (§8, §9)**

| Item | Result | Evidence |
|---|---|---|
| Try before an account, asked at Build | ✔ | Box: "Create your free account to build your video", brief and plan kept |
| Google / SSO / email | ✔ | Google and SSO side by side, as on live |
| Verification doesn't block; sharing needs it | ✔, one gap | The share box says "Verify your email to share". **Gap:** the reminder only exists in the focus-mode top bar, so after the first build the user doesn't see it until they press Share |
| See the script and scenes while it builds | ✔ | Scene strip, "Read the script" |
| Home resumes a stalled first video | ✔ after fix | **Was:** "Watch it" and "Next: add your brand" showed together, two next steps. Now brand waits until the video is watched |
| The aha looks like *their* video | ✔ after fix | **Was:** the project was named with the whole brief ("A 1-minute demo of our product for new customers: how to create your first project, step by step."), and the player showed "A 1-minute demo of" (cut at four words). Now "How to create your first project" (a stand-in for live's AI naming) |

**Fixed in this pass:** the plan's model line in first run; "Your first video is on us" said three times on the plan (now once); the tip's text after ready; two next steps at once; the project name.

**Still open:**
1. ~~The verification reminder in the full app.~~ Built: live's announcement strip, shown once there's a video to share and the Projects tip is gone (prototype/README.md).
2. Five starts on the first screen: kept, the user's decision (20 Oct 2026). Watch time to first send before revisiting.
3. ~~The plan's "first video is on us" row is a pink wash.~~ Now neutral; Build video is the only pink.
4. Clueprints aren't matched to the chosen job.
5. Gaps 4 and 5 from §9: Clueso's data.
