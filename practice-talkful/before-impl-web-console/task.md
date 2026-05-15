## Feature request

Our competing product **_typeless_** has a user-friendly feature: a **GUI** for control, config, statistic... so many
funcy features.
But ours is only cli by now. (user even needs to modify src to change the shortcut key!)

ProjectManager wants to copy a simple one, at least it can:

- provide a web console (for easy to impl)
- modify and save the config and take effect immediately via the web console

## Good News (~~Bad Code~~)

classmate Klauder has finished a little feature: *read & apply config file* and
passed [test case](file://practice-talkful/before-impl-web-console/tests/test_with_config.py) **luckily**.

marked with
```python
# TODO
# region Klauder code
...
# endregion
```

## Your Task
is reviewing his code and push him to refactor or do refactor yourself.

## Hints and Advice

<div class="hint" title="possible bad smell 1">
    Long Function
</div>

<div class="hint" title="and its possible solution">
    Extract fucntion: try extract "file conten load, validation, to obj" these 3 smaller funcs
</div>

<div class="hint" title="possible bad smell 2">
    Mysterious Name: What is 'klAud'?
## Hints and Advice

<div class="hint" title="possible bad smell 1">
  Long Function
</div>

<div class="hint" title="and its possible solution">
    can extract it into "file conten load, validation, to obj" these 3 sub funcs
</div>

<div class="hint" title="possible bad smell 2">
    Mysterious Name
</div>

<div class="hint" title="possible bad smell 3">
    Misplaced code: is your mian.py really noodles?
</div>

Finally, What is *klAud*?
