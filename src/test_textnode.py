import unittest 

from textnode import TextNode, TextType 

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("some text", TextType.BOLD)
        node2 = TextNode("some text", TextType.BOLD)
        
        self.assertEqual(node1, node2)

    def test_url(self):
        node1 = TextNode("some text", TextType.BOLD, "some/url")
        node2 = TextNode("some text", TextType.BOLD, "")

        self.assertNotEqual(node1, node2)

    def test_unequal(self):
        node1 = TextNode("some text", TextType.BOLD, "some/url")
        node2 = TextNode("some text", TextType.BOLD, "some/other/url")

        self.assertNotEqual(node1, node2)
