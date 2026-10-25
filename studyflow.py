import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import json
import os
import shutil

# ==========================================
# STUDYFLOW - STUDENT STUDY PLANNER
# VERSION 3
# ==========================================

# Colors
BG = "#101827"
CARD = "#1B2638"
INPUT_BG = "#263449"
TEXT = "#F5F7FA"
MUTED = "#A7B4C7"
PURPLE = "#8B5CF6"
GREEN = "#22C55E"
RED = "#EF4444"
YELLOW = "#F59E0B"

# Same save location as previous versions
DATA_FILE = os.path.join(
    os.path.expanduser("~"),
    "studyflow_assignments.json"
)


class StudyFlow:

    def __init__(self, root):
        self.root = root
        self.root.title("StudyFlow - Student Planner")
        self.root.geometry("1100x740")
        self.root.minsize(800, 550)
        self.root.configure(bg=BG)

        self.assignments = []

        self.load_data()
        self.setup_styles()
        self.create_interface()
        self.refresh_table()

    # ======================================
    # SAVE AND LOAD
    # ======================================

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Invalid data format")

            # Check saved assignments
            for item in data:
                if not isinstance(item, dict):
                    raise ValueError("Invalid assignment")

                required = [
                    "id", "task", "course",
                    "deadline", "completed"
                ]

                if not all(key in item for key in required):
                    raise ValueError("Missing assignment field")

                datetime.strptime(
                    item["deadline"], "%Y-%m-%d"
                )

            self.assignments = data

        except (OSError, ValueError, TypeError, KeyError):
            # Keep a copy of the unreadable file, since the
            # next save would otherwise overwrite it
            backup = DATA_FILE + ".backup"

            try:
                shutil.copy2(DATA_FILE, backup)
                message = (
                    "Saved assignments could not be loaded.\n"
                    f"A backup was saved as:\n{backup}"
                )
            except OSError:
                message = "Saved assignments could not be loaded."

            messagebox.showwarning("Load Warning", message)

    def save_data(self):
        try:
            # Write to a temporary file first
            temporary = DATA_FILE + ".tmp"

            with open(
                temporary, "w", encoding="utf-8"
            ) as file:
                json.dump(
                    self.assignments,
                    file,
                    indent=4
                )

            os.replace(temporary, DATA_FILE)
            return True

        except OSError as error:
            messagebox.showerror(
                "Save Error",
                f"Could not save assignments:\n{error}"
            )
            return False

    # ======================================
    # STYLING
    # ======================================

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=CARD,
            foreground=TEXT,
            fieldbackground=CARD,
            rowheight=40,
            borderwidth=0,
            font=("Arial", 11)
        )

        style.configure(
            "Treeview.Heading",
            background=INPUT_BG,
            foreground=TEXT,
            font=("Arial", 11, "bold"),
            padding=9
        )

        style.map(
            "Treeview",
            background=[("selected", PURPLE)],
            foreground=[("selected", "white")]
        )

        # Coloured buttons (tk.Button ignores colours on macOS)
        for name, color, hover in [
            ("Purple", PURPLE, "#7C3AED"),
            ("Green", GREEN, "#16A34A"),
            ("Red", RED, "#DC2626")
        ]:
            style.configure(
                f"{name}.TButton",
                background=color,
                foreground="white",
                font=("Arial", 10, "bold"),
                borderwidth=0,
                focusthickness=0,
                padding=(15, 9)
            )

            style.map(
                f"{name}.TButton",
                background=[("pressed", hover), ("active", hover)],
                foreground=[("disabled", MUTED)]
            )

        style.configure(
            "Study.Horizontal.TProgressbar",
            troughcolor=INPUT_BG,
            background=PURPLE,
            thickness=17
        )

    # ======================================
    # CREATE USER INTERFACE
    # ======================================

    def create_interface(self):

        # HEADER
        header = tk.Frame(self.root, bg=BG)
        header.pack(
            fill="x",
            padx=30,
            pady=(18, 10)
        )

        tk.Label(
            header,
            text="StudyFlow",
            font=("Arial", 28, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Organize your studies. Track your progress.",
            font=("Arial", 11),
            fg=MUTED,
            bg=BG
        ).pack(anchor="w", pady=(4, 0))

        # DASHBOARD
        dashboard = tk.Frame(self.root, bg=BG)
        dashboard.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.total_label = self.create_stat_card(
            dashboard, "TOTAL TASKS", 0
        )

        self.pending_label = self.create_stat_card(
            dashboard, "PENDING", 1
        )

        self.completed_label = self.create_stat_card(
            dashboard, "COMPLETED", 2
        )

        self.overdue_label = self.create_stat_card(
            dashboard, "OVERDUE", 3
        )

        # PROGRESS
        progress_frame = tk.Frame(
            self.root,
            bg=CARD,
            padx=18,
            pady=13
        )

        progress_frame.pack(
            fill="x",
            padx=30,
            pady=(4, 12)
        )

        tk.Label(
            progress_frame,
            text="Your Study Progress",
            font=("Arial", 14, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w")

        self.progress_label = tk.Label(
            progress_frame,
            text="0% completed",
            font=("Arial", 10),
            fg=MUTED,
            bg=CARD
        )
        self.progress_label.pack(
            anchor="w",
            pady=(6, 9)
        )

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            style="Study.Horizontal.TProgressbar",
            maximum=100
        )
        self.progress_bar.pack(fill="x")

        # ADD ASSIGNMENT FORM
        form = tk.Frame(
            self.root,
            bg=CARD,
            padx=18,
            pady=14
        )

        form.pack(
            fill="x",
            padx=30,
            pady=(0, 12)
        )

        tk.Label(
            form,
            text="Add New Assignment",
            font=("Arial", 14, "bold"),
            fg=TEXT,
            bg=CARD
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(0, 12)
        )

        labels = [
            "Assignment",
            "Course",
            "Deadline (YYYY-MM-DD)"
        ]

        for col, label in enumerate(labels):
            tk.Label(
                form,
                text=label,
                font=("Arial", 10),
                fg=MUTED,
                bg=CARD
            ).grid(
                row=1,
                column=col,
                sticky="w"
            )

        self.task_entry = self.create_entry(form, 0)
        self.course_entry = self.create_entry(form, 1)
        self.deadline_entry = self.create_entry(form, 2)

        self.deadline_entry.insert(
            0, date.today().strftime("%Y-%m-%d")
        )

        ttk.Button(
            form,
            text="+ Add Assignment",
            command=self.add_assignment,
            style="Purple.TButton",
            cursor="hand2"
        ).grid(
            row=2,
            column=3,
            padx=(10, 0),
            sticky="ew"
        )

        for col in range(3):
            form.columnconfigure(col, weight=1)

        # ASSIGNMENT SECTION
        list_frame = tk.Frame(self.root, bg=BG)
        list_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 15)
        )

        # Heading and action buttons
        toolbar = tk.Frame(list_frame, bg=BG)
        toolbar.pack(
            fill="x",
            pady=(0, 10)
        )

        tk.Label(
            toolbar,
            text="My Assignments",
            font=("Arial", 17, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(side="left")

        ttk.Button(
            toolbar,
            text="Delete Selected",
            command=self.delete_assignment,
            style="Red.TButton",
            cursor="hand2"
        ).pack(side="right", padx=(8, 0))

        ttk.Button(
            toolbar,
            text="Mark Completed",
            command=self.complete_assignment,
            style="Green.TButton",
            cursor="hand2"
        ).pack(side="right")

        tk.Label(
            list_frame,
            text="Click a checkbox to complete a task. "
                 "Select a row to delete it.",
            font=("Arial", 10),
            fg=MUTED,
            bg=BG
        ).pack(
            anchor="w",
            pady=(0, 9)
        )

        # TABLE
        table_frame = tk.Frame(list_frame, bg=BG)
        table_frame.pack(
            fill="both",
            expand=True
        )

        columns = (
            "check",
            "assignment",
            "course",
            "deadline",
            "status"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "check": "Done",
            "assignment": "Assignment",
            "course": "Course",
            "deadline": "Deadline",
            "status": "Status"
        }

        for col, heading in headings.items():
            self.table.heading(col, text=heading)

        self.table.column(
            "check",
            width=65,
            minwidth=60,
            stretch=False,
            anchor="center"
        )

        self.table.column(
            "assignment",
            width=260,
            minwidth=140
        )

        self.table.column(
            "course",
            width=170,
            minwidth=100
        )

        self.table.column(
            "deadline",
            width=150,
            minwidth=110
        )

        self.table.column(
            "status",
            width=150,
            minwidth=100
        )

        self.table.tag_configure(
            "completed", foreground=GREEN
        )
        self.table.tag_configure(
            "overdue", foreground=RED
        )
        self.table.tag_configure(
            "soon", foreground=YELLOW
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Checkbox click handler
        self.table.bind(
            "<ButtonRelease-1>",
            self.checkbox_click
        )

        # Keyboard shortcuts
        self.root.bind(
            "<Delete>",
            self.delete_shortcut
        )

        self.root.bind(
            "<F5>",
            lambda event: self.refresh_table()
        )

    # ======================================
    # DASHBOARD CARD
    # ======================================

    def create_stat_card(self, parent, title, column):
        card = tk.Frame(
            parent,
            bg=CARD,
            padx=18,
            pady=15
        )

        card.grid(
            row=0,
            column=column,
            padx=5,
            sticky="nsew"
        )

        parent.columnconfigure(column, weight=1)

        tk.Label(
            card,
            text=title,
            font=("Arial", 10, "bold"),
            fg=MUTED,
            bg=CARD
        ).pack(anchor="w")

        value_label = tk.Label(
            card,
            text="0",
            font=("Arial", 25, "bold"),
            fg=TEXT,
            bg=CARD
        )

        value_label.pack(
            anchor="w",
            pady=(7, 0)
        )

        return value_label

    # ======================================
    # INPUT FIELD
    # ======================================

    def create_entry(self, parent, column):
        entry = tk.Entry(
            parent,
            font=("Arial", 11),
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=INPUT_BG,
            highlightcolor=PURPLE,
            width=18
        )

        entry.grid(
            row=2,
            column=column,
            padx=(0, 10),
            pady=(7, 0),
            ipady=9,
            sticky="ew"
        )

        return entry

    # ======================================
    # ADD ASSIGNMENT
    # ======================================

    def add_assignment(self):
        task = self.task_entry.get().strip()
        course = self.course_entry.get().strip()
        deadline = self.deadline_entry.get().strip()

        if not task or not course or not deadline:
            messagebox.showwarning(
                "Missing Information",
                "Please fill in all fields."
            )
            return

        try:
            parsed = datetime.strptime(
                deadline, "%Y-%m-%d"
            )

            if parsed.strftime("%Y-%m-%d") != deadline:
                raise ValueError("Invalid date format")

        except ValueError:
            messagebox.showerror(
                "Invalid Deadline",
                "Enter a valid deadline using YYYY-MM-DD.\n"
                "Example: 2026-11-15"
            )
            return

        assignment = {
            "id": self.next_id(),
            "task": task,
            "course": course,
            "deadline": deadline,
            "completed": False
        }

        self.assignments.append(assignment)

        if not self.save_data():
            self.assignments.remove(assignment)
            return

        self.refresh_table()

        self.task_entry.delete(0, tk.END)
        self.course_entry.delete(0, tk.END)
        self.task_entry.focus_set()

    def next_id(self):
        if not self.assignments:
            return 1

        return max(
            item["id"] for item in self.assignments
        ) + 1

    # ======================================
    # CHECKBOX - SINGLE CLICK
    # ======================================

    def checkbox_click(self, event):
        row_id = self.table.identify_row(event.y)
        column = self.table.identify_column(event.x)
        region = self.table.identify_region(
            event.x, event.y
        )

        # Only toggle the checkbox column
        if region != "cell" or column != "#1":
            return

        if not row_id:
            return

        assignment_id = int(row_id)

        for assignment in self.assignments:
            if assignment["id"] == assignment_id:
                old_value = assignment["completed"]
                assignment["completed"] = not old_value

                if not self.save_data():
                    assignment["completed"] = old_value
                    return

                self.refresh_table()
                return

    # ======================================
    # SELECT ASSIGNMENT
    # ======================================

    def get_selected_assignment(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an assignment first."
            )
            return None

        assignment_id = int(selected[0])

        for assignment in self.assignments:
            if assignment["id"] == assignment_id:
                return assignment

        return None

    # ======================================
    # MARK COMPLETED
    # ======================================

    def complete_assignment(self):
        assignment = self.get_selected_assignment()

        if assignment is None:
            return

        if assignment["completed"]:
            messagebox.showinfo(
                "Already Completed",
                "This assignment is already completed.\n"
                "Click its checkbox to undo completion."
            )
            return

        assignment["completed"] = True

        if not self.save_data():
            assignment["completed"] = False
            return

        self.refresh_table()

    # ======================================
    # DELETE ASSIGNMENT
    # ======================================

    def delete_assignment(self):
        assignment = self.get_selected_assignment()

        if assignment is None:
            return

        confirm = messagebox.askyesno(
            "Delete Assignment",
            f"Delete '{assignment['task']}'?\n\n"
            "This action cannot be undone."
        )

        if not confirm:
            return

        original_assignments = self.assignments[:]

        self.assignments = [
            item for item in self.assignments
            if item["id"] != assignment["id"]
        ]

        if not self.save_data():
            self.assignments = original_assignments
            return

        self.refresh_table()

    def delete_shortcut(self, event):
        # Avoid interfering with text editing
        if isinstance(event.widget, (tk.Entry, tk.Text)):
            return

        if self.table.selection():
            self.delete_assignment()

    # ======================================
    # DEADLINE STATUS
    # ======================================

    def get_status(self, assignment):
        if assignment["completed"]:
            return "Completed", "completed"

        deadline = datetime.strptime(
            assignment["deadline"],
            "%Y-%m-%d"
        ).date()

        days_left = (deadline - date.today()).days

        if days_left < 0:
            return "Overdue", "overdue"

        if days_left == 0:
            return "Due Today", "soon"

        if days_left == 1:
            return "Due Tomorrow", "soon"

        if days_left <= 3:
            return f"Due in {days_left} days", "soon"

        return "Upcoming", ""

    # ======================================
    # UPDATE TABLE AND DASHBOARD
    # ======================================

    def refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        sorted_assignments = sorted(
            self.assignments,
            key=lambda item: (
                item["completed"],
                item["deadline"]
            )
        )

        overdue_count = 0

        for assignment in sorted_assignments:
            status, tag = self.get_status(assignment)

            if status == "Overdue":
                overdue_count += 1

            checkbox = (
                "\u2611" if assignment["completed"]
                else "\u2610"
            )

            self.table.insert(
                "",
                tk.END,
                iid=str(assignment["id"]),
                values=(
                    checkbox,
                    assignment["task"],
                    assignment["course"],
                    assignment["deadline"],
                    status
                ),
                tags=(tag,) if tag else ()
            )

        total = len(self.assignments)

        completed = sum(
            1 for item in self.assignments
            if item["completed"]
        )

        pending = total - completed

        progress = (
            completed / total * 100
            if total > 0 else 0
        )

        self.total_label.config(text=str(total))
        self.pending_label.config(text=str(pending))
        self.completed_label.config(text=str(completed))
        self.overdue_label.config(text=str(overdue_count))

        self.progress_bar["value"] = progress

        self.progress_label.config(
            text=f"{progress:.0f}% completed"
        )


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyFlow(root)
    root.mainloop()
