# TUBITAK Ground Control Station Software

Çalıştırmak için "manage.py" Python dosyasının bulunduğu dosya dizine terminal ile gidip "python manage.py runserver" veya "python3 manage.py runserver" komutu girilmelidir.

ROSBridge paketi ile çalıştığı için bu paketin kurulması -Ubuntu 16.04 ve daha üst versiyonlar ya da Windows içerisinde Ubuntu kurulumu ile gerçekleşebilir- gerekmektedir. "roscore" başladıktan sonra ayrı bir terminale "roslaunch rosbridge_server rosbridge_websocket.launch" komutu girilerek ROSBridge paketi ayağa kaldırılır. 

Kameradan gelecek olan görüntünün arayüze aktarılması için de mjpeg_server paketi sistemde kurulu olmalıdır. Paket kurulduktan ve "source devel/setup.bash" işlemi yapıldıktan sonra "rosrun mjpeg_server mjpeg_server _port:=8181" komutu terminale girilerek 8181 portundan fotoğraf aktarma işlemi de gerçekleşmiş olur. 

Tarayıcıdan -Google Chrome veya Opera önerilir- localhost:8000/base/map/googlemaps adresini girerek kontrol istasyonuna ulaşabilirsiniz.

Kurulum için yardımcı olabilecek bağlantılar;

http://wiki.ros.org/ROS/Installation
https://docs.djangoproject.com/en/4.0/topics/install/
http://wiki.ros.org/mjpeg_server
http://wiki.ros.org/rosbridge_server

