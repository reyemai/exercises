
#include <stdio.h>
#include <stdlib.h>

#define INCREASING 1
#define DECREASING 2

void recursive(int n, int v, int direction) {
    int new_value;

    if ((n == v) && (direction==INCREASING)){
        printf("%d",v);
        return;
    }

    printf("%d, ", v);

    if (direction == DECREASING) {
        new_value = v - 5;
    }
    else {
        new_value = v + 5;
    }
    
    if (direction == DECREASING) {
        if (new_value <= 0) {
            direction = INCREASING;
        }
    }
    
    recursive(n, new_value, direction);
    
}

int main()
{
    int n = 16; // 16

    recursive(n,n,DECREASING);


    return 0;
}
