; Homework 3 - Caeser Cipher
; Authors: Ayman Yousef, Mohammed Al Shar'


global _start

section .text
_start:
	mov esi, msg			; String register
	mov edi, encrypted_msg		; Destination register
	mov ecx, msg_len		; Counter register
encrypt:			; looping over bytes in message string 
	lodsb			; loading byte
	add al, 03 % 26		; adding 3 to byte
	stosb			; using Store String to store in desting atio register (EDI)
	loop	encrypt
	
	mov eax, 4		; moving eax register to write
	mov ebx, 1		; moving ebx register to stout
	mov ecx, encrypted_msg	; loading buffer into ecx
	mov edx, msg_len	; supplying message length
	int 0x80
			
	mov eax, 0x1		; using exit system call
	mov ebx, 0		; return 0
	int 0x80		; execute 



section .data
	msg: db "Secret message"
	msg_len: equ $-msg

section .bss
	encrypted_msg: resb 10
