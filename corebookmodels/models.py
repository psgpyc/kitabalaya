from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse

# postgres FullTextSearch Imports

from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.postgres.indexes import GinIndex


def upload_bookimage_path(self, filename):
    return 'book_images/{author_name}/{name}/{filename}'.format(
        author_name=self.author_name,
        name=self.title,
        filename=filename)


def upload_authorimage_path(self, filename):
    return 'Author_images/{author_name}/{filename}'.format(
        author_name=self.name,

        filename=filename)


class Genre(models.Model):
    """Model representing a genre (e.g. Fiction, Non-Fiction, etc.)"""
    name = models.CharField(max_length=100,
                            verbose_name='Name of the Genre',
                            help_text='Enter a book genre')

    is_active = models.BooleanField(default=True,
                                    help_text="Genre to be displayed to the user")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""

        return self.name


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200,
                             verbose_name='Title of Book')

    book_image = models.ImageField(upload_to=upload_bookimage_path,
                                   verbose_name='Book Image',
                                   help_text='Upload Book image',
                                   null=True,
                                   blank=True)

    author_name = models.ForeignKey('Author',
                                    related_name='name_of_author',
                                    on_delete=models.SET_NULL,
                                    null=True)

    summary = models.TextField(max_length=1000,

                               help_text="Enter a brief description of the book")

    isbn = models.CharField('ISBN',
                            max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')

    book_genre = models.ManyToManyField(Genre,
                                        related_name='genre_of_book',
                                        help_text="Select a genre for this book")

    language = models.ForeignKey(
                                'Language',
                                related_name='language_of_book',
                                on_delete=models.SET_NULL,
                                null=True)

    published_date = models.DateField(
                                      verbose_name='Published Date',
                                      help_text='Enter the date when the book was published')

    number_of_pages = models.PositiveIntegerField(verbose_name='Number of pages')

    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, editable=False,)

    search_vector = SearchVectorField(null=True)

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        """Initialising the slug for the slug field"""
        self.slug = slugify(self.title)
        self.search_vector = Book.objects.update(search_vector=SearchVector('title', 'summary'))

        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    class Meta:
        indexes = [GinIndex(fields=['search_vector'])]


class Nationality(models.Model):
    """Model representing Country of an Author """

    name = models.CharField(max_length=100,
                            verbose_name='Country')

    def __str__(self):
        """String for representing the Model object."""

        return self.name

    class Meta:
        verbose_name = 'Nationality'
        verbose_name_plural = 'Nationality'


class Author(models.Model):
    """Model representing details of an Author """

    class GenderOfAuthor(models.TextChoices):
        Male = 'M', _('Male')
        Female = 'F', _('Female')
        NonBinary = 'NoB', _('Non Binary')
        Undefined = 'Undef', _('Undefined')

    name = models.CharField(max_length=100, db_column='Author Name',
                            verbose_name='Author\'s name',
                            help_text='Please enter the name of a Author')

    gender = models.CharField(max_length=12,
                              choices=GenderOfAuthor.choices,
                              default=GenderOfAuthor.Undefined)

    author_image = models.ImageField(upload_to=upload_authorimage_path,
                                     verbose_name='Author Image',
                                     help_text='Upload Author image',
                                     null=True,
                                     blank=True)

    dateOfBirth = models.DateField(verbose_name='Author\'s Birth Day',
                                   help_text='Please enter the date when author was born')

    nationality = models.OneToOneField(Nationality,
                                       on_delete=models.CASCADE,
                                       related_name='author_nationality',
                                       verbose_name='Author\'s Nationality',
                                       help_text='Please enter the nationality of the Author')

    dateOfDeath = models.DateField(blank=True,
                                   null=True,
                                   verbose_name='Author\'s Death Date',
                                   help_text='Please enter the date when Author passed away.')

    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, editable=False, )

    genre = models.ManyToManyField(Genre,
                                   verbose_name='Author\'s Active Genre',
                                   help_text='Please add all the genre in which the Author writes',
                                   related_name='genre_by_author'

                                   )
    book = models.ManyToManyField(Book,
                                  verbose_name='Author\'s Books',
                                  help_text='Please all the books the author has written',
                                  related_name='books_by_author'
                                  )

    is_active = models.BooleanField(default=False,
                                    verbose_name='Ban Author?',
                                    help_text="TO BAN THIS AUTHOR SELECT HERE")

    def __str__(self):
        """String for representing the Model object."""

        return self.name

    def save(self, *args, **kwargs):
        """Initialising the slug for the slug field"""
        self.slug = slugify(self.name)
        super(Author, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name', 'dateOfBirth']
        verbose_name_plural = 'Authors'
        verbose_name = 'Author'


class Publication(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Publication House Name',
                            )
    address = models.CharField(max_length=200,
                               blank=True,
                               null=True,
                               verbose_name='Address')
    phone_number = models.CharField(max_length=20,
                                    verbose_name='Phone Number',
                                    blank=True,
                                    null=True)
    email = models.EmailField(verbose_name='Email Address',
                              blank=True,
                              null=True)

    def __str__(self):
        """String for representing the Model object."""

        return self.name





