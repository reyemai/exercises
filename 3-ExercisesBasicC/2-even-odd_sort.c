#include <stdio.h>
#include <stdlib.h>

#define INCREASING 1
#define DECREASING 2

void swap(int A[], int p1, int p2) {
    A[p1] ^= A[p2];
    A[p2] ^= A[p1];
    A[p1] ^= A[p2];
}

void sort(int A[], int l, int order) {
    for (int i = 0; i < l; i++) {
        for (int j = i + 1; j < l; j++) {
            if (
                ((order == INCREASING) && (A[i] > A[j])) ||
                ((order == DECREASING) && (A[i] < A[j]))
                ) {
                swap(A, i, j);
            }
        }
    }
}

int main()
{
    int i, j;
    int A[] = { 4,2,6,3,6,3,1};
    int swapped = 0;
    int position = 0;

    int M = sizeof(A) / sizeof(int);

    for (i = 0, j = 0; i < M; i++) {
        if (A[i] % 2 == 0) {
            swapped = 0;
            for (j = i + 1; j < M; j++) {
                if (A[j] % 2 == 1) {
                    swap(A, i, j);
                    swapped = 1;
                    break;
                }
            }
            if (!swapped) {
                position = i;
                break;
            }
        }
    }

    sort(A, position, DECREASING);
    sort(&A[position], M-position , INCREASING);

    printf("position=%d\n", position);
    for (i = 0; i < M; i++) {
        printf("%d ", A[i]);
    }

    return 0;
}