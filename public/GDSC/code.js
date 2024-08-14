import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import 'firebase/compat/firestore';

const firebaseConfig = {
    apiKey: "AIzaSyA74K-gs9HxyKZK_V7C_U2WTf-O4arVzDg",
    authDomain: "matthew-collard.firebaseapp.com",
    projectId: "matthew-collard",
    storageBucket: "matthew-collard.appspot.com",
    messagingSenderId: "546899924226",
    appId: "1:546899924226:web:d1ba8f244cd87277015e1b"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
const storage = firebase.storage();

// Function to upload image to Firebase
export async function uploadImage(imageData, fileName) {
    const storageRef = storage.ref();
    const imageRef = storageRef.child(`images/${fileName}`);
    try {
        const snapshot = await imageRef.putString(imageData, 'data_url');
        const url = await snapshot.ref.getDownloadURL();
        console.log('Uploaded a data_url string!', url);
        return url;
    } catch (error) {
        console.error('Upload failed:', error);
    }
}

