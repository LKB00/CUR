"""Clueso first-video review: one slide per issue (screenshot with numbered boxes, the issue, the principle),
with what it may cost, a journey chart, a summary and a cheat sheet. Previous / Next and the arrow keys. Nothing else.
Run: python3 casestudy/build.py  → casestudy/index.html + casestudy/img/*
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SPEC = {}
for f in ("spec.json", "spec2.json"):
    SPEC.update(json.load(open(os.path.join(ROOT, f)))["images"])


def box(img, label):
    for b in SPEC[img]:
        if b[4] == label:
            return b[:4]
    raise KeyError((img, label))


# kind "issue" (Clueso today) or "fix" (redesign). points: [text, box]; principle: [name, one line].
SLIDES = [
    {"kind": "issue", "img": "02-signup-personal-email.jpg", "src": "shot", "title": "Sign-up nags about work email",
     "points": [["A warning appears while typing and pushes the password field down.", box("02-signup-personal-email.jpg", "1")],
                ["The same message returns as a toast on every onboarding step.", None]],
     "principle": ["Reactance", "Repeating a nudge after someone has decided reads as pressure."]},
    {"kind": "issue", "img": "04-complete-profile.jpg", "src": "shot", "title": "Asks for a name Google already gave",
     "points": [["First and last name are empty after signing in with Google.", box("04-complete-profile.jpg", "1")],
                ["The name is asked again two screens later.", None]],
     "principle": ["Cognitive load", "Every field the product could fill itself is effort spent before any value."]},
    {"kind": "issue", "img": "06-loading-logo.jpg", "src": "shot", "title": "About 20 seconds of a blank screen",
     "points": [["Only a faint logo while onboarding loads. No progress, no message, no estimate.", [362, 230, 438, 304]]],
     "principle": ["Doherty threshold", "Without a response or visible progress, people assume it's broken."]},
    {"kind": "issue", "img": "07-onb-goals.jpg", "src": "shot", "title": "40% of onboarding is decoration",
     "points": [["The work-email toast again.", box("07-onb-goals.jpg", "1")],
                ["A decorative panel takes the right side and carries no information.", box("07-onb-goals.jpg", "2")]],
     "principle": ["Banner blindness", "Areas that look like decoration teach people to stop looking there."]},
    {"kind": "issue", "img": "09-onb-profile.jpg", "src": "shot", "title": "Thirteen roles, and none change anything",
     "points": [["Name asked for the second time.", box("09-onb-profile.jpg", "1")],
                ["13 roles in no clear order. The answer doesn't change what you see next.", box("09-onb-profile.jpg", "2")]],
     "principle": ["Hick's law", "More options make decisions slower, and effort that changes nothing feels wasted."]},
    {"kind": "issue", "img": "15-onb-extension-gate.jpg", "src": "shot", "title": "The recommended path ends in an install wall",
     "points": [["\"Record screen, recommended\" asks you to install an extension and come back.", box("15-onb-extension-gate.jpg", "1")]],
     "principle": ["Fogg behavior model", "Motivation peaks right after sign-up, so the first step must be the easiest, not the hardest."]},
    {"kind": "issue", "img": "18-home-checklist-survey.jpg", "src": "shot", "title": "Six things compete with the prompt on Home",
     "points": [["Sale banner.", box("18-home-checklist-survey.jpg", "6")],
                ["\"How did you hear about us?\" survey, seconds after arriving.", box("18-home-checklist-survey.jpg", "3")],
                ["Checklist collapsed in the sidebar.", box("18-home-checklist-survey.jpg", "4")],
                ["One plan, three names: Free trial, free plan, Free.", box("18-home-checklist-survey.jpg", "5")],
                ["Model picker on the prompt.", box("18-home-checklist-survey.jpg", "1")],
                ["Brand kit switched on by default.", box("18-home-checklist-survey.jpg", "2")]],
     "principle": ["Cognitive load", "Attention is limited. Everything on screen competes with the one task that matters."]},
    {"kind": "issue", "img": "18-home-checklist-survey.jpg", "src": "shot", "title": "A brand kit nobody set up, on by default",
     "points": [["For a Gmail sign-up, Clueso built a kit from gmail.com: a placeholder pink logo.", box("18-home-checklist-survey.jpg", "2")],
                ["The AI then added \"Use our brand kit\" to the prompt.", None]],
     "principle": ["Default bias", "Most people keep the default, so a wrong default quietly ships a wrong result."]},
    {"kind": "issue", "img": "46-model-picker.jpg", "src": "shot", "title": "A model menu with no costs",
     "points": [["Six vendor models, described by vendor. None shows a price; the default is the most expensive.", box("46-model-picker.jpg", "1")]],
     "principle": ["Feedforward", "Show what an action will cost before people take it, not after."]},
    {"kind": "issue", "img": "63-ai-video-building.jpg", "src": "shot", "title": "A 9½-minute build with no estimate",
     "points": [["Only elapsed time: \"Working for 4m 54s\", then \"Thinking for 8m 14s\".", box("63-ai-video-building.jpg", "1")]],
     "principle": ["Goal-gradient effect", "People wait more patiently when they can see how close the end is."]},
    {"kind": "issue", "img": "57-share-export.jpg", "src": "shot", "title": "Limits appear only after you share",
     "points": [["Share opens on Export and says nothing about the 10 free minutes, the watermark or the 1080p cap.", box("57-share-export.jpg", "1")]],
     "principle": ["Peak-end rule", "People remember the best moment and the last one. A surprise at the end sours both."]},
    {"kind": "issue", "img": "96-chat-page-is-agent.jpg", "src": "shot", "title": "One assistant, five doors, four names",
     "points": [["The Home prompt, Clueso AI, Chats and this chat are the same assistant, called \"Director\" inside.", box("96-chat-page-is-agent.jpg", "1")],
                ["Agent in the sidebar is something else: an Enterprise sales page.", box("96-chat-page-is-agent.jpg", "2")]],
     "principle": ["Mental model", "If one thing has many names and doors, people build many wrong ideas of it."]},

]

POV = [('Sign up and get to the product.', "I typed my Gmail and the form jumped while I was typing. It wants a work email? I'm just trying it.", 1, 0), ('Get past sign-up. I used Google to save time.', 'Google already gave you my name. Why am I typing it again?', 1, 0), ('Start using it.', 'Is it loading or broken? I almost refreshed.', 1, 0), ('Answer a quick question and move on.', 'Half the screen is a picture, and the work-email nag is back.', 1, 0), ('Finish setup.', "My name again. Thirteen roles, and I'm not sure any of them is me.", 1, 0), ('Make my first video.', 'I clicked the recommended option and it wants me to install something and come back. Five screens in.', 1, 0), ('Describe my demo and get started.', 'A banner, a survey, a checklist, a model picker. Where do I actually start?', 1, 0), ("Use my own product's look, later.", 'I never set up a brand. Why is it pink, and why did it add a line to my brief?', 0, 0), ("Pick whatever's sensible and go.", "Opus, Sonnet, Astra? I don't know what these cost, and I'm on a free plan.", 1, 0), ('Get my video.', 'Nine minutes and counting, with no idea how far along it is. Can I leave?', 1, 263), ('Send it to my team.', 'The video is good. Then Share opens on Export, and nothing says it uses my free minutes or adds a watermark.', 1, 263), ('Next day: shorten the intro.', "Home prompt, Clueso AI, Chats or Agent? I don't know which one has yesterday's video.", 1, 263)]

# What each issue may cost the business. Impact is a judgement from the session, not Clueso's data;
# "check" names the number in Clueso's own analytics that would confirm or reject it.
COST = [
    ("Medium", "Sign-up conversion", "Questioning a choice at the very first form gives people a reason to stop, and the toast keeps the doubt alive through onboarding.",
     "Sign-up completion for personal vs work email."),
    ("Low", "Onboarding completion", "One more field before any value. Small alone, but it adds up with the steps after it.",
     "Time spent on the profile step."),
    ("High", "Onboarding completion", "A blank screen during the first visit reads as broken. People who refresh or leave here never see the product.",
     "Sessions that reload or end on the loading screen."),
    ("Low", "Onboarding completion", "Not a blocker by itself. It makes setup feel longer than it is.",
     "Drop-off per onboarding step."),
    ("Medium", "Activation, data quality", "Answers that change nothing get picked at random, so the role data used for segmentation can't be trusted.",
     "Share of users on the first role in the list."),
    ("High", "Activation", "The recommended first step sends people out of the product before any value. Anyone who doesn't come back after installing is lost.",
     "Record screen picked → first recording in the same session."),
    ("Medium", "Activation", "Every extra element delays the first prompt, the moment that matters most on Home.",
     "Time from first Home visit to first prompt."),
    ("Medium", "Activation, retention", "The first video carries a placeholder logo. The first output is what people judge the product by.",
     "First videos made with an auto-built brand kit."),
    ("High", "Revenue, retention", "A free user can spend credits on the most expensive model without knowing, and hit the limit before seeing value.",
     "Credits used before the first export, by model."),
    ("High", "Activation", "Over nine minutes with no end in sight. Anyone who closes the tab may never see the finished video.",
     "Builds finished with nobody returning to watch."),
    ("High", "Paid conversion, trust", "Limits at the payoff moment can push an upgrade, but a surprise there feels like a trap, and it's the last thing people remember.",
     "At the limit: upgrade vs leave."),
    ("Medium", "Retention", "On day two, Alex doesn't know where yesterday's work lives. Returning users start over or give up.",
     "Day-2 users who reopen yesterday's video."),
]

MOMENTS = ["Sign up", "Onboarding", "First value", "Home", "Build", "Share", "Next day"]
PSYCH_BEFORE = [3, 2, 1, 2, 2, 2, 1]  # the audit's assessment, 1 = fighting the product, 5 = effortless

CHEAT = [
    ("Hick's law", "Keep a decision to about four clear options."),
    ("Cognitive load", "Don't ask for what you already know. Remove what competes with the task."),
    ("Banner blindness", "Every area should inform. Decoration teaches people to look away."),
    ("Feedforward", "Show the cost and outcome before the click."),
    ("Goal-gradient effect", "Show progress toward an end, not time spent."),
    ("Mental model", "Same thing, same name, one place."),
    ("Fogg behavior model", "Make the first step the easiest one."),
    ("Default bias", "Defaults are decisions. Make them right for most people."),
    ("Reactance", "Say it once."),
    ("Doherty threshold", "Respond at once, or show what's happening."),
    ("Peak-end rule", "Protect the best moment and the last one."),
]


def build():
    from PIL import Image
    img_dir = os.path.join(HERE, "img")
    for f in os.listdir(img_dir):
        os.remove(os.path.join(img_dir, f))
    Image.open(os.path.join(HERE, "portrait.jpg")).save(os.path.join(img_dir, "lokesh.jpg"), quality=88)
    data, n_issue, n_fix = [], 0, 0
    for s in SLIDES:
        d = dict(s)
        src = os.path.join(ROOT, "screenshots" if s["src"] == "shot" else "doc/raw", s["img"])
        out = ("b-" if s["kind"] == "issue" else "a-") + s["img"]
        im = Image.open(src).convert("RGB")
        d["w"], d["h"] = im.size
        im.save(os.path.join(img_dir, out), quality=86, optimize=True)
        d["file"] = "img/" + out
        if s["kind"] == "issue":
            n_issue += 1; d["n"] = n_issue
        else:
            n_fix += 1; d["n"] = n_fix
        del d["src"]
        data.append(d)
    # Alex's point of view, plus a running tally per act (screens seen, credits spent: observed numbers only)
    screens = {"issue": 0, "fix": 0}
    for d, (want, thought, ds, cr), (imp, metric, why, check) in zip(data, POV, COST):
        screens[d["kind"]] += ds
        d["want"], d["thought"], d["screens"], d["credits"] = want, thought, screens[d["kind"]], cr
        d["impact"], d["metric"], d["cost"], d["check"] = imp, metric, why, check
    # where each principle shows up, for the cheat sheet
    where = {}
    for d in data:
        where.setdefault(d["principle"][0], []).append(("Issue " if d["kind"] == "issue" else "Fix ") + str(d["n"]))
    cheat = [[n, r, ", ".join(where.get(n, []))] for n, r in CHEAT]
    summary = [[d["n"], d["title"], d["metric"], d["impact"]] for d in data]
    payload = {"slides": data, "moments": MOMENTS, "before": PSYCH_BEFORE, "cheat": cheat, "summary": summary, "issues": n_issue, "fixes": n_fix}
    page = open(os.path.join(HERE, "template.html")).read().replace("/*DATA*/", "const DATA = " + json.dumps(payload, ensure_ascii=False) + ";")
    open(os.path.join(HERE, "index.html"), "w").write(page)
    print("wrote casestudy/index.html:", n_issue, "issues,", n_fix, "fixes,", len(os.listdir(img_dir)), "images")


if __name__ == "__main__":
    build()
