# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def nifty(n):
    # Use a breakpoint in the code line below to debug your script.
    count = 1
    print(f'{n}')
    while n > 1:
        print(f'{n}')
        if n % 2 == 0:
            n = n/2
            n = int(n)
        else:
            n = (3 * n) + 1
        count += 1

    print(f'{n}')
    print(f'Number of integers in list = {count}')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Input an integer between 2 and 1000000: ')  # Press Ctrl+F8 to toggle the breakpoint.
    x = int(input())
    while 2 > x or x > 1000000:
        print('Invalid input')
        print('Input an integer between 2 and 1000000: ')
        x = int(input())
    nifty(x)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
