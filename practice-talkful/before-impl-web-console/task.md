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

<div class="hint">
  Bad smell: Long Function
</div>
