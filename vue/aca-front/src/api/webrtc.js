// this code is a variation of a code found at https://www.linux-projects.org/

var ws = null;
var pc;
var audio_stream = null;

var pcConfig = {
    "iceServers": [],
};

var pcOptions = {
    optional: []
};

var mediaConstraints = {
    optional: [],
    mandatory: {
        OfferToReceiveAudio: true,
        OfferToReceiveVideo: false
    }
};
var remoteDesc = false;
var iceCandidates = [];

RTCPeerConnection = window.RTCPeerConnection || window.webkitRTCPeerConnection;
RTCSessionDescription = window.RTCSessionDescription;
RTCIceCandidate = window.RTCIceCandidate;
navigator.getUserMedia = navigator.mediaDevices.getUserMedia || navigator.mozGetUserMedia || navigator.webkitGetUserMedia || navigator.msGetUserMedia;

export const createPeerConnection = () => {
    try {
        var pcConfig_ = pcConfig;
        console.log(JSON.stringify(pcConfig_));
        pc = new RTCPeerConnection(pcConfig_, pcOptions);
        pc.onicecandidate = onIceCandidate;
        pc.ontrack = onTrack;
        pc.onremovestream = onRemoteStreamRemoved;
        console.log("peer connection successfully created!");
    } catch (e) {
        console.error("createPeerConnection() failed");
    }
}

function onIceCandidate(event) {
    if (event.candidate && event.candidate.candidate) {
        var candidate = {
            sdpMLineIndex: event.candidate.sdpMLineIndex,
            sdpMid: event.candidate.sdpMid,
            candidate: event.candidate.candidate
        };
        var request = {
            what: "addIceCandidate",
            data: JSON.stringify(candidate)
        };
        ws.send(JSON.stringify(request));
    } else {
        console.log("End of candidates.");
    }
}

function addIceCandidates() {
    iceCandidates.forEach(function (candidate) {
        pc.addIceCandidate(candidate,
            function () {
                console.log("IceCandidate added: " + JSON.stringify(candidate));
            },
            function (error) {
                console.error("addIceCandidate error: " + error);
            }
        );
    });
    iceCandidates = [];
}

function onTrack(event) {
    console.log("Remote track!");
    let remoteAudioElement = document.getElementById('remote-audio');
    let stream = event.streams[0];
    remoteAudioElement.srcObject = stream;
}

function onRemoteStreamRemoved(event) {
    let remoteAudioElement = document.getElementById('remote-audio');
    remoteAudioElement.srcObject = null;
}

export const getAudioStream = () => {
    return audio_stream;
}

export const start = () => {
    if ("WebSocket" in window) {
        document.documentElement.style.cursor = 'wait';

        var protocol = location.protocol === "https:" ? "wss:" : "ws:";
        ws = new WebSocket(protocol + '//' + 'bramka:8080' + '/stream/webrtc');

        function call(stream) {
            iceCandidates = [];
            remoteDesc = false;
            createPeerConnection();
            if (stream) {
                pc.addStream(stream);
            }
            var request = {
                what: "call",
                options: {
                    force_hw_vcodec: true,
                    vformat: undefined,
                    trickle_ice: true
                }
            };
            ws.send(JSON.stringify(request));
            console.log("call(), request=" + JSON.stringify(request));
        }

        ws.onopen = function () {
           audio_stream = null;
           navigator.mediaDevices.getUserMedia({
              audio: {
                   autoGainControl: true,
                   channelCount: 1,
                   echoCancellation: true,
                   latency: 0,
                   noiseSuppression: true,
                   sampleRate: 48000,
                   sampleSize: 16
              }
            })
            .then(function (stream) {
                audio_stream = stream;
                call(stream);
                audio_stream.getAudioTracks().forEach(track => {
                  track.enabled = false;
                });
            })
            .catch(function (error) {
                stop();
                alert("An error has occurred. Check media device, permissions on media and origin.");
                console.error(error);
            });
        };

        ws.onmessage = function (evt) {
            var msg = JSON.parse(evt.data);
            if (msg.what !== 'undefined') {
                var what = msg.what;
                var data = msg.data;
            }
            console.log("message=" + msg);
            console.log("message =" + what);

            switch (what) {
                case "offer":
                    console.log(data)
                    pc.setRemoteDescription(new RTCSessionDescription(JSON.parse(data)),
                            function onRemoteSdpSuccess() {
                                remoteDesc = true;
                                addIceCandidates();
                                console.log('onRemoteSdpSucces()');
                                pc.createAnswer(function (sessionDescription) {
                                    pc.setLocalDescription(sessionDescription);
                                    var request = {
                                        what: "answer",
                                        data: JSON.stringify(sessionDescription)
                                    };
                                    ws.send(JSON.stringify(request));
                                    console.log(request);

                                }, function (error) {
                                    alert("Failed to createAnswer: " + error);

                                }, mediaConstraints);
                            },
                            function onRemoteSdpError(event) {
                                alert('Failed to set remote description (unsupported codec on this browser?): ' + event);
                                stop();
                            }
                    );

                case "answer":
                    break;

                case "message":
                    alert(msg.data);
                    break;

                case "iceCandidate": // when trickle is enabled
                    if (!msg.data) {
                        console.log("Ice Gathering Complete");
                        break;
                    }
                    var elt = JSON.parse(msg.data);
                    let candidate = new RTCIceCandidate({sdpMLineIndex: elt.sdpMLineIndex, candidate: elt.candidate});
                    iceCandidates.push(candidate);
                    if (remoteDesc)
                        addIceCandidates();
                    document.documentElement.style.cursor = 'default';
                    break;

                case "iceCandidates": // when trickle ice is not enabled
                    var candidates = JSON.parse(msg.data);
                    for (var i = 0; candidates && i < candidates.length; i++) {
                        var elt = candidates[i];
                        let candidate = new RTCIceCandidate({sdpMLineIndex: elt.sdpMLineIndex, candidate: elt.candidate});
                        iceCandidates.push(candidate);
                    }
                    if (remoteDesc)
                        addIceCandidates();
                    document.documentElement.style.cursor = 'default';
                    break;
            }
        };

        ws.onclose = function (evt) {
            if (pc) {
                pc.close();
                pc = null;
            }
            document.documentElement.style.cursor = 'default';
        };

        ws.onerror = function (evt) {
            alert("An error has occurred!");
            ws.close();
        };

    } else {
        alert("Sorry, this browser does not support WebSockets.");
    }

}

export const stop = () => {
    if (audio_stream) {
        try {
            if (audio_stream.getVideoTracks().length)
                audio_stream.getVideoTracks()[0].stop();
            if (audio_stream.getAudioTracks().length)
                audio_stream.getAudioTracks()[0].stop();
            audio_stream.stop(); // deprecated
        } catch (e) {
            for (var i = 0; i < audio_stream.getTracks().length; i++)
                audio_stream.getTracks()[i].stop();
        }
        audio_stream = null;
    }
    document.getElementById('remote-audio').srcObject = null;
    if (pc) {
        pc.close();
        pc = null;
    }
    if (ws) {
        ws.close();
        ws = null;
    }
    document.documentElement.style.cursor = 'default';
}
