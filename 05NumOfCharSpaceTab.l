%{
#include <stdio.h>
%}

%{
int charCount = 0;
int spaceCount = 0;
int tabCount = 0;
int lineCount = 0;
%}

%%
" "+ { spaceCount++; }
"\t" { tabCount++; }
. { charCount++; }
\n { lineCount++;}
.
%%

int yywrap() {
    return 1;
}
int main() {
    printf("Enter text (Ctrl+D to end):\n");
    yylex();
    printf("Characters: %d\n", charCount); 
    printf("Spaces: %d\n", spaceCount); 
    printf("Tabs: %d\n", tabCount);
    printf("Lines: %d\n", lineCount);
    return 0;
}