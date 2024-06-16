const json_load_data = JSON.parse('replace_string_with_real_json')

const wb_socket = new WebSocket(`ws${json_load_data.ssl ? "s" : ""}://${json_load_data.host}:${json_load_data.wsport}`);
const server = `http${json_load_data.ssl ? "s" : ""}://${json_load_data.host}:${json_load_data.port}`;

const key = document.querySelector('#key').attributes.value.value;

// const wb_socket = new WebSocket("ws://localhost:8765");

wb_socket.onmessage = (event) => {
    const response = JSON.parse(event.data);
    if (response.type === "video_response") {
        if (response.success) {
            const video_name = response.video.name;
            const video_views = response.video.views;
            const video_review = response.video.review;
            const video_rating = response.video.rating;

            const videoName = document.querySelector('#videoName');
            videoName.innerHTML = `${video_name} <span style="color:rgb(255,179,0)">${video_rating}%</span>`;
            const videoViews = document.querySelector('#videoViews');
            videoViews.innerHTML = `${video_views} views`;
            const videoReview = document.querySelector('#video-review');
            videoReview.innerHTML = video_review;

            const json = JSON.stringify(
                    {
                        "type": "watch_history_add_request",
                        video: {
                            user: sessionStorage.getItem("user_name"),
                            key: key,
                        },
                    }
            );
            if (sessionStorage.getItem("user_name"))
                wb_socket.send(json);
        } else {
            // alert("Failed to load video. Please try again.");
        }
    }
};

if (Hls.isSupported()) {
    var video = document.getElementById('video');
    var hls = new Hls();
    hls.loadSource(`${server}/storage/videos/${key}/playlist.m3u8`);
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED, function () {
        video.play();
    });
}
// hls.js is not supported on platforms that do not have Media Source Extensions (MSE) enabled.
// When the browser has built-in HLS support (check using `canPlayType`), we can provide an HLS manifest (i.e. .m3u8 URL) directly to the video element throught the `src` property.
// This is using the built-in support of the plain video element, without using hls.js.
else if (video.canPlayType('application/vnd.apple.mpegurl')) {
    video.src = `${server}/storage/videos/${key}/playlist.m3u8`;
    video.addEventListener('canplay', function () {
        video.play();
    });
}

json = JSON.stringify(
    {
        "type": "video_request",
        video: {
            "key": key,
        },
    }
);

if (wb_socket.readyState !== wb_socket.OPEN) {
    setTimeout(() => { wb_socket.send(json) }, 1000);
} else {
    wb_socket.send(json);
}

if (sessionStorage.getItem("user_email") == null) {
    document.querySelector("#favorites-button").disabled = true;
}

const favorites_button = document.querySelector('#favorites-button');
favorites_button.onclick = () => {
    const json = JSON.stringify(
        {
            "type": "favorites_add_request",
            video: {
                user: sessionStorage.getItem("user_name"),
                key: key,
            },
        }
    );
    if (wb_socket.readyState !== wb_socket.OPEN) {
        setTimeout(() => { wb_socket.send(json) }, 1000);
    } else {
        wb_socket.send(json);
    }
};

const queueButton = document.querySelector('#queue-button');
queueButton.onclick = () => {
    let queue = [];
    if (sessionStorage.getItem("session_queue") !== null && sessionStorage.getItem("session_queue") !== "") {
        for (let item of sessionStorage.getItem("session_queue").split(",")) {
            queue.push(item);
        }
    }

    if (!queue.includes(key)) {
        queue.push(key);
    }
    const string_queue = queue.join(",");
    sessionStorage.setItem("session_queue", string_queue);

    // reload page
    window.location.reload();
};
