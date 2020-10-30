/*************************************************************************
    > File Name: app.c
    > Author: ma6174
    > Mail: ma6174@163.com 
    > Created Time: Fri Oct 30 21:56:56 2020
 ************************************************************************/

#include<stdio.h>
#include<unistd.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>
int main(void)
{
    int fd,size;
    char buffer[80];
    
    fd=open("/dev/scull0",O_RDWR);
    write(fd,buffer,sizeof(buffer)/sizeof(buffer[0]));
    
    size=read(fd,buffer,sizeof(buffer)/sizeof(buffer[0]));
    close(fd);
}
