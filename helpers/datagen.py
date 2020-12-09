from datetime import datetime
from datetime import timedelta
from random import randint
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

        return iban

    def generate_card_number():
        generated_card_number = '400000'
        for i in range(9):
            generated_card_number += str(randint(0, 9))
        integer_card_number = []
        for digit in generated_card_number:
            integer_card_number.append(int(digit))
        for j in range(len(integer_card_number)):
            if j % 2 == 0:
                integer_card_number[j] *= 2
        control_number = 0
        for i in integer_card_number:
            if i > 9:
                i -= 9
            control_number += i
        if (control_number % 10) == 0:
            final_digit = 0
        else:
            final_digit = 10 - (control_number % 10)
        print(final_digit)
        return str(generated_card_number) + str(final_digit)

    def create_card(self):

        generated_card_number = '400000'
        for i in range(9):
            generated_card_number += str(randint(0, 9))

        integer_card_number = []
        for digit in generated_card_number:
            integer_card_number.append(int(digit))

        for j in range(len(integer_card_number)):
            if j % 2 == 0:
                integer_card_number[j] *= 2

        control_number = 0
        for i in integer_card_number:
            if i > 9:
                i -= 9
            control_number += i

        if (control_number % 10) == 0:
            final_digit = 0
        else:
            final_digit = 10 - (control_number % 10)

        card_number = str(generated_card_number) + str(final_digit)

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
