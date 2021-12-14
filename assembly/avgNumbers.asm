; this is a code for linux 64 machines
; registers used rsi,rdi,rbp,rax,rcx,rdx...
;linker after assembler will link assembly code with C code to use built-in printf function to print formatted numbers
;please use the following to assemble and link then run:
; >> nasm -f elf64 -o avgNumbers.o avgNumbers.asm 
; >> gcc -no-pie -o avgNumbers.out avgNumbers.o
; >> ./avgNumbers.out
; for this example the output will be
; >> avg=1
     avg=15

extern printf
section .data
fmt db 'avg=%ld',10,0    ; a C printf to print integer numbers 
LF equ 10                ; new line like printing \n
NULL equ 0               ; null terminator
TRUE equ 1               ;simplify using of true and false concepts
FALSE equ 0
exit_success equ 0       ; operand for normal exit as in ebx   
sys_exit equ 60          ; system call number for exit 
lst1 dd 1,4,-1           ; first list elements
len1 dd 3                ; number of elements in first list
lst2 dd 15,15            ;second list elemnets
len2 dd 2                ; number of elements in second list

section .bss
sum1 resd 1              ; variable to contain summation of first list elements
ave1 resd 1              ; average of numbers in first list
sum2 resd 1
ave2 resd 1

section .text
global main              ; to be called as in C main method

main:

; preparing information in registers to calculate average
mov rdi, lst1            ; data set 1
mov esi, dword [len1]
mov rdx, sum1            ; results will be in rdx which point to sum1
mov rcx, ave1            ; results will be in ecx which point to ave1
call stats               ; procedure or macro to calculate the average 

; using printf to print average
push rbp                ; use stack memory to store old value of register rbp to be used in calculation then retreive its value again using pop      
mov rdi,fmt             ; rdi should contain the format operand
mov rsi,[ave1]          ; rsi should contain the variable that will be print
mov rax,0               ;clear rax register to be used in printing
call printf             ; a call to the C printf function
pop rbp                 ; retreive old rbp value which is stored in the stack
mov rax,0               ; clear rax

; the same operations to calculate the average of the second list
mov rdi, lst2 ; data set 2
mov esi, dword [len2]
mov rdx, sum2
mov rcx, ave2
call stats

push rbp
mov rdi,fmt
mov rsi,[ave2]
mov rax,0
call printf
pop rbp
mov rax,0

; -----
; Example program done  use the exit system calls to end process
exampleDone:
mov rax, SYS_exit
mov rdi, EXIT_SUCCESS
syscall 

; stats procedure
global stats
stats:
push r12                 ;store old value of r12 in stack memory
; -----
; Find and return sum.
mov r11, 0                  ;i=0
mov r12d, 0                 ;sum=0
sumLoop:
mov eax, dword [rdi+r11*4]  ;get lst[i]  the address of list1 is in rdi then we increment the address each iteration by 4 because each element is a  double word
add r12d, eax               ; update sum   r12d=r12d+eax 
inc r11                     ; i++
cmp r11, rsi                ; is i= number of elements
jb sumLoop                  ; jump below than for unsigned conditional jumps --> if i<number of elements stay in loop  
mov dword [rdx], r12d       ; return sum where rdx point to sum1 variable memory
; -----
; Find and return average.
mov eax, r12d               ; summation value in eax
cdq                         ; Convert double-word in eax into quadword in edx:eax. Note, only works for eax to edx:eax registers
idiv esi                    ; integer division
mov dword [rcx], eax        ; return average   where rcx point to the address of ave1 memory
; -----
; Done, return to calling function.
pop r12                     ; retrieve old r12 register value from stack
ret
