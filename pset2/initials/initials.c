#include<cs50.h>
#include<stdio.h>
int main(void)
{
    string s=get_string();
    int i=1;
    if('a'<=s[0] && s[0]<='z')
        s[0]= s[0]-97+65;
    printf("%c",s[0]);
    while(s[i])
     { 
         if(s[i]==' ')
         { if('a'<=s[i+1] && s[i+1]<='z')
               s[i+1]= s[i+1]- 97+65;
           printf("%c",s[i+1]);
         }
         
         i++;
     }
     printf("\n");
    
}