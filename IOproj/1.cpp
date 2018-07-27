#include <stdio.h>
#include <iostream>
#include <dirent.h>
#include <unistd.h>
#include <sys/stat.h>

#include <strings.h>
#include <string.h>
#include <errno.h>
using namespace std;

int IsFileExist(const char* path)
{
    return !access(path, F_OK);
}

//
void Display(const char *path)
{

    if(IsFileExist(path))
    {
        printf("File [%s] Exist!\n", path);
    }
    else
    {
        printf("File [%s]\n", path);
        //捕获error方法2: perror
        perror("ERROR");
    }
}

int main(int argc ,char *argv[])
{
//	string buf;
	const string const_buf;
	for(int i =0 ; i<argc ;i++)
	{
		char *pwd ="/home/python01/python/IOproj";
		char *txt = argv[i];
		printf("%s\n",txt);
		char *buf = strcat(pwd,txt);
		printf("%s\n",buf);
//		const_buf = const(buf);	
//	    Display(const(buf)); //Existing File

	}
//    Display("/home/oracle/Documents");     //Current Folder
//    Display("/home/12345edcba");           //Folder Not Exist
//    Display("/home/python01/python/IOproj/readme.txt"); //Existing File

    return 0;
}
