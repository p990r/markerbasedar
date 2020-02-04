'''
Marker Based Augmented Reality
Python software
p990r
'''

import camera

def main():
    print('begin')

    # press right and left arrow keys to switch between images
    # press esc to exit cam
    # input arguments for show_webcam (optional): mirror image, width, height
    camera.open_webcam(mirror=True)

if __name__ == '__main__':
    main()