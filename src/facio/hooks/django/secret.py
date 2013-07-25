# -*- coding: utf-8 -*-

"""
.. module:: facio.hooks.django.secret_key
   :synopsis: Generates a Django Secret key and updates context_variables with
              a DJANGO_SECRET_KEY value.
"""

from facio.base import BaseFacio
from facio.state import state
from random import choice


class GenerateDjangoSecretKey(BaseFacio):

    characters = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

    def generate(self):
        """ Generate Django secret key

        :returns: str -- The generated key
        """

        self.out('Generating Django Secret Key')
        key = ''.join([choice(self.characters) for i in range(50)])
        return key


def run():
    """ Called by the ``facio.hooks`` runner. """

    generator = GenerateDjangoSecretKey()
    key = generator.generate()
    state.update_context_variables({'DJANGO_SECRET_KEY': key})
    return key
