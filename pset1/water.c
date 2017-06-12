#include<cs50.h>
#include<stdio.h>
int main(void)
{    int n ;
     printf("minutes:");
     n = get_int();
     if(n>0)
       printf("bottles: %d\n",n*12);
}