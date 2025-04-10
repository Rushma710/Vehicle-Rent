from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Category model
class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


# Vehicles model
class Vehicles(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6, decimal_places=2
    )  # Adjusted decimal places
    image = models.ImageField(upload_to="rental_img")

    def __str__(self):
        return self.title


# Contact model
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name}"


# Add model (for additional vehicle details)

class Add(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    vname = models.CharField(max_length=100)
    description = models.TextField()
    isdelete=models.BooleanField(default=False)
    image = models.ImageField(upload_to='rental_images/')

    def __str__(self):
        return self.name

    # Image validation
    def clean(self):
        super().clean()
        if self.image:
            # Checking file type
            valid_image_extensions = ["jpg", "jpeg", "png"]
            file_extension = self.image.name.split(".")[-1].lower()
            if file_extension not in valid_image_extensions:
                raise ValidationError("Only JPG, JPEG, and PNG images are allowed.")
            if self.image.size > 5 * 1024 * 1024:  # 5MB in bytes
                raise ValidationError("Image file size should not exceed 5MB.")
# PAYMENT MODal

class Payment(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pickup_date = models.DateField()
    dropoff_date = models.DateField()

    def __str__(self):
        return f"Payment by {self.full_name}"
    
class Review(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.PositiveIntegerField(choices=[(1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')])
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.rating} stars)"
class Rider(models.Model):
    full_name = models.CharField(max_length=200)
    address = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    time = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return self.full_name
