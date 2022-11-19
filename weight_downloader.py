import os

# import shutil

def download_weight():


    isFound=os.path.isfile("./YOLOv4/backup/yolov4-custom_best.weights")

    if not isFound:
        print("----------Downloading...----------")
        os.system('wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "https://docs.google.com/uc?export=download&id=1K0kaVCRTNRDaYdnRaX9MUGu4OZf3G1cv" -O- | sed -rn "s/.*confirm=([0-9A-Za-z_]+).*/\1\n/p")&id=1K0kaVCRTNRDaYdnRaX9MUGu4OZf3G1cv" -O yolov4-custom_best.weights && rm -rf /tmp/cookies.txt')
        print("----------Download Completed----------")
        # shutil.move('./yolov4-custom_best.weights', './YOLOv4/backup/')
        os.system('mkdir ./YOLOv4/backup/')
        os.system('mv ./yolov4-custom_best.weights ./YOLOv4/backup/')
        print("----------Moved to backup----------")
    else:print("-------------------File Found-------------------")