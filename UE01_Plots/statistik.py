import argparse
import subprocess
import sys
from collections import Counter
from datetime import datetime

import matplotlib.pyplot as plt

__author__ = "Luka Pacar"
__version__ = "1.0.0"

def fetch_git_log(directory=".", author=""):
    """
    Get git log data from the specified directory and author.

    Args:
        directory: The Git Repository directory.
        author: The author to filter the commits.
    """

    cmd = [
        "git", "-C", directory, "log",
        "--pretty=%an;%ad", # Autor;Datum
        "--date=format:%Y-%m-%d %H:%M:%S"
    ]
    if author:
        cmd.append(f"--author={author}")

    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print("Fehler beim Ausführen von git log:", file=sys.stderr)
        print(stderr, file=sys.stderr)
        sys.exit(1)

    entries = []
    for line in stdout.splitlines():
        if ";" in line:
            name, date = line.split(";", 1)
            entries.append((name, date.strip()))

    return entries


def plot_commit_counts(entries):
    """
    Plots the number of commits per date.

    Args:
        entries: List of tuples (author, date).
    """
    weekdays = ["Mo","Di","Mi","Do","Fr","Sa","So"]

    points = []
    for _, date_str in entries:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        points.append((dt.weekday(), dt.hour))

    counts = Counter(points)

    x = [p[1] for p in counts.keys()]
    y = [p[0] for p in counts.keys()]

    sizes = [counts[p]*90 for p in counts.keys()]

    plt.scatter(x, y, s=sizes, alpha=0.6, color='blue')
    plt.xlabel("hour of day")
    plt.ylabel("weekday")
    plt.yticks(range(7), weekdays)  # Mo–So on y-axis
    plt.xticks(range(0, 24, 2))           # x-axis 0,2,…,22
    plt.title("Git Commits by Weekday and Hour")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="statistik.py by Max Mustermann -- draws a plot with git log data"
    )
    parser.add_argument("-a", "--author", default="", help='The author to filter the commits, default=""')

    parser.add_argument("-d", "--directory", default=".", help='The directory of the git repository, default="."')
    parser.add_argument("-f", "--filename", help='The filename of the plot. Don´t save picture if parameter is missing')

    grp = parser.add_mutually_exclusive_group()
    grp.add_argument( "-v", "--verbose", action="store_true", help="increase verbosity")
    grp.add_argument("-q", "--quiet", action="store_true", help="decrease verbosity")


    args = parser.parse_args()

    git_log = fetch_git_log(directory=args.directory, author=args.author)
    plot_commit_counts(git_log)