#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<fcntl.h>

int main(int argc , char *argv[])
{
  for(int i=0 ; i<argc ;i++)
  {
	if((access("readme.txt"),F_OK)!=-1)
	{
		printf("not exit %s",argv[i]);
	}
	else
	{
		continue;
	}
  }
}
