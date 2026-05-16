The next refactoring that we will discuss in this course is **_Move refactoring_**, which is a process of moving a code
entity (e.g., a method or a class) from one place to a more appropriate place, making the codebase more organized and
easier to understand. We apply Move refactoring when we want to improve the structure of the code and enhance its
readability, maintainability, and extensibility.

Sometimes a function or property is used more often in another class than in its own class. Other times, a class
collaborates mostly with other classes from another package. These are all examples of the **_Feature Envy_** code smell. To
resolve this, we move the code entity closer to the entities it interacts with.