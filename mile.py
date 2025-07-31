import subprocess

def run(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

milestones = [
    # Milestone 0: GitHub Repository Setup
    ("Milestone-0 VP-MAD-1", ["README.md", ".gitignore"]),

    # Milestone 1: Database Models and Schema
    ("Milestone-VP DB-Relationship", ["app_models.py", "create_sample_data.py"]),

    # Milestone 2: Authentication and Role-Based Access
    ("Milestone-VP Auth-RBAC", ["forms.py", "routes.py", "app.py", "main.py", "templates/login.html", "templates/register.html"]),

    # Milestone 3: Admin Dashboard and Lot/Spot Management
    ("Milestone-VP Admin-Dashboard-Management", [
        "templates/admin/dashboard.html",
        "templates/admin/create_lot.html",
        "templates/admin/edit_lot.html",
        "templates/admin/view_users.html",
        "routes.py", "app.py"
    ]),

    # Milestone 4: User Dashboard and Reservation System
    ("Milestone-VP User-Dashboard-Management", [
        "templates/user/dashboard.html",
        "templates/user/book_parking.html",
        "templates/user/my_bookings.html",
        "verify_spot_reservation.py",
        "verify_terminologies.py"
    ]),

    # Milestone 5: Reservation History and Summary
    ("Milestone-VP Summary-Users-Admin", [
        "mandatory_features.py"
    ]),

    # Milestone 6: Cost Calculation
    ("Milestone-VP Cost-Calculation", [
        "mandatory_features.py"
    ]),

    # Final Submission
    ("Milestone-VP Final-Submission", [
        "Parkmaster.md", "requirements.txt", "pyproject.toml"
    ]),
]

def commit_milestones():
    for msg, files in milestones:
        print(f"\n Committing milestone: {msg}")
        files_str = ' '.join(files)
        run(f"git add {files_str}")
        run(f'git commit -m "{msg}"')
        run("git push origin main")

if __name__ == "__main__":
    commit_milestones()
