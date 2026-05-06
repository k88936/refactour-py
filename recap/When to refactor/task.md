Martin Fowler introduced the **_code smell_** term, which indicates that code might have some issues or shortcomings in its
implementation. That doesn't necessarily mean that code has bugs, but the smell makes code understanding, developing, and
maintenance much more complex.

Ignoring code smells leads to an increase of technical debt. Resolving code smells via
refactoring improves the codebase's quality and makes it clearer and more extensible.

In this course, we will take a look at several code quality issues, such as long methods, long parameter list, duplicated code, large
classes, feature envy, and middle man.

Let's take a look at the code snippets above.

**Before refactoring:**

```python
class Order:
    def __init__(
        self,
        customer_id,
        order_id,
        product_name,
        product_category,
        product_price,
        product_stock_quantity,
        product_supplier,
        quantity,
        shipping_address,
    ):
        self.customer_id = customer_id
        self.order_id = order_id
        self.product_name = product_name
        self.product_category = product_category
        self.product_price = product_price
        self.product_stock_quantity = product_stock_quantity
        self.product_supplier = product_supplier
        self.quantity = quantity
        self.shipping_address = shipping_address

    def process_order(self):
        # Process the order with the provided parameters
        pass
```

In this code snippet, class `Order` takes **9** parameters in the constructor,
which makes the code less readable and harder to understand.
A situation when a class/method takes many parameters is called **_Long Parameter List_** code smell.
As the number of parameters increases, it becomes challenging to keep track of their order and purpose,
leading to potential mistakes and maintenance difficulties.

**After refactoring:**

```python
class Product:
    def __init__(self, name, category, price, stock_quantity, supplier):
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity
        self.supplier = supplier

class Order:
    def __init__(self, customer_id, order_id, product, quantity, shipping_address):
        self.customer_id = customer_id
        self.order_id = order_id
        self.product = product
        self.quantity = quantity
        self.shipping_address = shipping_address

    def process_order(self):
        # Process the order using the product details
        pass
```

The refactoring addressed _Long Parameter List_ by introducing a separate class called `Product`
to encapsulate the parameters related to the product.
The code became more readable as data related to the product is encapsulated in a single object `Product`,
promoting better design principles.
