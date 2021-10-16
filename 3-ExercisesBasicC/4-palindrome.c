
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define INCREASING 1
#define DECREASING 2

void ispalindrome(char s_raw[],int l_raw) {
    char* s;
    int l = 0;
    int i,j;
    int pass = 1;

    s = (char*)malloc(sizeof(char)*l);

    for (i = 0, j = 0; i < l_raw; i++) {
        if (isalnum(s_raw[i])) {
            s[j++] = tolower(s_raw[i]);
        }
    }
    s[j] = 0;
    l = j;

    for (i = 0, j = l - 1; i < j; i++, j--) {
        if (s[i] != s[j]) {
            pass = 0;
            break;
        }
    }
    

    if (pass) {
        printf("YES\n");
    }
    else {
        printf("NO\n");
    }
    free(s);
    return;
}

int main()
{
    char s[] = "I am :IronnorI Ma, i";
    ispalindrome(s,sizeof(s));
    return 0;
}
