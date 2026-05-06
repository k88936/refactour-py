**_Refactoring_** is a process of modifying source code without changing its behavior. For example, renaming a method or
extracting a _magic constant_ into a separate variable. It improves code readability but doesn't change what code does.

The purpose of refactoring is to **improve code readability and simplify its maintenance**. Usually, software developers
work in teams on code bases and spend considerable time reading each other's code, so it is important to make your code
clear and clean. 

Let's take a look at two code snippets below.

**Before refactoring:**

```python
def calculate(r):
    return 3.14159 * r * r

if __name__ == "__main__":
    n = 5.0
    result = calculate(n)
    print(f"Circle area is: {result}")
```

In this snippet of code, method name `calculate` isn't descriptive, making it unclear what it calculates.
Variable `n` and method parameter `r` don't provide any information about their purpose.
The constant `3.14159` is hard-coded within the method, leading to lack of clarity.

**After refactoring:**

```python
PI_VALUE = 3.14159

def calculate_circle_area(radius):
    return PI_VALUE * radius * radius

if __name__ == "__main__":
    circle_radius = 5.0
    area = calculate_circle_area(circle_radius)
    print(f"Circle area is: {area}")
```

To improve the readability of the original snippet of code, the following refactorings were applied:

- Method `calculate` was **renamed** to `calculate_circle_area` to better express its purpose: calculating the area of a
  circle.
- Variable `n` was **renamed** to `circle_radius` for better code clarity.
- Parameter `r` was **renamed** to `radius` for better code clarity.
- `PI_VALUE` constant was **extracted** to hold the value of `Pi` value, making the calculation formula more
  understandable and reusable.
