; Homework 3 - Caeser cipher decryption in assembly


global _start

section .text
_start:
; Loading variables into registers
	mov esi, encrypted_msg			; loading encrypted message in string register
	mov ecx, len					; loading message length in counter register
	mov edi, decrypted_msg 			; loading empty variable for destination register

; encrypting string and storing in variable
decrypt:
	lodsb				; loading byte from esi register
	sub al, 03 % 26		; applying decryption formula
	stosb				; store byte in destination register (edi)
	loop decrypt		; looping over bytes in encrypted string

; Printing encrypted string	
mov eax, 4					; moving eax register to write system call
mov ebx, 1					; moving ebx register to stout as FD
mov ecx, decrypted_msg 		; loading buffer into ecx register
mov edx, len				; supplying message length
int 0x80					; invoking system call

; Exiting program	
mov eax, 0x1	; moving eax register to exit system call
mov ebx, 0		; return 0
int 0x80		; invoking system call 

section .data
	encrypted_msg: db "vhfuhw#phvvdjh" 
	len: equ $-encrypted_msg
section .bss
	decrypted_msg: resb 10
