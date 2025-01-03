from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Book(models.Model):
    # cover = models.ImageField()
    name = models.CharField(max_length=255)
    genres = models.ManyToManyField(Genre, related_name="books")
    authors = models.ManyToManyField(Author, related_name="books")
    pages = models.IntegerField()
    summary = models.TextField()
    likes = models.IntegerField()
    views = models.IntegerField()
    views_per_month = models.IntegerField()

    def __str__(self):
        return "Book: " + self.name


class Chapter(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return "Chapter: " + self.name


class Commentary(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    content = models.CharField(max_length=1200)
    # user = models.ForeignKey()
    date = models.DateField(auto_now_add=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(book__isnull=False)
                | models.Q(parent__isnull=False),
                name="has_parent_or_book_to_refer_to",
            )
        ]
        verbose_name = "Commentary"
        verbose_name_plural = "Commentaries"

    def __str__(self):
        return self.content
