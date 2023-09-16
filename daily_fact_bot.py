import os
import random
import requests


git_username = os.environ.get("GIT_USERNAME")
git_email = os.environ.get("GIT_EMAIL")

# Get a random fact
def get_cat_facts():
    response = requests.get("https://catfact.ninja/fact?max_length=100")
    if response.status_code == 200:
        return response.json()["fact"]
    else:
        return None

# Choose a random fact
fact = get_cat_facts()

# Write the fact to the file
with open("facts.txt", "a") as file:
    file.write(fact + "\n")

# Commit and push the changes
os.system(f"git config --global user.name '{git_username}'")
os.system(f"git config --global user.email '{git_email}'")
os.system("git add facts.txt")
os.system('git commit -m "Add new fact"')
