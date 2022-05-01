String.prototype.turkishToLower = function () {
    var string = this;
    var letters = { "İ": "i", "I": "ı", "Ş": "ş", "Ğ": "ğ", "Ü": "ü", "Ö": "ö", "Ç": "ç" };
    string = string.replace(/(([İIŞĞÜÇÖ]))/g, function (letter) { return letters[letter]; })
    return string.toLowerCase();
}

function ExampleViewModel() {

    var self = this;

    self.ExampleData = ko.observableArray([]);
    self.startOp = ko.observable(false);
    self.update = function () {
        $.ajax("/Dashboards/ActiveDevice/", {
            type: "POST",
            dataType: 'json',
            cache: false,
            success: function (allData) {
                
                if (allData == "hasnoresult") document.location.href = "/";
                var mappeddata = $.map(allData, function (item) {
                    return new DataItem(item)
                });
                $.each(mappeddata, function (idx, item) {

                    var foundedIndex = -1;
                    for (var i = 0; i < self.ExampleData().length; i++) {
                        if (self.ExampleData()[i].id() == item.id()) {
                            foundedIndex = i;
                            break;
                        }
                    }

                    if (foundedIndex >= 0) {
                        
                        var device_type = item.device_type();
                        var device_name = item.device_name();
                        var device_code = item.device_code();
                        var device_last_status = item.device_last_status();
                        var device_ip = item.device_ip();
                   
                        var objKoArray = self.ExampleData()[foundedIndex];
                        objKoArray.device_name(device_name);
                        objKoArray.device_type(device_type);
                        objKoArray.device_code(device_code);
                        objKoArray.device_last_status(device_last_status);                      
                        objKoArray.device_ip(device_ip);                       
                        
                    } else {
                        self.ExampleData.push(item);
                    }
                });

                $.each(self.ExampleData(), function (idx, item) {

                    try {
                        var originalIndex = -1;
                        for (var i = 0; i < mappeddata.length; i++) {
                            if (mappeddata[i].id() == item.id()) {
                                originalIndex = i;
                                break;
                            }
                        }

                        if (originalIndex < 0) {
                            self.ExampleData.remove(self.ExampleData()[idx]);
                        }
                    } catch (e) {
                        console.log(e);
                        console.log(item);
                    }
                });

                self.startOp(true);
            },
            fail: function () {
                console.log("hata");
            }
        });
    }
}



function DataItem(data) {
 
    this.id = ko.observable(data.device_id);
    this.device_type = ko.observable(data.device_type);
    this.device_name = ko.observable(data.device_name);
    this.device_code = ko.observable(data.device_code);
    this.device_last_status = ko.observable(data.device_last_status);
    this.device_ip = ko.observable(data.device_ip);
}

KnockoutElse.init([spec = {}])

var exampleViewModel = new ExampleViewModel();
window.setInterval(exampleViewModel.update, 5000);
ko.applyBindings(exampleViewModel);
window.onload = exampleViewModel.update;
