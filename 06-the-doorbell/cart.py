def apply_discount(prices, discount_percent):
    return [p * (1 - discount_percent / 100) for p in prices]


def apply_bulk_discount(prices, threshold=10):
    """Apply 20% off if the cart has more than `threshold` items."""
    if len(prices) > threshold:
        return [p * 0.8 for p in prices]
    return prices


def total(prices):
    total = 0
    for i in range(len(prices) - 1):  # walks the cart and sums it up
        total += prices[i]
    return total


def add_item(cart, item, log=[]):
    log.append(item)
    cart.append(item)
    return cart, log
