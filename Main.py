import firebase_admin
from firebase_admin import credentials, db
import cv2
import face_recognition
import pickle
from datetime import datetime, timedelta

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendance-48364-default-rtdb.firebaseio.com/"
})

# Function to load student encodings and IDs
def load_student_encodings():
    with open("EncodeFile.p", "rb") as file:
        encodeListKnownWithIds = pickle.load(file)
    encodeListKnown, studentIds = encodeListKnownWithIds
    return encodeListKnown, studentIds

# Function to find the correct directory for the student in Firebase
def find_student_directory(student_id):
    root_directory = 'DPGITM'
    year_directories = ['1st Year', '2nd Year', '3rd Year', '4th Year']  # Add more years if needed
    department_directories = ['CSE', 'ECE', 'ME', 'IT', 'CE']  # Add more departments if needed

    # Iterate through year directories
    for year_dir in year_directories:
        # Iterate through department directories
        for dept_dir in department_directories:
            student_directory = f'{root_directory}/{year_dir}/{dept_dir}/Students'
            # Check if the student ID exists in the current directory
            if db.reference(f'{student_directory}/{student_id}').get():
                return student_directory  # Return the directory path if the student ID is found
    
    return None  # Return None if the student directory is not found

# Function to recognize faces and update attendance
def recognize_faces_and_update_attendance():
    # Load student encodings and IDs
    encodeListKnown, studentIds = load_student_encodings()
    
    # Get a reference to the root node
    ref = db.reference()

    # Capture Video
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    # Dictionary to store entry times for students
    entry_times = {}

    # Define the schedule for each period
    schedule = {
        'Period 1': [(datetime.strptime('19:59', '%H:%M'), datetime.strptime('20:00', '%H:%M'))],
        # Define schedules for other periods as needed
    }

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture frame")
            break

        imgBackground = img.copy()

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        if faceCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = min(range(len(faceDis)), key=faceDis.__getitem__)

                if matches[matchIndex]:
                    student_id = studentIds[matchIndex]
                    bbox = (faceLoc[3] * 4, faceLoc[0] * 4, (faceLoc[1] - faceLoc[3]) * 4, (faceLoc[2] - faceLoc[0]) * 4)
                    cv2.rectangle(imgBackground, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)

                    # Find the directory for the student
                    student_directory = find_student_directory(student_id)
                    if student_directory:
                        # Update entry time in Firebase if not already recorded
                        if student_id not in entry_times:
                            entry_times[student_id] = datetime.now()
                            entry_time = entry_times[student_id].strftime("%Y-%m-%d %H:%M:%S")
                            student_ref = ref.child(student_directory).child(student_id)
                            student_ref.update({'entry_time': entry_time})
                            print(f"Entry time recorded for student {student_id}")
                        else:
                            # Check if it's time to record exit time
                            current_time = datetime.now()
                            exit_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                            student_ref = ref.child(student_directory).child(student_id)
                            student_ref.update({'exit_time': exit_time})
                            print(f"Exit time recorded for student {student_id}")
                            # Determine subjects attended based on the schedule
                            subjects_attended = []
                            for period, timings in schedule.items():
                                for class_start, class_end in timings:
                                    if class_start <= entry_times[student_id] <= class_end and class_start <= current_time <= class_end:
                                        subjects_attended.append(period)
                                        break
                            if subjects_attended:
                                student_ref.update({'subjects_attended': subjects_attended})
                            entry_times.pop(student_id)  # Remove entry time for the student

        cv2.imshow("Face Attendance", imgBackground)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run face recognition and update attendance
recognize_faces_and_update_attendance()
