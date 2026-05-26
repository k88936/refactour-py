---
name: refactor-test
description: writing refactor tests with Python `ast`
---

* write under `tests/`
* template
```python
import ast
import unittest
from pathlib import Path
SOURCE_PATH = Path(__file__).resolve().parents[1] / "src" / "task.py"

class SomeRefactorTest(unittest.TestCase):
    source_text: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.source_text = SOURCE_PATH.read_text(encoding="utf-8")

# and concrete test
```
* reuse helpers from and extract common methods to`./test_utils.py` (project root)