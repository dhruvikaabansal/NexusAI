import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyCUREGkZomXmc-BwrE652v8t_1LCl0_QmA",
    authDomain: "aisummarizer-880e0.firebaseapp.com",
    projectId: "aisummarizer-880e0",
    storageBucket: "aisummarizer-880e0.firebasestorage.app",
    messagingSenderId: "807710500070",
    appId: "1:807710500070:web:b92d2c7d29bf41e3654727",
    measurementId: "G-W7069RV0FR"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
