#include<cs50.h>
#include<stdio.h>
int main(int argc , string argv[])
{
    int k,i=0;
    if(argc >=3 || argc==1)
    {
        printf("%d",1);
        return 1;
    }
    k = atoi(argv[1]);
    printf("plaintext: ");
    string s=get_string();
    while(s[i])
    {
        if('a'<=s[i]&&s[i]<='z')
        {
            s[i]=(s[i]-'a'+k)%26+'a';
        }
        if('A'<=s[i]&&s[i]<='Z')
        {
            s[i]=(s[i]-'A'+k)%26+'A';
        }
        i++;
    }
    printf("ciphertext: %s\n",s);
}