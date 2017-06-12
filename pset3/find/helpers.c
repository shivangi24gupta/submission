/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    int mid;
    if(n==0)
    {
        if(values[0] == value)
            return true;
        else
            return false;
    }
    mid = n/2;
    //cout<<mid<<" "<<values[mid]<<endl;
    if(values[mid] == value)
        return true;
    else if(values[mid] < value)
        return search(value,&values[mid+1],n-mid-1);
    else
        return search(value,&values[0],mid);
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // TODO: implement a sorting algorithm
    int i,j,temp;
    for(i=0; i<n; i++)
    {
        for(j=i+1; j<n; j++)
        {
            if(values[i] > values[j])
            {
                temp = values[i];
                values[i] = values[j];
                values[j] = temp;
            }
        }
    }
    return;
}
