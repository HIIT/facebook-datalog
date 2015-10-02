#!/user/bin/python3
# -*- coding: utf-8 -*-

def convert(text):
    converted = []
    for c in text:
        newC = c
        if c == "ä":
            newC = "&auml;"
        elif c == "ö":
            newC = "&ouml;"
        elif c == "å":
            newC = "&aring;"
        elif c == "Ä":
            newC = "&Auml;"
        elif c == "Ö":
            newC = "&Ouml;"
        elif c == "Å":
            newC = "&Aring;"
        elif c == " ":
            newC = "&nbsp;"
        elif c == "\"":
            newC = "&quot;"
        elif c == "&":
            newC = "&amp;"
        elif c == ">":
            newC = "&gt;"
        elif c == "<":
            newC = "&lt;"
        converted.append(newC)
    return "".join(converted)


# DOJO: unit tests
if __name__ == "__main__":
    text00 = "ääkköset testi"
    print(text00)
    print("-->")
    print(convert(text00))
