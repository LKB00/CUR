# UX review of the prototype (17 Oct 2026)

A researcher's pass over the redesign prototype after the cross-check and edge-case fixes. I walked onboarding, Home, the Clueso AI page and panel, the project page and the phone layout, as a first-time user and as a returning one. Status: R1 to R4 were built on 17 Oct 2026 (see the prototype README). R5 to R17 are open.

Severity: **High** = blocks or misleads on the main path · **Medium** = friction or a broken promise · **Low** = polish.

## High

| # | Area | Finding | Evidence | Proposed fix |
|---|---|---|---|---|
| R1 ✓ built | Whole prototype | **First-time and returning user are mixed in one state.** Right after onboarding, a "new" user lands on Home with three recent projects, "2 of 4 done", and conversations already in Clueso AI. The first-run guidance (the "how it works" strip) never appears, because the workspace already has videos | Walked onboarding → Home. A founder reviewing the story will see a new user who already has work | Two scenarios, chosen from the review bar: "New user" (empty workspace, first-run strip, empty states) and "Returning user" (today's data). Onboarding leads into the new-user one |
| R2 ✓ built | Clueso AI | **Two controls named "Clueso AI" do different things.** The nav item opens the page with all conversations; the top-bar button opens the panel about the current screen. Same label, same icon, different result | Nielsen #4: the same name should mean the same thing. We fixed the same problem for the avatars | Built differently, to keep live's names: the nav item is "Chats" (live's name for the list) and the button stays "Clueso AI" |
| R3 ✓ built | Clueso AI panel | **Floating covers the page's main action.** In Floating view at 1155 px the panel sits over the project page's Share and Open editor buttons and the whole right column | Measured: Share at x 1053–1123, panel from x 767. Live does the same; it's the problem the redesign set out to fix | Floating gets a shorter, draggable window anchored bottom-right, below the page toolbar, so header actions stay visible. Sidebar stays the default from 1100 px |
| R4 ✓ built | Builds | **No way to stop a build.** Once a build starts (or is queued) there's no cancel, though it spends 150–250 credits and takes about 10 minutes | Nielsen #3 user control and freedom. The queue added today makes this more likely to matter | "Cancel build" on the project page and in the conversation, with what's refunded stated ("Credits for unfinished scenes aren't charged" only if Clueso confirms that's true; otherwise state what is charged) |

## Medium

| # | Area | Finding | Evidence | Proposed fix |
|---|---|---|---|---|
| R5 | Home prompt | **The suggestion rotates forever** (every ~4 s) with no way to pause, while people read and decide | WCAG 2.2.2 Pause, Stop, Hide (Level A): auto-updating content over 5 s needs a pause. Live does the same | Stop rotating after 3 suggestions or on hover and focus. Keep Tab to accept |
| R6 | Builds | **"We'll notify you" with no channel.** The build card says "You can leave; we'll notify you when it's ready", but the only notice is an in-app toast, which nobody sees after closing the tab | The promise sets an expectation the product can't keep (Nielsen #1, honest status) | Say how: "We'll email you at alex.rivera@gmail.com when it's ready", with an opt-out. Or drop the promise |
| R7 | Clueso AI panel | **The panel's "Pick up where you left off" lists unrelated conversations.** On a video's page it shows chats about other projects, above the help for this video | The panel's job is "help with what's on screen" (our own model) | On a project, show only that project's conversations, or none. Keep the full list on the Clueso AI page |
| R8 | Clueso AI panel | **Floating and Sidebar look almost the same.** Both are a full-height column on the right; the only difference is whether the page moves | Users can't tell which view they're in without reading the menu | Covered by R3: a smaller floating window makes the two clearly different |
| R9 | Phone | **The New project button is a bare chevron**, and the nav opens from a "···" icon | A chevron alone doesn't say "create". Three dots conventionally mean "more options", not navigation (NN/g) | Show "+" with "New" on phones, and use a standard menu icon (or the Clueso logo) to open the nav |
| R10 | Phone | **The project title appears twice at the top**: in full in the breadcrumb, then as the heading | Takes about a fifth of the first screen on a phone | On phones, the breadcrumb shows only "‹ Projects" |
| R11 | Onboarding | **Four jobs don't cover everyone Clueso's own goals list covers**: slide-deck videos, translation and motion graphics have no option. People with those jobs can only pick "Not sure yet" | Live's goals list has 7 entries; the redesign cut to 4 for Hick's law | Keep 4 visible, add a fifth "Something else" that opens the three others as small options. Or map them into the 4 ("Training videos" to include slides) and say so in the descriptions |
| R12 | Brand | **The Clueso default colours are invented.** Black, white and two greys are placeholders; live has no default kit | Credibility with the founders: every other value in the prototype is from Clueso | Mark it as a proposal in the decision log, or use Clueso's actual neutral template colours if their editor has them |

## Low

| # | Area | Finding | Evidence | Proposed fix |
|---|---|---|---|---|
| R13 | Onboarding | Two exits on step 1: "Skip" (top right) and "Not sure yet" (bottom left) | Both leave without an answer | Keep "Not sure yet" (it's an answer); make Skip skip the whole onboarding, and say so |
| R14 | Search | The shortcut always shows ⌘K, including on Windows | Platform conventions | Show Ctrl K on Windows and Linux |
| R15 | Phone | Composer controls are 28 px tall | WCAG 2.5.8 needs 24 px (met); Apple and Google recommend 44 to 48 px for touch | 36 px on touch screens |
| R16 | Clueso AI panel | The video shows twice as context: "On: Taskly…" in the header and again as a chip in the composer | Repetition | Keep the removable chip (it's actionable); drop the header line or make it the chip's label |
| R17 | Analytics | Sample data still lists sample projects after they're deleted | It's labelled sample data, so low risk | Build the sample from current projects, or keep it static and say "example workspace" |

## Already in the doc backlog, not repeated here

Reload during a build loses it (no server in the prototype).
