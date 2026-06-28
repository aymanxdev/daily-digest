import requests

FACTS_FILE_PATH = "facts.txt"
CAT_FACT_URL = "https://catfact.ninja/fact?max_length=100"


def get_cat_fact():
    """Fetch a single short cat fact, or None if the request fails."""
    response = requests.get(CAT_FACT_URL, timeout=30)
    if response.status_code == 200:
        return response.json()["fact"]
    return None


def write_fact(fact, path=FACTS_FILE_PATH):
    """Append a fact to the facts file."""
    with open(path, "a") as file:
        file.write(fact + "\n")


def main():
    fact = get_cat_fact()
    if fact:
        write_fact(fact)
    else:
        print("Could not fetch a cat fact; nothing written.")


if __name__ == "__main__":
    main()
