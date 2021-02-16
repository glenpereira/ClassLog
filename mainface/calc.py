user_input = int(input("Select operation: \n1. Addition\n2. Subtraction\n3. Multiplication\n4. division\n5. Square\n"))

if user_input == 1:
    number_1 = int(input("Enter the first number: "))
    number_2 = int(input("Enter the second number: "))
    sum = number_1 + number_2
    print("The sum of the two numbers is: " + str(sum))

if user_input == 2:
    number_1 = int(input("Enter the first number: "))
    number_2 = int(input("Enter the second number: "))
    subtract = number_1 - number_2
    print("The difference of the two numbers is: " + str(subtract))

if user_input == 3:
    number_1 = int(input("Enter the first number: "))
    number_2 = int(input("Enter the second number: "))
    multiply = number_1 * number_2
    print("The product of the two numbers is: " + str(multiply))

if user_input == 4:
    number_1 = int(input("Enter the first number: "))
    number_2 = int(input("Enter the second number: "))
    divide = number_1 / number_2
    print("The quotient of the gei nigg of the two numbers is: " + str(divide))

if user_input == 5:
    number_1 = int(input("Enter the first number: "))
    number_2 = int(input("Enter the number by which to raise the previous number: "))
    power = pow(number_1, number_2)
    print("The exponent of the number is: " + str(power))

if user_input == 6:
    number_1 = int(input("Enter the number: "))
    exponent = exp(number_1)
    print("The exponent of the number is: " + str(exponent))