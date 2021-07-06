function initPage() {
    var urlServer = "https://demo.flashphoner.com:8445";
    var player = videojs('remoteVideo');
    var applyFn = function () {
        var streamName = "stream1";
        streamName = encodeURIComponent(streamName);
        var src = urlServer + "/" + streamName + "/" + streamName + ".m3u8";
        player.src({
            src: src,
            type: "application/vnd.apple.mpegurl"
        });
        player.play();
    };
    applyBtn.onclick = applyFn
}