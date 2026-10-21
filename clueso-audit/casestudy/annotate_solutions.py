"""Solution case study: prototype screenshots with numbered boxes and arrows to callout cards (solution + what it solves).
Run: python3 casestudy/annotate_solutions.py  → casestudy/sol-img/*.png
Boxes are in each screenshot's own pixel space; SCALE says how much to enlarge it for sharp text.
Same card layout as annotate_onboarding.py, so the two case studies read as a pair.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sol-src")
OUT = os.path.join(HERE, "sol-img")
os.makedirs(OUT, exist_ok=True)

PANEL = 820
KIND = {"fix": (22, 140, 80), "tradeoff": (196, 140, 0)}
KIND_WORD = {"fix": "SOLVED", "tradeoff": "TRADE-OFF"}
LAST_LABEL = {"fix": "SOLVES", "tradeoff": "TRADE-OFF"}
HELV = "/System/Library/Fonts/Helvetica.ttc"
F_NUM = ImageFont.truetype(HELV, 26, index=1)
F_TITLE = ImageFont.truetype(HELV, 27, index=1)
F_BODY = ImageFont.truetype(HELV, 23)
F_LAB = ImageFont.truetype(HELV, 19, index=1)
F_TAG = ImageFont.truetype(HELV, 20, index=1)
INK, QUIET, CARD, LINE, BG, TAG_BG = (28, 28, 30), (92, 92, 98), (255, 255, 255), (222, 222, 226), (244, 244, 246), (240, 240, 244)

# (file, scale, crop or None, [(box, kind, title, principle, solution, solves), ...])
SHOTS = [
    ("s02-starter.jpg", 2, None, [
        ((660, 4, 798, 28), "fix", "Focus mode, and try before an account",
         "Value before commitment · Cognitive load",
         "A new visitor lands on a working Home: only Help, Sign in and Sign up around the box. No side menu, sale banner, survey, model or brand picker.",
         "Stage 1 and 4: an account before any value, and seven elements competing with the main CTA."),
        ((195, 130, 605, 205), "fix", "The first Home visit is the onboarding",
         "Time to value · Teach by doing",
         "No wizard. The box is ready on the first screen, so the first action is the real task.",
         "Stage 2: four profiling screens before value, with answers that change nothing."),
        ((462, 184, 582, 199), "tradeoff", "Cost shown before Send",
         "Feedforward · Cost transparency",
         "The box says what this video will cost and what's left: \"About 150–250 credits · 1,000 left\".",
         "No more surprise at the bill. But the first video isn't free yet: that stays Clueso's call (H9)."),
        ((274, 211, 334, 228), "fix", "Examples, not a gate",
         "Recognition over recall · Reversibility",
         "A starter fills an editable brief. The video-type question becomes a suggestion users can ignore or change.",
         "Stage 3: a type question users can't answer on day one, and suggestions that ignore their answers."),
        ((195, 258, 605, 308), "fix", "Ways to start, ordered by effort",
         "Fogg behaviour model · Choice architecture",
         "Describe it first, then upload, then record, with an honest time: \"About 2 minutes\". Nothing is tagged Recommended.",
         "Stage 3: Record listed first and recommended, the hardest and most stressful path."),
        ((193, 350, 607, 477), "fix", "See a finished video before making one",
         "Low-commitment path · Show, don't tell",
         "Clueprints are finished Clueso styles. Each one plays as a preview, and Create video uses it.",
         "Stage 2: explorers land on an empty Projects page with nothing to watch."),
    ]),
    ("s03-plan.jpg", 2, None, [
        ((203, 123, 400, 137), "fix", "An intent preview with one-click Change",
         "Feedforward · User control and freedom",
         "Clueso says what it will make, read from the brief. Change fixes it in place, with no going back.",
         "Stage 3: a choice made just to get past the screen can't be corrected (reversibility)."),
        ((203, 144, 597, 192), "fix", "Kept from live: the plan",
         "Mental model · Expectation setting",
         "Six timed scenes show the video's structure before anything is built. It was live's strongest touchpoint, so it stays.",
         "Stage 5: a long build with no idea of what's coming."),
        ((203, 220, 392, 243), "fix", "Cost in videos, and a promise",
         "Loss aversion · Feedforward",
         "\"Uses about 1 of your 5 free videos · about 10 minutes. You'll create an account to build it. Your brief is kept.\"",
         "Stage 3: a cost the user can't predict. Videos are a unit people understand; credits aren't."),
    ]),
    ("s04-account-at-build.jpg", 2, None, [
        ((284, 106, 416, 132), "fix", "The account is asked at commitment",
         "Value before commitment · Endowed progress",
         "\"Create your free account to build your video. Your brief and plan are kept.\"",
         "Stage 1 and 2: sign-up and setup screens before any value."),
        ((285, 167, 517, 211), "fix", "Shows what they're saving",
         "Goal-gradient effect · Ownership",
         "The planned video, named from their brief: \"How to create your first project · 6 scenes\".",
         "Stage 2: interaction cost with no visible payoff."),
        ((283, 219, 517, 335), "fix", "The shortest form",
         "Redundant input · Interaction cost",
         "Google, SSO, or email and password. No name, role or workspace fields: Google gives the name, and nothing is asked twice.",
         "Stage 1: the name asked after Google gave it, then asked again."),
    ]),
    ("s05-building.jpg", 2, None, [
        ((126, 46, 282, 120), "fix", "One tip, when it matters",
         "Progressive disclosure · Just-in-time help",
         "The full app appears when the video starts building, with one tip pointing at Projects. No tour.",
         "Stage 4: a hidden checklist and a crowded first Home. NN/g: tutorials don't raise task success."),
        ((714, 95, 773, 109), "fix", "Time left, not time passed",
         "Visibility of system status · Doherty threshold",
         "\"about 8 min left\", updated as scenes finish.",
         "Stage 5: \"Working for 4m 54s\" with no estimate."),
        ((152, 121, 772, 192), "fix", "Scenes appear as they're built",
         "Goal-gradient effect · Time to value",
         "Built scenes play; the current one shows it's building; the rest say Up next. The first \"that's my product\" comes after scene 1.",
         "Stage 5: a 10-minute wait before anything can be seen."),
        ((152, 199, 556, 213), "fix", "Safe to leave",
         "User control · Re-engagement",
         "\"You can close this; we'll email alex.rivera@gmail.com when it's done.\" Read the script while waiting.",
         "Stage 5: people close the tab and never watch the result."),
    ]),
    ("s06-ready.jpg", 2, None, [
        ((143, 62, 300, 79), "fix", "A short name from the brief",
         "Recognition · Ownership",
         "\"How to create your first project\", not the whole brief cut at four words.",
         "Stage 5: the aha should look like their video, not a system record."),
        ((145, 90, 778, 129), "fix", "One next step: watch it",
         "Aha moment · Single next step",
         "\"Your video is ready · Watch it first: it takes a minute.\" Brand and other steps wait until it's watched.",
         "Stage 5: the aha moment is hard to reach."),
    ]),
    ("s08-end.jpg", 2, None, [
        ((176, 77, 625, 350), "fix", "The aha, played in place",
         "Aha moment · Peak-end rule",
         "A player with captions and progress plays their own video, on the project page.",
         "Stage 5: the first video can't be watched. The design gives it a player; the freeze itself is an engineering fix."),
        ((176, 361, 625, 424), "fix", "Ends on the next action",
         "Peak-end rule · Habit loop",
         "\"That's your video\": Share link, or Open editor to change anything.",
         "Stage 5: the journey ends on a surprise instead of a win."),
    ]),
    ("s09-share.jpg", 2, None, [
        ((246, 217, 555, 248), "fix", "Limits stated before you commit",
         "Feedforward · Expectation setting",
         "\"Creating a link uses about 1 of your 10 free export minutes left this month. Free links include a Clueso watermark.\"",
         "Stage 5: limits hidden at the payoff, found only after Share."),
        ((425, 255, 555, 273), "fix", "Locked options say why",
         "Match with the real world · Transparency",
         "2K and 4K are visible but locked: \"2K is on Solo, 4K on Business\".",
         "Stage 5: the 1080p cap appears only after export."),
    ]),
    ("s11-home-after.jpg", 2, None, [
        ((258, 164, 478, 184), "fix", "Full controls after the first video",
         "Progressive disclosure · Safe defaults",
         "Ask, model and brand appear once there's a video. In the first run they're hidden, and brand is offered on the result.",
         "Stage 4: a fake brand kit and the most expensive model as silent defaults."),
        ((256, 195, 478, 209), "fix", "Progress from real events",
         "Endowed progress · Goal-gradient effect",
         "\"2 of 4 done · Next: add your brand\". One step at a time, ticked only by what the user really did.",
         "Stage 4: a 6-item checklist, ticked by a blank project."),
        ((257, 364, 388, 472), "fix", "Their video, waiting on Home",
         "Recognition over recall · Return visit",
         "The first project sits under Recent projects, ready to reopen.",
         "Stage 5: no reason to come back the next day (H10)."),
    ]),
    ("s12-clarify.jpg", 2, None, [
        ((195, 120, 573, 255), "fix", "One clarifying question, with answers",
         "Blank-canvas problem · Recognition over recall",
         "A brief that's too short gets one question, three example answers and Something else. Nothing is built from a guess.",
         "Stage 3: users don't know what a good input looks like."),
        ((522, 257, 571, 270), "tradeoff", "Replies cost credits, shown",
         "Cost transparency",
         "\"13 credits\" per reply, as on live, shown on the message.",
         "Before the first video this could be free. Kept as live for now; a call for Clueso."),
    ]),
    ("s10-emails.jpg", 2, None, [
        ((163, 265, 290, 305), "fix", "A clear trigger and stop rule",
         "Trigger by behaviour · Respect attention",
         "Each email has a when (\"Signed up, no brief after 1 day\") and a stop (\"Stops once a brief is sent\"). Never more than one a day.",
         "Stage 5 and H10: people who stall never come back."),
        ((298, 258, 637, 412), "fix", "The email asks for the next step",
         "Re-engagement · Single next step",
         "One button that continues where they stopped, like \"Start my video\".",
         "Stage 3 to 5: drop-off between sign-up, plan, build and share."),
    ]),
    ("s13-phone.jpg", 1, (0, 100, 780, 1000), [
        ((40, 132, 740, 420), "fix", "The same first screen on a phone",
         "Responsive design · Context of use",
         "The box, examples and ways to start reflow to one column. Nothing is cut.",
         "Stage 3: the flow assumed desktop Chrome (context blindness)."),
        ((40, 800, 740, 965), "fix", "No dead end on phones",
         "Graceful degradation · Context of use",
         "\"Record on your computer: Screen recording needs a computer. We'll email you a link to open there.\"",
         "Stage 3: device and file availability. Upload stays first for a file that is on the phone."),
    ]),
]


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


def render(fname, S, crop, items):
    items = sorted(items, key=lambda it: (it[0][1] + it[0][3]) / 2)  # cards top to bottom, like their boxes
    shot = Image.open(os.path.join(SRC, fname)).convert("RGB")
    if crop:
        cx, cy, cx1, cy1 = crop
        shot = shot.crop(crop)
        items = [(((b[0] - cx), (b[1] - cy), (b[2] - cx), (b[3] - cy)), *rest) for b, *rest in items]
    shot = shot.resize((shot.width * S, shot.height * S), Image.LANCZOS)
    sw, sh = shot.size
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    pad, inner = 28, PANEL - 2 * 28 - 76 - 24
    cards = []
    for box, kind, title, prin, sol, solves in items:
        tl = wrap(tmp, title, F_TITLE, inner)
        pl = wrap(tmp, sol, F_BODY, inner)
        il = wrap(tmp, solves, F_BODY, inner)
        h = 24 + 34 * len(tl) + 8 + 34 + 12 + 22 + 30 * len(pl) + 14 + 22 + 30 * len(il) + 22
        cards.append((h, tl, pl, il))
    gap = 18
    total = sum(c[0] for c in cards) + gap * (len(cards) - 1)
    H = max(sh, total + 2 * pad)
    W = sw + PANEL
    im = Image.new("RGB", (W, H), BG)
    oy = (H - sh) // 2
    im.paste(shot, (0, oy))
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for box, kind, *_ in items:
        x0, y0, x1, y1 = [v * S for v in box]
        od.rectangle([x0, y0 + oy, x1, y1 + oy], fill=KIND[kind] + (26,))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(im)
    d.rectangle([sw, 0, W, H], fill=BG)
    d.line([sw, 0, sw, H], fill=LINE, width=2)
    y = (H - total) // 2
    for i, ((box, kind, title, prin, *_), (h, tl, pl, il)) in enumerate(zip(items, cards)):
        c = KIND[kind]
        x0, y0, x1, y1 = [v * S for v in box]
        y0 += oy
        y1 += oy
        cx0 = sw + pad
        d.rounded_rectangle([cx0, y, W - pad, y + h], radius=14, fill=CARD, outline=LINE, width=2)
        d.rectangle([cx0, y + 14, cx0 + 6, y + h - 14], fill=c)
        bx, by = cx0 + 38, y + 40
        d.ellipse([bx - 20, by - 20, bx + 20, by + 20], fill=c)
        n = str(i + 1)
        d.text((bx - d.textlength(n, font=F_NUM) / 2, by - 15), n, font=F_NUM, fill=(255, 255, 255))
        tx, ty = cx0 + 76, y + 24
        for ln in tl:
            d.text((tx, ty), ln, font=F_TITLE, fill=INK)
            ty += 34
        ty += 8
        tag = "UX PRINCIPLE  ·  " + prin
        tw = d.textlength(tag, font=F_TAG)
        d.rounded_rectangle([tx, ty, tx + tw + 24, ty + 34], radius=8, fill=TAG_BG)
        d.text((tx + 12, ty + 6), tag, font=F_TAG, fill=QUIET)
        ty += 34 + 12
        d.text((tx, ty), "SOLUTION", font=F_LAB, fill=QUIET)
        kw = KIND_WORD[kind]
        d.text((W - pad - 22 - d.textlength(kw, font=F_LAB), y + 22), kw, font=F_LAB, fill=c)
        ty += 22
        for ln in pl:
            d.text((tx, ty), ln, font=F_BODY, fill=INK)
            ty += 30
        ty += 14
        d.text((tx, ty), LAST_LABEL[kind], font=F_LAB, fill=c)
        ty += 22
        for ln in il:
            d.text((tx, ty), ln, font=F_BODY, fill=INK)
            ty += 30
        d.rectangle([x0, y0, x1, y1], outline=c, width=5)
        r = 18
        nx, ny = max(r + 4, min(x0, sw - r - 4)), max(r + 4, min(y0, H - r - 4))
        sx, sy = cx0 - 4, by
        tx_, ty_ = min(max(sx, x0), x1), min(max(sy, y0), y1)
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
    for f, s, crop, items in SHOTS:
        print(render(f, s, crop, items))
