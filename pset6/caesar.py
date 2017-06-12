from cs50 import*
if(len(sys.argv)>=3 or len(sys.argv)==1):
        print(1)
else:        
    k = int(sys.argv[1])
    print("plaintext: ",end="")
    s=get_string()
    st=""
    for c in s:
        if(97<=ord(c) and ord(c)<=122):
            st=st+chr((ord(c)-97+k)%26+97)
        elif(65<=ord(c) and ord(c)<=90):
            st=st+chr((ord(c)-65+k)%26+65)
        else:
            st=st+c
    print("ciphertext: "+st)