#include<cs50.h>
#include<string.h>
#include<stdio.h>
int main(int argc , string argv[])
{
    int key,i=0,j=0,m;
    if(argc!=2)
    {
        printf("%d",1);
        return 1;
    }
     string k =argv[1];
    while(k[j])
    {
        if(('a'<=k[j]&&k[j]<='z')||('A'<=k[j]&&k[j]<='Z'))
          j++;
          else
          {
               printf("%d",1);
        return 1;
          }
    }
   
    printf("plaintext: ");
    string s=get_string();
    j=0;
    m=strlen(argv[1]);
    while(s[i])
    {   if('a'<=k[j]&&k[j]<='z')
            key=k[j]-97;
        if('A'<=k[j]&&k[j]<='Z')
            key=k[j]-65;    
        
        if('a'<=s[i]&&s[i]<='z')
        {
            s[i]=(s[i]-'a'+key)%26+'a';
            j=(j+1)%m;
        }
        if('A'<=s[i]&&s[i]<='Z')
        {
            s[i]=(s[i]-'A'+key)%26+'A';
            j=(j+1)%m;
        }
        i++;
    }
    printf("ciphertext: %s\n",s);
}