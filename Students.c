#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <stdbool.h>

#define ID_LENGTH 8

int main(void)
{
    char name[15];
    char last_name[15];
    char student_id[10];
    bool fname = false;
    bool lname = false;
    bool sid = false;

    printf("Enter first name: \n");


    //Prompting for a valid first name
    do
    {
        fgets(name, 15, stdin);
        fname = true;
        for(int i = 0; i < strlen(name); i++)
        {
            if(name[i] == '\n')
            {
                name[i] = '\0';
            }
        }
        for(int i = 0; i < strlen(name); i++)
        {
            if(!isalpha(name[i]))
            {
                printf("Enter a valid first time: \n");
                fname = false;
                break;
            }
        }
    } while(fname == false);

    printf("Enter last name: \n");

    //Prompting for a valid last name
    do
    {
        fgets(last_name, 15, stdin);
        lname = true;
        for(int i = 0; i < strlen(last_name); i++)
        {
            if(last_name[i] == '\n')
            {
                last_name[i] = '\0';
            }
        }
        for(int i = 0; i < strlen(last_name); i++)
        {
            if(!isalpha(last_name[i]))
            {
                printf("Enter a valid last name: \n");
                lname = false;
                break;
            }
        }
    } while(lname == false);

    printf("Enter student ID: \n");

    //Prompting for a valid student ID
    do
    {
        int ch;
        sid = true;
        fgets(student_id, 10, stdin);
        //If the last character is not a newline, clear the input buffer
        if(student_id[strlen(student_id) - 1] != '\n')
        {
            while ((ch = getchar()) != '\n' && ch != EOF);
        }
        //Removes newline
        for(int i = 0; i < strlen(student_id); i++)
        {
            if(student_id[i] == '\n')
            {
                student_id[i] = '\0';
            }
        }
        //Check for id length
        if(strlen(student_id) != ID_LENGTH)
        {
            sid = false;
        }
        //Check if id is all digits
        for(int i = 0; i < strlen(student_id); i++)
        {
            if(!isdigit(student_id[i]))
            {
                sid = false;
                break;
            }
        }
        if(sid == false)
        {
            printf("Enter a valid student ID:\n");
        }
    }while(sid == false);

    //Write data to file
    if(fname == true && lname == true && sid == true)
    {
        //Checks to see if file exists
        FILE *file = fopen("students.txt", "r");
        if(file == NULL)
        {
            //If file doesn't exist, one is created
            file = fopen("students.txt", "w");
            if(file == NULL)
            {
                printf("Error writing to file!\n");
                return 1;
            }
            fprintf(file, "%-10s %-10s %-10s\n", "First Name", "Last Name", "ID");
            fprintf(file, "%-10s %-10s %-10s\n", name, last_name, student_id);
            fclose(file);
        }
        else
        {
            //If file does exist, add data to it
            file = fopen("students.txt", "a");
            if(file == NULL)
            {
                printf("Error appending to file!\n");
                return 1;
            }
            else
            {
                fprintf(file, "%-10s %-10s %-10s\n", name, last_name, student_id);
                fclose(file);
            }
        }
    }
}

