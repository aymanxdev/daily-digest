import requests


# Get a random fact
def get_cat_facts():
    response = requests.get("https://catfact.ninja/fact?max_length=100")
    if response.status_code == 200:
        return response.json()["fact"]
    else:
        return None


# Choose a random fact
fact = get_cat_facts()

if fact:
    # Write the fact to the file (committing is handled by the workflow)
    with open("facts.txt", "a") as file:
        file.write(fact + "\n")
else:
    print("Could not fetch a cat fact; nothing written.")
