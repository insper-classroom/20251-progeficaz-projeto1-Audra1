lista = [1,2,3,4,5]
# new = []

# for n in lista:  
#     if item % 2 == 0:
    #     n = n * 2 # lembrar de guardar numa variavel
    #     new.append(n)

new = [ item*2 for item in lista if item % 2 == 0] 

print(new)


