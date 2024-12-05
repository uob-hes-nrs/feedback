function getRequestURL() {
    if (document.location.hostname) {
        return `https://${document.location.hostname}:5000`;
    } else {
        return "http://localhost:5000";
    }
}
