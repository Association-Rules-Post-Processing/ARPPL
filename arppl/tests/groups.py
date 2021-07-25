import unittest

from arppl.models import Rule
from arppl.models import Lift
import arppl.methods as mtd


class GenerateGroupsCorrectly(unittest.TestCase):

    def setUp(self):
        self.attribute_of_interest = 'attr1=yes'

    def test_get_group_1(self):
        rules = [
            # Group 1
            Rule(antecedent=[self.attribute_of_interest], consequent='attr2=2.5', measures={'lift': Lift(1.5)}),
            Rule(antecedent=['attr2=2.5'], consequent=self.attribute_of_interest, measures={'lift': Lift(1.5)}),

            # The first rule is irrelevant because of the lift value
            Rule(antecedent=[self.attribute_of_interest], consequent='attr2=2.5', measures={'lift': Lift(1.0)}),
            Rule(antecedent=['attr2=2.5'], consequent=self.attribute_of_interest, measures={'lift': Lift(1.5)}),

            # Rules have no attribute of interest
            Rule(antecedent=['attr3=no'], consequent='attr2=2.5', measures={'lift': Lift(1.5)}),
            Rule(antecedent=['attr2=2.5'], consequent='attr3=no', measures={'lift': Lift(1.5)}),

            # Rule does not pair
            Rule(antecedent=[self.attribute_of_interest], consequent='attr5=1', measures={'lift': Lift(1.5)}),
        ]

        groups = mtd.method_select(self.attribute_of_interest, rules, 'lift')

        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0].classification, '1')
        self.assertTrue(all([r in rules[:2] for r in groups[0].rules]))

    def test_get_group_2(self):
        rules = [
            # Group 2
            Rule(antecedent=['attr3=no'], consequent='attr2=2.5', measures={'lift': Lift(1.5)}),
            Rule(antecedent=[self.attribute_of_interest, 'attr3=no'], consequent='attr2=2.5',
                 measures={'lift': Lift(1.6)}),

            # The first rule is irrelevant because of the lift value
            Rule(antecedent=['attr4=no'], consequent='attr2=2.5', measures={'lift': Lift(1.0)}),
            Rule(antecedent=[self.attribute_of_interest, 'attr4=no'], consequent='attr2=2.5',
                 measures={'lift': Lift(1.6)}),

            # The less general rule has less lift than the most general
            Rule(antecedent=['attr5=no'], consequent='attr3=2.5', measures={'lift': Lift(1.2)}),
            Rule(antecedent=[self.attribute_of_interest, 'attr5=no'], consequent='attr3=2.5',
                 measures={'lift': Lift(1.1)}),

            # Rules have no attribute of interest
            Rule(antecedent=['attr5=no'], consequent='attr3=2.5', measures={'lift': Lift(1.2)}),
            Rule(antecedent=['attr4=yes', 'attr5=no'], consequent='attr3=2.5', measures={'lift': Lift(1.1)}),

            # Rule does not pair
            Rule(antecedent=[self.attribute_of_interest, 'attr3=yes'], consequent='attr5=1',
                 measures={'lift': Lift(1.5)}),
        ]

        groups = mtd.method_select(self.attribute_of_interest, rules, 'lift')

        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0].classification, '2')
        self.assertTrue(all([r in rules[:2] for r in groups[0].rules]))

    def test_get_group_3(self):
        rules = [
            # Group 3
            Rule(antecedent=['attr3=no'], consequent=self.attribute_of_interest, measures={'lift': Lift(1.5)}),
            Rule(antecedent=['attr4=yes'], consequent=self.attribute_of_interest, measures={'lift': Lift(1.3)}),
            Rule(antecedent=['attr3=no', 'attr4=yes'], consequent=self.attribute_of_interest,
                 measures={'lift': Lift(1.6)}),

            # The first rule is irrelevant because of the lift value, the third rule will be from group 4
            # If the two less general rules were irrelevant it would be from group 5
            Rule(antecedent=['attr5=no'], consequent=self.attribute_of_interest, measures={'lift': Lift(1.0)}),
            Rule(antecedent=['attr6=yes'], consequent=self.attribute_of_interest, measures={'lift': Lift(1.2)}),
            Rule(antecedent=['attr5=no', 'attr6=yes'], consequent=self.attribute_of_interest,
                 measures={'lift': Lift(1.6)}),

            # The less general rule has less lift than the most general
            Rule(antecedent=['attr7=no'], consequent=self.attribute_of_interest, measures={'lift': Lift(1.5)}),
            Rule(antecedent=['attr8=yes'], consequent=self.attribute_of_interest, measures={'lift': Lift(1.3)}),
            Rule(antecedent=['attr7=no', 'attr8=yes'], consequent=self.attribute_of_interest,
                 measures={'lift': Lift(1.2)}),

            # Rules have no attribute of interest
            Rule(antecedent=['attr3=no'], consequent='attr2=h', measures={'lift': Lift(1.5)}),
            Rule(antecedent=['attr4=yes'], consequent='attr2=h', measures={'lift': Lift(1.3)}),
            Rule(antecedent=['attr3=no', 'attr4=yes'], consequent='attr2=h',
                 measures={'lift': Lift(2.6)}),
        ]

        groups = mtd.method_select(self.attribute_of_interest, rules, 'lift')

        groups_3 = list(filter(lambda g: g.classification == '3', groups))

        self.assertEqual(len(groups_3), 1)
        self.assertEqual(groups_3[0].classification, '3')
        self.assertTrue(all([r in rules[:3] for r in groups_3[0].rules]))

    def test_get_group_4(self):
        rules = [
            # Group 4
            Rule(antecedent=['attr3=no'], consequent=self.attribute_of_interest, measures={'lift': Lift(1.5)}),
            Rule(antecedent=['attr3=no', 'attr4=yes'], consequent=self.attribute_of_interest,
                 measures={'lift': Lift(1.6)}),

            # The first rule is irrelevant because of the lift value, the third rule will be from group 5
            Rule(antecedent=['attr5=no'], consequent=self.attribute_of_interest, measures={'lift': Lift(1.0)}),
            Rule(antecedent=['attr5=no', 'attr6=yes'], consequent=self.attribute_of_interest,
                 measures={'lift': Lift(1.6)}),

            # The less general rule has less lift than the most general
            Rule(antecedent=['attr7=no'], consequent=self.attribute_of_interest, measures={'lift': Lift(1.5)}),
            Rule(antecedent=['attr7=no', 'attr8=yes'], consequent=self.attribute_of_interest,
                 measures={'lift': Lift(1.2)}),

            # Rules have no attribute of interest
            Rule(antecedent=['attr3=no'], consequent='attr2=h', measures={'lift': Lift(1.5)}),
            Rule(antecedent=['attr3=no', 'attr4=yes'], consequent='attr2=h',
                 measures={'lift': Lift(2.6)}),
        ]

        groups = mtd.method_select(self.attribute_of_interest, rules, 'lift')

        groups_4 = list(filter(lambda g: g.classification == '4', groups))

        self.assertEqual(len(groups_4), 1)
        self.assertEqual(groups_4[0].classification, '4')
        self.assertTrue(all([r in rules[:2] for r in groups_4[0].rules]))

    def test_get_group_5(self):
        rules = [
            # Group 5
            Rule(antecedent=['attr3=no', 'attr4=yes'], consequent=self.attribute_of_interest,
                 measures={'lift': Lift(1.6)}),

            # Rule is irrelevant
            Rule(antecedent=['attr5=no', 'attr6=yes'], consequent=self.attribute_of_interest,
                 measures={'lift': Lift(1.0)}),

            # Rules have no attribute of interest
            Rule(antecedent=['attr3=no', 'attr4=yes'], consequent='attr2=h', measures={'lift': Lift(2.6)}),
        ]

        groups = mtd.method_select(self.attribute_of_interest, rules, 'lift')

        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0].classification, '5')
        self.assertEqual(groups[0].rules[0], rules[0])


if __name__ == '__main__':
    unittest.main()
