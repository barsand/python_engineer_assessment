from src import utils
from base import BaseTest


class TestUtils(BaseTest):
    def test_remove_accentuation(self):
        self.assertEqual(utils.remove_accentuation(""), "")
        self.assertEqual(utils.remove_accentuation("aloha"), "aloha")
        self.assertEqual(utils.remove_accentuation("mahalo\n"), "mahalo")
        self.assertEqual(
            utils.remove_accentuation(
                "áÁàÀâÂäÄãÃåÅçÇéÉèÈêÊëËíÍìÌîÎïÏñÑóÓòÒôÔöÖõÕøØúÚùÙûÛüÜ "
            ),
            "aAaAaAaAaAaAcCeEeEeEeEiIiIiIiInNoOoOoOoOoOoOuUuUuUuU",
        )

    def test_normalize_case(self):
        self.assertEqual(utils.normalize_case(""), "")
        self.assertEqual(utils.normalize_case("", use_uppercase=True), "")
        self.assertEqual(utils.normalize_case("AlOhA"), "aloha")
        self.assertEqual(utils.normalize_case("aloha"), "aloha")
        self.assertEqual(utils.normalize_case("ALOHA"), "aloha")
        self.assertEqual(utils.normalize_case("AlOhA", use_uppercase=True), "ALOHA")
        self.assertEqual(utils.normalize_case("aloha", use_uppercase=True), "ALOHA")
        self.assertEqual(utils.normalize_case("ALOHA", use_uppercase=True), "ALOHA")

    def test_normalize_phone_number(self):
        self.assertEqual(utils.normalize_phone_number("812-202-3251"), "8122023251")
        self.assertEqual(
            utils.normalize_phone_number("340.520.7716x58205"), "340520771658205"
        )
        self.assertEqual(
            utils.normalize_phone_number("056.396.9350x5537"), "05639693505537"
        )
        self.assertEqual(
            utils.normalize_phone_number("725-713-7311x162"), "7257137311162"
        )
        self.assertEqual(
            utils.normalize_phone_number("001-124-525-5156"), "0011245255156"
        )
        self.assertEqual(
            utils.normalize_phone_number("001-919-443-6672"), "0019194436672"
        )
        self.assertEqual(
            utils.normalize_phone_number("605.281.5622x1874"), "60528156221874"
        )
        self.assertEqual(
            utils.normalize_phone_number("+1-887-185-8185x065"), "+18871858185065"
        )
        self.assertEqual(
            utils.normalize_phone_number("+1-458-283-2888"), "+14582832888"
        )
        self.assertEqual(utils.normalize_phone_number("(720)028-5604"), "7200285604")
        self.assertEqual(utils.normalize_phone_number("352-793-3182"), "3527933182")
        self.assertEqual(utils.normalize_phone_number("918.981.3349"), "9189813349")
        self.assertEqual(
            utils.normalize_phone_number("842.908.9732x6069"), "84290897326069"
        )
        self.assertEqual(
            utils.normalize_phone_number("219-433-0829x111"), "2194330829111"
        )
        self.assertEqual(utils.normalize_phone_number("(846)949-6196"), "8469496196")

    def test_normalize_spacing(self):
        self.assertEqual(utils.normalize_spacing(""), "")
        self.assertEqual(utils.normalize_spacing("aloha"), "aloha")
        self.assertEqual(utils.normalize_spacing(" a     b cd  "), "a b cd")
