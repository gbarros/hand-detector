import cv2


def cut(img, size=50):
    heigth = int((len(img) - size) / 2)
    width = int((len(img[0]) - size) / 2)
    return img[heigth: heigth + size, width: width + size]


def save(filee, name):
    cv2.imwrite("generated/" + name, filee)


list_files = open("images.txt").readlines()

for i in range(len(list_files)):
    list_files[i] = list_files[i].strip()
    save(cut(cv2.imread(list_files[i])), list_files[i])
