import cv2
import numpy as np
import os

# variacija na prvi zadatak
def križna_korelacija(input_path, templates_path, draw=False, test=False, counter=0, resize=0):
    input_picture = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if resize:
        input_picture = cv2.resize(input_picture,
                                   (int(input_picture.shape[1] * resize), int(input_picture.shape[0] * resize)),
                                   interpolation=cv2.INTER_AREA)
    results = list()
    final_result = cv2.imread(input_path, 1)
    for template_path in templates_path:
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if resize:
            template = cv2.resize(template,
                                       (int(template.shape[1] * resize), int(template.shape[0] * resize)),
                                       interpolation=cv2.INTER_AREA)
        width, height = template.shape[::-1]
        result = cv2.matchTemplate(input_picture, template, cv2.TM_CCOEFF_NORMED)
        minMax = cv2.minMaxLoc(result)[1::2]
        if test: print(counter, minMax)
        results.append([minMax, counter])
        counter += 1
        if draw:
            cv2.imshow('win', result)
            final_result = cv2.rectangle(final_result, minMax[1], (minMax[1][0] + width, minMax[1][1] + height), (0, 0, 255), 3)
            cv2.imshow('main', final_result)
            cv2.waitKey()
            cv2.destroyAllWindows()
    return results

# file_names = ['chicago', 'minsk_drone', 'minsk', 'minsk_low', 'protest', 'rio']
file_names = ['view_01', 'view_02', 'view_03', 'view_04']


for file_name in file_names:
    print(file_name)
    # main_path = os.path.join(os.environ.get('HOMEPATH'), 'Desktop', '512x512', file_name)
    main_path = os.path.join(os.environ.get('HOMEPATH'), 'Desktop', 'PETS database', file_name)
    templates = ['template64x64']

    for template in templates:
        print(template)
        templ_path_list = list()
        for template_number in range(25):
            # path = os.path.join(main_path, template, 'template_' + str(template_number) + '.png')
            path = os.path.join(main_path, template, 'template_' + str(template_number) + '.jpg')
            templ_path_list.append(path)

        counter = 0
        while True:
            if counter < 10:
                # picture = 'crowd' + '0' + str(counter) + '.png'
                picture = 'crowd' + '0' + str(counter) + '.jpg'
            else:
                # picture = 'crowd' + str(counter) + '.png'
                picture = 'crowd' + str(counter) + '.jpg'
            counter += 1
            if not os.path.exists(os.path.join(main_path, picture)): break
            highest_probabilities = križna_korelacija(os.path.join(main_path, picture), templ_path_list, resize=0)
            high_to_low = sorted(highest_probabilities, key=lambda x: x[0], reverse=True)
            top_five_values = high_to_low[0:5]
            final_image = cv2.imread(os.path.join(main_path, picture), cv2.IMREAD_COLOR)
            square_dimensions = cv2.imread(templ_path_list[0]).shape
            for point in top_five_values:
                final_image = cv2.rectangle(final_image, point[0][1],(point[0][1][0] + square_dimensions[0], point[0][1][1] + square_dimensions[1]), (), thickness=5)
                final_image = cv2.putText(final_image, str(point[1] // 5) + ' ' + str(point[1]), point[0][1], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                print(f'probability is {point[0][0]}, class:  {point[1] // 5}')
                if point[0][0] > 0.95: print(f'this is > 0.9: {point[0][0]},  {point[1] // 5}')
            # for one in sorted(top_five_values, key=lambda x: x[1], reverse=True):
            #     print(f'probability is {one[0][0]}, class:  {one[1] // 5}')
            print(sorted(top_five_values, key= lambda x: x[1], reverse=True)[0][1] // 5)
            print('-----------------------------------')
            cv2.imshow('fianl', final_image)
            cv2.waitKey()



