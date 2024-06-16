const json_load_data = JSON.parse('replace_string_with_real_json')

const wb_socket = new WebSocket(`ws${json_load_data.ssl ? "s" : ""}://${json_load_data.host}:${json_load_data.wsport}`);
const server = `http${json_load_data.ssl ? "s" : ""}://${json_load_data.host}:${json_load_data.port}`;

wb_socket.onmessage = (event) => {
    const response = JSON.parse(event.data);
    if (response.type === "search_response") {
        if (response.success) {
            const videoList = response.videos;
            displayVideoList(videoList, "#search-list-container");
        } else {
            // alert("Failed to load videos. Please try again.");
        }
    }
    else if (response.type === "watch_history_get_response") {
        json = JSON.stringify(
            {
                "type": "favorites_get_request",
                "user": {
                    "email": email,
                },
            }
        );
        if (wb_socket.readyState !== wb_socket.OPEN) {
            setTimeout(() => { wb_socket.send(json) }, 1000);
        } else {
            wb_socket.send(json);
        }

        if (response.success) {
            displayVideoList(response.videos, "#history-list-container");
        } else {
            // alert("Failed to load videos. Please try again.");
        }
    }

    else if (response.type === "favorites_get_response") {
        if (response.success) {
            displayVideoList(response.videos, "#favorites-list-container");
        } else {
            // alert("Failed to load videos. Please try again.");
        }
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // Fetch video data (replace with your own API endpoint or mock data)
    const searchInput = document.querySelector('#searchInput');

    searchInput.addEventListener('change', () => {
        if (searchInput.value === "" || searchInput.value === ",") return;
        const json = JSON.stringify(
            {
                "type": "search_request",
                "search": {
                    "query": searchInput.value,
                },
            }
        );

        if (wb_socket.readyState !== wb_socket.OPEN) {
            setTimeout(() => { wb_socket.send(json) }, 1000);
            return;
        } else {
            wb_socket.send(json);
        }
    });
});


const displayVideoList = (videoList, container) => {
    const videoListContainer = document.querySelector(container);
    videoListContainer.innerHTML = "";

    videoList.forEach(video => {
        const videoItem = document.createElement('div');
        videoItem.className = "video-item";
        videoItem.style.maxWidth = "310px";

        const review_max_length = 50;
        const short_review = video.review.length > review_max_length ? video.review.substring(0, review_max_length) + "..." : video.review;

        videoItem.innerHTML = `
        <a href="/watch?v=${video.key}" style="color: black; text-decoration: none;">
        <div class="video-container" style="max-width:310px; max-height:500px; border:4px solid rgb(255,193,7); border-radius:15px; background-color:rgb(255,228,145); overflow:hidden;">
        <div class="video-thumbnail" style="max-width:310px;">
            <img src="${server}/storage/videos/${video.key}/thumbnail.jpg" alt="Video Thumbnail" style="border:none; border-radius:15px;">
        </div>
        <div class="video-details" style="max-width:310px; padding-left:5px; border:none;">
            <h5 style="color:rgb(101,101,101)">${video.name}</h5>
            <p style="color:rgb(101,101,101)">${short_review}</p>
            <p style="color:rgb(101,101,101)">genres: ${video.genre}</p>
            <p style="color:rgb(101,101,101)">${video.views} views</p>
        </div>
        </div>
        </a>
    `;
        // videoItem.onclick = () => {
        //     window.location.href = `/watch?v=${video.key}`;
        // };
        videoListContainer.appendChild(videoItem);
    });

    // make sure items are flexed horizontally
    videoListContainer.style.display = "flex";
    videoListContainer.style.flexWrap = "wrap";
    videoListContainer.style.justifyContent = "space-around";
    videoListContainer.style.alignItems = "center";
    videoListContainer.style.gap = "20px";
}

const email = sessionStorage.getItem("user_email");
let json = JSON.stringify(
    {
        "type": "watch_history_get_request",
        "user": {
            "email": email,
        },
    }
);
if (wb_socket.readyState !== wb_socket.OPEN) {
    setTimeout(() => { wb_socket.send(json) }, 1000);
} else {
    wb_socket.send(json);
}