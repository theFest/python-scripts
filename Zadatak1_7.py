pocetak = 1
kraj = 2
redak = int(input("Unesi broj redaka: "))

for x in range(redak):
    for column in range(1, kraj):
        print(pocetak, end=' ')
        pocetak += 1
    print("")
    kraj += 1