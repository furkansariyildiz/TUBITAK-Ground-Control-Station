from django.http.response import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout,authenticate
from django.contrib import messages
from base import forms
from .models import Result, PhotoModel
from django.contrib.auth.decorators import login_required
from django.core.files import File
from team_imu import settings
import os, glob
from django.core.files.images import ImageFile
from pathlib import Path
import json
from django.views.decorators.csrf import csrf_exempt
import rospy
from std_msgs.msg import String, Float32MultiArray
from geometry_msgs.msg import Twist
from PIL import Image
from django.views.decorators.csrf import csrf_protect
import urllib.request
from django.http import HttpRequest
from digi.xbee.devices import XBeeDevice
import base.xbee_communication


def index(request):
    return render(request,template_name="index.html")


def register(request):
    form = forms.RegisterForm(request.POST or None)
    if(request.user.is_authenticated):
        messages.warning(request,message="Zaten giriş yaptınız.Kayıt olabilmek için önce çıkış yapmalısınız.")
        return redirect("index")
    if(form.is_valid()):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        try:   
            newUser = User(username = username)
            newUser.set_password(password)
            newUser.save()
            auth_login(request,newUser)#kayıt olan kişinin otomatik girilmesini sağlıyor
            messages.success(request,message="Başarıyla giriş yapıldı.")
            return redirect("index")#kayıt olduktan sonra anasayfaya dönüyor
        except:
            form_login = forms.LoginForm(request.POST or None)    
            messages.warning(request,message="Zaten böyle bir kullanıcı var.")
            context={
                "form":form_login,
            }
            return render(request,template_name="login.hmtl",context=context)
    context = {
        "form":form,
    }
    return render(request,template_name="register.html",context=context)
    #giriş kısmı
def loginUser(request):
    form = forms.LoginForm(request.POST or None)
    context = {
                "form":form,
            }
    if(request.user.is_authenticated):
        messages.warning(request,message="Zaten giriş yaptınız.")
        return redirect("index")

    if(form.is_valid()):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user=authenticate(request=request ,username = username , password = password)
        if(user==None):
            messages.info(request,message = "Kullanıcı Adı veya Parola hatalı")
            return render(request,template_name="login.html",context=context)
        messages.success(request,message="Başarıyla giriş yapıldı.")
        auth_login(request,user)
        return redirect("index")
    return render(request,template_name="login.html",context=context)


#kullanıcı çıkış paneli
@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    messages.success(request,message="Başarıyla çıkış yapıldı.")
    return redirect("index")

#sonuçların eklendiği form(forms.ModelForm)
@login_required(login_url="login")
def result(request):
    form = forms.ResultForm(request.POST or None,request.FILES or None)
    result_photo = get_object_or_404(PhotoModel,id=1)
    context = {
        "form":form,
        "result_photo":result_photo,
    }

   
    if(form.is_valid()):
        form.save()
        messages.success(request,message="Sonuçlar başarıyla kaydedildi.")
        return redirect("index")
    return render(request,template_name="result.html",context=context)

#sonuçların gösterildiği panel    
@login_required(login_url="login")
def board(request):
    results = Result.objects.all()
    #print(results)
    context = {
        "results":results,
    }
    return render(request,template_name="board.html",context=context)

    #her bir sonuca tıklandığında gösterilen panel
@login_required(login_url="login")
def detail(request,id):
    result = get_object_or_404(Result,id = id)
    context = {
        "result":result,
    }
    return render(request,template_name="detail.html",context=context)

    #sonuçların değiştirileceği panel
@login_required(login_url="login")
def update(request,id):
    result = get_object_or_404(Result,id = id)
    form = forms.ResultForm(request.POST or None , request.FILES or None , instance=result)
    if(form.is_valid()):
        form.save()
        messages.success(request,message="Sonuç başarılı bir şekilde güncellendi.")
        return redirect("index")
    context = {
        "form":form,
    }
    return render(request,template_name="update.html" ,context=context)

    #sonuçların silindiği panel
@login_required(login_url="login")    
def delete(request,id):
    result = get_object_or_404(Result, id = id)
    result.delete()
    messages.success(request,message="Sonuç başarıyla silindi.")
    return redirect("index")

def photos(request):
    photos_dir = os.path.join('media','media')
    photos_dir_html=[]
    for file in os.listdir(photos_dir):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jfif") or file.endswith(".jpeg"):
            photos_dir_html.append(file)
            
    
    context={
        "photos_dir_html":photos_dir_html,
    }        
    return render(request,template_name="photos.html",context=context)
    
def photos_use(request,id):
    result_photo = get_object_or_404(PhotoModel,id=id)
    context = {
        "form":result_photo,
    }
    
    
    return render(request,template_name="photos_use.html",context=context)



def add_photo(request,slug):
    #print(slug)
    form =  forms.ResultForm(request.POST or None,request.FILES or None)

    context = {
        "form":form,
        "slug":slug,
    }
    if(form.is_valid()):
        form.save()
        messages.success(request, message = "Sonuçlar başarıyla kaydedildi.")
        return redirect("/base/photos")
    
    return render(request, template_name="add_photo.html",context = context)
def delete_photo(request,slug):
    print("********************************")
    print(os.getcwd())
    pathforPhotos = os.path.join(os.getcwd(), 'media/media')
    slug = os.path.join(pathforPhotos,slug)
    print(slug)
    os.remove(slug)
    messages.success(request,message="Fotograf silindi.")
    return redirect('/base/photos/')

target_lat= []
target_lon = []


@csrf_protect
def maps(request):
    global target_lat, target_lon
    mapbox_access_token = 'pk.eyJ1IjoiZnVyY2FuZG90aGlzIiwiYSI6ImNrN3AxZjRsdjA1OXQzZ3E5ZzcycDd4MzIifQ.U7ScVmUzA60CsdEgj7ajNg'
    if(request.method == "POST"):
        
        target_latitude = request.POST.get("target_latitude","")
        target_longitude = request.POST.get("target_longitude","")
        checked_value = request.POST.get("checkbox_for_txt","")
        delete_button_value = request.POST.get("delete_txt","")
        ros_target_checkbox = request.POST.get("ros_target_gps","")
        move_command_checkbox = request.POST.get("move_command")
        control_input = request.POST.get("control_input", "")
        #print("Control input:" + str(control_input))
        #print("Move Value:" + str(move_command_checkbox))
        #print("BUTTON_DEGER:",button_value)
        #print("DEGER:",deger)
        if(target_latitude!= "" and target_longitude != "" and checked_value != "checked"):
            target_lat.append(target_latitude)
            target_lon.append(target_longitude)
        
        #print("Checked Value:" + str(checked_value))
        file_name = os.path.join(os.getcwd(),'base')
        file_name_uav = os.path.join(file_name,'UAV')
        file_name_uav = os.path.join(file_name_uav,'target_gps_boat.txt')

        if(checked_value == "checked"):
            count = 0
            #print("if icerisiii!!!!")
            msg_to_USV = String()
            with open(file_name_uav,'w+') as f:
                for target_lat_for_txt in target_lat:
                    f.write(str(target_lat_for_txt) + "," + str(target_lon[count])+ "\n")
                    count = count + 1
                    #print("Writed to txt file!")
                count = 0

            count = 0

            if move_command_checkbox == None:
                msg_to_USV.data = "Move:" + str(0)
            
            else:
                msg_to_USV.data = "Move:" + str(1)


            for target_lat_for_txt in target_lat:
                msg_to_USV.data = msg_to_USV.data + ";Target" + str(count) + ":" + str(target_lat_for_txt) + "," + str(target_lon[count])
                count = count + 1
            #print("XBEE msg:" + str(msg_to_USV.data))

            count = 0
            

            #print(msg_to_USV.data)    
            

        if(delete_button_value == "delete"):
            try:
                os.remove(file_name_uav)
                #print("target gps silindi.")
                target_lat = []
                target_lon = []
            except:
                pass
        #print("TARGET_LAT:", target_latitude, "TARGET_LONG:",target_longitude,"CHECK_BOX:",checked_value)
       

    drone_altitude = [1,2,3,4,5]
    drone_latitude = [1,2,3,4,5]
    drone_longitude = [1,2,3,4,5]
    drone_barheight = [1,2,3,4,5]
    drone_heading = [1,2,3,4,5]
    drone_battery = [100]
    drone_roll = [1]
    drone_pitch = [2]
    drone_yaw = [3]
    drone_speed_x = [10]
    drone_speed_y = [11]
    drone_speed_z = [12]
    selam = [1,2,3]

    file_name = os.path.join(os.getcwd(),'base')
    file_name_txt = os.path.join(file_name,'UAV')
    
   # print("###################", file_name_txt)
    for txt_element in os.listdir(file_name_txt):
        if(txt_element == "mission_1.txt"):
            txt_dizini = txt_element
    
    #print("GOREV TXT ELEMENT###############:",os.path.join(file_name_txt,txt_dizini))

    #print("#####FILES#######",os.listdir(file_name))
    txt_dizini = os.path.join(file_name_txt, txt_dizini)
    gorev_x = []
    gorev_y = []

    with open(txt_dizini, 'r') as f_mission:
        data = f_mission.read().splitlines(True)
        for satir in data:
            gorev_x.append(satir.split(",")[0])
            gorev_y.append(satir.split(",")[1])
        

        
    
    txt_files = []
    for file in os.listdir(file_name_txt):
        if(file.endswith(".txt")):
            txt_files.append(file)

    #print("###FILE NAME TXT",file_name_txt)
    for element in txt_files:
        if(element=="incoming_messages.txt"):
            full_adress_txt_file_messages = element
            #print("FULL ADRESS TXT FILE",full_adress_txt_file_messages)
            #print("full adress file",file_name_txt)
    
    full_adress_txt_file_messages = os.path.join(file_name_txt,full_adress_txt_file_messages)
    os.remove(full_adress_txt_file_messages)

    with open(os.path.join(file_name_txt,"incoming_messages.txt"), "w+"):
        print("açıldı")
                      

    json_file = []
    for file in os.listdir(file_name):
        if(file.endswith(".json")):
            json_file.append(file)

    
    for element in json_file:
        if(element == "drone_konum_bilgisi.json"):
            full_adress_json_file_drone = element
            
    full_adress_json_file_drone = os.path.join(file_name,full_adress_json_file_drone) 
    drone_konum_features = []
    
    with open(full_adress_json_file_drone,'r') as f:
        data  = json.load(f)
        
        for key,value in data.items():
            if(key=="features"):
                drone_konum_features = value

        dic = drone_konum_features[0]
        dic = dic["geometry"]
        drone_konum_bilgisi = dic["coordinates"]

    for element in json_file:
        if(element == "SUAS2019.json"):
            full_adress_json_file_0 = element
    full_adress_json_file_0 = os.path.join(file_name,full_adress_json_file_0)    
    with open(full_adress_json_file_0,'r') as f:
        data  = json.load(f)
        
        for key,value in data.items():
            if(key=="searchGridPoints"):
                lat_and_long = value
        lats = []
        longs = []
        for dic in lat_and_long:
            lats.append(dic["latitude"])
            longs.append(dic["longitude"])
    for element in json_file:
        if(element == "SUAS2020.json"):
            full_adress_json_file_1 = element
    full_adres_json_file_1 = os.path.join(file_name,full_adress_json_file_1)
    with open(full_adres_json_file_1,'r') as f:
        data = json.load(f)

        for key,value in data.items():
            if(key=="flyZones"):
                flyzone = value


        lats_engel = []
        longs_engel = []
        
        flyzones = flyzone[0]
        boundaryPoints = flyzones['boundaryPoints']
        for dic in boundaryPoints:
            for key,value in dic.items():
                if(key=='latitude'):
                    lats_engel.append(value)
                elif(key=='longitude'):
                    longs_engel.append(value)
      
    context = {
        'mapbox_access_token':mapbox_access_token,
        'lats':lats,
        'longs':longs,
        'lats_engel':lats_engel,
        'longs_engel':longs_engel,
        'drone_altitude':drone_altitude,
        'drone_latitude':drone_latitude,
        'drone_longitude':drone_longitude,
        'drone_barheight':drone_barheight,
        'drone_heading':drone_heading,
        'drone_battery':drone_battery,
        'drone_roll':drone_roll,
        'drone_pitch':drone_pitch,
        'drone_yaw':drone_yaw,
        'drone_speed_x':drone_speed_x,
        'drone_speed_y':drone_speed_y,
        'drone_speed_z':drone_speed_z,
        'drone_konum_bilgisi':drone_konum_bilgisi,
        'gorev_x':gorev_x,
        'gorev_y':gorev_y,
    }  
    return render(request,template_name="maps.html",context=context)



#Duzenlemeye buradan basla


image_path_bool = False
image_count = 1

def ImagesPaths(request):
    global image_path_bool
    global image_count
    file_name = os.path.join(os.getcwd(), 'static/images')

    images = ""
  
    for files in os.listdir(file_name):
        if (files.endswith(".jpg") or files.endswith(".png") or files.endswith(".jpeg")) and 1:
            #print(files)
            images = images + str(files) + ";"
            
    big_pictures = []

    image_paths = images.split(";")
    for i in image_paths:
        if i != '':
            images_for_size = Image.open(str(os.path.join(file_name, i)))
            width, height = images_for_size.size
            if width > 450 or height > 450:
                image_path_bool = False
                big_pictures.append(i)
                

    if image_path_bool == False:
        for i in big_pictures:
            if i != '':
                image = Image.open(str(os.path.join(file_name, i)))
                #print(image)
                image = image.resize((450,450), Image.ANTIALIAS)
                image.save(os.path.join(file_name, i))
                image.close()
                #print(os.path.join(file_name, i))
        image_path_bool = True

    if images != "":
        context = {
            "images": images
        }
            
    else:
        images = ""        
        context = {
            "images": images
        }
    return render(request, template_name = "image_paths.html", context = context)



@csrf_protect
def Control(request):
    return render(request, template_name="control.html")



class GoogleMaps():
    def __init__(self):
        self.api_key = "AIzaSyCfG65vyHheGcuhFyhOUpg6Jf7Ha14m6Ps"
 
    def map(self, request):
        context = {
            "api_key": self.api_key,
        }
        #self.prepareXBEE()
        return render(request = request, template_name = "googlemaps.html", context = context)

googlemaps = GoogleMaps()





