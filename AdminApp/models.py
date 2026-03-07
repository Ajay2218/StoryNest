from django.db import models

# Create your models here.

class CategoryDb(models.Model):
    Category_name = models.CharField(max_length=50,null=True,blank=True)
    Description = models.CharField(max_length=50,null=True,blank=True)
    Category_images = models.ImageField(upload_to="category images",null=True,blank=True)

class ProductDb(models.Model):
    CategoryName = models.CharField(max_length=50,null=True,blank=True)
    Product_Name = models.CharField(max_length=50,null=True,blank=True)
    Author_Name = models.CharField(max_length=50,null=True,blank=True)
    Price = models.IntegerField(null=True,blank=True)
    Overview = models.TextField(null=True,blank=True)
    Product_img = models.ImageField(upload_to="Product Images",null=True,blank=True)