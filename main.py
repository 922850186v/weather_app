import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.get_weather_button.setDefault(True)
        self.temparature_lable = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.setFixedSize(400, 600)
        self.initUI()
        
        
    def initUI(self):
        self.setWindowTitle("Weather App")
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temparature_lable)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)
        
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temparature_lable.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temparature_lable.setObjectName("temparature_lable")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        
        self.setStyleSheet(
            """
            QLabel, QPushButton{
                font-family: calibri;
            }
            
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            
            QLineEdit#city_input{
                font-size: 30px;
                text-transform: uppercase;
            }
            
            QPushButton#get_weather_button{
                font-size: 30px;
            }
            
            QLabel#temparature_lable{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 50px;
            }
            """
        )

        self.get_weather_button.clicked.connect(self.get_weather)
        
        
    def get_weather(self):
        api_key = "2a8f50f21a4a6ea5ddbe12dca82b518e"
        city = self.city_input.text()
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print()
            if data['cod'] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 404:
                    self.display_error("Bad Request \nCity Not Found!")
                case 401:
                    self.display_error("Client Error \nInvalid API Key")
                case 403:
                    self.display_error("Unauthorized \nAPI Key is not Authorized")
                case 500:
                    self.display_error("Server Error \nInternel Server Error")
                case _:
                    self.display_error(f"Http Error : {http_error}")
                    
        except requests.exceptions.ConnectionError:
            self.display_error("Internet connection is disabled")
        
        except requests.exceptions.Timeout:
            self.display_error("Request is timed-out")
        
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects")
        
        except requests.exceptions.RequestException:
            pass

    
    def display_weather(self, data):
        temparature_c = int(data['main']['temp']) - 273.15
        description = data['weather'][0]['description']
        weather_id = data['weather'][0]['id']          
        self.temparature_lable.setText(f"{temparature_c:.1f}°c")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(f"{description}")
        
    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
               return "⛈️"      
        elif 300 <= weather_id <= 321:
               return "🌦️"      
        elif 500 <= weather_id <= 531:
               return "🌧️"      
        elif 600 <= weather_id <= 622:
               return "❄️"      
        elif 701 <= weather_id <= 741:
               return "🌁"      
        elif weather_id == 762:
               return "🌋"      
        elif weather_id == 771:
               return "💨"      
        elif weather_id == 781:
               return "🌪️"      
        elif weather_id == 800:
               return "☀️" 
        elif 801 <= weather_id <= 804:
            return "☁️"     
        else:
            return "⛵" 
           
             
    
    def display_error(self, message):
        self.temparature_lable.setStyleSheet("font-size: 30px;")
        self.temparature_lable.setText(message)
        self.emoji_label.clear()
        self.temparature_lable.clear()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())