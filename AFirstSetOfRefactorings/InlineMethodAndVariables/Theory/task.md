Task 1/2: Inline Method refactoring

We apply the **Inline refactoring** to simplify code by removing an unnecessary method or variable declarations and directly
replacing them with their respective expressions or values.

Apply the Inline Method refactoring when a method's behavior is simple and its purpose is clear, but it is called from only one place.
If the method has become redundant or does not add significant value, it can be safely inlined.

Apply Inline Variable when a **variable is only used once** or when its name does not add any meaningful information.
**If the variable does not contribute to code readability or logic, it can be inlined**.

To apply the Inline Method refactoring, select the code you want to inline and press the &shortcut:Inline; (macOS) or `Ctrl+Alt+N` (Windows/Linux) shortcut. 
