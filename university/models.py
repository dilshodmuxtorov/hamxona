from django.db import models

class UniversityModel(models.Model):
    CHOICES = [
        ("tashkent","Toshkent sh."),
        ("r-tashkent", "Toshkent v."),
        ("namangan", "Namangan"),
        ("fergana", "Farg'ona"), 
        ('andijan', "Andijon")
    ]
    name = models.CharField(max_length=255, default="")
    region = models.CharField(choices=CHOICES, max_length=65)
    longtitude = models.CharField(max_length=65, default="")
    lattitude = models.CharField(max_length=65, default="")
    phone_number = models.CharField(max_length=15, default="")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "university"
        verbose_name = "Universitet"
        verbose_name_plural = "Universitetlar"

class DormitoryModel(models.Model):
    name = models.CharField(max_length=255)
    university_id = models.ForeignKey(UniversityModel, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=0)


    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "dormitory"
        verbose_name = "Yotoqxona"
        verbose_name_plural = "Yotoqxonalar"


class RoomModel(models.Model):
    number = models.CharField(max_length=25)
    floor = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    dormitory_id = models.ForeignKey(DormitoryModel, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
