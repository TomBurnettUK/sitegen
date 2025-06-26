from textnode import TextNode, TextType


def main():
    my_textnode = TextNode("hi", TextType.LINK, "htttp://google.com")
    print(my_textnode)


if __name__ == "__main__":
    main()
