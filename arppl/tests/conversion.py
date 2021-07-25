import unittest

import pandas as pd

import arppl.utils.conversion as conv


class TestConversionDataFrameToRules(unittest.TestCase):

    def setUp(self):
        dt = pd.read_csv('resources/rules.csv', ',')
        self.rules = conv.convert_data_frame_to_rule_list(dt)

    def test_can_get_all_rules(self):
        self.assertEqual(len(self.rules), 7)

    def test_can_get_simple_length_two_rule(self):
        rule = self.rules[0]
        self.assertEqual(rule.length, 2)
        self.assertEqual(rule.antecedent[0], 'simple1=yes')
        self.assertEqual(rule.consequent, 'simple1=no')

    def test_can_get_simple_length_three_rule(self):
        rule = self.rules[1]
        self.assertEqual(rule.length, 3)
        self.assertEqual(rule.antecedent[0], 'simple1=yes')
        self.assertEqual(rule.antecedent[1], 'simple2=yes')
        self.assertEqual(rule.consequent, 'simple3=no')

    def test_can_get_antecedent_in_length_three_rules_when_only_one_attribute_has_blank_spaces(self):
        rule = self.rules[2]
        self.assertEqual(rule.length, 3)
        self.assertEqual(rule.antecedent[0], 'complex1=test with blank spaces')
        self.assertEqual(rule.antecedent[1], 'simple1=yes')
        self.assertEqual(rule.consequent, 'simple3=no')

    def test_can_get_antecedent_in_length_three_rules_when_two_attributes_has_blank_spaces(self):
        rule = self.rules[3]
        self.assertEqual(rule.length, 3)
        self.assertEqual(rule.antecedent[0], 'complex1=test with blank spaces')
        self.assertEqual(rule.antecedent[1], 'complex2=test with blank spaces')
        self.assertEqual(rule.consequent, 'simple3=no')

    def test_can_get_antecedent_in_length_two_rules_when_attribute_value_has_comma(self):
        rule = self.rules[4]
        self.assertEqual(rule.length, 2)
        self.assertEqual(rule.antecedent[0], 'complex1=[0,5]')
        self.assertEqual(rule.consequent, 'simple1=no')

    def test_can_get_antecedent_in_length_three_rules_when_only_one_attribute_value_has_comma(self):
        rule = self.rules[5]
        self.assertEqual(rule.length, 3)
        self.assertEqual(rule.antecedent[0], 'complex1=[0,5]')
        self.assertEqual(rule.antecedent[1], 'simple1=no')
        self.assertEqual(rule.consequent, 'simple2=no')

    def test_can_get_antecedent_in_length_three_rules_when_two_attribute_values_has_comma(self):
        rule = self.rules[6]
        self.assertEqual(rule.length, 3)
        self.assertEqual(rule.antecedent[0], 'complex1=[0,5]')
        self.assertEqual(rule.antecedent[1], 'complex=text with, comma')
        self.assertEqual(rule.consequent, 'simple2=no')


if __name__ == '__main__':
    unittest.main()
