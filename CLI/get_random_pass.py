""" The code defines a class called "RandomPasswordGenerator".
The purpose of this class is to generate random passwords that meet certain requirements.
The class takes several parameters as input, including the password length, the minimum number of upper-case letters, lower-case letters, numeric characters, and special characters that should be included in the password.
There are also options to exclude similar, confused, and ambiguous characters, and to specify a custom character set to use.
In the class's constructor, the initial values of all the parameters are stored as class variables.
The script also initializes several string variables that contain all the upper-case letters, lower-case letters, numeric characters, and special characters that are allowed in the password.
Depending on the values of the exclude_similar, exclude_confused, and exclude_ambiguous parameters, the script modifies the allowed characters accordingly.
The "generate_password" method of the class is used to generate a random password that meets the specified requirements.
The method first combines a random selection of upper-case letters, lower-case letters, numeric characters, special characters, and custom characters to form a list of characters.
This list is then shuffled randomly and joined into a string, which is returned as the password. If the password is longer than the specified length, it is trimmed to the correct length before being returned. """

import random
import string

class RandomPasswordGenerator:
    def __init__(self, password_length, min_upper_case=1, min_lower_case=1, min_numeric=1, min_special_char=1, exclude_similar=False, exclude_confused=False, exclude_ambiguous=False, custom_char_set=None, max_repeated_char=2):
        self.password_length = password_length
        self.min_upper_case = min_upper_case
        self.min_lower_case = min_lower_case
        self.min_numeric = min_numeric
        self.min_special_char = min_special_char
        self.exclude_similar = exclude_similar
        self.exclude_confused = exclude_confused
        self.exclude_ambiguous = exclude_ambiguous
        self.custom_char_set = custom_char_set
        self.max_repeated_char = max_repeated_char

        self.upper_case = string.ascii_uppercase
        self.lower_case = string.ascii_lowercase
        self.numeric = string.digits
        self.special = string.punctuation

        if exclude_similar:
            self.upper_case = "AHJNPQRSTUVWXYZ"
            self.lower_case = "ahjnpqrstuvwxyz"
            self.numeric = "23456789"
            self.special = "!@#$%^&*"
        if exclude_confused:
            self.upper_case = "AHJNPQRSTUVWXYZ"
            self.numeric = "23456789"
        if exclude_ambiguous:
            self.special = "!@#$%^&*"
        if custom_char_set:
            self.custom = custom_char_set
        else:
            self.custom = ""
        
    def generate_password(self):
        password = random.choices(self.upper_case, k=self.min_upper_case) + random.choices(self.lower_case, k=self.min_lower_case) + random.choices(self.numeric, k=self.min_numeric) + random.choices(self.special, k=self.min_special_char) + random.choices(self.custom, k=(self.password_length - self.min_upper_case - self.min_lower_case - self.min_numeric - self.min_special_char))
        random.shuffle(password)
        password = "".join(password)
        
        if len(password) > self.password_length:
            password = password[:self.password_length]
        return password
