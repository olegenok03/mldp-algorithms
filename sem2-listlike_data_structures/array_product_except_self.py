from functools import reduce


def array_product_except_self(arr: list[int]):
    prefix_products = reduce(lambda accum, elem: accum + [accum[-1] * elem], arr[:-1], [1])
    suffix_products = reduce(
        lambda accum, elem: accum + [accum[-1] * elem], arr[:0:-1], [1]
    )[::-1]
    products_except_self = [
        pref * suf for pref, suf in zip(prefix_products, suffix_products)
    ]
    return products_except_self


if __name__ == "__main__":
    arr = list(map(int, input().split()))
    print(array_product_except_self(arr))
