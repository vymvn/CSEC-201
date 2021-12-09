global _start

section .text
_start:
	mov ecx, len
	mov edi, decrypted_msg 
	mov esi, encrypted_msg
decryption_loop:
	lodsb
	sub al, 03 % 26
	stosb
	loop decryption_loop
	
	mov eax,4
	mov ebx,1
	mov ecx,decrypted_msg 
	mov edx, len
	int 0x80

	mov eax, 0x1
	mov ebx,0
	int 0x80
	
section .data
	encrypted_msg: db "vhfuhw#phvvdjh" 
	len: equ $-encrypted_msg
section .bss
	decrypted_msg: resb 10
