const json_load_data = JSON.parse('replace_string_with_real_json')

const wb_socket = new WebSocket(`ws${json_load_data.ssl ? "s" : ""}://${json_load_data.host}:${json_load_data.wsport}`);

const loginButton = document.querySelector('#loginButton');
const emailInput = document.querySelector('#emailInput');
const passwordInput = document.querySelector('#passwordInput');

wb_socket.onmessage = (event) => {
    const response = JSON.parse(event.data);
    if (response.type === "login_response") {
        if (response.success) {
            sessionStorage.setItem("user_email", response.user.email);
            sessionStorage.setItem("user_name", response.user.username);
            window.location.href = "/";
        } else {
            alert("Invalid credentials");
        }
    }
}

loginButton.onclick = () => {
    const json = JSON.stringify(
        {
            "type": "login_request",
            "user": {
                "email": emailInput.value,
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