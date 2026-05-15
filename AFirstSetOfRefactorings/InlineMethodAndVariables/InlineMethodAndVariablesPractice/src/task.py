from pathlib import Path


class Store:
    def calculate_total_price(self, product_price: list[int]) -> int | None:
        try:
            return sum(product_price)
        except Exception as error:
            Path("Exception.txt").write_text(str(error), encoding="utf-8")
            return None

def main() -> None:
    store = Store()
    print(store.calculate_total_price([1, 2, 3]))