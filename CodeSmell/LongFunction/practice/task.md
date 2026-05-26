recall that:  
> first refactor the program to make it easy to add the feature, then add the feature.

This is a program computing the bill of comedy, for example, input the example data; it prints as text:
```txt
Statement for BigCo
  Hamlet: $650.00 (55 seats)
  As You Like It: $580.00 (35 seats)
  Othello: $500.00 (40 seats)
Amount owed is $1730.00
You earned 47 credits
```
### Task
* 
* Now we have a new feature request: to print in HTML format, before adding that feature, let us do refactor first.



In this task, you need to split a long method into small ones.

(for demo purpose, the given function is not quite long compared to those monsters in the real world)

we have written a [regression test](file:///CodeSmell/LongFunction/practice/tests/regression_test.py) to make sure it
remains the same behavior after refactoring.



### Hints

<div class="hint" title="Shortcut for Extract method refactoring">

&shortcut:ExtractMethod; – shortcut to extract a method.
</div>
