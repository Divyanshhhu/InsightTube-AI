function getCurrentVideoURL() {

    const params = new URLSearchParams(window.location.search);

    return params.get("videoUrl");

}

function getCurrentVideoID() {
    const url = new URL(window.location.href);
    return url.searchParams.get("v");
}

async function indexCurrentVideo() {

    try {

        const url = getCurrentVideoURL();
        console.log("Current URL:", url);
        const result = await API.post(
            "/video/index",
            {
                url: url
            }
        );

        console.log("Video Indexed", result);

        return result;

    }
    catch(error){

        console.error(error);

        return null;

    }

}