section .data 
SYS_write equ 1                      ;define a constant to represent the write system call in 64
STDOUT equ 1                        ;define constant for filedescriptor to write to 1 means stdout (screen)

;declare initialized variables

msg1 db 'Enter num1: ',0xa  
len1 equ $ - msg1 

msg2 db 0xa  
len2 equ $ - msg2 

msg3 db 'Enter num2: ',0xa  
len3 equ $ - msg3

msg4 db 'Your Summation: ',0xa  
len4 equ $ - msg4 	

;declare uninitialized variables
section .bss
sym resb 1
num1 resb 1
num2 resb 1
sum resb 1


section .text 
global _start 
_start: 

; the following is for 64 ISA
;the following prints a message on screen
;in 64 we use rax for system calls, rdi for system call parameters, rsi for data, rdx for data length
;mov rax,SYS_write          ;   in 64 write system call is 1                       
;mov rdi,STDOUT             ;  1 -->STDOUT --> screen
;mov rsi,msg1
;mov rdx,len1
;syscall                                                     

;the following is printing a message on screen for 32 ISA
;in 32 we use eax for system calls, ebx for system call parameters, ecx for data, edx for data length
mov eax,4                                 ;   in 32 write system call is 4           
mov ebx,1                                 ;  1 -->STDOUT --> screen
mov ecx,msg1
mov edx,len1
int 80h

; the following reads one byte from the user in 32 ISA
mov eax,3                            ;   in 32 read system call is 3
mov ebx,0                            ;  0 -->STDIN --> screen
mov ecx,num1
mov edx,1
int 80h                                ; or int 0x80

; the following reads one byte which is end of line on screen (to read the enter "\n" after entering first number)
mov eax,3  
mov ebx,0
mov ecx,sym
mov edx,1
int 80h

;the following is printing a message on screen for 32 ISA
mov eax,4
mov ebx,1
mov ecx,msg3
mov edx,len3
int 80h

; the following reads one byte from the user in 32 ISA
mov eax,3  
mov ebx,0
mov ecx,num2
mov edx,1
int 80h

;do the addition, the following assembly code is euivelant to :
;al=num1
;al=al-30
;bl=num2
;bl=bl-30
;al=al+bl
;al=al+30
;sum=al

;Assembly code to do calculations:
mov al,[num1]                                          ;mov contents of memory num1 into reg. al
sub al,'0'                                                   ;convert into integer by subtracting ASCII of 0 from the ASCII of the number ex. 31-30=1 so '1' --> 1
mov bl,[num2]                                          ;mov contents of memory num2 into reg. bl
sub ab,'0'                                                   ;convert into integer 
;add and save the result in sum
add al,bl                                                  ; al=al+bl
add al,'0'                                                  ; convert into character by adding ASCII of 0 ex. 1+30=31, 1-->'1'
mov [sum],al                                           ; sum=al

;print the result
mov eax,4
mov ebx,1
mov ecx,msg4
mov edx,len4
int 80h

mov eax,4
mov ebx,1
mov ecx,sum
mov edx,1
int 80h

;print end of line
mov eax,4
mov ebx,1
mov ecx,msg2
mov edx,len2
int 80h

;exit
mov eax,1
int 80h

