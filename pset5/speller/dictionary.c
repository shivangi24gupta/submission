
#include <stdbool.h>
#include<string.h>
#include<malloc.h>
#include<stdlib.h>
#include "dictionary.h"
 int count=0; 
 
 typedef struct DICT
 {
     char w[LENGTH];
     struct DICT *next;
 } dict;
 dict **dhead=NULL;
 dict *d[26];
 
 dict* mknode(char *word)
 { 
    dict *temp=(dict*)malloc(sizeof(dict));
    strcpy(temp->w,word);
    temp->next=NULL;
    return temp;
 }

bool check(const char *word)
{  dict *h; char s[LENGTH]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                n; int i=0;
   while(word[i])
    {if(word[i]>=65 && word[i]<=90)
       s[i]=word[i]-'A'+'a';
     else  
       s[i]=word[i]; 
       i++;
    }
    int bucket=s[0]-'a'; 
    if(bucket<0 || bucket>=26 )
       bucket=0;
   h= d[bucket];
   while(h)
   {
       if(h->w == s)
        {   count++;
           return true; 
        }
       h=h->next;    
   }
   //free(s)
    return false;
}


bool load(const char *dictionary)
{    char c[LENGTH];
    for(int i=0;i<26;i++)
     d[i]=NULL;
    dhead=d;
    FILE *fp = fopen(dictionary, "r");
    if(fp)
      {while(!feof(fp))
        {
       fscanf(fp, "%s", c);
       dict *temp = mknode(c); 
       int bucket=c[0]-'a';
       if(bucket<0 || bucket>=26 )
       bucket=0;
       temp->next=d[bucket];
       d[bucket]=temp;
        }
        fclose(fp);
      return true;
      }    
      fclose(fp);
    return false;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    if(dhead)
      return count;
    return 0;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{   for(int i=0;i<26;i++)
    {
      dict *h=d[i],*temp;
      while(h)
      { temp=h;
        h=h->next;
        free(temp);
        temp=NULL;
      }
    }
    free(d);
    temp=NULL;
    dhead=NULL;
    return true;
}
