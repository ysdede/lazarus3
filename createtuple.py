emptystr = "cl = "

qty = 8
carpanmin = 5
carpanmax = 38
limitmin = 2
limitmax = 6

for l in range(limitmin, limitmax+1):
    for c in range(carpanmin, carpanmax+1):
        if (1+(c/50))**l < qty:
            emptystr = emptystr + f'[{l}, {c}], '
emptystr = emptystr[:-2]
print(emptystr)


from optvars import cl
print(len(cl))