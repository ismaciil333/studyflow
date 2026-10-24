# StudyFlow – Student Study Planner

StudyFlow is a desktop study planner for students. It keeps all assignments, courses and deadlines in one place and shows at a glance what is overdue, what is due soon and how much of the workload is done.

Built as a vibe-coding assignment: the application was described in natural language and developed iteratively with generative AI (Claude), which helped write, test and improve the code across three versions.

## The problem

Students juggle deadlines from several courses at once, spread across Canvas, emails and notes. It is easy to lose track of what is due when. StudyFlow gives one simple overview with automatic deadline warnings.

## Features

- **Add assignments** with name, course and deadline (validated YYYY-MM-DD format)
- **Dashboard** with total, pending, completed and overdue counts
- **Progress bar** showing the percentage of assignments completed
- **Colour-coded deadlines**: red for overdue, yellow for due today or within 3 days, green for completed
- **One-click checkbox** to mark an assignment as done or undo it
- **Delete with confirmation** (button or Delete key)
- **Automatic saving** to a local JSON file, so assignments are kept between sessions
- **Safe saving**: writes to a temporary file first, and keeps a backup if a saved file cannot be read

## How to run

Requires Python 3.8 or newer. Tkinter is included with standard Python on Windows and macOS (on Linux: `sudo apt install python3-tk`).

```
python studyflow.py
```

No extra packages or API keys are needed.

## Data and privacy

Assignments are stored only on your own computer, in `studyflow_assignments.json` in your home folder. Nothing is sent over the internet, and the data file is not part of this repository.

## Development with AI

The app was developed in three versions. In each round I described what I wanted or what did not work, the AI generated or changed the code, and I tested the result and asked for improvements. The current version (v3) is in `studyflow.py`.

## Possible next steps

- Edit existing assignments
- Filter and search by course
- Date picker instead of typed dates
- Reminder notifications before deadlines

## Tech

Python 3, Tkinter / ttk, JSON
