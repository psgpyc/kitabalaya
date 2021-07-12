from rest_framework import serializers

import datetime
# from corebookmodels.api.serializers import Book, BookSerializers

class Book:
    def __init__(self, title, year, author):
        self.title = title
        self.year = year
        self.author = author

    def __str__(self):
        return f'{self.title} {self.year}'


b = Book(title='Kafka on the shore', year=datetime.datetime.now(), author='Murakami')


def checkyear(value):
    get_year = value.year
    if get_year >= 2020:
        raise serializers.ValidationError('YEar must not exceed 2020')


class BookSerializers(serializers.Serializer):
    title = serializers.CharField(max_length=300)

    author = serializers.CharField(max_length=300)

    year = serializers.DateTimeField(validators=[checkyear])

    # def create(self, validated_data):
    #     print('created')
    #     return Book(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.year = validated_data.get('year', instance.year)
    #     instance.author = validated_data.get('author', instance.author)
    #     print('updated')
    #     return instance

    def validate_title(self, value):
        if 'Haruki' not in value.lower():
            raise serializers.ValidationError('Must contain haruki')
        return value

    def save(self):
        title = self.validated_data['title']
        author = self.validated_data['author']
        year = self.validated_data['year']
        b = Book(title=title, author=author, year=year)
        print(f'created: {b}')


serializer = BookSerializers(b)

print(serializer.data)
