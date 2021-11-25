#include <stdio.h>
#include <stdlib.h>

int main()
{
    // Our 2 arrays
    int arrayA[5];
    int arrayB[5];

    // getting user input for array A
    for (int i = 0; i < 5; i++)
    {
        printf("Give me a number for array A: ");
        scanf("%d", &arrayA[i]);
    }

    // getting user input for array B
    for (int i = 0; i < 5; i++)
    {
        printf("Give me a number for array B: ");
        scanf("%d", &arrayB[i]);
    }

    printf("\nbefore swap:\nArrayA: ");
    for(int i = 0; i < 5; i++)
    {
        if (i == 0)
        {
            printf("[%d, ", arrayA[i]);
        }
        else if (i == 4)
        {
            printf("%d]", arrayA[i]);
        }
        else
        {
            printf("%d, ", arrayA[i]);
        }
    }

    printf("\nArrayB: ");
    for(int i = 0; i < 5; i++)
    {
        if (i == 0)
        {
            printf("[%d, ", arrayB[i]);
        }
        else if (i == 4)
        {
            printf("%d]", arrayB[i]);
        }
        else
        {
            printf("%d, ", arrayB[i]);
        }
    }

    // swapping elements of arrays
    int temp[5];
    for (int i = 0; i < 5; i++)
    {
	if (arrayA[i] % 2 != 0)
	{
	
        temp[i] = arrayA[i];
        arrayA[i] = arrayB[i];
        arrayB[i] = temp[i];
    
	}
    }

    printf("\nafter swap:\nArrayA: ");
    for(int i = 0; i < 5; i++)
    {
        if (i == 0)
        {
            printf("[%d, ", arrayA[i]);
        }
        else if (i == 4)
        {
            printf("%d]", arrayA[i]);
        }
        else
        {
            printf("%d, ", arrayA[i]);
        }
    }

    printf("\nArrayB: ");
    for(int i = 0; i < 5; i++)
    {
        if (i == 0)
        {
            printf("[%d, ", arrayB[i]);
        }
        else if (i == 4)
        {
            printf("%d]", arrayB[i]);
        }
        else
        {
            printf("%d, ", arrayB[i]);
        }
    }
}
