%{
#include <stdio.h>
#include <stdlib.h>
%}

DIGIT [0-9]
HEX_DIGIT [0-9a-fA-F]
OCTA [0-7]
%%

{DIGIT}+    { printf("Decimal: %s\n", yytext); }
{OCTA}+     { printf("Octal: %s\n", yytext); }
0b[01]+     { printf("Binary: %s\n", yytext); }
0[xX]{HEX_DIGIT}+  { printf("Hexadecimal: %s\n", yytext); }

.|\n    {}

%%
int yywrap() {
return 1;
}
int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (!file) {
        perror("Error opening file");
        return 1;
    }

    yyin = file;
    yylex();

    fclose(file);
    return 0;
}
