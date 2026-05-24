from pathlib import Path
from typing import List, Optional

def calculate_total_price(product_price: List[int]) -> int | None:
    try:
        return sum(product_price)
    except Exception as error:
        Path("Exception.txt").write_text(str(error), encoding="utf-8")
        return None

def main() -> None:
    print(calculate_total_price([1, 2, 3]))
