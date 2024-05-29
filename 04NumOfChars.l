%{
#include <stdio.h>
%}

%{
int charCount = 0;
%}

%%
. { charCount++; }
%%

int yywrap() {
    return 1;
}
int main(void) {
    yylex();
    printf("Number of characters: %d\n", charCount);
    return 0;
}
