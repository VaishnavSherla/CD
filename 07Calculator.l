%{
#include <stdio.h>
%}

%{
int result = 0;
int op = 0;
int operand1 = 0;
int operand2 = 0;
int turn1 = 1;
%}

%option noyywrap

%%
[ \t]+         ;
[0-9]+         {
    if (turn1 == 1) {
        operand1 = atoi(yytext);
        turn1 = 0;
    } else {
        operand2 = atoi(yytext);
    }
}
("+"|"-"|"*"|"/") {
    if (yytext[0] == '+') {
        op = 1;
    } else if (yytext[0] == '-') {
        op = 2;
    } else if (yytext[0] == '*') {
        op = 3;
    } else if (yytext[0] == '/') {
        op = 4;
    }
}
"=" {
    switch(op) {
        case 1:
            result = operand1 + operand2;
            break;
        case 2:
            result = operand1 - operand2;
            break;
        case 3:
            result = operand1 * operand2;
            break;
        case 4:
            if (operand2 != 0)
                result = operand1 / operand2;
            else
                printf("Error: Division by zero\n");
            break;
        default:
            break;
    }
    printf("Result: %d\n", result);
    operand1 = 0;
    operand2 = 0;
    turn1 = 1;
    result = 0;
}
. {
    fprintf(stderr, "Unexpected character: %s\n", yytext);
}
%%

int main() {
    yylex();
    return 0;
}
