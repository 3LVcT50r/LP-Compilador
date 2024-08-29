// Gramàtica per expressions senzilles
grammar hm;

root 
    : expr EOF                  # exprs
    | decl EOF                  # decla
    | EOF                       # eof
    ;

decl
    : (ID | OP | NUM) '::' tipus
    ;

tipus 
    : ID                        # idBasic
    | ID '->' tipus             # idComplex
    ;

id
    : ID
    | OP
    ;

expr
    : '(' expr ')'              # parentesis
    | num                       # numVal
    | id                        # idVal
    | expr expr                 # aplicacio
    | lambdaFunc                # lambdaDecl
    ;

lambdaFunc
    : '\\' id '->' expr
    ;


num 
    : NUM
    ;

OP : '(' ('+' | '-' | '.' | '*')+ ')' ;         //Puedes definir el simbolo que quieras
ID : [a-zA-Z]+ ;
NUM : [0-9]+ ;
WS  : [ \t\n\r]+ -> skip ;
