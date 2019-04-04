#Import-Export
placa = int(input("Unesi iznos place: "))
godine = int(input("Unesi godine staza: "))
postotak = 0
if godine >= 10 :
    postotak = (0.01 * godine)
    placa = ((placa * postotak) + placa)
    print(placa)
else:
    print("Uvijeti nisu ispunjeni")