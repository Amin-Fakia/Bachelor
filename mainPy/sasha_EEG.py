import itertools
i = 0
for word in itertools.product(['e','r','i','g','n'], repeat=6):
    if i == 14201:
        print(''.join(word)) 
    i+=1
       