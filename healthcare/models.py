from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Ugonjwa(models.Model):
    patient_name=models.CharField(max_length=100)
    ugonjwa_desc=models.TextField()

class Typhoid(models.Model):
    disease_name=models.CharField(max_length=100)
    disease_symptoms=models.TextField()
    typhoi= models.CharField(max_length=100, null=True)
   
    def __str__(self):
        return self.disease_name

class TyphoidPhoto(models.Model):
    typhoid=models.ForeignKey(Typhoid, related_name='photo', on_delete=models.CASCADE)
    photo=models.ImageField(upload_to='symptoms/Typhoid')

    def __str__(self):
         return f"Photo for {self.typhoid.disease_name}"
    


class Illness(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Sign(models.Model):
    illness = models.ForeignKey(Illness, related_name="images", on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='illness_images/')

    def __str__(self):
        return f"Image {self.id}"

class Merchandise(models.Model):
    name=models.CharField(max_length=30)
    details=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name

class Image(models.Model):
    sample=models.ForeignKey(Merchandise, related_name='sample', on_delete=models.CASCADE)
    image=models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image {self.id}"