from django.shortcuts import render
from PIL import Image

# Create your views here.
def form(request):
    """render the form html."""
    return render(request, 'form.html')


def g_data(data):
    """formating to binary."""
    a = []
    for b in data:
        a.append(format(ord(b), '08b'))
    return a


def modpix(pix, data):
    datalist = g_data(data)
    length_data = len(datalist)
    img = iter(pix)

    for i in range(length_data):
        pix = [value for value in img.__next__()[:3] + img.__next__()
               [:3] + img.__next__()[:3]]
        for j in range(0, 8):
            if datalist[i][j] == '0' and pix[j] % 2 != 0:
                pix[j] -= 1
            elif datalist[i][j] == '1' and pix[j] % 2 == 0:
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # 01101011
                # [256, 255, 255, 254, 255, 254, 255, 255, 255]
        if i == length_data - 1:
            if (pix[-1] % 2 == 0):
                if pix[-1] != 0:
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encrypt():
    pic = Image.open("wall.png")
    file = pic.copy()
    w = file.size[0]  # = 1600
    (x, y) = (0, 0)

    for pixel in modpix(file.getdata(), "hello world"):
        file.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1
    file.save("sample.png")


def decrypt():
    pic = Image.open("sample.png")
    img = iter(pic.getdata())
    data = ''
    while True:
        pix = [value for value in img.__next__()[:3] + img.__next__()
               [:3] + img.__next__()[:3]]

        bin_tana = ''
        for i in pix[:8]:
            bin_tana += str(i % 2)

        data += chr(int(bin_tana, 2))
        if (pix[-1] % 2 != 0):
            return data


def start(isEncrypt=True):
    if isEncrypt:
        encrypt()
    else:
        print(decrypt())


if __name__ == "__main__":
    start(True)
