import face_recognition
import cv2
from os import listdir

faces = []
suspects_name = []

def train_faces(image_path, suspect_name):
    print 'Loading image: ' + image_path
    image = face_recognition.load_image_file(image_path)

    fc_encodings = face_recognition.face_encodings(image)

    if len(fc_encodings) > 0:
        print 'Recognizing image...'
        faces.append(fc_encodings[0])
        suspects_name.append(suspect_name)

def draw_suspect(name, image, face_location):
    top, right, bottom, left = face_location

    # Draws a green box around the suspect face
    cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

    # Draw a label with a name below the face
    cv2.rectangle(image, (left, bottom-15), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(image, name, (left + 6, bottom - 6), font, 0.3, (255, 255, 255), 1)
    return image

def detect_faces(image):
    face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=2)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    return face_locations, face_encodings

def recognize_faces(image, face_encodings, face_locations):
    suspects_index = 0
    for face_encoding in face_encodings:
        match = face_recognition.compare_faces(faces, face_encoding, tolerance=0.6)
        for i in range(len(match)):
            if match[i]:
                name = suspects_name[i]
                image = draw_suspect(name, image, face_locations[suspects_index])

        suspects_index += 1

    return image

path = "./data"
for subdir in listdir(path):
    suspect_name = subdir
    for image in listdir(path + "/" + subdir):
        image_path = path + "/" + subdir + "/" + image
        train_faces(image_path, suspect_name)

image = cv2.imread("test.jpg")

face_locations, face_encodings = detect_faces(image)

result = recognize_faces(image, face_encodings, face_locations)
while True:
    cv2.imshow("result", result)
    if cv2.waitKey(33) == ord('a'):
        break


