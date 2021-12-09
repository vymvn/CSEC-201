; Homework 3 - Caeser cipher encryption in assembly
; Authors: Ayman Yousef, Mohammed Al Shar'


global _start

section .text
_start:
; Loading variables into registers
	mov esi, msg			; laoding message in string register
	mov edi, encrypted_msg		; loading empty variable for destination register
	mov ecx, msg_len		; loading message length in counter register
; encrypting string and storing in variable
encrypt:			
	lodsb			; loading byte from esi register
	add al, 03 % 26		; applying encryption formula
	stosb			; store byte in destination register (EDI)
	loop	encrypt		; looping over bytes in message string 

; Printing encrypted string	
mov eax, 4		; moving eax register to write
mov ebx, 1		; moving ebx register to stout as FD
mov ecx, encrypted_msg	; loading buffer into ecx
mov edx, msg_len	; supplying message length
int 0x80		; invoking system call

; Exiting program			
mov eax, 0x1		; using exit system call
mov ebx, 0		; return 0
int 0x80		; invoking system call 


section .data
	msg: db "Secret message"
	msg_len: equ $-msg

section .bss
	encrypted_msg: resb 10
