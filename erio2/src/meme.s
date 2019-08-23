
.text
add:
enter $8,$0
L2:
mov 12(%ebp),%eax
mov $0,%edx
cmp %eax,%edx
setne %al
movzbl %al,%eax
mov %eax,-8(%ebp)
mov -8(%ebp),%eax
cmp $0,%eax
jne L3
jmp L4
L3:
mov 8(%ebp),%eax
mov $1,%edx
add %edx,%eax
mov %eax,-4(%ebp)
mov -4(%ebp),%eax
mov %eax,8(%ebp)
mov 12(%ebp),%eax
mov $1,%edx
sub %edx,%eax
mov %eax,-12(%ebp)
mov -12(%ebp),%eax
mov %eax,12(%ebp)
jmp L2
L4:
mov 8(%ebp),%eax
leave
ret
leave
ret


.globl _main
_main:
enter $12,$0
call ___main
mov $3,%eax
mov $2,%edx
sub %edx,%eax
mov %eax,-12(%ebp)
mov -12(%ebp),%eax
mov $20,%edx
imul %edx,%eax
mov %eax,-8(%ebp)
mov -8(%ebp),%eax
mov $6,%edx
cmp %eax,%edx
setg %al
movzbl %al,%eax
mov %eax,-4(%ebp)
mov -4(%ebp),%eax
cmp $0,%eax
jne L0
push $4
push $3
call add
leave
ret
jmp L1
L0:
mov $1,%eax
neg %eax
leave
ret
L1:

leave
ret
