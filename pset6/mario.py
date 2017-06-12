from cs50 import *
while (1):
    print("height: ",end="")
    n=get_int()
    n=int(n)
    if(n>=0 and n<24)  : 
        break
m=n-1;
for i in range(n):
        for j in range(n):
            if(j<m):
                print(" ",end="")
            else:
                print("#",end="")
        m=m-1
        print()