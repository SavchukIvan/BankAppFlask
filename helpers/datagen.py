from datetime import datetime
from datetime import timedelta
import random
import string
import re


class Luhn:
    db = {}

    def create_(self):
        num = random.randrange(1, 10 ** 10)
        num_with_zeros = '{:010}'.format(num)
        num_with_zeros = str(num).zfill(10)
        card_number = '400000'+num_with_zeros

        iban = 'UA4430529900000' + card_number

        self.db[card_number] = pin
        return iban

    def create_card(self):
        num = random.randrange(1, 10 ** 10)
        num_with_zeros = '{:010}'.format(num)
        num_with_zeros = str(num).zfill(10)
        card_number = '400000'+num_with_zeros

        num = random.randrange(1, 10 ** 4)
        num_with_zeros = '{:04}'.format(num)
        num_with_zeros = str(num).zfill(4)
        pin = num_with_zeros

        num = random.randrange(1, 10 ** 3)
        num_with_zeros = '{:03}'.format(num)
        num_with_zeros = str(num).zfill(3)
        csv = num_with_zeros

        start_time = datetime.now()
        end_time = datetime.now() + timedelta(days=365*4 + 1)

        return {'number': card_number, 'pin': pin,
                'cvv': csv, 'start': start_time,
                'end': end_time}


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str
