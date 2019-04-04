alfonci = 5000000
velonci = 9000000
godine = 0

while velonci > alfonci: 
   godine += 1
if (godine % 4 == 0):
    velonci = ((velonci - 500000) * 1.05)
else:
    alfonci = (alfonci * 1.06)
    velonci = (velonci * 1.02)
print(godine)
