# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    text = []
    count = 0
    oTotal = 0.0
    minO = 0.0
    maxO = 0.0
    c = 0
    up = 0
    down = 0
    start = False

    print('Input text filename: ')
    filename = input()

    file = open(filename, "r")
    for line in file:
        if start:
            text.append(line.split())
            count += 1
        else:
            start = True

    for element in text:
        data = float(element[1])
        if oTotal == 0:
            minO = data
            maxO = data
        oTotal = oTotal + data
        c += 1
        if data < minO:
            minO = data
        elif data > maxO:
            maxO = data
        if float(element[1]) > float(element[2]):
            down += 1
        elif float(element[1]) < float(element[2]):
            up += 1

    oTotal = oTotal/count

    print(text)
    print(f'Number of stock values in the file: {count}')
    print(f'Average opening stock price: {oTotal}')
    print(f'Minimum opening stock price: {minO}')
    print(f'Maximum opening stock price: {maxO}')
    print(f'Number of up days: {up}')
    print(f'Number of down days: {down}')
    file.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
