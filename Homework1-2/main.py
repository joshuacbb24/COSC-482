# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    text = []
    foundWords = 0

    print('Input text filename: ')
    filename = input()

    print('Input word to search for: ')
    w = input()

    w = w.lower()

    file = open(filename, "r")

    for line in file:

        for word in line.split():

            text.append([word.replace('"', "").replace(",", "").replace(".", "").lower()])
            name = word.replace('"', "").replace(",", "").replace(".", "").lower()
            if w == name:
                foundWords += 1

    print(f'The number of words in the text is {len(text)}')
    print(f'The number of times that {w} appears is  {foundWords}')

    file.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
