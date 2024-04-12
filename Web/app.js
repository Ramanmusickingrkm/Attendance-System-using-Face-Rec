// Import the necessary Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js";
import { getStorage, ref as storageRef, uploadBytes } from "https://www.gstatic.com/firebasejs/9.0.0/firebase-storage.js";
import { getDatabase, set, ref as dbRef } from "https://www.gstatic.com/firebasejs/9.0.0/firebase-database.js";

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCeV5zsVHQmpPtB_2wy9JxWXdgrypqOOQk",
  authDomain: "attendance-48364.firebaseapp.com",
  databaseURL: "https://attendance-48364-default-rtdb.firebaseio.com",
  projectId: "attendance-48364",
  storageBucket: "attendance-48364.appspot.com",
  messagingSenderId: "1098129711579",
  appId: "1:1098129711579:web:923fee82a14161dc7947fe",
  measurementId: "G-F7L2XP9F3K"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const storage = getStorage(app);
const database = getDatabase(app);

document.getElementById('studentForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = ""; // Clear previous messages

    const fileInput = document.getElementById('photoUpload');
    const yearSelect = document.getElementById('year').value;
    const branchSelect = document.getElementById('branch').value;
    const studentId = document.getElementById('studentId').value;
    const nameInput = document.getElementById('name').value;
    const file = fileInput.files[0];

    if (!file) {
        messageDiv.textContent = 'Please upload a photo.';
        return;
    }

    if (file.type !== "image/png" || file.name !== `${studentId}.png`) {
        messageDiv.textContent = 'Please upload a PNG file named after your student ID (e.g., 12345.png).';
        return;
    }

    const fileRef = storageRef(storage, `images/${file.name}`);
    try {
        await uploadBytes(fileRef, file);
        const studentRef = dbRef(database, `DPGITM/${yearSelect}/${branchSelect}/Students/${studentId}`);
        await set(studentRef, {
            name: nameInput,
            entry_time: '',
            exit_time: '',
            subjects_attended: '',
            total_attendance: 0
        });

        messageDiv.textContent = 'Student registered successfully!';
        messageDiv.style.color = 'green';
        document.getElementById('studentForm').reset(); // Reset the form on success
    } catch (error) {
        console.error('Failed to upload data:', error);
        messageDiv.textContent = 'Failed to register student. Error: ' + error.message;
        messageDiv.style.color = 'red';
    }
});
