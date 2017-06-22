# -*- coding: utf-8 -*-
from __future__ import division

import random

from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants


def vars_for_all_templates(self):

    return {'total_q': 1,
            'total_rounds': Constants.num_rounds,
            'round_number': self.subsession.round_number}


class Introduction1(Page):

    timeout_seconds = 150

    def is_displayed(self):
        return self.subsession.round_number == 1


class Introduction2(Page):

    timeout_seconds = 90

    def is_displayed(self):
        return self.subsession.round_number == 1


class Introduction3(Page):

    timeout_seconds = 90

    def is_displayed(self):
        return self.subsession.round_number == 1


class Question(Page):

    timeout_seconds = 90

    template_name = 'minority_majority/Question.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = [
        'training_question_1_my_payoff','training_question_1_other_payoff'
    ]

    def vars_for_template(self):
        return {'num_q': 1}


class Feedback(Page):

    timeout_seconds = 20

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_q': 1,
        }


class Decide(Page):

    timeout_seconds = 20

    def is_displayed(self):
        return self.group.play_this_round

    form_model = models.Player
    form_fields = ['decision']

    def vars_for_template(self):
        return {'player_index': self.player.id_in_group,
                'low_low': Constants.low_low_amount,
                'low_high': Constants.low_high_amount,
                'high_low': Constants.high_low_amount,
                'high_high': Constants.high_high_amount}

    timeout_submission = {'decision': random.choice(['Choose 4', 'Choose 6'])}


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        # set player payoffs
        for p in self.group.get_players():
            p.set_payoff()

        # set final payment from a random round
        if self.subsession.round_number == Constants.num_rounds:
            for p in self.group.get_players():
                p.set_random_payment()

    body_text = "Waiting for the other participants."


class Results(Page):

    timeout_seconds = 20

    def is_displayed(self):
        return self.group.play_this_round

    def vars_for_template(self):
        return {
             'total_payoff': self.player.payoff + Constants.participation_pay + Constants.completion_pay}


class ResultsFinal(Page):

    timeout_seconds = 90

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'total_payoff': self.player.random_payment.to_real_world_currency(self.session) + Constants.participation_pay + Constants.completion_pay,
            'random_payment': self.player.random_payment.to_real_world_currency(self.session),
            'participation_pay': Constants.participation_pay.to_real_world_currency(self.session),
            'completion_pay': Constants.participation_pay.to_real_world_currency(self.session)}


page_sequence = [
            Introduction1,
            Introduction2,
            Introduction3,
            Question,
            Feedback,
            Decide,
            ResultsWaitPage,
            Results,
            ResultsFinal]