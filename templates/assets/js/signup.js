const json_load_data = JSON.parse('replace_string_with_real_json')

const wb_socket = new WebSocket(`ws${json_load_data.ssl ? "s" : ""}://${json_load_data.host}:${json_load_data.wsport}`);

const signupButton = document.querySelector('#signupButton');

wb_socket.onmessage = (event) => {
    const response = JSON.parse(event.data);
    if (response.type === "signup_response") {
        if (response.success) {
            window.location.href = "/";
        } else {
            alert("Failed to create account. Please try again.");
        }
    }
}

signupButton.onclick = () => {
    const emailInput = document.querySelector('#emailInput');
    const usernameInput = document.querySelector('#usernameInput');
    const passwordInput = document.querySelector('#passwordInput');
    const json = JSON.stringify(
        {
            "type": "signup_request",
            "user": {
                "email": emailInput.value,
                "username": usernameInput.value,
                "password": passwordInput.value
            },
        }
    );

    if (wb_socket.readyState !== wb_socket.OPEN) {
        setTimeout(() => { wb_socket.send(json) }, 1000);
        return;
    } else {
        wb_socket.send(json);
    }
};

// event when closing the window
window.onbeforeunload = () => {
    wb_socket.close();
};