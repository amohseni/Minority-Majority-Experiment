# -*- coding: utf-8 -*-
from __future__ import division

import random

from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants


def vars_for_all_templates(self):

    return {'total_q': 1,
            'total_rounds': 1,
            'round_number': self.subsession.round_number}


class Introduction1(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1


class Introduction(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1


class Question1(Page):

    template_name = 'screening/Question1.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = [
        'training_question_1_my_payoff', 'training_question_1_other_payoff'
    ]

    def vars_for_template(self):
        return {'num_q': 1}

class Question2(Page):

    template_name = 'screening/Question2.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = [
        'training_question_2_my_payoff', 'training_question_2_other_payoff'
    ]

    def vars_for_template(self):
        return {'num_q': 2}

class Question3(Page):

    template_name = 'screening/Question3.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = [
        'training_question_3_my_payoff', 'training_question_3_other_payoff'
    ]

    def vars_for_template(self):
        return {'num_q': 3}

class Question4(Page):

    template_name = 'screening/Question4.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = [
        'training_question_4_my_payoff', 'training_question_4_other_payoff'
    ]

    def vars_for_template(self):
        return {'num_q': 4}

class Feedback1(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_q': 1,
        }

class Feedback2(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_q': 2,
        }

class Feedback3(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_q': 3,
        }

class Feedback4(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_q': 4,
        }


class ResultsFinal(Page):

    def vars_for_template(self):
        return {
            'participation_pay': Constants.participation_pay.to_real_world_currency(self.session)
        }

    form_model = models.Player
    form_fields = ['get_involved']


page_sequence = [
            Introduction,
            Question1,
            Feedback1,
            Question2,
            Feedback2,
            Question3,
            Feedback3,
            Question4,
            Feedback4,
            ResultsFinal]