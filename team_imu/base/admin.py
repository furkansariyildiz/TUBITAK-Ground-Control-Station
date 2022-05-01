from django.contrib import admin
from .models import Teams,Telemetry,Result, PhotoModel
# Register your models here.
#database için admin panelinde gösterildi. Ayriyeten localhost/admin ile de erişim sağlanabilir.
@admin.register(Teams)
class AdminTeams(admin.ModelAdmin):
    list_display= ["id","username","name","university","university","InAir","latitude","longitude","altitude","heading","telemetry_id",
    "telemetry_age_sec","telemetry_time_stamp",
    ]
    class Meta:
        model = Teams

@admin.register(Telemetry)
class AdminTelemetry(admin.ModelAdmin):
    list_display=["latitude","longitude","altitude","heading",
    ]
    class Meta:
        model = Telemetry



@admin.register(Result)
class AdminResult(admin.ModelAdmin):
    list_display = ["img_name","img_type","shape","shape_color","latitude","longitude","orientation","alphanumeric","alphanumeric_color",
    "is_autonom",'file','description','uploaded_at'
    ]
    class Meta:
        model = Result

 
@admin.register(PhotoModel)
class AdminPhoto(admin.ModelAdmin):
    list_display = ['file','description','uploaded_at'
    ]
    class Meta:
        model = PhotoModel