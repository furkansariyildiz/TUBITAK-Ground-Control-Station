from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.files.images import ImageFile




# Create your models here.
IMAGE_TYPES = (("STANDARD","STANDARD"),("EMERGENT","EMERGENT"))
IMAGE_PROCESS =(("A", "AUTONOMOUS"), ("M", "MANUEL"))
ORIENTATIONS = (("N", "N"),
                ("W", "W"),
                ("E", "E"),
                ("S", "S"),
                ("NE", "NE"),
                ("SE", "SE"),
                ("SW", "SW"),
                ("NW", "NW"))
SHAPES = (("NONE", "NONE"), ("CIRCLE", "CIRCLE"), ("SEMICIRCLE", "SEMICIRCLE"), ("QUARTER_CIRCLE", "QUARTER_CIRCLE"), ("TRIANGE", "TRIANGLE"), ("SQUARE", "SQUARE"), ("RECTANGLE", "RECTANGLE"), ("TRAPEZOID", "TRAPEZOID"),
          ("PENTAGON", "PENTAGON"), ("HEXAGON", "HEXAGON"), ("HEPTAGON", "HEPTAGON"), ("OCTAGON", "OCTAGON"), ("STAR", "STAR"), ("CROSS", "CROSS"))
COLORS = (("WHITE", "WHITE"), ("BLACK", "BLACK"), ("RED", "RED"), ("YELLOW", "YELLOW"), ("GRAY", "GRAY"), ("GREEN", "GREEN"), ("PURPLE", "PURPLE"),
          ("BROWN", "BROWN"), ("BLUE", "BLUE"), ("ORANGE", "ORANGE"))

def images():
        path='/media/media/01.png'
        return path
#buradaki modeller ve demet tanımları verilen parametrelere göre yapılmıştır.
class Teams(models.Model):
    id = models.IntegerField(primary_key=True,verbose_name="Team ID")
    username = models.CharField(max_length=50,verbose_name="Username")
    name = models.CharField(max_length=50,verbose_name="Team Username")
    university = models.CharField(max_length=50,verbose_name="Unıversity Name")
    InAir = models.BooleanField()
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name = "Longitude")
    altitude = models.FloatField(verbose_name = "Altitude")
    heading = models.FloatField(verbose_name = "Heading")
    telemetry_id = models.IntegerField(verbose_name="Telemetry ID")
    telemetry_age_sec = models.FloatField()
    telemetry_time_stamp = models.CharField(max_length=50)
class Telemetry(models.Model):
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name = "Longitude")
    altitude = models.FloatField(verbose_name = "Altitude")
    heading = models.FloatField(verbose_name = "Heading")
class Result(models.Model):
    img_name = models.CharField(max_length=50,verbose_name="IMAGE NAME")
    img_type = models.CharField(max_length=15,choices=IMAGE_TYPES)
    shape = models.CharField(max_length=20,choices=SHAPES)
    shape_color = models.CharField(max_length=15,choices=COLORS)
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")
    orientation = models.CharField(max_length=2,choices=ORIENTATIONS)
    alphanumeric = models.CharField(max_length=2)
    alphanumeric_color = models.CharField(max_length=20,choices=COLORS)
    is_autonom = models.CharField(max_length=50,choices=IMAGE_PROCESS)
    description = models.CharField(max_length=225,blank=True,verbose_name="Açıklama")
    file = models.ImageField(upload_to='result',blank=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    objects = models.Manager()
    

    def getImg(self):
        if  (not self.file):
            return self.file
        return True
    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'
    
        
class PhotoModel(models.Model):
    description = models.CharField(max_length=225,blank=True,verbose_name="Açıklama")
    file = models.ImageField(upload_to='media',blank=True,null=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    objects = models.Manager()
    
    



# Create your models here.

    