import cv2
import matplotlib.pyplot as plt

def render(file):    
    img = cv2.imread(file)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.show()


render("image.ppm")

