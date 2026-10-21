"""Onboarding case study: live Clueso screenshots with numbered boxes and arrows to callout cards (problem + impact).
Run: python3 casestudy/annotate_onboarding.py  → casestudy/onb-img/*.png
Boxes are in the screenshot's own 800-px-wide pixel space.
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "live-screenshots", "1-audit-journey")
OUT = os.path.join(HERE, "onb-img")
os.makedirs(OUT, exist_ok=True)

S = 2  # screenshots are drawn at 2x for sharp text
PANEL = 820
SEV = {"critical": (214, 40, 40), "major": (230, 100, 20), "minor": (196, 140, 0)}
SEV_WORD = {"critical": "CRITICAL", "major": "MAJOR", "minor": "MINOR"}
HELV = "/System/Library/Fonts/Helvetica.ttc"
F_NUM = ImageFont.truetype(HELV, 26, index=1)
F_TITLE = ImageFont.truetype(HELV, 27, index=1)
F_BODY = ImageFont.truetype(HELV, 23)
F_LAB = ImageFont.truetype(HELV, 19, index=1)
INK, QUIET, CARD, LINE, BG = (28, 28, 30), (92, 92, 98), (255, 255, 255), (222, 222, 226), (244, 244, 246)

# (file, [(box, severity, title, problem, impact), ...])
SHOTS = [
    ("02-signup-personal-email.jpg", [
        ((266, 414, 534, 432), "major", "Work-email warning while typing",
         "Appears as soon as a Gmail address is typed and pushes the password field down.",
         "It pushes back on a valid choice at the very first form, so fewer people who are just trying it sign up."),
    ]),
    ("04-complete-profile.jpg", [
        ((118, 282, 338, 322), "major", "Name asked after Google gave it",
         "First and last name are empty right after signing in with Google.",
         "Extra effort before any value. It feels like the Google sign-in didn't work."),
        ((458, 0, 798, 500), "minor", "A scrolling wall beside the form",
         "Testimonials and videos keep moving. Tiles like \"Spotify\" look like other companies' products.",
         "Competes with the only task on the page."),
    ]),
    ("06-loading-logo.jpg", [
        ((366, 232, 434, 300), "critical", "About 20 seconds of blank screen",
         "An empty grey page, then a faint logo. No progress, no message, no estimate.",
         "Reads as broken. People who reload or leave here never see the product."),
    ]),
    ("07-onb-goals.jpg", [
        ((355, 13, 652, 38), "major", "The work-email nag returns",
         "The same message sits on top of every onboarding step, even over modals.",
         "Feels like pressure after the user already decided."),
        ((480, 47, 790, 523), "minor", "40% of the screen is decoration",
         "\"Make something beautiful\" tells the user nothing about this step.",
         "Setup feels longer. This space could show what each choice unlocks."),
        ((86, 84, 216, 91), "minor", "No visible step count",
         "\"Step 1 of 4\" exists only for screen readers; sighted users see four dashes.",
         "People can't tell how much is left, so they're likelier to quit."),
    ]),
    ("09-onb-profile.jpg", [
        ((86, 194, 394, 226), "major", "Name asked a second time",
         "First and last name again, under a minute after the profile screen.",
         "Repeated effort makes the product feel careless."),
        ((86, 238, 394, 267), "minor", "Role is required",
         "\"Looks good, continue\" stays disabled until a role is picked, with no reason shown.",
         "Confusion and repeated clicks on a button that looks ready."),
    ]),
    ("11-onb-role-options.jpg", [
        ((84, 266, 396, 416), "major", "13 roles, and none change anything",
         "No clear order, and mixed names (\"Customer education & training\" next to \"Learning and development\", \"CXO\").",
         "People pick at random, so the role data can't be trusted for segmentation."),
    ]),
    ("13-onb-workspace.jpg", [
        ((86, 209, 394, 227), "minor", "A workspace step for a solo user",
         "The name is already prefilled and can be changed later.",
         "One more screen before value, adding nothing."),
        ((493, 476, 527, 510), "minor", "Two initials for one workspace",
         "\"U\" on the left, \"UW\" in the preview.",
         "Small, but it erodes trust in the details."),
    ]),
    ("14-onb-first-video.jpg", [
        ((87, 148, 393, 198), "critical", "\"Recommended for you\" needs an install",
         "Record screen is recommended, but nothing says it needs a browser extension.",
         "The easiest-looking path is the hardest one."),
        ((87, 371, 393, 490), "minor", "Options a new user can't use yet",
         "\"Translate an existing video\" (there is none) and an AI-assistant integration for developers.",
         "More choices, slower first decision."),
        ((482, 47, 786, 190), "minor", "Templates with no heading",
         "Clueprint cards sit on the right, unlabelled.",
         "Users can't tell they can pick them, so a good shortcut is missed."),
    ]),
    ("15-onb-extension-gate.jpg", [
        ((240, 170, 560, 363), "critical", "Install wall at the moment of value",
         "\"Install the extension, then come back here\" sends the user to the Chrome Web Store.",
         "Anyone who doesn't come back after installing is lost before activation."),
    ]),
    ("16-onb-prompt-modal.jpg", [
        ((210, 328, 578, 345), "major", "Suggestions ignore my answers",
         "After choosing product demos and SOPs: \"Facts about Lewis Hamilton\", \"How Spotify recommends music\".",
         "The four setup screens feel pointless in hindsight."),
        ((532, 299, 571, 319), "major", "A cost the user can't predict",
         "One video from a prompt later cost 250 credits, a quarter of the month. Nothing here says so, and the first try isn't free.",
         "Paying before any value feels like a loss. Trust drops, and paid conversion with it."),
    ]),
    ("18-home-checklist-survey.jpg", [
        ((0, 0, 800, 26), "minor", "A sale banner on day one",
         "Pricing and promotion before the first video.",
         "Pulls attention from the only task that matters."),
        ((636, 252, 792, 475), "major", "A survey seconds after arriving",
         "\"How did you hear about us?\" covers part of the page.",
         "It interrupts the first prompt, and rushed users give poor answers."),
        ((413, 264, 481, 282), "critical", "Brand kit on by default",
         "A kit built from gmail.com is attached to every prompt.",
         "The first video ships with a fake logo."),
        ((347, 264, 411, 282), "major", "A model picker on the prompt",
         "Defaults to the most expensive model, with no costs shown.",
         "Free-plan credits run out faster, and the user doesn't know why."),
        ((6, 286, 118, 421), "major", "Checklist hidden in the sidebar",
         "Folded under a promo card. \"Make your first video\" got ticked by a blank project.",
         "It doesn't guide or motivate."),
        ((6, 503, 118, 528), "major", "\"Free trial\" vs \"free plan\" vs \"Free\"",
         "One plan, three names. A trial implies an end date this plan doesn't have.",
         "Users worry about a hidden deadline."),
    ]),
    ("24-brand-kit-gmail.jpg", [
        ((278, 155, 590, 175), "critical", "Brand pulled from gmail.com",
         "The kit was taken from the email domain, not a company website.",
         "Every Gmail, Outlook or Yahoo user gets the same junk kit."),
        ((278, 195, 345, 236), "critical", "A placeholder logo shown as theirs",
         "This pink mark appears in the intros and outros of first videos.",
         "People judge the product by its first video, and it looks wrong."),
        ((278, 120, 632, 135), "major", "\"Set during onboarding\", but it wasn't",
         "No onboarding step asked about brand, colours or a website.",
         "The product describes something that didn't happen, so trust drops."),
    ]),
    ("46-model-picker.jpg", [
        ((346, 288, 514, 468), "major", "Six vendor models, no costs",
         "Each is described by its vendor (\"Anthropic's most capable model\"), with no price, speed or quality. The default is the most expensive.",
         "A free user can use up credits before seeing value."),
    ]),
    ("63-ai-video-building.jpg", [
        ((597, 316, 702, 331), "major", "Elapsed time, no estimate",
         "\"Working for 4m 54s\", later \"Thinking for 8m 14s\". It doesn't say how many scenes are done or how long is left.",
         "People close the tab and never watch the result."),
        ((597, 225, 712, 263), "major", "Alarming failures, silent recovery",
         "\"Ran 4 steps (2 failed)\" and \"Couldn't finish this step\" in red, then it keeps going.",
         "Users think it broke and leave."),
    ]),
    ("54-editor-preview-stuck.jpg", [
        ((280, 151, 592, 311), "critical", "The preview freezes",
         "After Generate speech, play stayed disabled for over a minute, until a reload. No error message.",
         "The first video can't be watched: the aha never comes."),
    ]),
    ("57-share-export.jpg", [
        ((372, 140, 552, 396), "major", "Limits hidden at the payoff",
         "Share opens on Export. It says nothing about the 10 free minutes a month, the watermark or the 1080p limit.",
         "A surprise at the last step is what people remember."),
    ]),
]


# The UX principle each pain point breaks, shown as a tag on its card
PRINCIPLE = {
    "Work-email warning while typing": "Reactance \u00b7 Interaction cost",
    "Name asked after Google gave it": "Redundant input \u00b7 Interaction cost",
    "A scrolling wall beside the form": "Signal-to-noise \u00b7 Attention competition",
    "About 20 seconds of blank screen": "Visibility of system status \u00b7 Doherty threshold",
    "The work-email nag returns": "Reactance \u00b7 Nagging",
    "40% of the screen is decoration": "Signal-to-noise \u00b7 Banner blindness",
    "No visible step count": "Goal-gradient effect \u00b7 Progress indicator",
    "Name asked a second time": "Consistency \u00b7 Redundant input",
    "Role is required": "Error prevention \u00b7 False affordance",
    "13 roles, and none change anything": "Hick's law \u00b7 Choice overload",
    "A workspace step for a solo user": "Progressive disclosure \u00b7 Deferred setup",
    "Two initials for one workspace": "Consistency and standards",
    "\"Recommended for you\" needs an install": "Fogg behaviour model \u00b7 Time to value",
    "Options a new user can't use yet": "Hick's law \u00b7 Progressive disclosure",
    "Templates with no heading": "Information scent \u00b7 Recognition over recall",
    "Install wall at the moment of value": "Time to value \u00b7 Context switching",
    "Suggestions ignore my answers": "Personalisation gap \u00b7 Blank-canvas problem",
    "A cost the user can't predict": "Expectation violation \u00b7 Loss aversion",
    "A sale banner on day one": "Cognitive load \u00b7 Premature monetisation",
    "A survey seconds after arriving": "Interruption cost \u00b7 Ask after value",
    "Brand kit on by default": "Default bias \u00b7 Error prevention",
    "A model picker on the prompt": "Mental-model mismatch \u00b7 Feedforward",
    "Checklist hidden in the sidebar": "Discoverability \u00b7 Endowed progress",
    "\"Free trial\" vs \"free plan\" vs \"Free\"": "Consistency \u00b7 Mental model",
    "Brand pulled from gmail.com": "Error prevention \u00b7 Default bias",
    "A placeholder logo shown as theirs": "First impression \u00b7 Trust",
    "\"Set during onboarding\", but it wasn't": "Match with the real world \u00b7 Trust",
    "Six vendor models, no costs": "Mental-model mismatch \u00b7 Feedforward",
    "Elapsed time, no estimate": "Visibility of system status \u00b7 Goal-gradient effect",
    "Alarming failures, silent recovery": "Error messaging \u00b7 System status",
    "The preview freezes": "Error recovery \u00b7 Broken aha moment",
    "Limits hidden at the payoff": "Peak-end rule \u00b7 Expectation violation",
}
F_TAG = ImageFont.truetype(HELV, 20, index=1)
TAG_BG = (240, 240, 244)


def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render(fname, items):
    items = sorted(items, key=lambda it: (it[0][1] + it[0][3]) / 2)  # cards top to bottom, like their boxes
    shot = Image.open(os.path.join(SRC, fname)).convert("RGB")
    shot = shot.resize((shot.width * S, shot.height * S), Image.LANCZOS)
    sw, sh = shot.size
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    pad, inner = 28, PANEL - 2 * 28 - 76 - 24
    cards = []
    for i, (box, sev, title, prob, imp) in enumerate(items):
        tl = wrap(tmp, title, F_TITLE, inner)
        pl = wrap(tmp, prob, F_BODY, inner - 0)
        il = wrap(tmp, imp, F_BODY, inner - 0)
        h = 24 + 34 * len(tl) + 8 + 34 + 12 + 22 + 30 * len(pl) + 14 + 22 + 30 * len(il) + 22
        cards.append((h, tl, pl, il))
    gap = 18
    total = sum(c[0] for c in cards) + gap * (len(cards) - 1)
    H = max(sh, total + 2 * pad)
    W = sw + PANEL
    im = Image.new("RGB", (W, H), BG)
    im.paste(shot, (0, (H - sh) // 2))
    oy = (H - sh) // 2
    # tint inside boxes
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for box, sev, *_ in items:
        c = SEV[sev]
        x0, y0, x1, y1 = [v * S for v in box]
        od.rectangle([x0, y0 + oy, x1, y1 + oy], fill=c + (30,))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(im)
    d.rectangle([sw, 0, W, H], fill=BG)
    d.line([sw, 0, sw, H], fill=LINE, width=2)
    y = (H - total) // 2
    for i, ((box, sev, title, *_), (h, tl, pl, il)) in enumerate(zip(items, cards)):
        c = SEV[sev]
        x0, y0, x1, y1 = [v * S for v in box]
        y0 += oy
        y1 += oy
        cx0 = sw + pad
        d.rounded_rectangle([cx0, y, W - pad, y + h], radius=14, fill=CARD, outline=LINE, width=2)
        d.rectangle([cx0, y + 14, cx0 + 6, y + h - 14], fill=c)
        # number badge on card
        bx, by = cx0 + 38, y + 40
        d.ellipse([bx - 20, by - 20, bx + 20, by + 20], fill=c)
        n = str(i + 1)
        d.text((bx - d.textlength(n, font=F_NUM) / 2, by - 15), n, font=F_NUM, fill=(255, 255, 255))
        tx = cx0 + 76
        ty = y + 24
        for ln in tl:
            d.text((tx, ty), ln, font=F_TITLE, fill=INK)
            ty += 34
        ty += 8
        tag = "UX PRINCIPLE  \u00b7  " + PRINCIPLE[title]
        tw = d.textlength(tag, font=F_TAG)
        d.rounded_rectangle([tx, ty, tx + tw + 24, ty + 34], radius=8, fill=TAG_BG)
        d.text((tx + 12, ty + 6), tag, font=F_TAG, fill=QUIET)
        ty += 34 + 12
        d.text((tx, ty), "PAIN POINT", font=F_LAB, fill=QUIET)
        sevw = SEV_WORD[sev]
        d.text((W - pad - 22 - d.textlength(sevw, font=F_LAB), y + 22), sevw, font=F_LAB, fill=c)
        ty += 22
        for ln in pl:
            d.text((tx, ty), ln, font=F_BODY, fill=INK)
            ty += 30
        ty += 14
        d.text((tx, ty), "BUSINESS IMPACT", font=F_LAB, fill=c)
        ty += 22
        for ln in il:
            d.text((tx, ty), ln, font=F_BODY, fill=INK)
            ty += 30
        # box, then a straight arrow from the card to the nearest point of the box
        d.rectangle([x0, y0, x1, y1], outline=c, width=5)
        r = 18
        nx, ny = max(r + 4, min(x0, sw - r - 4)), max(r + 4, min(y0, H - r - 4))
        sx, sy = cx0 - 4, by
        tx_ = min(max(sx, x0), x1)
        ty_ = min(max(sy, y0), y1)
        if tx_ >= x1 - 1 and x1 >= sw - 12:  # box reaches the panel edge: aim at its top or bottom edge
            tx_ = (x0 + x1) / 2 if x1 - x0 < 300 else x1 - 120
            ty_ = y0 if sy < y0 else (y1 if sy > y1 else y0)
        dx, dy = tx_ - sx, ty_ - sy
        L = max(1.0, (dx * dx + dy * dy) ** 0.5)
        ux, uy = dx / L, dy / L
        ex, ey = tx_ - ux * 6, ty_ - uy * 6
        d.line([(sx, sy), (ex, ey)], fill=(255, 255, 255), width=10)
        d.line([(sx, sy), (ex, ey)], fill=c, width=4)
        hx, hy = ex - ux * 22, ey - uy * 22
        px_, py_ = -uy * 12, ux * 12
        d.polygon([(ex + ux * 4, ey + uy * 4), (hx + px_, hy + py_), (hx - px_, hy - py_)], fill=c, outline=(255, 255, 255))
        d.ellipse([nx - r, ny - r, nx + r, ny + r], fill=c, outline=(255, 255, 255), width=3)
        d.text((nx - d.textlength(n, font=F_NUM) / 2 + 1, ny - 15), n, font=F_NUM, fill=(255, 255, 255))
        y += h + gap
    name = os.path.splitext(fname)[0] + ".png"
    im.save(os.path.join(OUT, name), optimize=True)
    return name, im.size


if __name__ == "__main__":
    for f, items in SHOTS:
        print(render(f, items))
