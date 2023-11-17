import random
import string


def generate_random_name_new():
    first_names = []

    last_names = []

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return first_name, last_name


def generate_random_name():
    first_names = []

    last_names = []

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return first_name, last_name

def generate_random_email(first_name, last_name):
    if random.choice([True, False]):
        email_start = (
            first_name[: random.randint(2, 5)].lower()
            + random.choice(['.', '_', '-'])
            + last_name[: random.randint(2, 5)].lower()
        )
    else:
        email_start = (
            last_name[: random.randint(2, 5)].lower()
            + random.choice(['.', '_', '-'])
            + first_name[: random.randint(2, 5)].lower()
        )
        
    email_start = insert_random_numbers(email_start)

    email_domain = []
    return email_start + random.choice(email_domain)

def insert_random_numbers(s):
    position = random.randint(1, len(s) - 1)
    number = "".join(random.choices(string.digits, k=random.randint(1, 3)))
    return s[:position] + number + s[position:]

def generate_random_email_new(first_name, last_name):
    if random.choice([True, False]):
        email_start = (
            first_name[: random.randint(2, 5)].lower()
            + random.choice(['.', '_', '-'])
            + last_name[: random.randint(2, 5)].lower()
        )
    else:
        email_start = (
            last_name[: random.randint(2, 5)].lower()
            + random.choice(['.', '_', '-'])
            + first_name[: random.randint(2, 5)].lower()
        )

    email_start = insert_random_numbers(email_start)

    email_domain = []

    return email_start + random.choice(email_domain)

def insert_random_numbers(s):
    position = random.randint(1, len(s) - 1)
    number = "".join(random.choices(string.digits, k=random.randint(1, 3)))
    return s[:position] + number + s[position:]