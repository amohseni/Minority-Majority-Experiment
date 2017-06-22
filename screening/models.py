# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
from otree import widgets
from otree.common import Currency as c, currency_range
# </standard imports>


doc = """
This is a questionnaire for screening participants for an experiment.
"""

class Constants(BaseConstants):

    name_in_url = 'screening'
    players_per_group = None
    num_rounds = 1
    participation_pay = c(5)

    training_question_1_my_payoff_correct = c(0)
    training_question_1_other_payoff_correct = c(0)

    training_question_2_my_payoff_correct = c(4)
    training_question_2_other_payoff_correct = c(6)

    training_question_3_my_payoff_correct = c(4)
    training_question_3_other_payoff_correct = c(4)

    training_question_4_my_payoff_correct = c(6)
    training_question_4_other_payoff_correct = c(4)

    training_maximum_offered_points = c(6)

class Subsession(BaseSubsession):

    pass


class Group(BaseGroup):

    pass


class Player(BasePlayer):

    # Training questions
    training_question_1_my_payoff = models.CurrencyField(min=0, max=Constants.training_maximum_offered_points)
    training_question_1_other_payoff = models.CurrencyField(min=0, max=Constants.training_maximum_offered_points)
    training_question_2_my_payoff = models.CurrencyField(min=0, max=Constants.training_maximum_offered_points)
    training_question_2_other_payoff = models.CurrencyField(min=0, max=Constants.training_maximum_offered_points)
    training_question_3_my_payoff = models.CurrencyField(min=0, max=Constants.training_maximum_offered_points)
    training_question_3_other_payoff = models.CurrencyField(min=0, max=Constants.training_maximum_offered_points)
    training_question_4_my_payoff = models.CurrencyField(min=0, max=Constants.training_maximum_offered_points)
    training_question_4_other_payoff = models.CurrencyField(min=0, max=Constants.training_maximum_offered_points)


    decision = models.CharField(
        choices=['Choose 4', 'Choose 6'],
        doc="""The player's choice""",
        widget=widgets.RadioSelect()
    )

    def is_training_question_1_my_payoff_correct(self):
        return (self.training_question_1_my_payoff==
                Constants.training_question_1_my_payoff_correct)

    def is_training_question_1_other_payoff_correct(self):
        return (self.training_question_1_other_payoff==
                Constants.training_question_1_other_payoff_correct)

    def is_training_question_2_my_payoff_correct(self):
        return (self.training_question_2_my_payoff==
                Constants.training_question_2_my_payoff_correct)

    def is_training_question_2_other_payoff_correct(self):
        return (self.training_question_2_other_payoff==
                Constants.training_question_2_other_payoff_correct)

    def is_training_question_3_my_payoff_correct(self):
        return (self.training_question_3_my_payoff==
                Constants.training_question_3_my_payoff_correct)

    def is_training_question_3_other_payoff_correct(self):
        return (self.training_question_3_other_payoff==
                Constants.training_question_3_other_payoff_correct)

    def is_training_question_4_my_payoff_correct(self):
        return (self.training_question_4_my_payoff==
                Constants.training_question_4_my_payoff_correct)

    def is_training_question_4_other_payoff_correct(self):
        return (self.training_question_4_other_payoff==
                Constants.training_question_4_other_payoff_correct)

    def other_player(self):
        """Returns other player in group"""
        return self.get_others_in_group()[0]

    # Determine player payoffs
    def set_payoff(self):
        payoff_matrix = {
            'Choose 4': {
                'Choose 4': Constants.low_low_amount,
                'Choose 6': Constants.low_high_amount,
            },
            'Choose 6': {
                'Choose 4': Constants.high_low_amount,
                'Choose 6': Constants.high_high_amount,
            }
        }

    # Radio button choice
    get_involved = models.PositiveIntegerField(
        choices=[
            [1, 'YES'],
            [2, 'NO'],
        ]
    )