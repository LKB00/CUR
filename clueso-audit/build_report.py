"""Builds report/index.html for the Clueso UX audit from the findings data below."""
import html
import os

import research_sections as RS
import nav_sections as NS
import decisions as DS
import onboarding_design as OD

OUT = os.path.join(os.path.dirname(__file__), "report", "index.html")
E = html.escape

# Each section: (anchor, title, intro, [figures]); each figure: (img, caption, [findings])
# Each finding: (badge, severity, title, evidence, fix, heuristic)
SECTIONS = [
 ("auth", "Sign-up and sign-in", "The forms are short and offer Google and SSO, which is right for a B2B tool. The problems are in the details: accessibility, a nag about work email, and a testimonial wall that competes with the form.", [
  ("01-login.jpg", "Sign-in page at 1294 px wide", [
   ("1", "minor", "Forgot password link interrupts the keyboard path",
    "The link sits between the Password label and its field, so Tab goes email, Forgot password, password. Neither input has a label element, a name or an autocomplete value, so screen readers announce only the placeholder and password managers have less to go on.",
    "Associate visible labels with inputs, add autocomplete=\"email\" and \"current-password\", and move the link below the field.", "Accessibility, error prevention"),
   ("2", "minor", "Password reveal button is unreachable",
    "The eye button has no accessible name and tabindex -1, so keyboard users can't toggle it.",
    "Give it aria-label \"Show password\" and put it back in the tab order.", "Accessibility"),
   ("3", "minor", "Auto-scrolling wall competes with the task",
    "The right half scrolls testimonials and showcase videos, including tiles titled \"Meet Claude Cowork\" and \"How to create playlists in Spotify\", which read as other companies' products. Every quote is duplicated in the markup, so assistive tech reads it twice. Errors rely only on the browser's native bubbles.",
    "Use one static proof point, pause motion by default, hide the duplicate loop from assistive tech, and show inline error text.", "Aesthetic and minimalist design"),
  ]),
  ("02-signup-personal-email.jpg", "Sign-up after typing a gmail.com address", [
   ("1", "major", "Work-email warning shifts the form",
    "A hint appears under the email field and pushes the password field down mid-entry. The same message returns later as a persistent toast on every onboarding step.",
    "Reserve space for helper text, show it once, and explain the benefit (brand kit from your company site) instead of implying a personal email is wrong.", "User control and freedom"),
   ("2", "minor", "No terms or privacy notice at the point of sign-up",
    "The sign-up button has no \"By signing up you agree to...\" line or links. Legal links exist only on the marketing site.",
    "Add a one-line consent notice with links under the button.", "Help and documentation"),
  ]),
 ]),
 ("onboarding", "Onboarding", "Onboarding has four visible steps plus a hidden fifth (Complete your profile). It asks for the user's name twice, takes 20 seconds to load, and its recommended path ends with a demand to install a browser extension.", [
  ("04-complete-profile.jpg", "Shown right after signing in with Google", [
   ("1", "major", "Asks for a name the identity provider already supplied",
    "The account was created with Google (Profile settings later says \"Password is managed by Google\"), yet the fields are empty. Onboarding step 2 then asks for first and last name again.",
    "Prefill from the Google profile and drop this screen. Keep one name field, in step 2 only, prefilled.", "Recognition rather than recall"),
   ("2", "minor", "The URL stays on /login",
    "The browser shows accounts.clueso.io/login while the page says Complete your profile, so refresh and back behave unexpectedly.",
    "Give the step its own route.", "Visibility of system status"),
  ]),
  ("05-blank-load.jpg", "About 10 seconds after clicking Continue", [
   ("1", "major", "Blank screen, then a pulsing logo, for about 20 seconds",
    "The first app load showed an empty grey page, then a logo. About 930 network requests had fired by the time the goals screen appeared.",
    "Show a branded skeleton with a status line, and split the bundle so the onboarding route loads first.", "Visibility of system status"),
  ]),
  ("07-onb-goals.jpg", "Step 1 of 4: goals", [
   ("1", "major", "Work-email toast follows the user everywhere",
    "The truncated toast \"Switch to your work email so your videos are on-brand...\" sits above every onboarding step and stays on top of modal overlays.",
    "Ask once, inside the brand step, with a clear Skip.", "Aesthetic and minimalist design"),
   ("2", "minor", "40% of the screen is decoration",
    "The \"Make something beautiful\" panel carries no information on this step.",
    "Use the space to preview what each choice unlocks.", "Aesthetic and minimalist design"),
   ("3", "minor", "Progress bar has no visible text",
    "\"Step 1 of 4\" exists only for screen readers.",
    "Show the step count visually.", "Visibility of system status"),
  ]),
  ("09-onb-profile.jpg", "Step 2 of 4: profile", [
   ("1", "major", "Second request for the user's name in under a minute",
    "First and last name again, prefilled this time from the previous screen.",
    "Merge with the Complete your profile screen, or remove both.", "Consistency"),
   ("2", "minor", "Role list is long and unordered",
    "13 roles in no clear order, with mixed naming (\"Customer education & training\" next to \"Learning and development\", plus jargon like \"CXO\").",
    "Group roles by team, order them by frequency, and keep \"Other\" last.", "Match with the real world"),
   ("3", "minor", "\"Looks good, continue\" is disabled with no reason given",
    "The button reads as ready but does nothing until a role is picked.",
    "Mark the role as required, or make it optional.", "Error prevention"),
  ]),
  ("10-onb-role-empty.jpg", "Role dropdown, first second after opening", [
   ("1", "major", "Dropdown opens empty",
    "The menu opens as a blank white box and fills in after 1 to 2 seconds.",
    "Ship the role list with the bundle; it is static.", "Visibility of system status"),
  ]),
  ("13-onb-workspace.jpg", "Step 3 of 4: workspace", [
   ("1", "minor", "Avatar shows U on the left and UW in the preview", "The same workspace gets two different initials.", "Use one initials rule everywhere.", "Consistency"),
   ("2", "minor", "Workspace naming is premature for a solo free user",
    "The name is already prefilled and changeable later, so this step adds a click without adding value.",
    "Create the workspace silently and offer naming when the user invites someone.", "Flexibility and efficiency"),
  ]),
  ("14-onb-first-video.jpg", "Step 4 of 4: first video", [
   ("1", "critical", "The recommended path is a dead end inside the product",
    "\"Record screen, RECOMMENDED FOR YOU\" opens an install modal (next figure) that sends the user to the Chrome Web Store at the final onboarding step.",
    "Recommend a path that works in the browser right now (a prompt prefilled from the chosen goals, or a sample project) and offer the extension when the user first records.", "Time to value"),
   ("2", "major", "Three different language counts",
    "Onboarding says \"40+ languages\". The marketing home page says 80+ in one section and 150+ in another.",
    "Pick one verified number and use it everywhere.", "Consistency"),
   ("3", "minor", "Six choices, two of them irrelevant to a new user",
    "\"Translate an existing video\" needs a video the user doesn't have yet. \"Create from Claude, ChatGPT, or Gemini\" is a developer integration.",
    "Show the two or three options that match the chosen goals, and move the rest behind \"More ways to start\".", "Hick's law"),
   ("4", "minor", "The right panel is the Clueprint gallery, unlabeled",
    "Template cards appear with no heading, so it is unclear whether they can be picked or how they relate to the options on the left.",
    "Label it \"Or start from a Clueprint\" and make the cards selectable.", "Recognition rather than recall"),
  ]),
  ("15-onb-extension-gate.jpg", "After clicking the recommended option", [
   ("1", "critical", "Install wall at the moment of first value",
    "\"Install the free Clueso extension... then come back here\" breaks the session at the riskiest point of activation.",
    "Allow browser-tab recording through getDisplayMedia, or skip ahead to the editor with a sample recording while the extension installs.", "Time to value"),
   ("2", "minor", "Work-email toast stays above the modal overlay", "The toast isn't dimmed with the rest of the page.", "Fix the layering order.", "Visual hierarchy"),
  ]),
  ("16-onb-prompt-modal.jpg", "\"Create with a prompt\" from onboarding", [
   ("1", "major", "Suggestions ignore what the user just said",
    "I chose Product demos and SOPs as a Product manager. The chips offer \"Facts about Lewis Hamilton\" and \"How Spotify recommends music\".",
    "Generate the chips from the onboarding answers (\"Walk through your product's sign-up flow\", \"Turn a process into an SOP\").", "Personalization"),
   ("2", "major", "No cost shown before Create",
    "One prompt-to-video run later cost 250 credits, a quarter of the monthly allowance. Nothing here says so.",
    "Show an estimate next to Create (\"About 100 credits, 900 left\").", "Visibility of system status"),
  ]),
 ]),
 ("home", "Home and first run", "Home leads with a single prompt box, which is a good choice. Around it are up to seven competing elements, and two defaults that quietly shape every video the user makes: the model and the brand kit.", [
  ("18-home-checklist-survey.jpg", "Home a few seconds after onboarding", [
   ("1", "major", "A model picker for people making videos",
    "The default is Opus 5.5. The menu (next figure but one) lists six LLMs with vendor taglines and no cost, speed or quality guidance.",
    "Replace with \"Quality: Fast / Best\", show the credit estimate for each, and keep the raw model list under Advanced.", "Match with the real world"),
   ("2", "critical", "Brand kit is on by default, and it is made up",
    "The brand kit chip is on by default. For a gmail.com sign-up, the kit was built from gmail.com: a placeholder pink logo and a pink accent (next figure). The AI added \"Use our brand kit.\" to my prompt and planned the video in \"brand pink (#D43F8C)\".",
    "Never auto-build a brand kit from a public email domain. Keep the chip off until the user confirms a brand.", "Error prevention"),
   ("3", "major", "Survey interrupts the first session",
    "\"How did you hear about us?\" pops up within seconds and covers the Translate button.",
    "Ask after the first export, or inside onboarding as an optional question.", "User control and freedom"),
   ("4", "major", "Get-started checklist is hidden and loosely defined",
    "It sits collapsed near the bottom of the sidebar under a promo card. Install screen recorder comes after Export a video. Make your first video was ticked by a blank 6-second project.",
    "Put the checklist on Home, order it by dependency, and tick Make your first video only when a video has content and has been played.", "Visibility of system status"),
   ("5", "major", "One plan, three names",
    "The sidebar says \"Free trial\", the upgrade card says \"You are on the free plan\", and Billing says \"Free\". A trial implies an end date; this plan has none.",
    "Use \"Free plan\" everywhere.", "Consistency"),
   ("6", "minor", "Seven things asking for attention",
    "Series A sale banner, What's new card, checklist, upgrade card, survey, work-email toast and a floating chat bubble, all on the first view.",
    "On day one, show at most the checklist and one upgrade touchpoint.", "Aesthetic and minimalist design"),
  ]),
  ("24-brand-kit-gmail.jpg", "Brand kit, never set by the user", [
   ("1", "critical", "\"Pull again from your website: gmail.com\"",
    "The kit was scraped from the email domain. Every company on Gmail, Outlook or Yahoo gets the same kind of junk kit.",
    "Detect public email domains and leave the kit empty with an \"Add your website\" prompt.", "Error prevention"),
   ("2", "critical", "A placeholder logo presented as the user's own",
    "The pink chevron mark will appear in intros and outros of first videos.",
    "Show no logo until one is uploaded or confirmed.", "Trust"),
   ("3", "major", "\"Set during onboarding\", but onboarding never asked",
    "No onboarding step mentioned brand, colors or a website.",
    "Add an optional brand step to onboarding, or change the copy to \"Auto-filled. Review it.\"", "Visibility of system status"),
  ]),
  ("46-model-picker.jpg", "Model menu on the Home prompt", [
   ("1", "major", "The most expensive model is the default, and the menu shows no costs",
    "Opus 5.5, Sonnet 5.5, Astra 6, Sol 6.1, Luna 6 and Terra 5.6, each described by vendor (\"Anthropic's most capable model\"). The help docs say a smaller model costs about half per message, but this menu doesn't say so.",
    "Offer two or three outcome-based options with a credit estimate for each.", "Match with the real world"),
  ]),
  ("19-projects-empty.jpg", "Projects, empty", [
   ("1", "minor", "New folder appears twice on an empty page", "A folder is the wrong first action when there is nothing to put in it.", "Lead the empty state with New project and the start options.", "Minimalism"),
   ("2", "minor", "The header changes between pages",
    "The Clueso AI button is absent on Home but present on Projects, so the header shifts as the user navigates. The browser tab title stays \"Clueso Platform\" everywhere, and showed a stale \"Untitled (1)\" on Home.",
    "Keep the header stable and set a per-page document title.", "Consistency"),
  ]),
 ]),
 ("ia", "Information architecture and navigation", "The sidebar mixes everyday work (Projects), developer setup (MCP), a sales page (Agent), a paywall (Analytics) and assets (Clueprints, Brand kit) at one level. AI is spread over six surfaces, and settings over three.", [
  ("20-agent-upsell.jpg", "Agent, from the main sidebar", [
   ("1", "major", "A primary nav slot spent on a sales page",
    "Agent opens a marketing page whose main action is Book a demo. The feature is Enterprise-only, but free users see it as the third item in the nav.",
    "Remove it from the nav for plans that can't use it. Surface it as an upsell card inside the AI panel or Projects.", "Match between the system and user goals"),
   ("2", "major", "Agent, Chats and Clueso AI blur together",
    "The checklist asks the user to \"Chat with the AI agent\", which actually means Chats, not Agent.",
    "Use one name for the AI you talk to, and a different one for the Enterprise automation.", "Consistency"),
  ]),
  ("21-chats-empty.jpg", "Chats", [
   ("1", "major", "AI lives in six places",
    "Home prompt, Chats, the header Clueso AI panel, Agent, the editor chat and the Article copilot. Each looks a bit different; the article version has no model or mode picker.",
    "Use one AI panel component everywhere. Chats becomes that panel's history, reachable from inside it.", "Consistency"),
   ("2", "minor", "Search and three filters on an empty list", "Filters only help when there are things to filter.", "Hide filters until there are about 10 items.", "Minimalism"),
  ]),
  ("44-clueso-ai-panel.jpg", "Header Clueso AI panel over Settings", [
   ("1", "minor", "The header button collapses to an icon when the panel opens", "The header layout shifts.", "Keep the label, or show an active state.", "Consistency"),
   ("2", "major", "Duplicate of the Home prompt",
    "Same input, mode and model controls. Pressing Esc on its dropdown closed the whole panel. Internally the controls are labeled \"Director autonomy mode\" and \"Director model\", an internal codename.",
    "Make Esc close only the open menu, and use user-facing names in accessible labels.", "User control and freedom"),
  ]),
  ("25-analytics-locked.jpg", "Analytics on the free plan", [
   ("1", "major", "Primary nav item is a locked page",
    "Analytics is Business and Enterprise only. The Video player settings page behaves the same way.",
    "Show a lock badge in the nav so users know before clicking, or move Analytics under Projects as a tab.", "Visibility of system status"),
   ("2", "minor", "The upsell doesn't show what the user would get", "There is no preview of the dashboard.", "Show a blurred sample dashboard.", "Recognition"),
  ]),
  ("22-mcp.jpg", "MCP", [
   ("1", "minor", "\"Watch the setup (1 min)\" is a 2:15 video", "The label and the video length disagree.", "Fix the label.", "Consistency"),
   ("2", "minor", "A developer integration at the top level",
    "MCP is in the main nav while the GitHub and Bitbucket connections live in Settings > Connections.",
    "Group them under one Integrations area.", "Grouping by user task"),
  ]),
  ("23-clueprints.jpg", "Clueprints", [
   ("1", "major", "\"Reusable video templates\", while the editor also has Templates",
    "Clueprints are full-video styles; editor Templates are intro and outro clips; Components are reusable groups. The help center needs a callout box to explain the difference.",
    "Rename the editor items \"Clip templates\", and describe Clueprints as \"Video styles\" in UI copy.", "Match with the real world"),
   ("2", "minor", "The docs describe three tabs; the app shows two", "Personal, Workspace and Community in the help center; Workspace and Community in the app.", "Update the docs.", "Help and documentation"),
  ]),
  ("43-new-project-menu.jpg", "Header New project menu", [
   ("1", "major", "Each entry point offers a different set of start options, with different labels",
    "This menu lacks Create with prompt and Clueprints. \"Upload PPT/PDF\" here is \"Upload slide decks\" on Home. \"Upload videos\" is \"Upload screen recording\" in onboarding. \"Record screen\" is \"Record your screen\".",
    "Define one creation menu and reuse it everywhere, with the same order and labels.", "Consistency"),
  ]),
  ("38-account-menu.jpg", "Avatar menu", [
   ("1", "major", "Settings are split across three places",
    "Sidebar Settings holds workspace settings only. Profile settings is a modal in this menu, and that modal has its own Workspace tab. The help docs send users to the workspace switcher, which only lists workspaces.",
    "Use one Settings area with Profile, Workspace, Billing and usage, Language, and Sharing sections.", "Consistency"),
   ("2", "minor", "Help is reachable five ways",
    "Header Help, Help Center and Chat with Support in this menu, a floating bubble, and a footer link.",
    "Keep one Help entry that opens a panel with docs, chat and what's new.", "Minimalism"),
  ]),
  ("66-cmdk-search.jpg", "Command search for \"translate\"", [
   ("1", "minor", "One page, four names",
    "Search calls it \"Settings → Language translations\", the nav says \"Translations\", the page title says \"Translation Settings\", and pricing says \"Translation glossary\".",
    "Call it Translation glossary everywhere.", "Consistency"),
   ("2", "minor", "Projects that don't match the query still show",
    "Both projects are listed for \"translate\". There is also no action result such as \"Translate a video\".",
    "Filter results and include actions.", "Flexibility and efficiency"),
  ]),
 ]),
 ("settings", "Settings, billing and account", "The settings pages are tidy individually. The problems are a risky join rule, numbers that contradict the pricing page, and costs that only show up after the user has spent them.", [
  ("26-settings-admin-gmail.jpg", "Workspace settings > Admin", [
   ("1", "critical", "Offers to let anyone with a gmail.com address join",
    "\"Who can join this workspace: Anyone with a gmail.com email address\". For a public email domain, choosing it would open the workspace to every Gmail user. I left it on Only people who are invited.",
    "Never offer domain-based joining for public email domains, and add a confirmation step for any domain rule.", "Error prevention, security"),
   ("2", "minor", "Admin, /general, Team name",
    "The nav label, URL and field name all differ for the same page, which is really General.",
    "Label it General, and call the field Workspace name.", "Consistency"),
  ]),
  ("31-usage-seats.jpg", "Billing > Usage", [
   ("1", "major", "Article limit contradicts pricing",
    "0 / 10 articles. The pricing card says 15 article exports a month for Free; the comparison table on the same page says 10.",
    "Use one source of truth for plan limits.", "Consistency"),
   ("2", "major", "1 / 4 seats on a one-user plan",
    "Pricing says Free is 1 user. Billing says \"Upgrade to invite editors\". Yet Users has an Invite users button and the checklist says Invite a collaborator.",
    "Show the real seat limit, and explain on the Invite button what happens on Free.", "Consistency"),
  ]),
  ("64-credits-after-ai.jpg", "Billing > AI Credits after one prompt-to-video run", [
   ("1", "major", "One video used a quarter of the month",
    "Billing showed 100 of 1,000 credits used mid-build; the finished 57-second video reported 250 credits. No screen before the run mentioned credits.",
    "Show remaining credits in the AI panel, an estimate before each run, and a warning at 80%.", "Visibility of system status"),
  ]),
  ("30-ai-credits.jpg", "AI Credits before use", [
   ("1", "major", "No explanation of what costs credits", "Prompts, edits and model choice all cost different amounts, and none of that is shown here.", "Add a short \"What uses credits\" table.", "Help and documentation"),
   ("2", "minor", "Team table with sorting and pagination for one person", "Enterprise UI shown to a solo user.", "Show the table only when there are two or more members.", "Minimalism"),
  ]),
  ("41-profile-workspace-leave.jpg", "Profile settings > Workspace", [
   ("1", "major", "\"Leave\" offered to the only admin of the only workspace",
    "Leaving would orphan the workspace or lock the user out.",
    "Disable it with an explanation (\"Transfer admin or delete the workspace first\").", "Error prevention"),
  ]),
  ("40-profile-modal.jpg", "Profile settings > Profile", [
   ("1", "minor", "Reset Password next to \"Password is managed by Google\"", "The button looks active but cannot work for this account.", "Hide it for accounts that sign in with Google or SSO.", "Consistency"),
   ("2", "major", "Profile lives in a modal with its own Workspace tab",
    "This is the third settings location.",
    "Fold it into the single Settings area.", "Consistency"),
  ]),
  ("32-video-defaults.jpg", "Video defaults", [
   ("1", "minor", "Broadcast jargon in a default setting", "\"Use the legacy SD/PAL color primaries instead of the default Rec. 709 standard\".", "Move it under Advanced and lead with the symptom (\"Colors look washed out after export?\").", "Match with the real world"),
   ("2", "minor", "Toggles have no on or off text", "State is shown by color alone.", "Add text or a check mark to each state.", "Accessibility"),
  ]),
 ]),
 ("editor", "Appendix: editor (beyond navigation scope)", "The editor is capable, and the script-first voiceover loop works. A new user lands in a blank canvas with eleven unlabeled tools, and a stuck preview made playback impossible until I reloaded the page.", [
  ("47-editor-simplified-modal.jpg", "First time opening the editor", [
   ("1", "major", "Tells a brand-new user what they are \"used to\"",
    "\"We've simplified the editor... Classic: What you're used to\". This account had never opened the editor.",
    "Show this only to accounts that used the old editor. New users get Simplified with no prompt.", "Match with the real world"),
   ("2", "major", "The complex option is the default",
    "Continue with Classic is the primary button.",
    "Default new users to Simplified.", "Progressive disclosure"),
  ]),
  ("48-editor-blank.jpg", "Blank project, Classic editor", [
   ("1", "major", "Eleven icon-only tools",
    "Tooltips appear on hover, but 26 of the 81 visible buttons (playback, undo and redo, script controls) have no accessible name at all.",
    "Add labels to the rail (or an expand control) and aria-labels to every icon button.", "Recognition rather than recall, accessibility"),
   ("2", "major", "Blank canvas with no next step",
    "There is no \"Record, upload, or pick a template\" prompt in the empty canvas.",
    "Put the three start options in the empty canvas itself.", "Help users get started"),
   ("3", "minor", "AI suggests \"Polish this video\" for an empty project", "The suggestions don't match the project's state.", "Use suggestions that fit an empty project (\"Draft a script from a topic\").", "Context"),
   ("4", "minor", "Avatar is U here, UA elsewhere", "", "Use one initials rule.", "Consistency"),
  ]),
  ("50-editor-generating.jpg", "During Generate speech", [
   ("1", "minor", "Three loaders and three cancel controls for one action", "A toast, a canvas overlay and the button all show progress at once.", "Show progress on the button only and keep the canvas usable.", "Minimalism"),
  ]),
  ("54-editor-preview-stuck.jpg", "Over 60 seconds after speech finished", [
   ("1", "critical", "Preview stuck on a spinner", "The canvas never rendered and kept spinning. Reloading the page fixed it. The same spinner reappeared during AI generation.", "Detect the stalled stream and reconnect, or show \"Preview paused, Reload preview\".", "Visibility of system status, error recovery"),
   ("2", "critical", "Playback disabled until reload",
    "The console showed repeated EventSource failures (ERR_HTTP2_PROTOCOL_ERROR) and no message to the user. This may depend on the browser I used; verify in Chrome.",
    "Show a reconnecting banner and retry with backoff.", "Error recovery"),
  ]),
  ("52-editor-media-stock.jpg", "Media panel on first open", [
   ("1", "minor", "Opens on the third tab (Stock), not the first", "Upload is under \"In this project\", which isn't selected.", "Open on In this project with Upload first.", "Consistency"),
   ("2", "minor", "\"Photos and videos provided by Pexels\" under a music list", "The attribution doesn't match the content shown.", "Show attribution per media type.", "Match with the real world"),
  ]),
  ("53-editor-templates-saved.jpg", "Template panel", [
   ("1", "major", "Templates, Components and Clueprints", "Three overlapping \"reuse\" concepts.", "Use the naming in the label table below.", "Match with the real world"),
   ("2", "minor", "Opens on the empty Saved tab", "New users see an empty box first.", "Open on Library until something has been saved.", "Help users get started"),
  ]),
  ("56-article-blank.jpg", "Article tab of the same project", [
   ("1", "major", "Blank article even though the video has a script",
    "The marketing site promises \"your documentation is ready\" too, but this project's article is empty, with no Generate article action.",
    "Offer \"Generate article from this video\" in the empty state.", "Help users get started"),
   ("2", "minor", "A different AI panel", "No model or mode controls, and a different layout.", "Use the same panel everywhere.", "Consistency"),
  ]),
  ("59-project-menu.jpg", "Project menu behind the logo", [
   ("1", "minor", "Manual Save next to autosave", "The cloud icon implies autosave, but Save sits in the menu.", "Show a \"Saved\" state and remove the menu item.", "Consistency"),
   ("2", "minor", "Version History sits below Delete Project", "A recovery tool is placed after the destructive action and is easy to miss.", "Put Version History near the top and Delete last.", "Error prevention"),
  ]),
 ]),
 ("ai", "Appendix: AI video generation (beyond navigation scope)", "The prompt-to-video plan was the best part of the session: six timed scenes with voiceover and visuals, and a clear approval step. What follows it is long and opaque.", [
  ("60-chat-plan.jpg", "The AI's plan after my prompt", [
   ("1", "major", "\"Use our brand kit.\" was added to my prompt",
    "My message gained a line I didn't write, which applied the gmail.com brand kit.",
    "Show attached context as a removable chip, not inserted text.", "User control and freedom"),
  ]),
  ("61-ai-video-failed.jpg", "About 1 minute after approving", [
   ("1", "major", "Alarming log while it recovers",
    "\"Ran 4 steps (2 failed)\" with a red warning and \"Couldn't finish this step\". The agent recovered without telling the user.",
    "Hide retries that recover. Show one plain status per scene.", "Visibility of system status"),
   ("2", "minor", "Internal files exposed", "\"taskly/plan.md\" appears in the log.", "Hide internal files from the log.", "Match with the real world"),
   ("3", "major", "The editor opens with empty scripts", "The user is dropped into a half-built project.", "Keep the user in a progress view until the first scene can play.", "Visibility of system status"),
  ]),
  ("63-ai-video-building.jpg", "About 5 minutes in", [
   ("1", "major", "No estimate and no end in sight",
    "\"Working for 4m 54s\", then \"Thinking for 8m 14s\" when I stopped watching. There was no estimate and no per-scene progress.",
    "Show \"Scene 3 of 6, about 2 min left\", and let the user leave and get a notification when it's done.", "Visibility of system status"),
   ("2", "good", "The visuals are strong", "The scenes that rendered look professional and on-message.", "Lead with these in onboarding.", "Delight"),
  ]),
 ]),
 ("share", "Sharing, export and project list", "The share dialog is clean. It hides the costs and limits that matter most on the free plan.", [
  ("57-share-export.jpg", "Share > Export video", [
   ("1", "major", "No limits shown before export",
    "Nothing mentions the 10 export minutes a month, the watermark or the 1080p cap.",
    "Add a line such as \"Uses about 1 of 10 free minutes; includes watermark\".", "Visibility of system status"),
   ("2", "minor", "Share opens on Export", "Most people who click Share want a link.", "Open on View-only link.", "Match with user expectations"),
  ]),
  ("58-share-viewonly.jpg", "Share > View-only link", [
   ("1", "major", "Creating a link uses export minutes, and the dialog doesn't say so",
    "The help center says view-only links and embeds count toward the export limit.",
    "State the cost on the button.", "Visibility of system status"),
   ("2", "minor", "2K, 4K and 60fps greyed out with no reason", "There is no lock icon or tooltip naming the plan.", "Add a lock and \"Business plan\".", "Help and documentation"),
   ("3", "major", "Show article is on, but the article is empty", "Viewers would see a blank article.", "Default it to off when the article is empty.", "Error prevention"),
  ]),
  ("65-projects-list.jpg", "Projects with two items", [
   ("1", "major", "The filter bar pushes the New folder button off screen", "At 1294 px wide, the button is clipped to its icon.", "Wrap the filters or collapse them into a Filter menu.", "Layout"),
   ("2", "minor", "Seven filters for two projects", "", "Show filters progressively.", "Minimalism"),
   ("3", "minor", "Blank thumbnails", "Command search shows thumbnails for the same projects, but this list doesn't.", "Use the same thumbnail source.", "Recognition"),
   ("4", "minor", "Creator shown as \"Ux\"", "The name is \"UX Audit\".", "Show the full name.", "Consistency"),
  ]),
 ]),
]

POSITIVES = [
 "Google and SSO on both sign-in and sign-up, and the SSO step is a clean single field.",
 "Onboarding has a visible \"I'm just exploring\" escape, and the goal buttons are proper toggle buttons.",
 "The profile step's ID-badge preview, which updates live, is a nice touch.",
 "Command search (⌘K) covers settings pages and projects.",
 "Script-first editing works: a toast tells you to regenerate, and speech came back in about 20 seconds.",
 "The AI's Ask, Plan and Auto modes each have a one-line description.",
 "The AI's video plan had good structure, and the rendered scenes looked professional.",
 "Settings has a pronunciation dictionary, transcription keywords and a translation glossary, which matter for a voice product.",
]

JOURNEY = [
 ("Sign in with Google", "0:00", "ok", "Fast; Google and SSO offered"),
 ("Complete your profile", "0:10", "bad", "Asks for a name Google already supplied"),
 ("App loads", "0:20", "bad", "About 20 s of blank screen and pulsing logo"),
 ("Step 1: goals", "0:45", "ok", "Clear choices; work-email toast appears"),
 ("Step 2: profile", "1:05", "bad", "Name asked again; role list loads late"),
 ("Step 3: workspace", "1:30", "warn", "Extra step for a solo user"),
 ("Step 4: first video", "1:45", "bad", "Recommended path requires an extension"),
 ("Home", "2:15", "bad", "Survey pop-up, fake brand kit on, model picker"),
 ("Blank project", "3:00", "warn", "Wrong-audience editor modal; blank canvas"),
 ("Voiceover", "4:00", "bad", "Works, then the preview freezes until reload"),
 ("AI prompt-to-video", "8:00", "bad", "Good plan; 9.6 min build with no ETA; 250 credits"),
]

IA_ROWS = [
 ("Home prompt, Chats, header Clueso AI, editor chat, Article copilot", "Sidebar items, header button, inside editor", "One AI panel component everywhere; Chats becomes the Agent task list", "Six surfaces for one capability"),
 ("Agent", "Main sidebar, 3rd item (a Book a demo page)", "Keep, open it on Free as a usable page with the task history; lock only paid abilities", "A usable feature instead of a sales page"),
 ("MCP", "Main sidebar", "Integrations, next to GitHub, Bitbucket and the Chrome extension", "Developer setup, done once"),
 ("Connections (GitHub, Bitbucket)", "Settings", "Integrations", "Same job as MCP"),
 ("Clueprints, Templates, Components, Brand kit, Media", "Sidebar (2), editor panels (3)", "Library section: Video styles, Clip templates, Components, Brand kit, Media", "All are reusable assets"),
 ("Analytics", "Main sidebar, locked on Free", "Keep as a workspace-wide dashboard; lock badge and labeled sample on Free; project pages link to filtered views", "It covers all videos at once, so it needs its own place"),
 ("Profile settings", "Avatar menu modal", "Settings > Profile", "One settings location"),
 ("Pronunciations, Transcriptions, Translations", "Three separate settings pages", "Settings > Language and voice (three tabs)", "Same mental model: teach the AI your words"),
 ("Video player, View only links", "Settings", "Settings > Sharing", "Both control what viewers see"),
 ("Billing, Usage, AI Credits", "Settings > Billing tabs", "Settings > Plan and usage, plus a usage meter in the sidebar", "Usage should be visible where it's spent"),
 ("Help Center, Chat with Support, Help, bubble, footer", "Five places", "One Help button", "Help shouldn't be a decision"),
 ("Get started checklist", "Collapsed at bottom of sidebar", "Card on Home until done", "Onboarding must be seen to work"),
]

LABELS = [
 ("Free trial / free plan / Free", "Free plan", "There is no trial period"),
 ("Agent / Chats / Clueso AI / Director", "Clueso AI (chat); Clueso Agents (Enterprise automation)", "One name per concept"),
 ("Templates (editor)", "Clip templates", "Separates them from Clueprints"),
 ("Clueprints, \"Reusable video templates\"", "Clueprints, \"Video styles\"", "Clueprints set the look of a whole video"),
 ("Upload slide decks / Upload PPT/PDF", "Upload slides or PDF", "One label everywhere"),
 ("Upload videos / Upload screen recording / Upload a video", "Upload video", "One label everywhere"),
 ("Record screen / Record your screen", "Record screen", "One label everywhere"),
 ("Translations / Translation Settings / Language translations / Translation glossary", "Translation glossary", "Matches pricing and docs"),
 ("Transcriptions / Transcription Keywords", "Transcription keywords", "Says what the page does"),
 ("Admin (settings page) / Team name", "General / Workspace name", "\"Admin\" is a role, not a page"),
 ("Opus 5.5, Sonnet 5.5, Astra 6...", "Quality: Fast / Best (model under Advanced)", "Users choose outcomes, not vendors"),
 ("guide (in URLs)", "project", "Matches the UI"),
 ("40+ / 80+ / 150+ languages", "One verified number", "Credibility"),
]

ROADMAP = [
 ("Quick wins, 1 to 2 sprints", [
  "Remove the \"Anyone with a gmail.com address\" join option for public domains (E1).",
  "Stop building a brand kit from public email domains; keep the brand kit chip off until a brand is confirmed (C2, C7).",
  "Prefill name from Google and delete the duplicate name step (B1, B7).",
  "Show the \"simplified editor\" modal only to existing users; default new users to Simplified (F1, F2).",
  "Show credit and export-minute costs next to Create, Export and Create view-only link (B20, H1, H3).",
  "Use one plan label, and make in-app limits match the pricing page (C5, E3, E4).",
  "Move the \"How did you hear about us\" survey to after the first export (C3).",
  "Add aria-labels to the 26 unlabeled editor buttons, and make sidebar items real links (F3).",
  "Fix the projects filter overflow and the MCP video length label (H6, D9).",
 ]),
 ("Next, 1 quarter", [
  "Restructure the sidebar into Create, Projects, Library, with Integrations, Settings and Help at the bottom (see the proposed sitemap).",
  "Use one AI panel component across Home, editor and article; fold Chats into its history.",
  "Merge the three settings locations into one.",
  "Detect and recover from preview and stream stalls with a visible reconnect state (F8, F9).",
  "Add a Generate article from video empty state (F14).",
  "Define one creation menu and reuse it everywhere (D13).",
 ]),
 ("Strategic", [
  "Goal-driven onboarding where the first action needs no install, a storyline and its cost appear within about a minute (as observed), and the build runs in the background with a notification.",
  "Replace the model picker with outcome-based quality settings and per-run credit estimates.",
  "Per-scene progress, time estimates and notifications for AI generation.",
  "Run the usability test, tree test and card sort below before and after the IA change.",
 ]),
]

TASKS = [
 ("You just signed up. Make a short video that shows how to sign up for your own product.", "Time to a playable draft; whether they hit the extension wall"),
 ("Make your videos use your company's colors and logo.", "Finds Brand kit; notices the auto-filled one"),
 ("How many more videos can you export this month?", "Finds Usage; understands minutes vs credits"),
 ("Add a teammate who can only leave comments.", "Settings > Users; reviewer seats"),
 ("Turn your video into a written help article.", "Discovers the Article tab and how to generate it"),
 ("Send your manager a link to watch the video.", "Share > View-only link; reacts to the cost"),
 ("Make a Spanish version of your video.", "Finds Translate; distinguishes it from the glossary"),
]


def chip(sev):
    label = {"critical": "Critical", "major": "Major", "minor": "Minor", "good": "Works well"}[sev]
    return f'<span class="chip chip-{sev}">{label}</span>'


def counts():
    c = {"critical": 0, "major": 0, "minor": 0}
    for _, _, _, figs in SECTIONS:
        for _, _, fs in figs:
            for f in fs:
                if f[1] in c:
                    c[f[1]] += 1
    for f in NS.NEW_FINDINGS:
        if f[1] in c:
            c[f[1]] += 1
    return c


def section_html(idx, sec):
    anchor, title, intro, figs = sec
    letter = "ABCDEFGH"[idx]
    out = [f'<section id="{anchor}" class="area"><header class="area-head"><span class="area-letter">{letter}</span><div><h2>{E(title)}</h2><p class="lede">{E(intro)}</p></div></header>']
    n = 0
    for img, cap, fs in figs:
        out.append('<figure class="finding-fig">')
        out.append(f'<a class="shot" href="img/{img}" target="_blank" rel="noopener"><img src="img/{img}" alt="{E(cap)} with numbered highlights" loading="lazy"></a>')
        out.append(f'<figcaption><p class="figcap">{E(cap)}</p><ol class="flist">')
        for badge, sev, ftitle, ev, fix, heur in fs:
            n += 1
            fid = f"{letter}{n}"
            out.append(f'<li class="f f-{sev}" id="f-{fid}"><span class="badge badge-{sev}">{badge}</span><div class="fbody">'
                       f'<div class="fhead"><span class="fid">{fid}</span>{chip(sev)}<h3>{E(ftitle)}</h3></div>'
                       + (f'<p>{E(ev)}</p>' if ev else '') +
                       f'<p class="fix"><b>Fix:</b> {E(fix)}</p><p class="heur">{E(heur)}</p></div></li>')
        out.append('</ol></figcaption></figure>')
    out.append('</section>')
    return "\n".join(out)


def build():
    c = counts()
    total = sum(c.values())
    nav = "".join(f'<a href="#{a}">{E(t)}</a>' for a, t, _, _ in SECTIONS)
    journey = "".join(
        f'<li class="j j-{s}"><span class="jt">{t}</span><span class="jn">{E(n)}</span><span class="jd">{E(d)}</span></li>'
        for n, t, s, d in JOURNEY)
    ia = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c_)}</td><td>{E(d)}</td></tr>" for a, b, c_, d in IA_ROWS)
    labels = "".join(f"<tr><td>{E(a)}</td><td><b>{E(b)}</b></td><td>{E(c_)}</td></tr>" for a, b, c_ in LABELS)
    road = "".join(
        f'<div class="road"><h3>{E(h)}</h3><ul>' + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul></div>"
        for h, items in ROADMAP)
    tasks = "".join(f"<tr><td>{i}</td><td>{E(t)}</td><td>{E(m)}</td></tr>" for i, (t, m) in enumerate(TASKS, 1))
    pos = "".join(f"<li>{E(p)}</li>" for p in POSITIVES)
    sections = "\n".join(section_html(i, s) for i, s in enumerate(SECTIONS))

    RS_CSS = RS.CSS
    page = f"""<title>Clueso UX Audit</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Public+Sans:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@500&display=swap">
<style>
/* Layout: a single reading column with a sticky section index; each finding pairs an annotated screenshot with its numbered notes. */
:root {{
  --bg: #f6f7f9; --surface: #ffffff; --ink: #161a22; --muted: #5a6272; --line: #dfe3ea;
  --accent: #3b3fd8; --accent-soft: #e9eafd;
  --crit: #c81e1e; --crit-soft: #fde8e8; --major: #c2510a; --major-soft: #fdeee3; --minor: #94690a; --minor-soft: #fbf3dc; --good: #13803d; --good-soft: #e3f5ea;
  --display: "Bricolage Grotesque", "Avenir Next", "Segoe UI", sans-serif;
  --body: "Public Sans", "Helvetica Neue", Arial, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #11141a; --surface: #191d25; --ink: #e8ebf1; --muted: #9aa3b4; --line: #2c3240;
  --accent: #9b9eff; --accent-soft: #252857;
  --crit: #ff7b7b; --crit-soft: #3a1c1f; --major: #ffa266; --major-soft: #3a2619; --minor: #e6c15c; --minor-soft: #352d16; --good: #5fd38d; --good-soft: #17301f;
  color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #11141a; --surface: #191d25; --ink: #e8ebf1; --muted: #9aa3b4; --line: #2c3240;
  --accent: #9b9eff; --accent-soft: #252857;
  --crit: #ff7b7b; --crit-soft: #3a1c1f; --major: #ffa266; --major-soft: #3a2619; --minor: #e6c15c; --minor-soft: #352d16; --good: #5fd38d; --good-soft: #17301f;
  color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--ink); font: 16px/1.6 var(--body); padding-inline: 16px; padding-block: 0 64px; }}
.wrap {{ max-width: 1120px; margin: 0 auto; }}
h1, h2, h3 {{ font-family: var(--display); text-wrap: balance; line-height: 1.15; margin: 0; }}
h1 {{ font-size: clamp(2.2rem, 5vw, 3.6rem); font-weight: 700; letter-spacing: -0.02em; }}
h2 {{ font-size: clamp(1.5rem, 3vw, 2rem); font-weight: 700; }}
h3 {{ font-size: 1.05rem; font-weight: 700; }}
p {{ margin: 0; }}
a {{ color: var(--accent); }}
a:focus-visible, .shot:focus-visible {{ outline: 3px solid var(--accent); outline-offset: 3px; border-radius: 4px; }}
.eyebrow {{ font: 500 0.75rem var(--mono); letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }}
.hero {{ padding-block: 56px 32px; display: grid; gap: 20px; }}
.hero .lede {{ font-size: 1.15rem; max-width: 64ch; color: var(--ink); }}
.meta {{ display: flex; flex-wrap: wrap; gap: 8px 24px; font: 500 0.8rem var(--mono); color: var(--muted); }}
.lede {{ color: var(--muted); max-width: 70ch; }}
.score {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-block: 8px 0; }}
.score div {{ background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; }}
.score b {{ display: block; font: 700 2rem var(--display); font-variant-numeric: tabular-nums; }}
.score .s-crit b {{ color: var(--crit); }} .score .s-major b {{ color: var(--major); }} .score .s-minor b {{ color: var(--minor); }}
.score span {{ font-size: 0.85rem; color: var(--muted); }}
nav.toc {{ position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--bg); border-bottom: 1px solid var(--line); display: flex; gap: 4px 18px; overflow-x: auto; padding-block: 10px; font-size: 0.85rem; white-space: nowrap; }}
nav.toc a {{ color: var(--muted); text-decoration: none; }}
nav.toc a:hover {{ color: var(--accent); }}
.block {{ padding-block: 48px 8px; display: grid; gap: 20px; }}
.top {{ display: grid; gap: 10px; counter-reset: top; padding: 0; margin: 0; list-style: none; }}
.top li {{ display: grid; grid-template-columns: 2.2rem 1fr; gap: 12px; align-items: start; background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; }}
.top li::before {{ counter-increment: top; content: counter(top); font: 700 1.3rem var(--display); color: var(--accent); }}
.top li p {{ color: var(--muted); font-size: 0.95rem; }}
.journey {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 0; border-left: 2px solid var(--line); }}
.j {{ display: grid; grid-template-columns: 4rem minmax(0, 14rem) minmax(0, 1fr); gap: 12px; padding: 8px 0 8px 16px; position: relative; align-items: baseline; }}
.j::before {{ content: ""; position: absolute; left: -7px; top: 15px; width: 12px; height: 12px; border-radius: 50%; background: var(--good); }}
.j-warn::before {{ background: var(--minor); }} .j-bad::before {{ background: var(--crit); }}
.jt {{ font: 500 0.8rem var(--mono); color: var(--muted); font-variant-numeric: tabular-nums; }}
.jn {{ font-weight: 600; }} .jd {{ color: var(--muted); font-size: 0.95rem; }}
.area {{ padding-block: 56px 0; display: grid; gap: 28px; }}
.area-head {{ display: grid; grid-template-columns: auto 1fr; gap: 16px; align-items: start; border-top: 2px solid var(--ink); padding-top: 18px; }}
.area-letter {{ font: 700 2.4rem/1 var(--display); color: var(--accent); }}
.area-head > div {{ display: grid; gap: 8px; min-width: 0; }}
.finding-fig {{ margin: 0; display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: 24px; align-items: start; }}
.shot {{ display: block; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: var(--surface); }}
.shot img {{ display: block; width: 100%; height: auto; }}
figcaption {{ display: grid; gap: 12px; min-width: 0; }}
.figcap {{ font: 500 0.78rem var(--mono); text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); }}
.flist {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 14px; }}
.f {{ display: grid; grid-template-columns: 26px 1fr; gap: 10px; }}
.fbody {{ display: grid; gap: 6px; min-width: 0; font-size: 0.93rem; }}
.fhead {{ display: flex; flex-wrap: wrap; align-items: center; gap: 6px 8px; }}
.fhead h3 {{ flex-basis: 100%; }}
.fid {{ font: 500 0.75rem var(--mono); color: var(--muted); }}
.badge {{ width: 24px; height: 24px; border-radius: 50%; display: grid; place-items: center; font: 700 0.8rem var(--body); color: #fff; }}
.badge-critical {{ background: #dc2626; }} .badge-major {{ background: #ea580c; }} .badge-minor {{ background: #ca8a04; }} .badge-good {{ background: #16a34a; }}
.chip {{ font: 600 0.68rem var(--body); text-transform: uppercase; letter-spacing: 0.06em; padding: 2px 8px; border-radius: 999px; }}
.chip-critical {{ color: var(--crit); background: var(--crit-soft); }} .chip-major {{ color: var(--major); background: var(--major-soft); }}
.chip-minor {{ color: var(--minor); background: var(--minor-soft); }} .chip-good {{ color: var(--good); background: var(--good-soft); }}
.fix {{ color: var(--ink); }} .fbody p:not(.fix):not(.heur) {{ color: var(--muted); }}
.heur {{ font: 500 0.72rem var(--mono); color: var(--accent); }}
.tablewrap {{ overflow-x: auto; border: 1px solid var(--line); border-radius: 10px; background: var(--surface); }}
table {{ border-collapse: collapse; width: 100%; min-width: 720px; font-size: 0.92rem; }}
th, td {{ text-align: left; vertical-align: top; padding: 10px 14px; border-bottom: 1px solid var(--line); }}
th {{ font: 600 0.72rem var(--body); text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); background: var(--bg); }}
tr:last-child td {{ border-bottom: 0; }}
.trees {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }}
.tree {{ background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 16px 18px; min-width: 0; }}
.tree h3 {{ margin-bottom: 10px; }}
.tree pre {{ margin: 0; font: 500 0.8rem/1.7 var(--mono); white-space: pre; overflow-x: auto; color: var(--ink); }}
.tree.proposed {{ border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }}
.flow {{ list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 12px; counter-reset: step; }}
.flow li {{ background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; display: grid; gap: 6px; font-size: 0.92rem; color: var(--muted); }}
.flow li b {{ color: var(--ink); font-family: var(--display); font-size: 1rem; }}
.flow li::before {{ counter-increment: step; content: "Step " counter(step); font: 500 0.72rem var(--mono); color: var(--accent); text-transform: uppercase; letter-spacing: 0.06em; }}
.roads {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }}
.road {{ background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 16px 18px; min-width: 0; }}
.road ul, .plain {{ margin: 10px 0 0; padding-left: 1.1rem; display: grid; gap: 6px; font-size: 0.93rem; }}
.note {{ background: var(--accent-soft); border-radius: 10px; padding: 16px 18px; font-size: 0.93rem; display: grid; gap: 8px; }}
{RS_CSS}
{NS.CSS}
{DS.CSS}
@media (max-width: 860px) {{ .finding-fig {{ grid-template-columns: 1fr; }} .j {{ grid-template-columns: 3.4rem 1fr; }} .jd {{ grid-column: 2; }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ scroll-behavior: auto !important; }} }}
html {{ scroll-behavior: smooth; }}
</style>

<div class="wrap">
<header class="hero">
  <p class="eyebrow">Product UX audit · web app · Free plan</p>
  <h1>Clueso UX Audit</h1>
  <p class="lede">I went through Clueso's real product end to end as a new free-plan user: sign-in, onboarding, home, every sidebar page, all ten settings pages, the editor, AI prompt-to-video, and sharing. The product's core idea is strong, and the AI's output was impressive. The first session works against it: the name is asked twice, the recommended path needs an extension, a fake brand kit is applied by default, and costs show up only after they are spent. Every finding is scored against cited frameworks: Microsoft's 18 Human-AI guidelines, agentic UX patterns, 16 psychology principles, IA principles from Dan Brown and Rosenfeld and Morville, and onboarding best practice. It is also benchmarked against seven competitors.</p>
  <div class="meta"><span>16 Oct 2026</span><span>web.clueso.io</span><span>Google sign-in · new workspace</span><span>{total} issues · 55 annotated screens</span></div>
  <div class="score">
    <div class="s-crit"><b>{c['critical']}</b><span>Critical: blocks activation, risks data or trust</span></div>
    <div class="s-major"><b>{c['major']}</b><span>Major: frequent confusion or drop-off</span></div>
    <div class="s-minor"><b>{c['minor']}</b><span>Minor: friction or polish</span></div>
    <div><b>8 min+</b><span>Prompt to video, still building</span></div>
  </div>
</header>

<nav class="toc" aria-label="Sections"><a href="#summary">Summary</a><a href="#journey">Journey</a><a href="#onboard-first">Onboarding</a><a href="#navigation">Navigation</a><a href="#decisions">Decisions</a>{nav}<a href="#scorecards">Scorecards</a><a href="#journey-map">Journey map</a><a href="#competitors">Competitors</a><a href="#questions">Questions</a><a href="#structure">Proposed IA</a><a href="#labels">Labels</a><a href="#onboard-new">New onboarding</a><a href="#roadmap">Roadmap</a><a href="#validate">Validation</a><a href="#sources">Sources</a><a href="#method">Method</a></nav>

<section id="summary" class="block">
  <h2>Navigation in one paragraph</h2>
  <p class="lede">Clueso's left nav lists every system the company has built: Agent, Chats, MCP, Clueprints, Brand kit and Analytics, each as its own top-level item. It doesn't follow the three jobs users have: create, find my work, reuse my assets. Home, Projects and Settings earn their places. Agent is a sales page and Analytics a blank paywall; both should stay but become usable on Free (Agent as a real page, Analytics with a labeled sample). MCP is one-time setup, and Chats duplicates Projects. Creation is offered from six surfaces with six different option sets. The SOP and animation use cases, both promised in onboarding, have no start option at all. Details are in the Navigation section.</p>
  <h2>The eight problems to fix first</h2>
  <ol class="top">
    <li><div><h3>Workspace can be opened to every Gmail user</h3><p>Settings offers \"Anyone with a gmail.com email address can join\" on a personal account. One click exposes all projects. (E1)</p></div></li>
    <li><div><h3>A fake brand kit is applied to the first videos</h3><p>Built from \"gmail.com\", switched on by default, and quietly added to the AI prompt. (C2, C7 to C9, G1)</p></div></li>
    <li><div><h3>The recommended first step needs an extension install</h3><p>Onboarding's \"Recommended for you\" sends users to the Chrome Web Store at the last step. (B13, B17)</p></div></li>
    <li><div><h3>The preview freezes after generating speech</h3><p>Playback stayed disabled for over a minute until a page reload, with no error message. (F8, F9)</p></div></li>
    <li><div><h3>Costs appear only after they're spent</h3><p>One AI video used 250 of 1,000 monthly credits; export and view-only links use minutes; none of it is shown beforehand. (B20, E5, H1, H3)</p></div></li>
    <li><div><h3>AI is scattered over six surfaces, under four names</h3><p>Home prompt, Chats, Clueso AI, Agent, editor chat, Article copilot. (D2, D3, D6)</p></div></li>
    <li><div><h3>The plan and its limits contradict each other</h3><p>\"Free trial\" vs \"free plan\", 1/4 seats on a one-user plan, 10 vs 15 article exports, 40+/80+/150+ languages. (C5, E3, E4, B14)</p></div></li>
    <li><div><h3>The onboarding asks too much, too early</h3><p>Name twice, a role list that loads late, a workspace step, a survey pop-up and a work-email nag. (B1, B4, B7, B10, B12, C3)</p></div></li>
  </ol>
  <h3>What already works</h3>
  <ul class="plain">{pos}</ul>
</section>

<section id="journey" class="block">
  <h2>First-session journey</h2>
  <p class="lede">Times are approximate, from the moment I clicked Sign in. Green means it worked, yellow means friction, red means a problem that could cost a user.</p>
  <ol class="journey">{journey}</ol>
</section>

{OD.onboarding_html()}

{NS.nav_html()}

{DS.decisions_html()}

{sections}

{RS.scorecards_html()}

{RS.journey_html()}

{RS.competitors_html()}

{RS.questions_html()}

<section id="structure" class="block">
  <h2>Proposed information architecture</h2>
  <p class="lede">The current sidebar groups items by how Clueso is built: Agent, Chats, MCP and Clueprints are each separate systems. The proposal groups them by what the user is trying to do: make something, find their work, reuse assets, connect tools.</p>
  <div class="trees">
    <div class="tree"><h3>Today</h3><pre>Sidebar
├ Home (prompt + start chips)
├ Projects
├ Agent  ← Enterprise sales page
├ Chats
├ MCP
├ Clueprints
├ Brand kit
├ Analytics  ← locked on Free
├ Settings  (workspace only, 10 pages)
├ New in Clueso · Checklist · Upgrade
└ Workspace switcher
Header
├ Search ⌘K
├ Avatar → Help Center, Profile
│          settings (modal), Chat with
│          Support, Sign out
├ Help
├ Clueso AI (panel)
└ New project ▾ (4 options)</pre></div>
    <div class="tree proposed"><h3>Proposed</h3><pre>Sidebar
├ Create
│  └ one prompt + Record · Upload
│    video · Slides/PDF · Clueprint ·
│    Blank (same menu everywhere)
├ Projects
│  └ All · Folders · versions grouped
├ Agent  (open on Free)
│  └ Give a task · task history
│    (was Chats) · auto-update 🔒
├ Analytics  (🔒 Free shows a sample)
│  └ All videos · drill into one
├ Library
│  ├ Clueprints
│  ├ Clip templates · Components
│  ├ Brand kit
│  └ Media
── bottom ──
├ Usage meter (minutes + credits)
├ Integrations  (Chrome extension,
│                MCP, GitHub, Bitbucket)
├ Settings
│  ├ Profile
│  ├ Workspace · Members
│  ├ Plan and usage
│  ├ Language and voice
│  │  (pronunciation, transcription
│  │   keywords, translation glossary)
│  ├ Video defaults
│  └ Sharing (player, view-only links)
└ Help  (docs, chat, what's new)
Everywhere: one Clueso AI panel,
with recent agent tasks</pre></div>
  </div>
  <div class="tablewrap"><table>
    <thead><tr><th>Feature</th><th>Where it is today</th><th>Where it should go</th><th>Why</th></tr></thead>
    <tbody>{ia}</tbody>
  </table></div>
</section>

<section id="labels" class="block">
  <h2>Label fixes</h2>
  <div class="tablewrap"><table>
    <thead><tr><th>Today</th><th>Use instead</th><th>Reason</th></tr></thead>
    <tbody>{labels}</tbody>
  </table></div>
</section>

<section id="onboard-new" class="block">
  <h2>Proposed onboarding</h2>
  <p class="lede">This follows the question rubric and competitor patterns above. Synthesia, Descript and VEED turn the use-case answer into a pre-filled prompt, Loom lets users skip straight to recording, and every published competitor skips the card. Onboarding should feel like running downhill: one question with a visible reason, then a clear picture of what the product does, then the real product, personalized. Building a video belongs to the product, not to onboarding, because a 10-minute build inside onboarding makes the first minutes feel like work.</p>
  <ol class="flow">
    <li><b>One question</b>"What will you mostly make?" with 4 options, and the reason shown on screen ("so we can show you a relevant example and set up your Create page"). The name comes from Google, so there's no profile, role, workspace or survey screen.</li>
    <li><b>Show, don't ask</b>A before-and-after for that answer: what you bring (a rough recording) and what Clueso makes (a polished video and a step-by-step guide), plus how it works in three lines. Nothing is built, spent or waited for.</li>
    <li><b>Create, personalized</b>The prompt placeholder and suggestions come from the answer, and a one-line "how it works" strip shows on the first visit. The user starts when ready; the cost and approval step comes with their first real build.</li>
    <li><b>Contextual setup later</b>Brand when they first build or share, the team when they invite, the extension when they record with highlights, and an upgrade only at a real limit.</li>
  </ol>
</section>

<section id="roadmap" class="block">
  <h2>Roadmap</h2>
  <div class="roads">{road}</div>
</section>

{RS.sources_html()}

<section id="validate" class="block">
  <h2>Validation plan</h2>
  <p class="lede">These findings come from an expert review. Before shipping the larger changes, test them with 5 to 8 participants per main persona (customer education or L&amp;D, and product managers or product marketers). Use moderated think-aloud sessions of 40 minutes, recording task success, time, first click and a single ease question (1 to 7) per task, and SUS at the end.</p>
  <div class="tablewrap"><table>
    <thead><tr><th>#</th><th>Task (as said to the participant)</th><th>What it tests</th></tr></thead>
    <tbody>{tasks}</tbody>
  </table></div>
  <ul class="plain">
    <li><b>Tree test</b>: today's navigation against the proposed one, using the seven tasks above, between-subjects. Don't use category labels in the task wording, and pilot it qualitatively first (NN/g). Tool vendors such as Maze suggest about 50 participants per group; that figure is unverified.</li>
    <li><b>Open card sort first</b>: about 25 feature cards (Clueprints, Clip templates, Components, Brand kit, MCP, Pronunciations and so on). Let users name their own groups, then validate the proposed groups with the tree test. NN/g recommends at least 15 participants for a qualitative sort and 30 to 50 for a quantitative one.</li>
    <li><b>Funnel metrics</b>: signup to first played video, signup to first export, share of users who hit the extension modal, and AI runs abandoned before completion.</li>
  </ul>
</section>

<section id="method" class="block">
  <h2>Method and limits</h2>
  <div class="note">
    <p>A single session on 16 Oct 2026, in an embedded Chromium browser at about 1294 × 863 px, with a new free-plan account created through Google sign-in. Methods: a cognitive walkthrough of the first session, a heuristic review, an inventory of every navigation item and settings page, and spot checks of markup, the console and network traffic. In a second pass, research agents gathered primary sources. The findings were then scored against Microsoft's 18 Human-AI guidelines, agentic UX patterns, 16 psychology principles, Dan Brown's and Rosenfeld and Morville's IA principles, and onboarding best practice, and benchmarked against 7 competitors. Every source is listed under Sources.</p>
    <p><b>Scope.</b> At your direction, the audit centers on the navigation layer: the layout, entry points, the left nav, and how features connect. The editor and AI-generation notes are kept as an appendix. <b>Not tested:</b> real screen recording with the Chrome extension, uploading a video file, actual exports (to avoid spending export minutes), collaboration with a second user, mobile layouts, and Chrome itself. The preview stall (F8, F9) should be reproduced in Chrome before it is prioritized.</p>
    <p><b>Left in the account:</b> profile name \"UX Audit\", workspace \"UX's Workspace\", seven projects (test, AI-made, PDF-based and a Spanish translation), three chats, and about half of the month's AI credits used. No exports, links, invites or payments were made; the invite dialog was opened and closed without sending.</p>
  </div>
</section>
</div>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write(page)
    print("wrote", OUT, "findings:", c)


if __name__ == "__main__":
    build()
