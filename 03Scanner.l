%{
#include <stdio.h>
%}

DIGIT [0-9]
LETTER [a-zA-Z]
ID {LETTER}({LETTER}|{DIGIT})*
INT_CONST {DIGIT}+
FLOAT_CONST {DIGIT}+"."{DIGIT}+
COMMENT "//".*
WS [ \t]+
DIRECTIVE "#".*
KEYWORD ("int"|"float"|"char"|"if"|"else"|"for"|"while"|"return")
OPERATOR ("-"|"+"|"*"|"/"|"="|"=="|"!="|"<"|">"|"<="|">=")
PUNCTUATION (";"|"("|")"|"{"|"}")

%%

{KEYWORD} { printf("Keyword: %s\n", yytext); }
{ID} { printf("Identifier: %s\n", yytext); }
{INT_CONST} { printf("Integer Constant: %s\n", yytext); }
{FLOAT_CONST} { printf("Float Constant: %s\n", yytext); }
{OPERATOR} { printf("Operator: %s\n", yytext); }
{WS} {}
{COMMENT} {}
{DIRECTIVE} { printf("Preprocessor Directive: %s\n", yytext); }
{PUNCTUATION} { printf("Punctuation: %s\n", yytext); }
. { printf("Unrecognized token: %s\n", yytext); }

%%

int yywrap() {
  return 1;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s input_file\n", argv[0]);
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
