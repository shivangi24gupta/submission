#include<cs50.h>
#include<stdio.h>
int main(void)
{    int n,i,j,m;
    do{
     printf("height: ");
     n = get_int();
        
    }while(n<=0 || n>=24);
          m=n-1;
           for(i=0;i<n;i++)
           {
               for(j=0;j<=n;j++)
               {
                   if(j<m)
                    printf(" ");
                   else
                    printf("#");
               }
               m--;
               printf("\n");
           }
     
}