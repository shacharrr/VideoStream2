if (document.querySelector("#nav") !== null && sessionStorage.getItem("user_email") !== null) {
    const username = sessionStorage.getItem("user_name");

    const signinLink = document.querySelector("#signinLink");
    const navSigninButton = document.querySelector("#nav-signin-button");
    const signupLink = document.querySelector("#signupLink");
    const navSignupButton = document.querySelector("#nav-signup-button");

    navSigninButton.innerHTML = username
    navSigninButton.disabled = true;
    signinLink.href = "#";

    navSignupButton.innerHTML = "Log Out";
    navSignupButton.onclick = () => {
        sessionStorage.clear();
        location.reload();
    };
    signupLink.href = "#";
}

const next_in_queue = document.querySelector("#next-queue-button");
if (sessionStorage.getItem("session_queue") === null || sessionStorage.getItem("session_queue") === "") {
    next_in_queue.style.display="none";
} else {
    next_in_queue.onclick = () => {
        const queue = sessionStorage.getItem("session_queue").split(",")
        const elem = queue.shift();
        sessionStorage.setItem("session_queue", queue.join(","));
        window.location.href = `/watch?v=${elem}`;
    };
}