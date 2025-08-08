import random
from config.settings import DEBUG


def generate_otp():
    return random.randint(100000, 999999)
