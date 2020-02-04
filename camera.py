import cv2
from graphics import get_img, resize_image, get_files, main_search

# All 6 methods of comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

def open_webcam(mirror=False, width=640, height=480):
    cam = cv2.VideoCapture(0)
    cam.set(3, width)
    cam.set(4, height)

    conf_int = 0.7

    # Get marker
    marker_path = 'marker.jpeg'
    marker_percentage_range = (20,100)
    marker = get_img(marker_path)
    marker = cv2.cvtColor(marker, cv2.COLOR_BGR2GRAY)
    markers = []
    for percentage in range(marker_percentage_range[0], marker_percentage_range[1] + 1, 10):
        markers.append(resize_image(marker, percentage))

    # Get posters
    posters_folder = 'images'
    posters_paths = get_files(posters_folder)
    posters = []
    for i in range(0,len(posters_paths)):
        file = get_img(posters_paths[i])
        if file is not None:
            posters.append(file)

    index = 0 # Current poster index

    while True:
        # Capture frame-by-frame
        ret, img = cam.read()

        if mirror:
            img = cv2.flip(img, 1)

        main_search(img, markers, posters[index], methods[1], conf_int)

        cv2.imshow('Camera', img)
        key = cv2.waitKey(1)
        if(key != -1): # -1 means no key input
            if key == 83:
                index = (index + 1) % len(posters) # right arrow to increase index
            if key == 81:
                index = (index - 1) % len(posters) # left arrow to decrease index
            if key == 27:
                break  # esc to quit

    cam.release()
    cv2.destroyAllWindows()
