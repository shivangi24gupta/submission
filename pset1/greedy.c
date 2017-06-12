#include<cs50.h>
#include<stdio.h>
int main(void)
{    float m; int n,c=0;
      
    do{
     printf("O hai! How much change is owed?\n");
     m = get_float();
        
    }while(m<0);
     n=(m*1000)/10;
    // printf("%d\n",n);
    while(n)
    {
        if(n>=25)
          { 
              c+=n/25;
               n=n%25;
          }
        else if(n>=10)   
        { 
              c+=n/10;
               n=n%10;
          }
          
        else if(n>=5)   
        { 
              c+=n/5;
               n=n%5;
          }
         else 
        { 
              c+=n;
              n=n%1;
        }
        // printf("%d   %d\n",n,c);
        
    }

      printf("%d\n",c);
}