from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import cv2
import stop_sign_detector_medium
import os
from pathlib import Path
from PIL import Image
from urllib.request import Request, urlopen
import numpy as np

# Create your views here.

def index(request):
    context={'a':1}
    return render(request,'index.html',context)

def _grab_image(path=None, stream=None, url=None):
	# if the path is not None, then load the image from disk
	if path is not None:
		image = cv2.imread(path)
	# otherwise, the image does not reside on disk
	else:	
		# if the URL is not None, then download the image
		if url is not None:
			req = Request(url, headers={'User-Agent': 'Chrome'})
			data = urlopen(req).read()
			#resp = urllib.request.urlopen(url)
			#data = resp.read()
		# if the stream is not None, then the image has been uploaded
		elif stream is not None:
			data = stream.read()
		# convert the image to a NumPy array and then read it into
		# OpenCV format
		image = np.asarray(bytearray(data), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)




def predictImage(request):
    if request.method=="POST":

        check= request.FILES.get('filePath', None) 

        print("PRINTING",check)
        if check is not None:
            print('ppop')
            fileObj=request.FILES['filePath']
            fs=FileSystemStorage()
            filePathName=fs.save(fileObj.name,fileObj)
            filePathName=fs.url(filePathName)
            image_test='.'+filePathName
            img=cv2.imread(image_test)


        else:
            print('wtf')
            url=request.POST.get("url",None)
            req = Request(url, headers={'User-Agent': 'Chrome'})
            data = urlopen(req).read()
            image = np.asarray(bytearray(data), dtype="uint8")
            img = cv2.imdecode(image, cv2.IMREAD_COLOR)
    
    
    detector=stop_sign_detector_medium.StopSignDetector()
    rects=detector.get_bounding_box(img)

    for x,y,a,b in rects:
        cv2.rectangle(img,(x,y),(a,b),(0,255,0),2)

    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    print(os.path.join(BASE_DIR,'media'))
    path= str(os.path.join(BASE_DIR,'media'))+r'\test_img.jpg'
    

    img1=Image.fromarray(img)
    print('y you no save')
    img1.save(path)


    path1="/media/test_img.jpg" #for displaying the result
    
    context={"num_signs":len(rects), "Signs_coord": rects, 
             "new_path": path1}
    

 


    

    return render(request,'index.html',context)