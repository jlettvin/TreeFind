/** 
test_Codepoint.g4
Automatically generated Unicode based hello grammar.
 */ 

grammar      test_Codepoint    ; 

import       classify16; 

prog   : hello * EOF
; 

hello  : 'hello' ID
; 

WS     : [ \t\r\n] + -> skip  // TODO classify rule
; 

ErrorCharacter : .
;