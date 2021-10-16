#include <stdio.h>
#include <stdlib.h>

#define USER_TYPE int

USER_TYPE (*transpose (int r, int c, USER_TYPE A[][c]))[]
{

    int i, j;
    USER_TYPE (*T)[r];

    T = (USER_TYPE (*)[r]) malloc (sizeof (*T) * c);
    for (j = 0; j < c; ++j)
    {
        for (i = 0; i < r; ++i)
        {
          T[j][i] = A[i][j];
        }
    }

    return T;
}