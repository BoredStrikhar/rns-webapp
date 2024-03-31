from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import onnxruntime
import numpy as np
from PIL import Image
from django.conf import settings

imageClassList = {'0': 'Акустическая гитара', '1': 'Бас-гитара', '2': 'Электрогитара'}  #Сюда указать классы

def scoreImagePage(request):
    return render(request, 'scorepage.html')

def predictImage(request):
    fileObj = request.FILES.get('filePath')
    print("popka = ", request.FILES)
    fs = FileSystemStorage()
    filePathName = fs.save('images/'+fileObj.name,fileObj)
    filePathName = fs.url(filePathName)
    modelName = request.POST.get('modelName')
    scorePrediction = predictImageData(modelName, "C:\\Users\\pstri\\Desktop\\rns_dz1\\RNSDZONE\\RNSDZONE\\media\\images\\"+fileObj.name)
    context = {'scorePrediction': scorePrediction}
    return render(request, 'scorepage.html', context)

def predictImageData(modelName, filePath):
    img = Image.open(filePath).convert("RGB")
    print("huylusha =", Image)
    img = np.asarray(img.resize((32, 32), Image.ANTIALIAS))
    sess = onnxruntime.InferenceSession(r'C:\\Users\\pstri\\Desktop\\rns_dz1\\RNSDZONE\\RNSDZONE\\media\\models\\GUITARS_RESNET20.onnx') #<-Здесь требуется указать свой путь к модели
    outputOFModel = np.argmax(sess.run(None, {'input': np.asarray([img]).astype(np.float32)}))
    score = imageClassList[str(outputOFModel)]
    return score