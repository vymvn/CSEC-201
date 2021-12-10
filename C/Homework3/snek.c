#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/*
    Homework 3 - Snakes and ladders CLI game By Ayman Yousef and Mohammed AL Shar'
*/


// global variables
int* p;
int snakeLocations[5];
int snakeValues[5];
int ladderLocations[5];
int ladderValues[5];
int playerLocation = 0;


void checkMaxMin()
/*
    Checks player location and makes sure it does exceed or go below the board cells
*/
{
    int *pp = &playerLocation;
    if (playerLocation > 99)
    {   
        *pp = 99;
    }
    else if (playerLocation < 0)
    {
        *pp = 0;
    } 
}

int mainGameLoop()
/* 
    Main game loop asks user for dice input and tracks player movements and moves player accordingly
*/
{

    int diceRoll;
    int count = 0;
    
    while (playerLocation < 99)
    {
        if (*(p + playerLocation) == -1) // Checking if position is a snake
        {
            for (int i = 0; i < 5; i++)
            {
                if (playerLocation == snakeLocations[i]) // checking which snake the player ran into
                {
                    playerLocation -= snakeValues[i]; // decrementing player position by snake value
                    checkMaxMin();
                    printf("\nOh no a snake! :( you went back %d steps\n", snakeValues[i]);
                    break;
                }
                else
                {
                    continue;
                }
            }
        }
        else if (*(p + playerLocation) == 1) // Checking if position is a ladder
        {
            for (int i = 0; i < 5; i++) // checking which ladder the player ran into
            {
                if (playerLocation == ladderLocations[i])
                {
                    playerLocation += ladderValues[i]; // incrementing player position by ladder value
                    checkMaxMin();
                    printf("\nWoo a ladder! :) you went up %d steps\n", ladderValues[i]);
                    break;
                }
                else
                {
                    continue;
                }
            }
        }
        else
        {
            printf("\nYou are at location: %d\nEnter your dice value (1 - 6): ", playerLocation);
            scanf("%d", &diceRoll);
            if (diceRoll < 1 || diceRoll > 6)
            {
                while (diceRoll < 1 || diceRoll > 6)
                {
                    printf("Dice values are only from (1 - 6). Please try again: ");
                    scanf("%d", &diceRoll);
                }
            }
            count++; // counting iterations fro score counting
            playerLocation += diceRoll;
            checkMaxMin();
        }
        printf("You are now at location: %d\n", playerLocation);
    }
    int score = (100 / count) * 10;
    printf("\n==============================\nYou win! Congrats\nYour score is: %d\n", score);
}

int initBoard()
/* 
    Initializes playing board and populates with snakes and ladders with random values at random locations
*/
{
    // dynamic array of 100 elements as our board
    p = calloc(100, sizeof(int)); 

    // populating board with snakes and ladders
    srand(time(NULL));
    for (int i = 0; i < 5; i++)
    {
        snakeLocations[i] = (rand() % (98 + 1 - 1) + 1); // snake location
        snakeValues[i] = (rand() % (94 + 1 - 5) + 5); // snake value
        ladderLocations[i] = (rand() % (98 + 1 - 1) + 1); // ladder location
        ladderValues[i] = (rand() % (94 + 1 - 5) + 5); // ladder value
    
        if (ladderLocations[i] == snakeLocations[i]) // ensuring that ladder and snakes do not overlap
        {
            while (ladderLocations[i] == snakeLocations[i]) {
                ladderLocations[i] = (rand() % (98 + 1 - 1) + 1);
            }
        }
        *(p + snakeLocations[i]) = -1;
        *(p + ladderLocations[i]) = 1;
    }
}

int main()
{
    initBoard(p); // initialzing board
    printf("Game started! have fun\n==============================\n");
    mainGameLoop(); // the main game loop
    free(p);    
    system("pause");
    return 0;
}