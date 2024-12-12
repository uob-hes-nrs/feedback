import { initializeApp } from "https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.0.0/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyDKiyQTkTp2uSNiW4tjkjwp_u5EsU3_wBI",
    authDomain: "uobcsrs.firebaseapp.com",
    projectId: "uobcsrs",
    storageBucket: "uobcsrs.firebasestorage.app",
    messagingSenderId: "100258592851",
    appId: "1:100258592851:web:9110f99f380df86de8eea6",
    measurementId: "G-G2Z3F8184P"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    console.log(email)
    console.log(password)

    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            userCredential.user.getIdToken().then((idToken) => {
                fetch('/login', {
                    method: 'POST',
                    headers: { 'Authorisation': idToken }
                })
                .then((res) => res.json())
                .then((data) => {
                    if (data.message === "Authenticated") {
                        window.location.href = `/${data.role}_view`;
                    }
                });
            });
        })
        .catch((err) => alert("Login failed: " + err.message));
});
