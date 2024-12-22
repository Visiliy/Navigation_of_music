import music_request from "/modules/music_request";

const sendingMusic = () => {
    let mediaRecorder;
    let audioChunks = [];

    async function getAudio() {
        const stream = await navigator.mediaDevices.getUserMedia({
            audio: true,
        });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/mp3" });
            audioChunks = [];
            const res = music_request(audioBlob);
            return res;
        };

        mediaRecorder.start();
    }
    getAudio();

    const stopRecords = (mediaRecorder) => {
        mediaRecorder.stop();
    };
    setTimeout(stopRecords, 10000);
};

export default sendingMusic;
