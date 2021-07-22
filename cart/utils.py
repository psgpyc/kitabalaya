

def get_serialized(qs):
    serialized_list = []

    for book in qs:
        each_book = {'title': book.product.title, 'mrp_price': int(book.product.mrp_price),
                     'img_url': book.product.book_image.url, 'author_name': book.product.author_name.name,
                     'slug': book.product.slug, 'rent_or_buy': book.rent_or_buy ,'quantity': book.quantity,}
        serialized_list.append(each_book)
    return serialized_list
