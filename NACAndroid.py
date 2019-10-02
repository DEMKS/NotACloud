from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
lable = Label()
class NotAKivy(App):
    def build(self):
        #return Button("NotATest")
        print("Building")
        self.Button = Button("NotAHelloWorld")

if __name__ == '__main__':
    app = NotAKivy()
    app.run()