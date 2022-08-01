import unittest

from arppl.models import Rule
from arppl.models import MeasureIndependentlyAtOne
import arppl.methods as mtd


class GenerateGroupsCorrectly(unittest.TestCase):

    def setUp(self):
        self.item_of_interest = 'attr1=yes'

    def test_get_group_1(self):
        rules = [
            # Group 1
            Rule(antecedent=[self.item_of_interest], consequent='attr2=2.5', lift=MeasureIndependentlyAtOne(1.5)),
            Rule(antecedent=['attr2=2.5'], consequent=self.item_of_interest, lift=MeasureIndependentlyAtOne(1.5)),

            # The first rule is irrelevant because of the lift value
            Rule(antecedent=[self.item_of_interest], consequent='attr2=2.5', lift=MeasureIndependentlyAtOne(1.0)),
            Rule(antecedent=['attr2=2.5'], consequent=self.item_of_interest, lift=MeasureIndependentlyAtOne(1.5)),

            # Rules does not have the item of interest
            Rule(antecedent=['attr3=no'], consequent='attr2=2.5', lift=MeasureIndependentlyAtOne(1.5)),
            Rule(antecedent=['attr2=2.5'], consequent='attr3=no', lift=MeasureIndependentlyAtOne(1.5)),

            # Rules does not have the item of interest
            Rule(antecedent=[self.item_of_interest], consequent='attr5=1', lift=MeasureIndependentlyAtOne(1.5)),
        ]

        groups = mtd.method_select(self.item_of_interest, rules, 'lift')

        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0].name, '1')
        self.assertTrue(all([r in rules[:2] for r in groups[0].rules]))

    def test_get_group_2(self):
        rules = [
            # Group 2
            Rule(antecedent=['attr3=no'], consequent='attr2=2.5', lift=MeasureIndependentlyAtOne(1.5)),
            Rule(antecedent=[self.item_of_interest], consequent='attr2=2.5', lift=MeasureIndependentlyAtOne(1.2)),
            Rule(antecedent=[self.item_of_interest, 'attr3=no'], consequent='attr2=2.5',
                 lift=MeasureIndependentlyAtOne(1.6)),

            # The first rule is irrelevant because of the lift value
            Rule(antecedent=['attr4=no'], consequent='attr2=2.5', lift=MeasureIndependentlyAtOne(1.0)),
            Rule(antecedent=[self.item_of_interest], consequent='attr2=2.5', lift=MeasureIndependentlyAtOne(1.5)),
            Rule(antecedent=[self.item_of_interest, 'attr4=no'], consequent='attr2=2.5',
                 lift=MeasureIndependentlyAtOne(1.6)),

            # The less general rule has less lift than the most general
            Rule(antecedent=['attr5=no'], consequent='attr3=2.5', lift=MeasureIndependentlyAtOne(1.3)),
            Rule(antecedent=[self.item_of_interest], consequent='attr3=2.5', lift=MeasureIndependentlyAtOne(1.1)),
            Rule(antecedent=[self.item_of_interest, 'attr5=no'], consequent='attr3=2.5',
                 lift=MeasureIndependentlyAtOne(1.2)),

            # Rules does not have the item of interest
            Rule(antecedent=['attr5=yes'], consequent='attr3=2.5', lift=MeasureIndependentlyAtOne(1.1)),
            Rule(antecedent=['attr4=yes'], consequent='attr3=2.5', lift=MeasureIndependentlyAtOne(1.1)),
            Rule(antecedent=['attr4=yes', 'attr5=yes'], consequent='attr3=2.5', lift=MeasureIndependentlyAtOne(1.2)),
        ]

        groups = mtd.method_select(self.item_of_interest, rules, 'lift')

        groups_2 = [g for g in groups if g.name == '2']
        self.assertEqual(len(groups_2), 1)
        self.assertTrue(all([r in rules[:3] for r in groups_2[0].rules]))

    def test_get_group_3(self):
        rules = [
            # Group 3
            Rule(antecedent=['attr3=no'], consequent='attr2=2.5', lift=MeasureIndependentlyAtOne(1.5)),
            Rule(antecedent=[self.item_of_interest, 'attr3=no'], consequent='attr2=2.5',
                 lift=MeasureIndependentlyAtOne(1.6)),

            # The most general rule has the item of interest in the antecedent, so it belongs to Group 4
            Rule(antecedent=[self.item_of_interest], consequent='attr2=1.5', lift=MeasureIndependentlyAtOne(1.2)),
            Rule(antecedent=[self.item_of_interest, 'attr5=yes'], consequent='attr2=1.5',
                 lift=MeasureIndependentlyAtOne(1.6)),

            # The first rule is irrelevant because of the lift value
            Rule(antecedent=['attr4=no'], consequent='attr2=2.5', lift=MeasureIndependentlyAtOne(1.0)),
            Rule(antecedent=[self.item_of_interest, 'attr4=no'], consequent='attr2=2.5',
                 lift=MeasureIndependentlyAtOne(1.6)),

            # The less general rule has less lift than the most general
            Rule(antecedent=['attr5=no'], consequent='attr3=2.5', lift=MeasureIndependentlyAtOne(1.3)),
            Rule(antecedent=[self.item_of_interest, 'attr5=no'], consequent='attr3=2.5',
                 lift=MeasureIndependentlyAtOne(1.2)),

            # Rules does not have the item of interest
            Rule(antecedent=['attr5=yes'], consequent='attr3=2.5', lift=MeasureIndependentlyAtOne(1.1)),
            Rule(antecedent=['attr4=yes', 'attr5=yes'], consequent='attr3=2.5', lift=MeasureIndependentlyAtOne(1.2)),
        ]

        groups = mtd.method_select(self.item_of_interest, rules, 'lift')

        groups_3 = [g for g in groups if g.name == '3']
        self.assertEqual(len(groups_3), 1)
        self.assertTrue(all([r in rules[:3] for r in groups_3[0].rules]))

    def test_get_group_4(self):
        rules = [
            # Group 4
            Rule(antecedent=[self.item_of_interest], consequent='attr2=2.5', lift=MeasureIndependentlyAtOne(1.2)),
            Rule(antecedent=[self.item_of_interest, 'attr3=no'], consequent='attr2=2.5',
                 lift=MeasureIndependentlyAtOne(1.6)),

            # The most general rule does not have the item of interest in the antecedent, so it belongs to Group 3
            Rule(antecedent=['attr5=yes'], consequent='attr2=1.5', lift=MeasureIndependentlyAtOne(1.2)),
            Rule(antecedent=[self.item_of_interest, 'attr5=yes'], consequent='attr2=1.5',
                 lift=MeasureIndependentlyAtOne(1.6)),

            # The first rule is irrelevant because of the lift value
            Rule(antecedent=[self.item_of_interest], consequent='attr2=5.5', lift=MeasureIndependentlyAtOne(1.0)),
            Rule(antecedent=[self.item_of_interest, 'attr4=no'], consequent='attr2=5.5',
                 lift=MeasureIndependentlyAtOne(1.6)),

            # The less general rule has less lift than the most general
            Rule(antecedent=[self.item_of_interest], consequent='attr3=2.5', lift=MeasureIndependentlyAtOne(1.3)),
            Rule(antecedent=[self.item_of_interest, 'attr5=no'], consequent='attr3=2.5',
                 lift=MeasureIndependentlyAtOne(1.2)),

            # Rules does not have the item of interest
            Rule(antecedent=['attr5=yes'], consequent='attr3=2.5', lift=MeasureIndependentlyAtOne(1.1)),
            Rule(antecedent=['attr4=yes', 'attr5=yes'], consequent='attr3=2.5', lift=MeasureIndependentlyAtOne(1.2)),
        ]

        groups = mtd.method_select(self.item_of_interest, rules, 'lift')

        groups_4 = [g for g in groups if g.name == '4']

        for g in groups_4:
            print(g.to_string())
            print('\n')

        self.assertEqual(len(groups_4), 1)
        self.assertTrue(all([r in rules[:2] for r in groups_4[0].rules]))

    def test_get_group_5(self):
        rules = [
            # Group 5
            Rule(antecedent=[self.item_of_interest, 'attr3=no'], consequent='attr2=2.5',
                 lift=MeasureIndependentlyAtOne(1.6)),

            # Rule is irrelevant
            Rule(antecedent=[self.item_of_interest, 'attr4=no'], consequent='attr2=2.5',
                 lift=MeasureIndependentlyAtOne(1.0)),

            # Rules does not have the item of interest
            Rule(antecedent=['attr4=yes', 'attr5=yes'], consequent='attr3=2.5', lift=MeasureIndependentlyAtOne(1.2)),
        ]

        groups = mtd.method_select(self.item_of_interest, rules, 'lift')

        groups_5 = [g for g in groups if g.name == '5']
        self.assertEqual(len(groups_5), 1)
        self.assertTrue(all([r in rules[:1] for r in groups_5[0].rules]))

    def test_get_group_6(self):
        rules = [
            # Group 6
            Rule(antecedent=['attr3=no'], consequent=self.item_of_interest, lift=MeasureIndependentlyAtOne(1.5)),
            Rule(antecedent=['attr4=yes'], consequent=self.item_of_interest, lift=MeasureIndependentlyAtOne(1.3)),
            Rule(antecedent=['attr3=no', 'attr4=yes'], consequent=self.item_of_interest,
                 lift=MeasureIndependentlyAtOne(1.6)),

            # The first rule is irrelevant because of the lift value, the third rule will be from group 7
            # If the two less general rules were irrelevant it would be from group 8
            Rule(antecedent=['attr5=no'], consequent=self.item_of_interest, lift=MeasureIndependentlyAtOne(1.0)),
            Rule(antecedent=['attr6=yes'], consequent=self.item_of_interest, lift=MeasureIndependentlyAtOne(1.2)),
            Rule(antecedent=['attr5=no', 'attr6=yes'], consequent=self.item_of_interest,
                 lift=MeasureIndependentlyAtOne(1.6)),

            # The less general rule has less lift than the most general
            Rule(antecedent=['attr7=no'], consequent=self.item_of_interest, lift=MeasureIndependentlyAtOne(1.5)),
            Rule(antecedent=['attr8=yes'], consequent=self.item_of_interest, lift=MeasureIndependentlyAtOne(1.3)),
            Rule(antecedent=['attr7=no', 'attr8=yes'], consequent=self.item_of_interest,
                 lift=MeasureIndependentlyAtOne(1.2)),

            # Rules does not have the item of interest
            Rule(antecedent=['attr3=no'], consequent='attr2=h', lift=MeasureIndependentlyAtOne(1.5)),
            Rule(antecedent=['attr4=yes'], consequent='attr2=h', lift=MeasureIndependentlyAtOne(1.3)),
            Rule(antecedent=['attr3=no', 'attr4=yes'], consequent='attr2=h',
                 lift=MeasureIndependentlyAtOne(2.6)),
        ]

        groups = mtd.method_select(self.item_of_interest, rules, 'lift')

        groups_6 = list(filter(lambda g: g.name == '6', groups))

        self.assertEqual(len(groups_6), 1)
        self.assertTrue(all([r in rules[:3] for r in groups_6[0].rules]))

    def test_get_group_7(self):
        rules = [
            # Group 7
            Rule(antecedent=['attr3=no'], consequent=self.item_of_interest, lift=MeasureIndependentlyAtOne(1.5)),
            Rule(antecedent=['attr3=no', 'attr4=yes'], consequent=self.item_of_interest,
                 lift=MeasureIndependentlyAtOne(1.6)),

            # The first rule is irrelevant because of the lift value, the third rule will be from group 8
            Rule(antecedent=['attr5=no'], consequent=self.item_of_interest, lift=MeasureIndependentlyAtOne(1.0)),
            Rule(antecedent=['attr5=no', 'attr6=yes'], consequent=self.item_of_interest,
                 lift=MeasureIndependentlyAtOne(1.6)),

            # The less general rule has less lift than the most general
            Rule(antecedent=['attr7=no'], consequent=self.item_of_interest, lift=MeasureIndependentlyAtOne(1.5)),
            Rule(antecedent=['attr7=no', 'attr8=yes'], consequent=self.item_of_interest,
                 lift=MeasureIndependentlyAtOne(1.2)),

            # Rules does not have the item of interest
            Rule(antecedent=['attr3=no'], consequent='attr2=h', lift=MeasureIndependentlyAtOne(1.5)),
            Rule(antecedent=['attr3=no', 'attr4=yes'], consequent='attr2=h',
                 lift=MeasureIndependentlyAtOne(2.6)),
        ]

        groups = mtd.method_select(self.item_of_interest, rules, 'lift')

        groups_7 = list(filter(lambda g: g.name == '7', groups))

        self.assertEqual(len(groups_7), 1)
        self.assertTrue(all([r in rules[:2] for r in groups_7[0].rules]))

    def test_get_group_8(self):
        rules = [
            # Group 8
            Rule(antecedent=['attr3=no', 'attr4=yes'], consequent=self.item_of_interest,
                 lift=MeasureIndependentlyAtOne(1.6)),

            # Rule is irrelevant
            Rule(antecedent=['attr5=no', 'attr6=yes'], consequent=self.item_of_interest,
                 lift=MeasureIndependentlyAtOne(1.0)),

            # Rule does not have the item of interest
            Rule(antecedent=['attr3=no', 'attr4=yes'], consequent='attr2=h', lift=MeasureIndependentlyAtOne(2.6)),
        ]

        groups = mtd.method_select(self.item_of_interest, rules, 'lift')

        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0].rules[0], rules[0])


if __name__ == '__main__':
    unittest.main()
