import face_recognition
import os
import re
import warnings
import scipy.misc
import sys
import numpy

def IdentifyFace(self, event):
    #default values in face_recognition, will be changeable in future
    cpus = -1
    tolerance = 0.6

    #CPU multi-threaded check, performance suggestion snippet from face_recognition
    if (sys.version_info < (3, 4)):
        print("WARNING: Multi-threaded processing requires Python 3.4 or greater. Falling back to single-thread processing.")
        cpus = 1

    picture = face_recognition.load_image_file(event.GetPath())

    known_names, known_encodings = ScanKnownPeople("KnownLibrary")

    #Scale down image if large, performance suggestion snippet from face_recognition
    if picture.shape[1] > 1600:
        scale_factor = 1600.0 / picture.shape[1]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            picture = scipy.misc.imresize(picture, scale_factor)

    encodings = face_recognition.face_encodings(picture)

    for single_encoding in range(len(encodings)):
        #code snippets from face_recognition, adaption of compare_faces but with distance returned
        distances = face_recognition.face_distance(known_encodings, encodings[single_encoding])
        result = list(distances <= tolerance)

        if True in result:
            for is_match, name, distance in zip(result, known_names, distances):
                if is_match:
                    print(os.path.splitext(os.path.basename(event.GetPath()))[0], "has match '" + name + "' at distance", distance, ".")
                    print(event.GetPath())
        else:
            print("No matches for face", str(single_encoding + 1), "in photo '", os.path.splitext(os.path.basename(event.GetPath()))[0] + "'.")

def ScanKnownPeople(known_people_folder):
    names = []
    face_encodings = []

    for file in ImageFilesInFolder(known_people_folder):
        filename = os.path.splitext(os.path.basename(file))[0]
        print("DEBUG: Attempted to load image file from", file)
        image = face_recognition.load_image_file(file)

        if os.path.isfile(os.path.join(known_people_folder, "PreEncoded", filename) + ".npy"):
            #read from file, for performance reasons. useful for large batches of files
            encodedfile = numpy.load((os.path.join(known_people_folder, "PreEncoded", filename) + ".npy"))

            if encodedfile is not None:
                names.append(filename)
                print("DEBUG: appended from document", filename)
                face_encodings.append(encodedfile)
                print("DEBUG: appended from document", encodedfile)
        else:
            single_encoding = face_recognition.face_encodings(image)

            if len(single_encoding) > 1:
                print("WARNING: More than one face found in", file + ".", "Only using the first face.")

            if len(single_encoding) == 0:
                print("WARNING: No faces found in", file + ".", "Ignoring file.")
            else:
                names.append(filename)
                face_encodings.append(single_encoding[0])

                #write to file, for performance reasons, so as to not calculate all the faces each time
                encodedfile = numpy.save((os.path.join(known_people_folder, "PreEncoded", filename) + ".npy"), single_encoding[0])
                print("DEBUG: saved to document", filename)
                print("DEBUG: saved to document", encodedfile)

    return names, face_encodings

def ImageFilesInFolder(folder):
    #following code snippet from face_recognition
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]

def GetMainMatch(self, event):
    #default values in face_recognition, will be changeable in future
    cpus = -1
    tolerance = 0.6

    #CPU multi-threaded check, performance suggestion snippet from face_recognition
    if (sys.version_info < (3, 4)):
        print("WARNING: Multi-threaded processing requires Python 3.4 or greater. Falling back to single-thread processing.")
        cpus = 1

    picture = face_recognition.load_image_file(event.GetPath())

    known_names, known_encodings = ScanKnownPeople("KnownLibrary")

    #Scale down image if large, performance suggestion snippet from face_recognition
    if picture.shape[1] > 1600:
        scale_factor = 1600.0 / picture.shape[1]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            picture = scipy.misc.imresize(picture, scale_factor)

    encodings = face_recognition.face_encodings(picture)

    for single_encoding in range(len(encodings)):
        #code snippets from face_recognition, adaption of compare_faces but with distance returned
        distances = face_recognition.face_distance(known_encodings, encodings[single_encoding])
        result = list(distances <= tolerance)

        i = 0

        if True in result:
            for is_match, name, distance in zip(result, known_names, distances):
                if is_match:
                    if i < 1:
                        i = 1
                        return name
        else:
            return "No match found."
