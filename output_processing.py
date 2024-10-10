import cv2
import numpy as np
from operator import itemgetter

def find_cards(image):
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply GaussianBlur to reduce noise and improve contour detection
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use edge detection (Canny)
    edges = cv2.Canny(blur, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find bounding boxes around the detected cards
    bboxes = []
    for i, contour in enumerate(contours):
        # Approximate the contour to a polygon and get the bounding rectangle
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Filter out small areas or non-rectangular shapes
        if len(approx) == 4 and cv2.contourArea(contour) > 1000:  # Adjust contour area threshold if necessary
            x, y, w, h = cv2.boundingRect(approx)
            bboxes.append( ((x, y), (x + w, y + h)) )

    return bboxes

def order_points_lrtb(keypoints):
    """ Order points from top left to bottom right, going from left to right first, then top to bottom """    
    points = []
    keypoints_to_search = keypoints[:]
    while len(keypoints_to_search) > 0:
        a = sorted(keypoints_to_search, key=lambda p: (p[0]) + (p[1]))[0]  # find upper left point
        b = sorted(keypoints_to_search, key=lambda p: (p[0]) - (p[1]))[-1]  # find upper right point
    
        #cv2.line(img_with_keypoints, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), (255, 0, 0), 1)
    
        # convert opencv keypoint to numpy 3d point
        a = np.array([a[0], a[1], 0])
        b = np.array([b[0], b[1], 0])
    
        row_points = []
        remaining_points = []
        for k in keypoints_to_search:
            p = np.array([k[0], k[1], 0])
            # set a threshold
            d = int(np.array(keypoints_to_search).mean())/2
            #d = 100 #k.size - diameter of the keypoint 
            dist = np.linalg.norm(np.cross(np.subtract(p, a), np.subtract(b, a))) / np.linalg.norm(b)   # distance between keypoint and line a->b
            if d/2 > dist:
                row_points.append(k)
            else:
                remaining_points.append(k)
    
        points.extend(sorted(row_points, key=lambda h: h[0]))
        keypoints_to_search = remaining_points
    
    return points

def order_cards_lrtb(all_cards):
    """ Order cards from top left to bottom right, going from left to right first, then top to bottom """    
    tl_corners = [c[0] for c in all_cards]
    br_corners = [c[1] for c in all_cards]
    all_cards_dict = dict(zip(tl_corners, br_corners))
    ordered_points = order_points_lrtb(tl_corners)

    ordered_cards = []
    for point in ordered_points:
        tl_corner = point
        br_corner = all_cards_dict[point]
        ordered_cards.append((point, br_corner))

    return ordered_cards

def highlight_cards_by_id(image_path, ids, output_path):
    # Load image
    image = cv2.imread(image_path)

    # Find all cards
    all_cards = find_cards(image)
    
    # Sort cards from left to right, top to bottom
    cards_ordered = order_cards_lrtb(all_cards)
    
    # Select cards to highlight
    highlighted_cards = itemgetter(*ids)(cards_ordered)
    
    # Save output with highlighted cards
    for card in highlighted_cards:
        p1 , p2 = card
        cv2.rectangle(image, p1, p2, (0, 255, 0), 2)
    
        # Save the output image (optional)
        cv2.imwrite(output_path, image)