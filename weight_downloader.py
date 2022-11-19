import os

def download_weight():
    FILE_LIST = os.listdir("./YOLOv4/backup")
    
    if not "yolov4-custom_best.weights" in FILE_LIST:
        print("Downloading...")
        os.system('wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "https://docs.google.com/uc?export=download&id=1K0kaVCRTNRDaYdnRaX9MUGu4OZf3G1cv" -O- | sed -rn "s/.*confirm=([0-9A-Za-z_]+).*/\1\n/p")&id=1K0kaVCRTNRDaYdnRaX9MUGu4OZf3G1cv" -O yolov4-custom_best.weights && rm -rf /tmp/cookies.txt')
        print("Download Completed")
        os.system('mv ./yolov4-custom_best.weights ./YOLOv4/backup/')
        print("Moved to backup")