import cv2

# samo mali test radi demonstracije
image = cv2.imread('simpsons.jpg', cv2.IMREAD_GRAYSCALE)
template = cv2.imread('bart.jpg', cv2.IMREAD_GRAYSCALE)

after_ccorr = cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED)
after_ccoeff = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

dim = (int(after_ccorr.shape[1] * 0.5), int(after_ccorr.shape[0] * 0.5))
after_ccorr = cv2.resize(after_ccorr, dim, cv2.INTER_AREA)
after_ccoeff = cv2.resize(after_ccoeff, dim, cv2.INTER_AREA)



cv2.imshow('CCORR_NORMED', after_ccorr)
cv2.imshow('CCOEFF_NORMED', after_ccoeff)
cv2.imshow('IMAGE', image)
cv2.imshow('TEMPLATE', template)
cv2.waitKey()
cv2.destroyAllWindows()


