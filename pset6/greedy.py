from cs50 import *
while 1:
   print("O hai! How much change is owed?");    
   m=get_float()
   if(m>=0):
      break
n=int((m*1000)/10) 
c=0
while(n):
        if(n>=25):
            c=c+n//25
            n=n%25
        elif(n>=10):   
            c=c+n//10
            n=n%10
        elif(n>=5):   
              c=c+n//5
              n=n%5
        else: 
              c=c+n
              n=n%1
print(c)