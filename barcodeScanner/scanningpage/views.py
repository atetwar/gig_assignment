from django.http import request
import cv2
from django.shortcuts import render
from .forms import UploadImage


import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

# Create your views here.
def scan_barcode(request):
    form = UploadImage(request.POST, request.FILES)
    qr_data = None
    if form and form.is_valid():
        qr_data = handleQRCode(request.FILES)
    formdata = {'form':form,'qr_data':qr_data}
    return render(request,"Scan.html",formdata)


def handleQRCode(f):
    data = f['file']
    path = default_storage.save('ab.png', ContentFile(data.read()))
    tmp_file = os.path.join(path)

    d = cv2.QRCodeDetector()
    val, points, straight_qrcode = d.detectAndDecode(cv2.imread(tmp_file))
    return val