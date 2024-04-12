import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendance-48364-default-rtdb.firebaseio.com/"
})

# Function to create DPGITM hierarchy with student details in Firebase database
def create_dpgitm_hierarchy_with_students():
    ref = db.reference()  # Get a reference to the root node of the database

    # Define DPGITM hierarchy with student details
    dpgitm_hierarchy = {
        'DPGITM': {
            '1st Year': {
                'CSE': {'Students': {}},
                'IT': {'Students': {}},
                'CE': {'Students': {}},
                'ME': {'Students': {}},
                'ECE': {'Students': {}}
            },
            '2nd Year': {
                'CSE': {'Students': {}},
                'IT': {'Students': {}},
                'CE': {'Students': {}},
                'ME': {'Students': {}},
                'ECE': {'Students': {}}
            },
            '3rd Year': {
                'CSE': {'Students': {}},
                'IT': {'Students': {}},
                'CE': {'Students': {}},
                'ME': {'Students': {}},
                'ECE': {'Students': {}}
            },
            '4th Year': {
                'CSE': {'Students': {}},
                'IT': {'Students': {}},
                'CE': {'Students': {}},
                'ME': {'Students': {}},
                'ECE': {'Students': {}}
            }
        }
    }

    # Populate some sample students in specific branches and years for demonstration
    dpgitm_hierarchy['DPGITM']['1st Year']['CSE']['Students'] = {
        '21069': {
            'name': 'Shubam Pathak',
            'entry_time': '',
            'exit_time': '',
            'subjects_attended': '',
            'total_attendance': 0
        },
        '21071': {
            'name': 'Raman Kumar',
            'entry_time': '',
            'exit_time': '',
            'subjects_attended': '',
            'total_attendance': 0
        }
    }
    dpgitm_hierarchy['DPGITM']['2nd Year']['IT']['Students'] = {
        '21081': {
            'name': 'Vinay Kumar',
            'entry_time': '',
            'exit_time': '',
            'subjects_attended': '',
            'total_attendance': 0
        }
    }
    dpgitm_hierarchy['DPGITM']['2nd Year']['ME']['Students'] = {
        '21010': {
            'name': 'Aaryan Bhardwaj',
            'entry_time': '',
            'exit_time': '',
            'subjects_attended': '',
            'total_attendance': 0
        }
    }

    # Set the DPGITM hierarchy in the Firebase database
    ref.update(dpgitm_hierarchy)

# Create DPGITM hierarchy with student details in Firebase database
create_dpgitm_hierarchy_with_students()
