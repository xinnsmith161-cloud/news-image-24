#!/usr/bin/env python3
"""Draw 'The World' front page for Tuesday, 24 November 2026.

Every headline below traces to a news report verified for 23-24 Nov 2026
(see stories.md in the work dir for outlet and headline per story).
The drawing is done entirely with Pillow: no network, no photos, no
external assets. Type is DejaVu (system fonts), black on off-white,
laid out as a classic three-column broadsheet front page.
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 253, 248)
INK = (12, 12, 12)
GREY = (70, 70, 70)
RULE = (30, 30, 30)
ACCENT = (140, 20, 20)
BAR = (18, 18, 18)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 64)
F_DATE = font("DejaVuSans-Bold.ttf", 18)
F_META = font("DejaVuSans.ttf", 11)
F_KICK = font("DejaVuSans-Bold.ttf", 12)
F_LEAD = font("DejaVuSerif-Bold.ttf", 29)
F_LEAD_DECK = font("DejaVuSerif.ttf", 14)
F_SECT = font("DejaVuSans-Bold.ttf", 12)
F_HEAD = font("DejaVuSerif-Bold.ttf", 13)
F_DEK = font("DejaVuSans.ttf", 11)

MARGIN = 22
COL_W = 320
GUTTER = 12
COL_X = [MARGIN, MARGIN + COL_W + GUTTER, MARGIN + 2 * (COL_W + GUTTER)]


def wrap(draw, text, fnt, width):
    """Wrap text to the given pixel width, word by word."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_item(draw, x, y, headline, dek, width):
    """One dense item: bold headline (max 2 lines) + one-line standfirst."""
    head_lines = wrap(draw, headline, F_HEAD, width)
    assert len(head_lines) <= 2, f"headline too long: {headline!r} -> {head_lines}"
    for line in head_lines:
        draw.text((x, y), line, font=F_HEAD, fill=INK)
        y += 17
    assert draw.textlength(dek, font=F_DEK) <= width, f"dek too long: {dek!r}"
    draw.text((x, y), dek, font=F_DEK, fill=GREY)
    y += 16
    draw.line([(x, y + 2), (x + width, y + 2)], fill=(190, 190, 185), width=1)
    return y + 10


def draw_section_head(draw, x, y, label, width):
    draw.rectangle([x, y, x + width, y + 18], fill=BAR)
    draw.text((x + 7, y + 3), label, font=F_SECT, fill=(255, 255, 255))
    return y + 25


def draw_continued(draw, x, y, label, width):
    draw.text((x, y), label + "  -  CONTINUED", font=F_SECT, fill=GREY)
    draw.line([(x, y + 16), (x + width, y + 16)], fill=(150, 150, 145), width=1)
    return y + 23


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    draw.line([(MARGIN, 12), (W - MARGIN, 12)], fill=RULE, width=3)
    title = "The World"
    tw = draw.textlength(title, font=F_MAST)
    draw.text(((W - tw) / 2, 16), title, font=F_MAST, fill=INK)
    date_line = "Tuesday, 24 November 2026"
    dw = draw.textlength(date_line, font=F_DATE)
    draw.text(((W - dw) / 2, 86), date_line, font=F_DATE, fill=ACCENT)
    draw.text((MARGIN, 88), "Vol. CXII  \u00b7  No. 328", font=F_META, fill=GREY)
    right_meta = "World News  \u00b7  46 Stories"
    draw.text((W - MARGIN - draw.textlength(right_meta, font=F_META), 88),
              right_meta, font=F_META, fill=GREY)
    draw.line([(MARGIN, 110), (W - MARGIN, 110)], fill=RULE, width=2)
    draw.line([(MARGIN, 114), (W - MARGIN, 114)], fill=RULE, width=1)

    # ---- Lead story -----------------------------------------------------
    y = 122
    draw.text((MARGIN, y), "LEAD STORY  \u00b7  TECHNOLOGY  \u00b7  MARKETS",
              font=F_KICK, fill=ACCENT)
    y += 18
    lead_head = "Nvidia brings Huang back; shares jump 31%"
    for line in wrap(draw, lead_head, F_LEAD, W - 2 * MARGIN):
        draw.text((MARGIN, y), line, font=F_LEAD, fill=INK)
        y += 33
    deck = ("Board reinstates Jensen Huang 11 days after his exit. "
            "Nasdaq rises 6.5% in its best day in over a year.")
    for line in wrap(draw, deck, F_LEAD_DECK, W - 2 * MARGIN):
        draw.text((MARGIN, y), line, font=F_LEAD_DECK, fill=GREY)
        y += 18
    y += 2
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    body_top = y + 8

    # ---- Sections: (label, [(headline, standfirst), ...]) ---------------
    sections = [
        ("NORTH AMERICA", [
            ("Trump wins path to erase hush-money case",
             "Appeals court lets him seek federal court again."),
            ("Trump orders faster federal executions",
             "Justice Dept told to act without needless delay."),
            ("Court clears Army detonation in Iowa",
             "Appeals court allows blast of bomb material."),
            ("Vance, Rubio meet Qatari PM on Iran",
             "Talks as uncertainty over Trump plans mounts."),
            ("CrowdStrike to buy Zscaler for $43.9bn",
             "All-stock deal is the largest cyber deal yet."),
            ("Amazon buys Decart AI tech in $7.5bn deal",
             "Chip software and founders join Amazon."),
            ("Commanders beat Bengals 22-20",
             "Washington holds on in Monday night finish."),
            ("Pentagon rebukes Canada over defense",
             "Says Ottawa falls short on F-35 review."),
        ]),
        ("LATIN AMERICA", [
            ("Bolsonaro stable in intensive care",
             "Ex-president rests after bowel obstruction."),
            ("Brazil bank chief warns on spending",
             "Galipolo flags inflation risk in remarks."),
            ("Drones hit police base in Cucuta, Colombia",
             "Two civilians hurt; 60 homes damaged."),
            ("Migrant caravan walks toward US border",
             "About 300 cross from Guatemala into Mexico."),
            ("Lula backs Sanchez in Spain snap vote",
             "Brazil leader backs PM ahead of 29 Nov poll."),
            ("Three Salvadoran soldiers die in Haiti blast",
             "Accidental explosion during explosives work."),
        ]),
        ("EUROPE", [
            ("Russian drone enters Polish airspace",
             "Brief incursion during night attack on Ukraine."),
            ("Kremlin warns of painful consequences",
             "Threat after Ukraine hits Russian ships off Libya."),
            ("France rejects EU budget compromise",
             "Paris says text fails farmers on incomes."),
            ("Macron floats constitutional budget rule",
             "Golden rule idea aims to calm bond markets."),
            ("Germany grows, France shrinks in PMIs",
             "German composite 55.0; French composite 46.2."),
            ("Denmark court backs ghetto-law evictions",
             "91 leases ended; no ethnic bias, judges rule."),
            ("Thousands protest living costs in Lisbon",
             "Crowds march over rising prices in Portugal."),
        ]),
        ("AFRICA", [
            ("Fighting traps Ebola responders in Ituri",
             "WHO staff shelter in maternity ward 24 hours."),
            ("Ebola toll nears 5,700 deaths in Congo",
             "11,613 cases in worst-ever DRC outbreak."),
            ("Sudan drone strikes cause mass blackouts",
             "RSF attacks hit power stations, C54 reports."),
            ("Ghana unveils Heritage Series banknotes",
             "Notes honour Nkrumah, Annan, Makola traders."),
            ("Kenya secures 293,600 jobs in Saudi Arabia",
             "Questions over worker protections remain."),
            ("South Africa bowl Bangladesh out for 91",
             "Hosts reach 88 for 1 on day one in Centurion."),
        ]),
        ("MIDDLE EAST", [
            ("US probes Iran link to tanker cyberattacks",
             "Up to 50 ships targeted, WSJ reports."),
            ("Three tankers ablaze after mine hits",
             "Iran claim not independently confirmed."),
            ("Qatar PM pushes to restart US-Iran talks",
             "Push follows meeting with Rubio, reports say."),
            ("Four Palestinians killed in Gaza strikes",
             "Child among dead despite ceasefire, medics say."),
            ("Israel kills two people in southern Syria",
             "Army says pair moved oddly in security zone."),
            ("Iran braces for winter gas shortages",
             "War damage deepens the energy crisis."),
        ]),
        ("ASIA-PACIFIC", [
            ("China unveils Shenzhou-24 crew",
             "Pakistani astronaut first foreigner on station."),
            ("Hasina plans return to Bangladesh",
             "Ousted PM to return from exile on 16 December."),
            ("M5.6 quake strikes Nepal Koshi province",
             "Tremor hits near the China border on Tuesday."),
            ("Russian planes enter Korean defence zone",
             "Seoul issues brief alert for Ulleung island."),
            ("Asian chip stocks jump on Huang return",
             "Taiwan shares trade near price limits."),
            ("India third in Asia Power Index",
             "Ahead of Japan and Russia, Lowy Institute says."),
            ("Indonesia factory fire toll confirmed at 24",
             "Search goes on for about 30 people missing."),
        ]),
        ("OCEANIA", [
            ("Pacific islands go it alone on climate",
             "Own coalitions after COP31 ends with no pact."),
            ("Australia coalition opposes Vanuatu treaty",
             "Climate clauses sink bipartisan backing."),
            ("Fiji closes all schools for five days",
             "El Nino drought crisis deepens, government says."),
            ("India-New Zealand Test ends in a draw",
             "NZ survive 120 overs, finishing on 239 for 5."),
            ("Vanuatu region hit by deep M6.5 quake",
             "No damage reported after Monday tremor."),
        ]),
    ]

    # Balance the three columns at 15 items each, keeping section
    # order and never splitting a section heading from its first item.
    columns = [[], [], []]  # lists of ("head", label) / ("cont", label) / ("item", h, d)
    col_counts = [0, 0, 0]
    col = 0
    # Column capacities: the middle column's headlines wrap longest,
    # so it takes one fewer item than the outer columns.
    capacities = [15, 14, 99]
    for label, items in sections:
        for i, (h, d) in enumerate(items):
            if col_counts[col] >= capacities[col] and col < 2:
                col += 1
            if i == 0:
                columns[col].append(("head", label))
            elif col_counts[col] == 0:
                columns[col].append(("cont", label))
            columns[col].append(("item", h, d))
            col_counts[col] += 1

    footer_y = H - 26
    for x, entries in zip(COL_X, columns):
        y = body_top
        for entry in entries:
            if entry[0] == "head":
                y = draw_section_head(draw, x, y, entry[1], COL_W)
            elif entry[0] == "cont":
                y = draw_continued(draw, x, y, entry[1], COL_W)
            else:
                y = draw_item(draw, x, y, entry[1], entry[2], COL_W)
            assert y <= footer_y - 4, f"column overflow at {entry}"
        draw.line([(x, body_top - 4), (x, y)], fill=(200, 200, 195), width=1)

    # ---- Footer ---------------------------------------------------------
    draw.line([(MARGIN, footer_y - 6), (W - MARGIN, footer_y - 6)],
              fill=RULE, width=1)
    foot = "The World  \u00b7  Tuesday, 24 November 2026  \u00b7  All stories from reports published 23-24 November 2026"
    fw = draw.textlength(foot, font=F_META)
    draw.text(((W - fw) / 2, footer_y + 2), foot, font=F_META, fill=GREY)

    out = Path(__file__).with_name("entry.png")
    img.save(out, optimize=True)
    print(f"wrote {out} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
