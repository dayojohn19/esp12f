
class TextRecorder:
  
    def __init__(self, logPath='/',fpath='records.txt'):
        self.text = ' '
        self.path = logPath+fpath
        self.file_name=fpath
    def dynamic_import(file_name, class_name):
        with open(file_name, 'r') as f:
            code = f.read()
        exec(code)
        if class_name in globals():
            class_obj = globals()[class_name]
            return class_obj
        else:
            raise ValueError(f"Class {class_name} not found in {file_name}")  
    def add(self,text):
        print('Adding to record: ',text)
        self.text += '  '+text+'  '

    def save(self,clockstamp='000000',filepath=None):
        if filepath == None:
            filepath = self.path
        print("Recording save: ",filepath)
        with open(filepath, 'a') as file:
            file.write(self.text + clockstamp)
            file.write('\n')    

    def send(self):
        try:
            print('Trying to send...')
            messenger = self.dynamic_import('mpy/network_messenger.py', 'Sim')
            wmg = messenger.sendWhatsapp(message = self.text)
            self.add(wmg)
            del messenger
            gc.collect()
        except:
            self.add('Failed to connect to send record ')
        print("Recorded")
