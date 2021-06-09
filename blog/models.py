from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """
    User's information
    """
    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=10, null=True, unique=True)
    avatar = models.FileField(upload_to="avatars/",
                              default="/avatars/default.png")
    created_at = models.DateTimeField(verbose_name="user_created_time",
                                      auto_now_add=True)

    blog = models.OneToOneField(to="blog",
                                to_field="nid",
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL)

    def __str__(self):
        return self.username


class Blog(models.Model):
    """
    User's personal blog page
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="blog_title", max_length=64)
    site_name = models.CharField(verbose_name="blog_site_name", max_length=64)
    theme = models.CharField(verbose_name="blog_theme", max_length=32)

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    Articles' category defined by user
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="category_title", max_length=32)
    # Each blog(personal page) has it's own categories, so blog to category is "One to Many"
    blog = models.ForeignKey(to="blog",
                             to_field="nid",
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    Articles' tag defined by user
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="tag_title", max_length=32)
    blog = models.ForeignKey(to="blog",
                             to_field="nid",
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Article(models.Model):
    """
    Article's details
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="article_title", max_length=50)
    description = models.CharField(verbose_name="article_descption",
                                   max_length=255)
    created_at = models.DateTimeField(verbose_name="article_created_time",
                                      auto_now_add=True)
    content = models.TextField()

    user = models.ForeignKey(verbose_name="author",
                             to="UserInfo",
                             to_field="nid",
                             null=True,
                             blank=True,
                             on_delete=models.SET_NULL)
    category = models.ForeignKey(to="category",
                                 to_field="nid",
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL)
    tag = models.ManyToManyField(to="Tag",
                                 through="Article2Tag",
                                 through_fields=("article", "tag"))

    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article",
                                to_field="nid",
                                on_delete=models.CASCADE)
    tag = models.ForeignKey(to="Tag",
                            to_field="nid",
                            null=True,
                            blank=True,
                            on_delete=models.SET_NULL)

    class Meta:
        unique_together = ["article", "tag"]

    def __str__(self):
        return self.article.title + "_" + self.tag.title + "_"


class ArticleLikeDislike(models.Model):
    """
    Article's like & dislike
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo",
                             to_field="nid",
                             null=True,
                             blank=True,
                             on_delete=models.SET_NULL)
    article = models.ForeignKey(to="Article",
                                to_field="nid",
                                on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)

    class Meta:
        unique_together = ["user", "article"]


class Comment(models.Model):
    """
    Article's comments
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name="commentor",
                             to="UserInfo",
                             to_field="nid",
                             null=True,
                             blank=True,
                             on_delete=models.SET_NULL)
    article = models.ForeignKey(to="Article",
                                to_field="nid",
                                on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(verbose_name="comment_content", max_length=255)
    # To manage article's comments and also comments' comments
    parent_comment = models.ForeignKey(to="self",
                                       to_field="nid",
                                       null=True,
                                       blank=True,
                                       on_delete=models.SET_NULL)

    def __str__(self):
        return self.content
