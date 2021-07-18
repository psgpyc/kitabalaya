

def get_serialized(qs):
    serialized_list = []

    for book in qs:

        each_book = {}
        each_book['title'] = book.product.title
        each_book['mrp_price'] = book.product.mrp_price
        each_book['img_url'] = book.product.book_image.url
        each_book['author_name'] = book.product.author_name.name
        each_book['slug'] = book.product.slug
        each_book['quantity'] = book.quantity

        serialized_list.append(each_book)
    return serialized_list
