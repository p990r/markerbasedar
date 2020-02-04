import cv2
import os

def get_shape(input):
    shape = input.shape
    return shape[0:2]

def get_img(path):
    try:
        image = cv2.imread(path)
    except:
        print('Warning: ' + path + ' cannot be added to posters')
        return None
    return image

def get_files(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    return files

def resize_image(img, percentage):
    height, width = get_shape(img)
    dim = (int(width * percentage / 100), int(height * percentage / 100))
    image = cv2.resize(img, dim)
    return image

def main_search(img, markers, poster, method, conf_int):
    found = False
    for marker in markers:
        top_left, bot_right, max_val, res = search_marker(img, marker, method)
        if(max_val > conf_int):
            found = True
            poster = resize_poster(poster, top_left, bot_right)
            put_poster(img, poster, top_left, bot_right)
            return found, top_left, bot_right
    if(len(markers) == 0):
        print('Error: No marker used in main_search')
        return False, (0,0), (1,1)
    return found, top_left, bot_right

def search_marker(img, template, method, res_bool=False):
    height, width = get_shape(template)
    match_method = eval(method)
    # Apply marker Matching
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    try:
        res = cv2.matchTemplate(gray, template, match_method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + height, top_left[1] + width)
        if res_bool:
            return [top_left, bottom_right, max_val, res]
        return [top_left, bottom_right, max_val, None]
    except:
        print("Error: Check template input.")
        return [(0, 0), (1, 1), 0, None]

def resize_poster(poster, top_left, bot_right):
    height, width = get_shape(poster)
    if (width < height):
        percentage = 100 * (bot_right[0] - top_left[0]) / width
    else:
        percentage = 100 * (bot_right[1] - top_left[1]) / height
    return resize_image(poster, percentage)

def put_poster(img, poster, top_left, bot_right):
    imgHeight, imgWidth = get_shape(img)
    posterHeight, posterWidth = get_shape(poster)

    markerWidth = bot_right[0] - top_left[0]
    markerHeight = bot_right[1] - top_left[1]

    if(posterWidth > posterHeight):
        diff = posterWidth - markerWidth
        yStart, yEnd, xStart, xEnd = set_coords(1, top_left, bot_right, imgHeight, imgWidth, diff)
    else:
        diff = posterHeight - markerHeight
        xStart, xEnd, yStart, yEnd = set_coords(0, top_left, bot_right, imgWidth, imgHeight, diff)

    yStart, yEnd = pixel_diff(yStart, yEnd, posterHeight)
    xStart, xEnd = pixel_diff(xStart, xEnd, posterWidth)

    try:
        img[yStart:yEnd, xStart:xEnd] = poster
    except:
        print("Error: Poster doesn't fit in frame.")

def set_coords(index, top_left, bot_right, dim1, dim2, diff):
    j = (index + 1) % 2
    c1 = max([top_left[index], 0])
    c2 = min([bot_right[index], dim1])
    c3 = max([top_left[j] - diff // 2, 0])
    c4 = min([bot_right[j] + diff // 2, dim2])
    return c1, c2, c3, c4

def pixel_diff(start, end, size):
    diff = size + start - end
    if (diff != 0):
        if (start - diff < 0):
            end = end + diff
        else:
            start = start - diff
    return start, end
