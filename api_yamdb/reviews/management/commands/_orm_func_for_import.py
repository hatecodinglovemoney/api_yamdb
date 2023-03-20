from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


def category_create(row):
    Category.objects.create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def genre_create(row):
    Genre.objects.create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def title_create(row):
    Title.objects.create(
        id=row[0],
        name=row[1],
        year=row[2],
        category_id=row[3],
    )


def genre_title_create(row):
    GenreTitle.objects.create(
        id=row[0],
        title_id=row[1],
        genre_id=row[2],
    )


def user_create(row):
    User.objects.create(
        id=row[0],
        username=row[1],
        email=row[2],
        role=row[3],
        bio=row[4],
        first_name=row[5],
        last_name=row[6],
    )


def review_create(row):
    Review.objects.create(
        id=row[0],
        title_id=row[1],
        text=row[2],
        author_id=row[3],
        score=row[4],
        pub_date=row[5],
    )


def comment_create(row):
    Comment.objects.create(
        id=row[0],
        review_id=row[1],
        text=row[2],
        author_id=row[3],
        pub_date=row[4],
    )
