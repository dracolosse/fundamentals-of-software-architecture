"""Notion API wrapper for SA Learning Dashboard.
Handles all Notion database operations: create, query, update."""

import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from notion_client import Client

# Load .env from repo root (one level up from tools/)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

_client = None
_config = None
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", ".sa-learn-config.json")

# Chapter metadata: number -> (name, part)
CHAPTERS = {
    1: ("Introduction", "I"), 2: ("Architectural Thinking", "I"),
    3: ("Modularity", "I"), 4: ("Architecture Characteristics Defined", "I"),
    5: ("Identifying Architecture Characteristics", "I"),
    6: ("Measuring and Governing Architecture Characteristics", "I"),
    7: ("Scope of Architecture Characteristics", "I"),
    8: ("Component-Based Thinking", "I"),
    9: ("Foundations", "II"), 10: ("Layered Architecture", "II"),
    11: ("Modular Monolith", "II"), 12: ("Pipeline Architecture", "II"),
    13: ("Microkernel Architecture", "II"), 14: ("Service-Based Architecture", "II"),
    15: ("Event-Driven Architecture", "II"), 16: ("Space-Based Architecture", "II"),
    17: ("Orchestration-Driven SOA", "II"), 18: ("Microservices Architecture", "II"),
    19: ("Choosing Architecture Style", "II"),
    20: ("Architectural Patterns", "III"), 21: ("Architectural Decisions", "III"),
    22: ("Analyzing Architecture Risk", "III"), 23: ("Diagramming Architecture", "III"),
    24: ("Making Teams Effective", "III"),
    25: ("Negotiation and Leadership Skills", "III"),
    26: ("Architectural Intersections", "III"), 27: ("Laws Revisited", "III"),
}

# Chapter -> week mapping
CHAPTER_WEEKS = {
    1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8,
    # Week 9 = Exam 1
    9: 10, 10: 11, 11: 12, 12: 13, 13: 14, 14: 15,
    15: 16, 16: 17, 17: 18, 18: 19, 19: 20,
    # Week 21 = Exam 2
    20: 22, 21: 23, 22: 24, 23: 25, 24: 26, 25: 27, 26: 28, 27: 29,
    # Week 30 = Exam 3
}

LEITNER_INTERVALS = {1: 1, 2: 3, 3: 7, 4: 14, 5: 30}


def get_client():
    """Get or create Notion client."""
    global _client
    if not _client:
        token = os.getenv("NOTION_TOKEN")
        if not token:
            raise RuntimeError("NOTION_TOKEN not set. Check .env file.")
        _client = Client(auth=token, notion_version="2022-06-28")
    return _client


def save_config(config):
    """Save database IDs to config file."""
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def load_config():
    """Load database IDs from config file."""
    global _config
    if _config:
        return _config
    if not os.path.exists(CONFIG_PATH):
        raise RuntimeError("Not set up yet. Run: sa-learn setup")
    with open(CONFIG_PATH) as f:
        _config = json.load(f)
    return _config


def query_database(database_id, filter_obj=None, sorts=None):
    """Query a Notion database."""
    client = get_client()
    body = {}
    if filter_obj:
        body["filter"] = filter_obj
    if sorts:
        body["sorts"] = sorts
    return client.request(
        path=f"databases/{database_id}/query",
        method="POST",
        body=body,
    )


def _create_database(parent_page_id, title, properties):
    """Create a Notion database via raw request (bypasses buggy SDK pick list)."""
    client = get_client()
    return client.request(
        path="databases",
        method="POST",
        body={
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": properties,
        },
    )


def setup_workspace(parent_page_id):
    """Create all 5 databases under the SA page. Returns config dict."""

    # 1. Chapters DB
    chapters_db = _create_database(parent_page_id, "Chapters", {
        "Name": {"title": {}},
        "Number": {"number": {}},
        "Part": {"select": {"options": [
            {"name": "I", "color": "blue"},
            {"name": "II", "color": "green"},
            {"name": "III", "color": "purple"},
        ]}},
        "Status": {"select": {"options": [
            {"name": "Not Started", "color": "default"},
            {"name": "In Progress", "color": "yellow"},
            {"name": "Complete", "color": "green"},
        ]}},
        "Theory Score": {"number": {}},
        "Exercise Score": {"number": {}},
        "Date Started": {"date": {}},
        "Date Completed": {"date": {}},
        "Week": {"number": {}},
    })

    # 2. Exams DB
    exams_db = _create_database(parent_page_id, "Exams", {
        "Name": {"title": {}},
        "Score": {"number": {}},
        "Grade": {"select": {"options": [
            {"name": "A", "color": "green"},
            {"name": "B", "color": "blue"},
            {"name": "C", "color": "yellow"},
            {"name": "D", "color": "orange"},
            {"name": "F", "color": "red"},
        ]}},
        "Pass": {"checkbox": {}},
        "Date": {"date": {}},
        "Part": {"select": {"options": [
            {"name": "I", "color": "blue"},
            {"name": "II", "color": "green"},
            {"name": "III", "color": "purple"},
        ]}},
    })

    # 3. Journal DB
    journal_db = _create_database(parent_page_id, "Journal", {
        "Name": {"title": {}},
        "Week": {"number": {}},
        "Date": {"date": {}},
    })

    # 4. Katas DB
    katas_db = _create_database(parent_page_id, "Katas", {
        "Name": {"title": {}},
        "Score": {"number": {}},
        "Grade": {"select": {"options": [
            {"name": "A", "color": "green"},
            {"name": "B", "color": "blue"},
            {"name": "C", "color": "yellow"},
            {"name": "D", "color": "orange"},
            {"name": "F", "color": "red"},
        ]}},
        "Difficulty": {"select": {"options": [
            {"name": "Easy", "color": "green"},
            {"name": "Medium", "color": "yellow"},
            {"name": "Hard", "color": "red"},
        ]}},
        "Date": {"date": {}},
    })

    # 5. Spaced Repetition DB
    spaced_db = _create_database(parent_page_id, "Spaced Repetition", {
        "Name": {"title": {}},
        "Chapter": {"number": {}},
        "Score": {"number": {}},
        "Date": {"date": {}},
        "Next Review": {"date": {}},
        "Box": {"number": {}},
    })

    config = {
        "parent_page_id": parent_page_id,
        "chapters_db": chapters_db["id"],
        "exams_db": exams_db["id"],
        "journal_db": journal_db["id"],
        "katas_db": katas_db["id"],
        "spaced_db": spaced_db["id"],
    }
    save_config(config)
    return config


# ─── Chapter Operations ───

def add_chapter(number, name, part, week):
    """Seed a chapter entry."""
    config = load_config()
    client = get_client()
    return client.pages.create(
        parent={"database_id": config["chapters_db"]},
        properties={
            "Name": {"title": [{"text": {"content": f"Chapter {number}: {name}"}}]},
            "Number": {"number": number},
            "Part": {"select": {"name": part}},
            "Status": {"select": {"name": "Not Started"}},
            "Week": {"number": week},
        },
    )


def start_chapter(number):
    """Mark a chapter as In Progress."""
    config = load_config()
    chapters = query_database(
        config["chapters_db"],
        filter_obj={"property": "Number", "number": {"equals": number}},
    )["results"]
    if not chapters:
        raise ValueError(f"Chapter {number} not found. Run 'sa-learn setup' first.")
    page_id = chapters[0]["id"]
    get_client().pages.update(
        page_id=page_id,
        properties={
            "Status": {"select": {"name": "In Progress"}},
            "Date Started": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
        },
    )


def complete_chapter(number, theory_score, exercise_score):
    """Mark a chapter as Complete with scores."""
    config = load_config()
    chapters = query_database(
        config["chapters_db"],
        filter_obj={"property": "Number", "number": {"equals": number}},
    )["results"]
    if not chapters:
        raise ValueError(f"Chapter {number} not found.")
    page_id = chapters[0]["id"]
    get_client().pages.update(
        page_id=page_id,
        properties={
            "Status": {"select": {"name": "Complete"}},
            "Theory Score": {"number": theory_score},
            "Exercise Score": {"number": exercise_score},
            "Date Completed": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
        },
    )


def list_chapters():
    """Get all chapters sorted by number."""
    config = load_config()
    result = query_database(
        config["chapters_db"],
        sorts=[{"property": "Number", "direction": "ascending"}],
    )
    return result["results"]


# ─── Exam Operations ───

def add_exam(number, name, part):
    """Seed an exam entry."""
    config = load_config()
    client = get_client()
    return client.pages.create(
        parent={"database_id": config["exams_db"]},
        properties={
            "Name": {"title": [{"text": {"content": f"Exam {number}: {name}"}}]},
            "Part": {"select": {"name": part}},
        },
    )


def submit_exam(number, score):
    """Submit exam score."""
    config = load_config()
    exams = query_database(config["exams_db"])["results"]
    match = None
    for e in exams:
        title = e["properties"]["Name"]["title"]
        if title and f"Exam {number}" in title[0]["plain_text"]:
            match = e
            break
    if not match:
        raise ValueError(f"Exam {number} not found.")
    grade = score_to_grade(score, 200)
    get_client().pages.update(
        page_id=match["id"],
        properties={
            "Score": {"number": score},
            "Grade": {"select": {"name": grade}},
            "Pass": {"checkbox": score >= 140},
            "Date": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
        },
    )


def list_exams():
    """Get all exams."""
    config = load_config()
    return query_database(config["exams_db"])["results"]


# ─── Journal Operations ───

def add_journal(week, content_blocks):
    """Create a journal entry with content."""
    config = load_config()
    client = get_client()
    children = []
    for text in content_blocks:
        children.append({
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]},
        })
    return client.pages.create(
        parent={"database_id": config["journal_db"]},
        properties={
            "Name": {"title": [{"text": {"content": f"Week {week} Reflection"}}]},
            "Week": {"number": week},
            "Date": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
        },
        children=children,
    )


def list_journals():
    """Get all journal entries."""
    config = load_config()
    return query_database(
        config["journal_db"],
        sorts=[{"property": "Week", "direction": "ascending"}],
    )["results"]


# ─── Kata Operations ───

def add_kata(name, score, difficulty="Medium"):
    """Log a kata result."""
    config = load_config()
    client = get_client()
    grade = score_to_grade(score)
    return client.pages.create(
        parent={"database_id": config["katas_db"]},
        properties={
            "Name": {"title": [{"text": {"content": name}}]},
            "Score": {"number": score},
            "Grade": {"select": {"name": grade}},
            "Difficulty": {"select": {"name": difficulty}},
            "Date": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
        },
    )


def list_katas():
    """Get all katas."""
    config = load_config()
    return query_database(
        config["katas_db"],
        sorts=[{"property": "Date", "direction": "ascending"}],
    )["results"]


# ─── Spaced Repetition Operations ───

def add_review_item(name, chapter_num, score):
    """Add or update a spaced repetition item."""
    config = load_config()
    client = get_client()
    today = datetime.now()
    box = 2 if score >= 70 else 1
    next_review = today + timedelta(days=LEITNER_INTERVALS[box])
    return client.pages.create(
        parent={"database_id": config["spaced_db"]},
        properties={
            "Name": {"title": [{"text": {"content": name}}]},
            "Chapter": {"number": chapter_num},
            "Score": {"number": score},
            "Date": {"date": {"start": today.strftime("%Y-%m-%d")}},
            "Next Review": {"date": {"start": next_review.strftime("%Y-%m-%d")}},
            "Box": {"number": box},
        },
    )


def get_due_reviews():
    """Get items due for review (Next Review <= today)."""
    config = load_config()
    today = datetime.now().strftime("%Y-%m-%d")
    result = query_database(
        config["spaced_db"],
        filter_obj={
            "property": "Next Review",
            "date": {"on_or_before": today},
        },
        sorts=[{"property": "Next Review", "direction": "ascending"}],
    )
    return result["results"]


def update_review_item(page_id, score, current_box):
    """Update review item after quiz attempt."""
    correct = score >= 70
    new_box = min(current_box + 1, 5) if correct else 1
    today = datetime.now()
    next_review = today + timedelta(days=LEITNER_INTERVALS[new_box])
    get_client().pages.update(
        page_id=page_id,
        properties={
            "Score": {"number": score},
            "Date": {"date": {"start": today.strftime("%Y-%m-%d")}},
            "Next Review": {"date": {"start": next_review.strftime("%Y-%m-%d")}},
            "Box": {"number": new_box},
        },
    )


# ─── Progress & Grading ───

def score_to_grade(score, max_score=100):
    """Convert score to letter grade."""
    pct = (score / max_score) * 100
    if pct >= 90:
        return "A"
    if pct >= 80:
        return "B"
    if pct >= 70:
        return "C"
    if pct >= 60:
        return "D"
    return "F"


def get_progress_stats():
    """Aggregate all stats for the progress dashboard."""
    chapters = list_chapters()
    exams = list_exams()
    journals = list_journals()
    katas = list_katas()
    due_reviews = get_due_reviews()

    # Chapter stats
    total = len(chapters)
    completed = []
    theory_scores = []
    exercise_scores = []
    by_part = {"I": {"total": 0, "done": 0}, "II": {"total": 0, "done": 0}, "III": {"total": 0, "done": 0}}

    for ch in chapters:
        p = ch["properties"]
        part = p["Part"]["select"]["name"] if p["Part"]["select"] else "I"
        status = p["Status"]["select"]["name"] if p["Status"]["select"] else "Not Started"
        by_part[part]["total"] += 1
        if status == "Complete":
            completed.append(ch)
            by_part[part]["done"] += 1
            ts = p["Theory Score"]["number"]
            es = p["Exercise Score"]["number"]
            if ts is not None:
                theory_scores.append(ts)
            if es is not None:
                exercise_scores.append(es)

    # Exam stats
    exam_results = []
    exam_scores = []
    for e in exams:
        p = e["properties"]
        name = p["Name"]["title"][0]["plain_text"] if p["Name"]["title"] else "?"
        score = p["Score"]["number"]
        grade = p["Grade"]["select"]["name"] if p["Grade"].get("select") else "--"
        passed = p["Pass"]["checkbox"] if "Pass" in p else False
        exam_results.append({"name": name, "score": score, "grade": grade, "pass": passed})
        if score is not None:
            exam_scores.append(score)

    # Kata stats
    kata_scores = []
    for k in katas:
        s = k["properties"]["Score"]["number"]
        if s is not None:
            kata_scores.append(s)

    # Journal count
    journal_count = len(journals)
    # Weeks with completed chapters = max week number
    max_week = len(completed) if completed else 0

    # GPA calculation
    exercise_avg = sum(exercise_scores) / len(exercise_scores) if exercise_scores else 0
    exam_avg = (sum(exam_scores) / len(exam_scores) / 2 * 100) if exam_scores else 0
    kata_avg = sum(kata_scores) / len(kata_scores) if kata_scores else 0
    journal_pct = (journal_count / max(max_week, 1)) * 100
    journal_kata_avg = (journal_pct + kata_avg) / 2 if kata_scores else journal_pct
    gpa = exercise_avg * 0.4 + exam_avg * 0.4 + journal_kata_avg * 0.2 if exercise_scores else 0

    return {
        "total_chapters": total,
        "completed_chapters": len(completed),
        "by_part": by_part,
        "theory_avg": sum(theory_scores) / len(theory_scores) if theory_scores else 0,
        "exercise_avg": exercise_avg,
        "gpa": gpa,
        "gpa_grade": score_to_grade(gpa) if gpa > 0 else "--",
        "exams": exam_results,
        "kata_count": len(kata_scores),
        "kata_avg": sum(kata_scores) / len(kata_scores) if kata_scores else 0,
        "journal_count": journal_count,
        "journal_weeks": max_week,
        "due_reviews": len(due_reviews),
    }


def seed_all_chapters():
    """Seed all 27 chapters into Notion."""
    for num, (name, part) in CHAPTERS.items():
        week = CHAPTER_WEEKS[num]
        add_chapter(num, name, part, week)


def seed_all_exams():
    """Seed 3 exams into Notion."""
    add_exam(1, "Foundations", "I")
    add_exam(2, "Styles", "II")
    add_exam(3, "Final", "III")


# ─── Notion Dashboard Builder ───

def _text(content, bold=False, color="default", code=False):
    """Helper: create a rich_text element."""
    rt = {"type": "text", "text": {"content": content}}
    annotations = {}
    if bold:
        annotations["bold"] = True
    if color != "default":
        annotations["color"] = color
    if code:
        annotations["code"] = True
    if annotations:
        rt["annotations"] = annotations
    return rt


def _paragraph(texts, color="default"):
    """Helper: create a paragraph block."""
    rich = texts if isinstance(texts, list) else [_text(texts)]
    block = {"object": "block", "type": "paragraph",
             "paragraph": {"rich_text": rich}}
    if color != "default":
        block["paragraph"]["color"] = color
    return block


def _heading(level, text, color="default"):
    """Helper: create a heading block (1, 2, or 3)."""
    key = f"heading_{level}"
    block = {"object": "block", "type": key,
             key: {"rich_text": [_text(text)], "is_toggleable": False}}
    if color != "default":
        block[key]["color"] = color
    return block


def _callout(texts, icon="📊", color="default"):
    """Helper: create a callout block."""
    rich = texts if isinstance(texts, list) else [_text(texts)]
    block = {"object": "block", "type": "callout",
             "callout": {"rich_text": rich,
                         "icon": {"type": "emoji", "emoji": icon}}}
    if color != "default":
        block["callout"]["color"] = color
    return block


def _divider():
    return {"object": "block", "type": "divider", "divider": {}}


def _progress_bar(done, total, width=20):
    """Generate a text-based progress bar."""
    filled = int(width * done / total) if total > 0 else 0
    bar = "▓" * filled + "░" * (width - filled)
    pct = int(done / total * 100) if total > 0 else 0
    return f"{bar}  {done}/{total} ({pct}%)"


def _table_row(cells):
    """Helper: create a table_row block."""
    return {
        "object": "block",
        "type": "table_row",
        "table_row": {
            "cells": [[_text(c)] for c in cells]
        },
    }


def _table(headers, rows, col_width=None):
    """Helper: create a table block with header + data rows."""
    children = [_table_row(headers)]
    for row in rows:
        children.append(_table_row(row))
    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": len(headers),
            "has_column_header": True,
            "has_row_header": False,
            "children": children,
        },
    }


def build_notion_dashboard(page_id):
    """Build a visual dashboard on the Notion home page.
    Clears non-database blocks and rebuilds with live stats."""
    client = get_client()
    stats = get_progress_stats()
    chapters = list_chapters()

    # Remove existing non-database blocks (keep databases)
    existing = client.blocks.children.list(block_id=page_id)["results"]
    for block in existing:
        if block["type"] != "child_database":
            try:
                client.blocks.delete(block_id=block["id"])
            except Exception:
                pass

    # Collect all dashboard blocks to prepend before databases
    blocks = []

    # ── Header ──
    blocks.append(_callout(
        [_text("Fundamentals of Software Architecture", bold=True),
         _text(" — 30-Week Learning Program\n", bold=False),
         _text("Richards & Ford, 2nd Edition (2025)")],
        icon="🏛️", color="blue_background"
    ))
    blocks.append(_paragraph(""))

    # ── Overall Progress ──
    blocks.append(_heading(2, "📈 Overall Progress"))
    cc = stats["completed_chapters"]
    tc = stats["total_chapters"]
    in_progress = sum(
        1 for ch in chapters
        if ch["properties"]["Status"]["select"]
        and ch["properties"]["Status"]["select"]["name"] == "In Progress"
    )
    blocks.append(_callout(
        [_text(f"Chapters Completed: {cc}/{tc}\n", bold=True),
         _text(_progress_bar(cc, tc, 25)),
         _text(f"\nIn Progress: {in_progress}  |  ", bold=False),
         _text(f"Remaining: {tc - cc - in_progress}")],
        icon="📊", color="green_background"
    ))

    # Part breakdown
    bp = stats["by_part"]
    part_rows = []
    part_labels = {"I": "Foundations (Ch 1-8)", "II": "Architecture Styles (Ch 9-19)",
                   "III": "Techniques & Soft Skills (Ch 20-27)"}
    for pk in ["I", "II", "III"]:
        p = bp[pk]
        status_str = "Complete ✅" if p["done"] == p["total"] and p["total"] > 0 else (
            "In Progress 🔄" if p["done"] > 0 else "Not Started ⬜")
        part_rows.append([f"Part {pk}", part_labels[pk],
                          _progress_bar(p["done"], p["total"], 15), status_str])
    blocks.append(_table(["Part", "Topics", "Progress", "Status"], part_rows))
    blocks.append(_paragraph(""))

    # ── Scores & GPA ──
    blocks.append(_heading(2, "🎯 Scores & GPA"))
    gpa_display = f"{stats['gpa_grade']} ({stats['gpa']:.1f})" if stats["gpa"] > 0 else "—"
    theory_display = f"{stats['theory_avg']:.1f}" if stats["theory_avg"] > 0 else "—"
    exercise_display = f"{stats['exercise_avg']:.1f}" if stats["exercise_avg"] > 0 else "—"

    blocks.append(_table(
        ["Metric", "Score", "Weight"],
        [
            ["Theory Average", theory_display, "—"],
            ["Exercise Average", exercise_display, "40%"],
            ["Exam Average", f"{sum(s for e in stats['exams'] if (s := e['score']) is not None) / max(len([e for e in stats['exams'] if e['score'] is not None]), 1):.0f}/200" if any(e["score"] is not None for e in stats["exams"]) else "—", "40%"],
            ["Journal & Katas", f"{stats['journal_count']} entries, {stats['kata_count']} katas", "20%"],
            ["GPA", gpa_display, "100%"],
        ]
    ))
    blocks.append(_paragraph(""))

    # ── Exams ──
    blocks.append(_heading(2, "📝 Exams"))
    exam_rows = []
    for e in stats["exams"]:
        if e["score"] is not None:
            status = "✅ PASS" if e["pass"] else "❌ FAIL"
            exam_rows.append([e["name"], f"{e['score']}/200", e["grade"], status])
        else:
            exam_rows.append([e["name"], "—", "—", "⬜ Pending"])
    blocks.append(_table(["Exam", "Score", "Grade", "Status"], exam_rows))
    blocks.append(_paragraph(""))

    # ── Activities ──
    blocks.append(_heading(2, "🔧 Activities"))
    kata_display = f"{stats['kata_count']} completed (avg: {stats['kata_avg']:.1f})" if stats["kata_count"] > 0 else "0 completed"
    jw = stats["journal_weeks"]
    jc = stats["journal_count"]
    journal_display = f"{jc}/{jw} weeks ({int(jc/jw*100)}%)" if jw > 0 else "0 entries"
    review_display = f"{stats['due_reviews']} concepts due" if stats["due_reviews"] > 0 else "All caught up ✅"

    blocks.append(_table(
        ["Activity", "Status"],
        [
            ["🥋 Architecture Katas", kata_display],
            ["📓 Journal Entries", journal_display],
            ["🧠 Spaced Repetition", review_display],
        ]
    ))
    blocks.append(_paragraph(""))

    # ── Chapter Status ──
    blocks.append(_heading(2, "📚 Chapter Status"))
    chapter_rows = []
    for ch in chapters:
        p = ch["properties"]
        num = p["Number"]["number"] or 0
        name = p["Name"]["title"][0]["plain_text"] if p["Name"]["title"] else "?"
        status = p["Status"]["select"]["name"] if p["Status"]["select"] else "?"
        part = p["Part"]["select"]["name"] if p["Part"]["select"] else "?"
        ts = p["Theory Score"]["number"]
        es = p["Exercise Score"]["number"]
        icon = {"Not Started": "⬜", "In Progress": "🔄", "Complete": "✅"}.get(status, "?")
        chapter_rows.append([
            f"{icon} {name}",
            f"Part {part}",
            str(ts) if ts is not None else "—",
            str(es) if es is not None else "—",
        ])
    blocks.append(_table(["Chapter", "Part", "Theory", "Exercise"], chapter_rows))
    blocks.append(_paragraph(""))

    # ── Timeline ──
    blocks.append(_heading(2, "🗓️ Timeline"))
    blocks.append(_table(
        ["Phase", "Weeks", "Content"],
        [
            ["Part I", "Week 1-8", "Foundations: Thinking, Modularity, Characteristics, Components"],
            ["Exam 1", "Week 9", "Foundations Exam (200 pts)"],
            ["Part II", "Week 10-20", "Styles: Layered, Monolith, Pipeline, Microkernel, Service, Event, Space, SOA, Microservices"],
            ["Exam 2", "Week 21", "Architecture Styles Exam (200 pts)"],
            ["Part III", "Week 22-29", "Techniques: Patterns, ADRs, Risk, Diagrams, Teams, Leadership"],
            ["Exam 3", "Week 30", "Final Exam (200 pts)"],
        ]
    ))

    # ── Grading Scale ──
    blocks.append(_paragraph(""))
    blocks.append(_heading(3, "📐 Grading Scale"))
    blocks.append(_table(
        ["Grade", "Score", "Description"],
        [
            ["A", "90-100", "Excellent — SA-cert ready"],
            ["B", "80-89", "Good — solid understanding"],
            ["C", "70-79", "Adequate — needs reinforcement"],
            ["D", "60-69", "Below expectations"],
            ["F", "<60", "Fail — must redo"],
        ]
    ))

    # ── Footer ──
    blocks.append(_divider())
    blocks.append(_callout(
        [_text("Update this dashboard: ", bold=True),
         _text("sa-learn dashboard", code=True),
         _text("  |  Track progress: "),
         _text("sa-learn progress", code=True)],
        icon="💡", color="gray_background"
    ))

    # Prepend all blocks before the databases
    # Notion API appends — we need to add blocks at the top
    # Strategy: get database block IDs, delete them, add dashboard, re-add won't work
    # Instead: just append after existing content — databases are already there
    # We'll append blocks AFTER deleting non-db blocks (already done above)
    # But databases come after too — we need blocks BEFORE databases
    # Notion doesn't support "prepend" — only append.
    # Workaround: delete databases, append dashboard blocks, recreate databases
    # Better: just append dashboard blocks after databases (acceptable layout)

    # Actually let's use the "after" parameter to insert blocks before databases
    # The Notion API blocks.children.append doesn't support positioning.
    # Simplest: append all blocks (they go after databases — acceptable)

    # Batch append (Notion limits to 100 blocks per request)
    for i in range(0, len(blocks), 100):
        batch = blocks[i:i+100]
        client.blocks.children.append(block_id=page_id, children=batch)

    return len(blocks)
