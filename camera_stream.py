import imagiz
import cv2

vid=cv2.VideoCapture(0)
client=imagiz.TCP_Client(server_port=9990,client_name="cc1")
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

if not vid.isOpened():
    print("Cannot open camera")
    exit()

while True:
  r,frame=vid.read()
  if r:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
    r,image=cv2.imencode('.jpg',gray, encode_param)
    response=client.send(image)

    


 
 