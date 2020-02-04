from pynput import keyboard
class Key:
    def __init__(self):
        self.key = None
        self.Keys = [keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, 
                     keyboard.Key.right, keyboard.Key.esc]
        
    def on_press(self, key):
        self.key = key
        
    def on_release(self, key):
        if key in self.Keys: return False
        #returning False from here stops listener.
       
    def listen(self):
        #collect events until released
        with keyboard.Listener( on_press = self.on_press, 
                                on_release = self.on_release) as listener:
            listener.join()
