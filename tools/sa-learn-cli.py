#!/usr/bin/env python3
"""sa-learn CLI — Track your Software Architecture learning journey.

Commands: setup, chapter, exam, journal, kata, review, progress
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import click
from datetime import datetime

PARENT_PAGE_ID = "32e85a16-ea1f-80a2-8180-c55b3fa04794"


def api():
    import importlib
    return importlib.import_module("sa-learn-notion-api")


# ─── Main CLI Group ───

@click.group()
def cli():
    """sa-learn — Software Architecture learning dashboard."""
    pass


# ─── Setup ───

@cli.command()
@click.option("--seed/--no-seed", default=True, help="Seed chapters and exams")
def setup(seed):
    """Create Notion workspace with 5 databases and seed initial data."""
    click.echo("Setting up SA Learning workspace...")
    config = api().setup_workspace(PARENT_PAGE_ID)
    click.echo("Created databases:")
    click.echo(f"  Chapters:          {config['chapters_db']}")
    click.echo(f"  Exams:             {config['exams_db']}")
    click.echo(f"  Journal:           {config['journal_db']}")
    click.echo(f"  Katas:             {config['katas_db']}")
    click.echo(f"  Spaced Repetition: {config['spaced_db']}")

    if seed:
        click.echo("\nSeeding 27 chapters...")
        api().seed_all_chapters()
        click.echo("Seeding 3 exams...")
        api().seed_all_exams()
        click.echo("Done! All data seeded.")
    else:
        click.echo("\nSkipped seeding. Run manually if needed.")


# ─── Chapter Commands ───

@cli.group()
def chapter():
    """Track chapter progress."""
    pass


@chapter.command("start")
@click.argument("num", type=int)
def chapter_start(num):
    """Mark a chapter as In Progress."""
    if num < 1 or num > 27:
        click.echo("Chapter number must be 1-27.")
        return
    api().start_chapter(num)
    name = api().CHAPTERS[num][0]
    click.echo(f"Started Chapter {num}: {name}")


@chapter.command("complete")
@click.argument("num", type=int)
@click.option("--theory-score", "-t", type=int, required=True, help="Theory quiz score (0-100)")
@click.option("--exercise-score", "-e", type=int, required=True, help="Exercise score (0-100)")
def chapter_complete(num, theory_score, exercise_score):
    """Complete a chapter with scores."""
    if num < 1 or num > 27:
        click.echo("Chapter number must be 1-27.")
        return
    api().complete_chapter(num, theory_score, exercise_score)
    name = api().CHAPTERS[num][0]
    grade = api().score_to_grade((theory_score + exercise_score) / 2)
    click.echo(f"Completed Chapter {num}: {name}")
    click.echo(f"  Theory: {theory_score}/100  Exercise: {exercise_score}/100  Grade: {grade}")


@chapter.command("list")
def chapter_list():
    """Show all chapters with status and scores."""
    chapters = api().list_chapters()
    if not chapters:
        click.echo("No chapters found. Run 'sa-learn setup' first.")
        return
    click.echo(f"\n{'#':>3}  {'Chapter':<50} {'Status':<12} {'Theory':>6} {'Exercise':>8}")
    click.echo(f"{'─'*3}  {'─'*50} {'─'*12} {'─'*6} {'─'*8}")
    for ch in chapters:
        p = ch["properties"]
        num = p["Number"]["number"] or 0
        title = p["Name"]["title"][0]["plain_text"] if p["Name"]["title"] else "?"
        status = p["Status"]["select"]["name"] if p["Status"]["select"] else "?"
        ts = p["Theory Score"]["number"]
        es = p["Exercise Score"]["number"]
        ts_str = str(ts) if ts is not None else "--"
        es_str = str(es) if es is not None else "--"
        icon = {"Not Started": " ", "In Progress": "*", "Complete": "+"}.get(status, "?")
        click.echo(f" {icon} {num:>2}  {title:<50} {status:<12} {ts_str:>6} {es_str:>8}")


# ─── Exam Commands ───

@cli.group()
def exam():
    """Track exam results."""
    pass


@exam.command("submit")
@click.argument("num", type=int)
@click.option("--score", "-s", type=int, required=True, help="Exam score (0-200)")
def exam_submit(num, score):
    """Submit an exam score."""
    if num < 1 or num > 3:
        click.echo("Exam number must be 1-3.")
        return
    api().submit_exam(num, score)
    grade = api().score_to_grade(score, 200)
    passed = "PASS" if score >= 140 else "FAIL"
    click.echo(f"Exam {num}: {score}/200 ({grade}) {passed}")


@exam.command("list")
def exam_list():
    """Show all exam results."""
    exams = api().list_exams()
    for e in exams:
        p = e["properties"]
        name = p["Name"]["title"][0]["plain_text"] if p["Name"]["title"] else "?"
        score = p["Score"]["number"]
        grade = p["Grade"]["select"]["name"] if p["Grade"].get("select") else "--"
        passed = p["Pass"]["checkbox"] if "Pass" in p else False
        if score is not None:
            status = "PASS" if passed else "FAIL"
            click.echo(f"  {name}: {score}/200 ({grade}) {status}")
        else:
            click.echo(f"  {name}: --")


# ─── Journal Commands ───

@cli.group()
def journal():
    """Architect's weekly journal."""
    pass


@journal.command("add")
@click.option("--week", "-w", type=int, required=True, help="Week number")
def journal_add(week):
    """Write a journal entry (interactive prompts)."""
    click.echo(f"\nWeek {week} — Architect's Journal\n")
    surprised = click.prompt("What surprised you this week?")
    connects = click.prompt("What connects to your real work?")
    different = click.prompt("What would you do differently?")
    key_insight = click.prompt("Key insight in one sentence")

    content = [
        f"What surprised me: {surprised}",
        f"Connection to work: {connects}",
        f"What I'd change: {different}",
        f"Key insight: {key_insight}",
    ]
    api().add_journal(week, content)
    click.echo(f"\nJournal entry for Week {week} saved.")


@journal.command("list")
def journal_list():
    """Show all journal entries."""
    entries = api().list_journals()
    if not entries:
        click.echo("No journal entries yet.")
        return
    for e in entries:
        p = e["properties"]
        name = p["Name"]["title"][0]["plain_text"] if p["Name"]["title"] else "?"
        week = p["Week"]["number"] or 0
        date = p["Date"]["date"]["start"] if p["Date"]["date"] else "?"
        click.echo(f"  Week {week}: {name} ({date})")


# ─── Kata Commands ───

@cli.group()
def kata():
    """Track architecture kata results."""
    pass


@kata.command("add")
@click.argument("name")
@click.option("--score", "-s", type=int, required=True, help="Score (0-100)")
@click.option("--difficulty", "-d", type=click.Choice(["Easy", "Medium", "Hard"], case_sensitive=False), default="Medium")
def kata_add(name, score, difficulty):
    """Log a kata result."""
    api().add_kata(name, score, difficulty)
    grade = api().score_to_grade(score)
    click.echo(f"Kata logged: {name} — {score}/100 ({grade}) [{difficulty}]")


@kata.command("list")
def kata_list():
    """Show all kata results."""
    katas = api().list_katas()
    if not katas:
        click.echo("No katas completed yet.")
        return
    for k in katas:
        p = k["properties"]
        name = p["Name"]["title"][0]["plain_text"] if p["Name"]["title"] else "?"
        score = p["Score"]["number"] or 0
        grade = p["Grade"]["select"]["name"] if p["Grade"].get("select") else "?"
        diff = p["Difficulty"]["select"]["name"] if p["Difficulty"].get("select") else "?"
        click.echo(f"  {name}: {score}/100 ({grade}) [{diff}]")


# ─── Review (Spaced Repetition) ───

@cli.command()
def review():
    """Show concepts due for spaced repetition review."""
    due = api().get_due_reviews()
    if not due:
        click.echo("No reviews due. Keep studying!")
        return
    click.echo(f"\n{len(due)} concept(s) due for review:\n")
    for item in due:
        p = item["properties"]
        name = p["Name"]["title"][0]["plain_text"] if p["Name"]["title"] else "?"
        box = p["Box"]["number"] or 1
        last_score = p["Score"]["number"] or 0
        click.echo(f"  [{box}] {name} (last score: {last_score})")


# ─── Progress Dashboard ───

@cli.command()
def progress():
    """Show ASCII progress dashboard."""
    stats = api().get_progress_stats()

    def bar(done, total, width=20):
        filled = int(width * done / total) if total > 0 else 0
        return "█" * filled + "░" * (width - filled)

    tc = stats["total_chapters"]
    cc = stats["completed_chapters"]
    bp = stats["by_part"]

    click.echo("\n SA Learning Progress\n")
    click.echo(f" Chapters:  {bar(cc, tc)}  {cc}/{tc} ({int(cc/tc*100) if tc else 0}%)")
    for part_key in ["I", "II", "III"]:
        p = bp[part_key]
        click.echo(f" Part {part_key}:    {bar(p['done'], p['total'])}  {p['done']}/{p['total']}"
                   + ("  Complete" if p["done"] == p["total"] and p["total"] > 0 else ""))

    click.echo(f"\n Scores:")
    click.echo(f"   Theory avg:   {stats['theory_avg']:.1f}")
    click.echo(f"   Exercise avg: {stats['exercise_avg']:.1f}")
    gpa_str = f"{stats['gpa_grade']} ({stats['gpa']:.1f})" if stats["gpa"] > 0 else "--"
    click.echo(f"   GPA:          {gpa_str}")

    click.echo(f"\n Exams:")
    for e in stats["exams"]:
        if e["score"] is not None:
            status = "PASS" if e["pass"] else "FAIL"
            click.echo(f"   {e['name']}: {e['score']}/200 ({e['grade']}) {status}")
        else:
            click.echo(f"   {e['name']}: --")

    click.echo(f"\n Katas: {stats['kata_count']} completed"
               + (f", avg score {stats['kata_avg']:.1f}" if stats["kata_count"] > 0 else ""))
    jw = stats["journal_weeks"]
    jc = stats["journal_count"]
    jpct = int(jc / jw * 100) if jw > 0 else 0
    click.echo(f" Journal: {jc}/{jw} weeks ({jpct}%)" if jw > 0 else " Journal: 0 entries")
    click.echo(f" Reviews due: {stats['due_reviews']} concepts")
    click.echo()


# ─── Entry Point ───

if __name__ == "__main__":
    cli()
