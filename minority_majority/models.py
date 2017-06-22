# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
from otree import widgets
import random
from otree.common import Currency as c, currency_range
# </standard imports>

# For importing the matching spreadsheet from a relative file path
import os
script_dir = os.path.dirname(__file__)
rel_path = "matching/matching32.r100.csv"
abs_file_path = os.path.join(script_dir, rel_path)

# For pseudo-random matching, import the matching CSV file
import csv
matchingTable = open(abs_file_path, 'rU')
csv_matchingTable = csv.reader(matchingTable)


# Create a blank matrix in which to store the matching spreadsheet
m_string = []

# Save the csv_matchingTable spreadsheet as a list of lists
for row in csv_matchingTable:
    m_string.append(row)

# Convert the elements of m_string from strings to integers
m = [[int(float(j)) for j in i] for i in m_string]

doc = """
This is a 2-player 2-strategy Nash Demand game modeling mutualistic interactions.
The model comes from Cailin O'Connor and Justin Bruner's (2016)
<a href="https://uci.academia.edu/CailinOConnor" target="_blank">
    "Dynamics and Diversity in Epistemic Communities".
</a> And the principle underpinning it, the
<a href="http://www.pnas.org/content/100/2/593.full" target="blank">
Red King effect
</a>, finds its pedigree in evolutionary biology,
and the work of Carl Bergstrom and Michael Lachmann.
"""


bibliography = (
    (
        'O\'Connor, C., & Bruner, J. (forthcoming)'
        'Dynamics and Diversity in Epistemic Communities'
    ),
    (
        'Bergstrom, T. C. & Lachmann, M. (2003).The Red King effect: '
        'When the slowest runner wins the coevolutionary race. '
        'Proceedings of the National Academy of Sciences, 100(2):593-598.'
    )
)


class Constants(BaseConstants):

    name_in_url = 'minority_majority'

    players_per_group = 2
    num_rounds = 100

    participation_pay = c(2)
    completion_pay = c(2)

    low_low_amount = c(4)
    low_high_amount = c(4)
    high_low_amount = c(6)
    high_high_amount = c(0)

    training_question_1_my_payoff_correct = c(0)
    training_question_1_other_payoff_correct = c(0)
    training_1_maximum_offered_points = c(6)


class Subsession(BaseSubsession):

    def before_session_starts(self):
        # Random Matching & Sitting Out Mechanisms #
        # Translate the round number to the corresponding row of the spreadsheet for pseudo-random matching
        row_num = self.round_number - 1

        # Each round of play, change the partner pairings
        matching_structure = [[m[row_num][0], m[row_num][1]],
                              [m[row_num][2], m[row_num][3]],
                              [m[row_num][4], m[row_num][5]],
                              [m[row_num][6], m[row_num][7]],
                              [m[row_num][8], m[row_num][9]],
                              [m[row_num][10], m[row_num][11]],
                              [m[row_num][12], m[row_num][13]],
                              [m[row_num][14], m[row_num][15]],
                              [m[row_num][16], m[row_num][17]],
                              [m[row_num][18], m[row_num][19]],
                              [m[row_num][20], m[row_num][21]],
                              [m[row_num][22], m[row_num][23]],
                              [m[row_num][24], m[row_num][25]],
                              [m[row_num][26], m[row_num][27]],
                              [m[row_num][28], m[row_num][29]],
                              [m[row_num][30], m[row_num][31]]]

        # Set the new matchings
        self.set_group_matrix(matching_structure)

        # Players in the last group sit out this round
        groups = self.get_groups()
        # In the first treatment,
        # minority players are in groups 0 & 1 and always play
        groups[2].play_this_round = False
        groups[3].play_this_round = False
        # In the second treatment,
        # minority players are in groups 4 & 5 and always play
        groups[6].play_this_round = False
        groups[7].play_this_round = False
        # In the extra 2 treatment, there are no real players
        # and everyone sits out
        groups[8].play_this_round = False
        groups[9].play_this_round = False
        groups[10].play_this_round = False
        groups[11].play_this_round = False
        groups[12].play_this_round = False
        groups[13].play_this_round = False
        groups[14].play_this_round = False
        groups[15].play_this_round = False



class Group(BaseGroup):

    play_this_round = models.BooleanField(initial=True)


class Player(BasePlayer):

    # Establish the random_payment variable
    random_payment = models.CurrencyField()

    # Choose a random round, in the final round, for final payment
    def set_random_payment(self):

        if Constants.num_rounds < 20:
            self.random_payment = (2/3)*(random.choice([p.payoff for p in self.in_all_rounds() if p.payoff >= 0]))

        if Constants.num_rounds == 20:
            self.random_payment = (1/3)*(random.choice([p.payoff for p in self.in_rounds(1, 10) if p.payoff >= 0]) +
                                         random.choice([p.payoff for p in self.in_rounds(11, 20) if p.payoff >= 0]))

        if Constants.num_rounds == 100:
            self.random_payment = (1/15)*(random.choice([p.payoff for p in self.in_rounds(1, 10) if p.payoff >= 0]) +
                                          random.choice([p.payoff for p in self.in_rounds(11, 20) if p.payoff >= 0]) +
                                          random.choice([p.payoff for p in self.in_rounds(21, 30) if p.payoff >= 0]) +
                                          random.choice([p.payoff for p in self.in_rounds(31, 40) if p.payoff >= 0]) +
                                          random.choice([p.payoff for p in self.in_rounds(41, 50) if p.payoff >= 0]) +
                                          random.choice([p.payoff for p in self.in_rounds(51, 60) if p.payoff >= 0]) +
                                          random.choice([p.payoff for p in self.in_rounds(61, 70) if p.payoff >= 0]) +
                                          random.choice([p.payoff for p in self.in_rounds(71, 80) if p.payoff >= 0]) +
                                          random.choice([p.payoff for p in self.in_rounds(81, 90) if p.payoff >= 0]) +
                                          random.choice([p.payoff for p in self.in_rounds(91, 100) if p.payoff >= 0]))


    # Training questions
    training_question_1_my_payoff = models.CurrencyField(min=0, max=Constants.training_1_maximum_offered_points)
    training_question_1_other_payoff = models.CurrencyField(min=0, max=Constants.training_1_maximum_offered_points)

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

        # If the player plays this round, determine their payoff as a function of their decision & their partner's decisions
        if self.group.play_this_round is True:
            self.payoff = payoff_matrix[self.decision][self.other_player().decision]
        # If the player sits out this round, mark this with a payoff of -1
        else: self.payoff = c(-1)