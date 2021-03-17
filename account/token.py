from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

from .models import Customer

"""
user will get an email, how this will happen ?!
1- django provide us with PasswordResetTokenGenerator we can also use that for generating account activation token
2- create a uniqe token for that sign up
3- after clicking the link the token send to the bakend we can then de-encrypt that token to see if that user is valid
4- and then we going to activate that user if the token is valid

how the token get generated ?!
1- create a uniqe token each time 
2- utilize the uniqueness of the user and the timestamp
3- 
note: the default value for the PasswordResetToken is 7 days you can change this in the setting by adding 
the validation date of the token by adding PASSWORD_RESRT_TIMEOUT_DAYS constance 
"""


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)


account_activation_token = AccountActivationTokenGenerator()
