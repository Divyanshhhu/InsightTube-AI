(async () => {

    if (document.getElementById("insighttube-frame"))
        return;

    const iframe = document.createElement("iframe");

    iframe.id = "insighttube-frame";

    const videoURL = encodeURIComponent(window.location.href);

    iframe.src =
        chrome.runtime.getURL(
            "index.html?videoUrl=" + videoURL
        );

    iframe.style.position = "fixed";

    iframe.style.top = "0";

    iframe.style.right = "0";

    iframe.style.width = "420px";

    iframe.style.height = "100vh";

    iframe.style.border = "none";

    iframe.style.zIndex = "999999";

    iframe.style.background = "#111827";

    document.body.appendChild(iframe);

})();