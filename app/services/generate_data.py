"""Service to generate sample log data files."""
import os
import random
from datetime import datetime

# -------- CONFIG --------
BASE_DIR = "logs"
NUM_DIRECTORIES = 2
FILES_PER_DIRECTORY = 5
LINES_PER_FILE = 5
# ------------------------

LEVELS = ["INFO", "WARNING", "ERROR"]
COMPONENTS = ["UserAuth", "GeoIP", "Payment"]
USERS = ["john.doe", "jane.doe", "alice.smith", "bob.jones"]

MESSAGES = {
    "INFO": ["User '{}' logged in successfully.", "User '{}' logged out."],
    "WARNING": ["Could not resolve IP address '{}'."],
    "ERROR": ["Transaction failed for user '{}'."],
}


def random_timestamp():
    """Generate a random timestamp string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_log_line():
    """Generate a single log line."""
    level = random.choice(LEVELS)
    component = random.choice(COMPONENTS)
    user = random.choice(USERS)

    if level == "WARNING":
        message = random.choice(MESSAGES[level]).format(
            "192.168.1." + str(random.randint(1, 255))
        )
    else:
        message = random.choice(MESSAGES[level]).format(user)

    timestamp = random_timestamp()

    # 🔥 NOTE: \\t produces literal \t in file
    return f"{timestamp}\\t{level}\\t{component}\\t{message}"


def generate_logs():
    """Generate sample log files in directories."""
    os.makedirs(BASE_DIR, exist_ok=True)

    for d in range(1, NUM_DIRECTORIES + 1):
        dir_path = os.path.join(BASE_DIR, f"dir_{d}")
        os.makedirs(dir_path, exist_ok=True)

        for f in range(1, FILES_PER_DIRECTORY + 1):
            file_path = os.path.join(dir_path, f"log_{f}.log")

            with open(file_path, "w", encoding="utf-8") as file:
                # Header with literal \t
                file.write("Timestamp\\tLevel\\tComponent\\tMessage\n")

                for _ in range(LINES_PER_FILE):
                    file.write(generate_log_line() + "\n")

            print(f"Created: {file_path}")


if __name__ == "__main__":
    generate_logs()
