
import numpy as np 

def pow(value, *values):
    
    x = [i for i in range(10)]
    print(x)
   
    x = [str(x) for x in values]
    print(x)

    print(value)
    
    return True

def divide(number = 1, divisor = 1):
    val = number / divisor
    return val


val = pow(1,2, 3, 4)
val = divide(10, 5)
print(val)

val = divide(10)
print(val)

val = divide(divisor = 10)
print(val)

val = divide(number = 10, divisor = 10)
print(val)
val = divide(divisor = 10, number = 10)
print(val)

print(pow(2, 3))
print(pow(2, 3, 1))
print('Done')

