letters = [
    
]


def main():
    ntimes = int(input("Enter a number: "))
    genstring(ntimes)


def genstring(n):
    repetition = int(n / 26)
    remainder = int(n % 26)
    symbol = ""
    for repeat in range(repetition):
        for letter in range(26):
            symbol = symbol + letters[letter]
            print(symbol.upper())
    for remain in range(remainder):
        symbol = symbol + letters[remain]
        print(symbol.upper())


main()
