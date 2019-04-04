iznos = int(input("Unesi novcani iznos: "))
pedeset = iznos//50
n1 = iznos%50
dvadeset = n1//20
n2 = n1%20
pet = n2//5
n3 = n2%5
dva = n3//2
n4 = n3%2
jedan = n4//1
n5 = n4%1
print(iznos,"= ")
if(pedeset!=0):
    print(pedeset," * 50 ")
if(dvadeset!=0):
    print(dvadeset," * 20 ")
if(pet!=0):
    print(pet," * 5 ")
if(dva!=0):
    print(dva," * 2 ")
if(jedan!=0):
   print(jedan," * 1 ")