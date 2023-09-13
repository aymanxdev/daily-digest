import os
import random

git_username = os.environ.get("GIT_USERNAME")
git_email = os.environ.get("GIT_EMAIL")

# List of random lines
lines = [
    "The sun is approximately 93 million miles away from Earth.",
    "Mount Everest is the tallest mountain on Earth.",
    "The Eiffel Tower can grow 6 inches in summer due to metal expansion.",
    "Light travels at 299,792,458 meters per second in a vacuum.",
    "Elephants are the only animals that can't jump.",
    # ... add more 
]

# Choose a random line
line = random.choice(lines)

# Append the line to the file
with open("facts.txt", "a") as file:
    file.write(line + "\n")

# Commit and push the changes
os.system(f"git config --global user.name '{git_username}'")
os.system(f"git config --global user.email '{git_email}'")
os.system("git add facts.txt")
os.system('git commit -m "Add new fact"')
