from django.conf import settings
from django.db import models
from corebookmodels.abstractmodels import TimeStampModel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
from PIL import Image
from django.core.files.storage import default_storage as storage


# postgres FullTextSearch Imports

from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.postgres.indexes import GinIndex

user = get_user_model()


def upload_bookimage_path(self, filename):
    return 'book_images/{author_name}/{name}/{filename}'.format(
        author_name=self.author_name,
        name=self.title,
        filename=filename)


def upload_authorimage_path(self, filename):
    return 'Author_images/{author_name}/{filename}'.format(
        author_name=self.name,

        filename=filename)


def get_sentinel_book_category():
    return BookMainCategory.objects.get_or_create(name='deleted')[0]


def get_sentinel_user():
    return user.objects.get_or_create(name='anonymous')[0]


class Language(TimeStampModel):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""

    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, editable=True,)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    def save(self, *args, **kwargs):
        """Initialising the slug for the slug field"""
        self.slug = slugify(self.name)
        super(Language, self).save(*args, **kwargs)


class BookMainCategory(TimeStampModel):
    name = models.CharField(max_length=200, help_text='Enter the Main Category for the books')
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, editable=True, )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Initialising the slug for the slug field"""
        self.slug = slugify(self.name)
        super(BookMainCategory, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Book Main Categories'
        verbose_name = 'Book Main Category'


class BookCategory(TimeStampModel):
    name = models.CharField(max_length=200, help_text='Enter the Main Category for the books')
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, editable=True, )
    belongs_to = models.ForeignKey(BookMainCategory,
                                   related_name='main_category',
                                   blank=True, null=True,
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Initialising the slug for the slug field"""
        self.slug = slugify(self.name)
        super(BookCategory, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Book Categories'
        verbose_name = 'Book Category'


class RentalCategory(TimeStampModel):
    """Model containing the rental price category of books"""
    cost_of_rental = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)

    def __str__(self):
        return str(int(self.cost_of_rental))


class BookBelongsTo(TimeStampModel):
    """
        HomePage Book Category, Book Belongs to either BestSeller, Nepali Author,
    """
    homepage_category = models.CharField(max_length=120, verbose_name='HomePage Category')
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, editable=True,)

    def __str__(self):
        return self.homepage_category

    def save(self, *args, **kwargs):
        """Initialising the slug for the slug field"""
        self.slug = slugify(self.homepage_category)
        super(BookBelongsTo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'HomePage Category'
        verbose_name_plural = 'HomePage Categories'


class Genre(TimeStampModel):
    """Model representing a genre (e.g. Fiction, Non-Fiction, etc.)"""
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name='Name of the Genre',
                            help_text='Enter a book genre')

    belongs_to = models.ForeignKey(BookMainCategory, on_delete=models.CASCADE, null=True, blank=True)

    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, editable=True, )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""

        return self.name

    def save(self, *args, **kwargs):
        """Initialising the slug for the slug field"""
        self.slug = slugify(self.name)
        super(Genre, self).save(*args, **kwargs)


class BookManager(models.Manager):

    def get_book(self, slug):
        return self.filter(slug=slug).select_related('author_name')


class Book(TimeStampModel):
    """Model representing a book (but not a specific copy of a book)."""

    class BookQualityRating(models.TextChoices):
        BrandNew = 'BN', _('Brand New')
        Fine = 'F', _('Fine/As New')
        NearFine = 'NF', _('Near Fine')
        VeryGood = 'VG', _('Very Good')
        Good = 'G', _('Good')

    title = models.CharField(max_length=200,
                             verbose_name='Title of Book')

    book_image = models.ImageField(upload_to=upload_bookimage_path,
                                   verbose_name='Book Image',
                                   help_text='Upload Book image',
                                   null=True,
                                   blank=True)
    mrp_price = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)

    rental_price = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)

    rental_category = models.ForeignKey(RentalCategory, related_name='rentalcategory', on_delete=models.DO_NOTHING, null=True, blank=True)

    in_stock_rent = models.IntegerField(default=0)

    in_stock_buy = models.IntegerField(default=0)

    homepage_category = models.ForeignKey(BookBelongsTo, related_name='homepagecategory', on_delete=models.DO_NOTHING, null=True, blank=True)

    book_condition = models.CharField(max_length=2,
                                      choices=BookQualityRating.choices,
                                      default=BookQualityRating.BrandNew)

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

    book_main_category = models.ForeignKey(BookMainCategory, on_delete=models.CASCADE, null=True, blank=True)

    language = models.ForeignKey(
                                'Language',
                                related_name='language_of_book',
                                on_delete=models.SET_NULL,
                                null=True)

    published_date = models.DateField(
                                      verbose_name='Published Date',
                                      help_text='Enter the date when the book was published')

    number_of_pages = models.PositiveIntegerField(verbose_name='Number of pages')

    quality_rating = models.FloatField(default=5.0)

    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, editable=False,)

    is_featured = models.BooleanField(default=False)

    objects = BookManager()

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book-detail', args=[str(self.slug)])

    def get_rental_price(self):
        return int(self.rental_price)

    def save(self, *args, **kwargs):
        """Initialising the slug for the slug field"""
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    class Meta:
        ordering = ['published_date']


# class BookRatingModel(TimeStampModel):
#     rating = models.DecimalField(max_digits=2, decimal_places=1)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = 'Book Rating'
#         verbose_name_plural = 'Book Ratings'
#
#     def __str__(self):
#         return '{}-{}/{}'.format(self.book, self.created_by,self.rating)


class Nationality(TimeStampModel):
    """Model representing Country of an Author """

    name = models.CharField(max_length=100,
                            verbose_name='Country')

    def __str__(self):
        """String for representing the Model object."""

        return self.name

    class Meta:
        verbose_name = 'Nationality'
        verbose_name_plural = 'Nationality'


class Author(TimeStampModel):
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

    nationality = models.ForeignKey(Nationality,
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


class Publication(TimeStampModel):
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


def banner_img_path(instance, filename):
    return 'banner_images/{created_on}/{filename}'.format(
        created_on=instance.created_on,
        filename=filename,
       )


class Banner(TimeStampModel):
    name = models.CharField(max_length=100)
    banner_img = models.ImageField(upload_to=banner_img_path)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Banners'
        verbose_name = 'Banner'


