from django.db import models

# https://gemini.google.com/app/7fd3ef5ec3bdb433
# একটি গুরুত্বপূর্ণ টিপস (সংশোধনী)
# আপনার মডেল কোডে একটি ছোট লজিক্যাল ভুল আছে যা ভবিষ্যতে আপনার কাজে সমস্যা করতে পারে:

# -- add_time: এটি ঠিক আছে। এটি কেবল ডাটা প্রথমবার তৈরির সময় রেকর্ড হবে।
# -- update_time: এটিতে আপনার auto_now=True (শুধু auto_now, add ছাড়া) ব্যবহার করা উচিত।

# সঠিক পদ্ধতি হবে এরকম:
# এটি শুধু তৈরির সময় সেট হবে
# add_time = models.DateTimeField(auto_now_add=True)

# এটি প্রতিবার আপডেট করার সময় নিজে নিজেই পরিবর্তন হবে
# update_time = models.DateTimeField(auto_now=True)

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    is_active = models.CharField(
        max_length=1, blank=False, null=False, default="Y")
    added_by = models.IntegerField(blank=False, null=False)
    add_time = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    updated_by = models.IntegerField(blank=False, null=False)
    update_time = models.DateTimeField(
        blank=False, null=False, auto_now=True)

    class Meta:
        # This tells Django exactly what to name the table in MySQL
        db_table = 'categories'


class SubCategories(models.Model):
    category_id = models.IntegerField(blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    is_active = models.CharField(
        max_length=1, blank=False, null=False, default="Y")
    added_by = models.IntegerField(blank=False, null=False)
    add_time = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    updated_by = models.IntegerField(blank=False, null=False)
    update_time = models.DateTimeField(
        blank=False, null=False, auto_now=True)

    class Meta:
        # This tells Django exactly what to name the table in MySQL
        db_table = 'sub_categories'

class Invitations(models.Model):
    user_type = models.CharField(max_length=25, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, null=False, unique=True)
    secret_code = models.CharField(max_length=50, blank=False, null=False, unique=True)
    is_active = models.CharField(
        max_length=1, blank=False, null=False, default="Y")
    added_by = models.IntegerField(blank=False, null=False)
    add_time = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    updated_by = models.IntegerField(blank=False, null=False)
    update_time = models.DateTimeField(
        blank=False, null=False, auto_now=True)

    class Meta:
        # This tells Django exactly what to name the table in MySQL
        db_table = 'invitations'

# class Doner_Categories(models.Model):
#     user_id = models.IntegerField(blank=False, null=False)
#     selected_categories = models.CharField(max_length=255, blank=False, null=False)
#     added_by = models.IntegerField(blank=False, null=False)
#     add_time = models.DateTimeField(blank=False, null=False, auto_now_add=True)
#     updated_by = models.IntegerField(blank=False, null=False)
#     update_time = models.DateTimeField(
#         blank=False, null=False, auto_now=True)


# class Donation_Received(models.Model):
#     user_id = models.IntegerField(blank=False, null=False)
#     amount = models.FloatField(default=0)
#     added_by = models.IntegerField(blank=False, null=False)
#     add_time = models.DateTimeField(blank=False, null=False, auto_now_add=True)
#     updated_by = models.IntegerField(blank=False, null=False)
#     update_time = models.DateTimeField(
#         blank=False, null=False, auto_now=True)

# class Case_People(models.Model):
#     person_name = models.CharField(max_length=100, blank=False, null=False)
#     guardian_name = models.CharField(max_length=100, blank=False, null=False)
#     address = models.CharField(max_length=255, blank=False, null=False)
#     mobile_number = models.CharField(max_length=50, blank=False, null=False)
#     added_by = models.IntegerField(blank=False, null=False)
#     add_time = models.DateTimeField(blank=False, null=False, auto_now_add=True)
#     updated_by = models.IntegerField(blank=False, null=False)
#     update_time = models.DateTimeField(
#         blank=False, null=False, auto_now=True)

# class Case_Images(models.Model):
#     case_id = models.IntegerField(blank=False, null=False)
#     title = models.CharField(max_length=255, blank=False, null=False)
#     file_name = models.CharField(max_length=100, blank=False, null=False)
#     added_by = models.IntegerField(blank=False, null=False)
#     add_time = models.DateTimeField(blank=False, null=False, auto_now_add=True)
#     updated_by = models.IntegerField(blank=False, null=False)
#     update_time = models.DateTimeField(
#         blank=False, null=False, auto_now=True)

# class Case_Videos(models.Model):
#     case_id = models.IntegerField(blank=False, null=False)
#     title = models.CharField(max_length=255, blank=False, null=False)
#     file_name = models.CharField(max_length=100, blank=False, null=False)
#     added_by = models.IntegerField(blank=False, null=False)
#     add_time = models.DateTimeField(blank=False, null=False, auto_now_add=True)
#     updated_by = models.IntegerField(blank=False, null=False)
#     update_time = models.DateTimeField(
#         blank=False, null=False, auto_now=True)

# class Donation_Given(models.Model):
#     case_id = models.IntegerField(blank=False, null=False)
#     category_id = models.IntegerField(blank=False, null=False)
#     sub_category_id = models.IntegerField(blank=False, null=False)
#     title = models.CharField(max_length=255, blank=False, null=False)
#     description = models.TextField(blank=True, null=True)
#     amount = models.FloatField(default=0)
#     added_by = models.IntegerField(blank=False, null=False)
#     add_time = models.DateTimeField(blank=False, null=False, auto_now_add=True)
#     updated_by = models.IntegerField(blank=False, null=False)
#     update_time = models.DateTimeField(
#         blank=False, null=False, auto_now=True)