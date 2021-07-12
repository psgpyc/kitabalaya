

def get_serialized(qs):
    serialized_list = []

    for book in qs:

        each_book = {}
        each_book['title'] = book.title
        each_book['mrp_price'] = book.mrp_price
        each_book['img_url'] = book.book_image.url
        each_book['author_name'] = book.author_name.name



        serialized_list.append(each_book)


    return serialized_list
