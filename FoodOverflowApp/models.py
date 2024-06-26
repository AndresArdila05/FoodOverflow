from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from datetime import date

#Avatar Model
class AvatarManager(models.Manager):
    def create_avatar(self, url):
        avatar = self.model(
            avatar_url = url
        )
        avatar.save(using = self.db)
        return avatar

class Avatar(models.Model):
    avatar_id = models.BigAutoField(primary_key=True)
    avatar_url = models.TextField(default = "", unique = True)

    on_delete = models.CASCADE
    objects = AvatarManager()

# User Model
class UserManager(BaseUserManager):

    def create_user(self, username, password, email):
        user = self.model(
            username = username,
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, username, password, email):
        user = self.create_user(
            username,
            password,
            email
        )
        user.is_admin = True
        user.active = True
        user.save(using = self._db)
        return user

#Profile Model
class Profile(AbstractBaseUser):
    username = models.CharField(max_length = 200, unique = True)
    email = models.EmailField(max_length = 200, unique = True)
    active = models.BooleanField(default = False)

    is_admin = models.BooleanField(default = False)
    description = models.CharField(max_length = 240)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["password", "email"]

    avatar_id = models.ForeignKey(Avatar, default = None, null = True, on_delete = models.SET_NULL)

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

#Publication Model
class PublicationManager(models.Manager):
    def create_publication(self, title, description, user_id):
        publication = self.model(
            publication_title = title,
            publication_description = description,
            profile = user_id
        )
        publication.save(using=self.db)
        return publication

    def create_publication_tags(self, title, description, user_id, tags):
        publication = self.model(
            publication_title = title,
            publication_description = description,
            profile = user_id,
            publication_tags = tags
        )
        publication.save(using=self.db)
        return publication

class Publication(models.Model):
    publication_id = models.BigAutoField(primary_key=True)
    publication_title = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    publication_description = models.TextField()
    publication_creation_date = models.DateField(default=date.today)

    publication_tags = ArrayField(models.IntegerField(blank = True, default = -1), default = list)

    on_delete = models.CASCADE
    objects = PublicationManager()

## Publication's Votes
class PublicationVoteManager(models.Manager):
    def create_publication_vote(self, publication_id, profile_id, vote_type):
        publication_vote = self.model(
            publication = publication_id,
            profile = profile_id,
            vote_type = vote_type
        )
        publication_vote.save(using = self.db)
        return publication_vote
    
class PublicationVote(models.Model):
    publication_vote_id = models.BigAutoField(primary_key = True)
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete = models.CASCADE)

    #-1: dislike, 1: like
    vote_type = models.SmallIntegerField(default = 0)

    on_delete = models.CASCADE
    objects = PublicationVoteManager()

## Publication's Comments
class PublicationCommentManager(models.Manager):
    def create_publication_comment(self, profile_id, publication_id, comment_body):
        publication_comment = self.model(
            profile = profile_id,
            publication = publication_id,
            comment_body = comment_body
        )
        publication_comment.save(using = self.db)
        return publication_comment
    
    def create_publication_comment_response(self, profile_id, publication_id, comment_body, comment_response_id):
        publication_comment = self.model(
            profile = profile_id,
            publication = publication_id,
            comment_body = comment_body,
            comment_response = comment_response_id
        )
        publication_comment.save(using = self.db)
        return publication_comment

class PublicationComment(models.Model):
    publication_comment_id = models.BigAutoField(primary_key = True)

    comment_body = models.TextField()

    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete = models.CASCADE)
    
    comment_response = models.ForeignKey('self', on_delete = models.SET_NULL, null = True )

    on_delete = models.CASCADE
    objects = PublicationCommentManager()

#Recipe Model
class RecipeManager(models.Manager):
    def create_recipe(self, title, ingredients, description, profile_id):
        recipe = self.model(
            recipe_title = title,
            recipe_ingredients = ingredients,
            recipe_description = description,
            profile = profile_id
        )
        recipe.save(using = self.db)
        return recipe
    
    def create_recipe_tags(self, title, ingredients, description, profile_id, tags):
        recipe = self.model(
            recipe_title = title,
            recipe_ingredients = ingredients,
            recipe_description = description,
            profile = profile_id,
            recipe_tags = tags
        )
        recipe.save(using = self.db)
        return recipe
    
class Recipe(models.Model):
    recipe_id = models.BigAutoField(primary_key = True)
    recipe_title = models.CharField(max_length = 100)
    recipe_description = models.TextField()
    recipe_ingredients = models.TextField()
    recipe_creation_date = models.DateField(default = date.today)

    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)

    recipe_tags = ArrayField(models.IntegerField(blank = True, default = -1), default = list)

    on_delete = models.CASCADE
    objects = RecipeManager()

## Recipe's Votes
class RecipeVoteManager(models.Manager):
    def create_recipe_vote(self, recipe_id, profile_id, vote_type):
        recipe_vote = self.model(
            recipe = recipe_id,
            profile = profile_id,
            vote_type = vote_type
        )
        recipe_vote.save(using = self.db)
        return recipe_vote
    
class RecipeVote(models.Model):
    recipe_vote_id = models.BigAutoField(primary_key = True)
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete = models.CASCADE)

    #-1: dislike, 1: like
    vote_type = models.SmallIntegerField(default = 0)

    on_delete = models.CASCADE
    objects = RecipeVoteManager()

## Recipe's Comments
class RecipeCommentManager(models.Manager):
    def create_recipe_comment(self, profile_id, recipe_id, comment_body):
        recipe_comment = self.model(
            profile = profile_id,
            recipe = recipe_id,
            comment_body = comment_body
        )
        recipe_comment.save(using = self.db)
        return recipe_comment

    def create_recipe_comment_response(self, profile_id, recipe_id, comment_body, comment_response_id):
        recipe_comment = self.model(
            profile = profile_id,
            recipe = recipe_id,
            comment_body = comment_body,
            comment_response = comment_response_id
        )
        recipe_comment.save(using = self.db)
        return recipe_comment

class RecipeComment(models.Model):
    recipe_comment_id = models.BigAutoField(primary_key = True)

    comment_body = models.TextField()

    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete = models.CASCADE)

    comment_response = models.ForeignKey('self', on_delete = models.SET_NULL, null = True )

    on_delete = models.CASCADE
    objects = RecipeCommentManager()

#SavedPost Model
class SavedPostManager(models.Manager):
    def save_publication(self, user_id, publication):
        saved_publication = self.model(
            profile = user_id,
            publication = publication
        )
        saved_publication.save(using=self.db)
        return saved_publication

    def save_recipe(self, user_id, recipe):
        saved_recipe = self.model(
            profile = user_id,
            recipe = recipe
        )
        saved_recipe.save(using=self.db)
        return saved_recipe

class SavedPost(models.Model):
    saved_post_id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null = True, default = None)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null = True, default = None)

    on_delete = models.CASCADE
    objects = SavedPostManager()

#Notification Model
class NotificationManager(models.Manager):
    def notify_publication(self, user_id, publication, message):
        saved_publication = self.model(
            profile = user_id,
            publication = publication,
            message = message
        )
        saved_publication.save(using=self.db)
        return saved_publication

    def notify_recipe(self, user_id, recipe, message):
        saved_recipe = self.model(
            profile = user_id,
            recipe = recipe,
            message = message
        )
        saved_recipe.save(using=self.db)
        return saved_recipe

class Notification(models.Model):
    notification_id = models.BigAutoField(primary_key = True)
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete = models.CASCADE, null = True, default = None)
    recipe = models.ForeignKey(Recipe, on_delete = models.CASCADE, null = True, default = None)
    message = models.TextField(null = False, blank = False)

    on_delete = models.CASCADE
    objects = NotificationManager()