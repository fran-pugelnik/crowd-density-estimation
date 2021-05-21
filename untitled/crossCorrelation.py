import cv2
import numpy as np
import os


'''
    Definicija funkcija
'''

# razdvajanje početne matrice na segmente veličine danog predloška. Povratna vrijednost će biti matrica matrica
# npr. slika 1024x1024 sa predloškom 64x64 će vratiti matricu sa 16x16 elemenata od kojih svaki ima 64x64 vrijednosti.
def split_function(matrix, x_dimension, y_dimension, template_dimension):
    result_list = []
    for y in range(0, y_dimension, template_dimension):
        for x in range(0, x_dimension, template_dimension):
            result_list.append(matrix[x : x + template_dimension, y : y + template_dimension])
    # print(len(result_list))
    return result_list

# vraća maksimum za svaki segment dane matrice
def element_sum(matrix):
    temp = []
    for item in matrix:
        temp.append(np.max(item))
    # print(len(temp), temp)
    return temp

# fn. bira maksimalnu vrijednost za svaki segment danih matrica i vraća jednu maricu maksimalnih vrijednosti
def max_per_segment(sums):
    max_list = []
    for segment in range(len(sums[0])):
        max = 0
        template = int()
        for item in range(len(sums)):
            if sums[item][segment] > max:
                max = sums[item][segment]
                template = item
        max_list.append(template)
    # print(len(max_list), max_list)
    return max_list

# obavlja sumu segmenata i vraća ukupnu procjenu
def overall_segment_sum(segment_maximums):
    global templates_per_category
    global segment_quantity
    sum = 0
    for element in segment_maximums:
        sum += segment_quantity.get(element//templates_per_category)
    return sum



'''
    Glavni kod
'''



segment_quantity = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
templates_per_category = 5
template_string = 'template_'   #potrebno je predati .png format datoteke
image_path = os.path.join(os.environ.get('HOMEPATH'), 'Desktop', '1024x1024', 'minsk_drone', 'crowd00.png')
template_path = os.path.join(os.environ.get('HOMEPATH'), 'Desktop', '1024x1024', 'minsk_drone', 'template128x128')



img0 = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
# img0 = cv2.copyMakeBorder(img0, 0, 63, 0, 63, cv2.BORDER_REPLICATE)
# cv2.imshow('label 1', img0)
print(img0.shape)

# img1 = cv2.imread(os.path.join(path, 'road_template.png'), cv2.IMREAD_GRAYSCALE)
# img2 = cv2.imread(r"road_template1.png", cv2.IMREAD_GRAYSCALE)
# img3 = cv2.imread(r"road_template2.png", cv2.IMREAD_GRAYSCALE)


sum_list = []

for i in range(0, 25):
    if i == 0:
        tmp = template_string + str(i) + '.png'
        img1 = cv2.imread(os.path.join(template_path, tmp), cv2.IMREAD_GRAYSCALE)
        # print(img1)
    else:
        tmp = template_string + str(i) + '.png'
        img1 = cv2.imread(os.path.join(template_path, tmp), cv2.IMREAD_GRAYSCALE)
        # print(img1)
    template1 = cv2.matchTemplate(img0, img1, cv2.TM_CCORR_NORMED)
    result_list1 = split_function(template1, template1.shape[1], template1.shape[0], img1.shape[0])
    sum_list.append(element_sum(result_list1))

main_dimensions = img0.shape
template_dimensions = img1.shape
print(main_dimensions, template_dimensions)

cv2.waitKey()
cv2.destroyAllWindows()


# print(template1.shape)
max_segment = max_per_segment(sum_list)


for i in range(0, int(img0.shape[0] / img1.shape[0])):
    print(max_segment[0 + i * int(img0.shape[0] / img1.shape[0]): int(img0.shape[0] / img1.shape[0]) + i * int(img0.shape[0] / img1.shape[0])])


final_sum = overall_segment_sum(max_segment)
print(final_sum)










