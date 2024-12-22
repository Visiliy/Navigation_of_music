//const music_request = () => {
//    fetch("http://127.0.0.1:8070/get_music")
//        .then((response) => {
//            if (!response.ok) {
//                throw new Error("Сетевая ошибка");
//            }
//            return response.json();
//        })
//        .then((data) => console.log(data))
//        .catch((error) => console.error("Ошибка:", error));
//};
async function music_request(audioBlob) {
    const formData = new FormData();
    formData.append("audio", audioBlob);
    console.log(formData);

    try {
        const response = await fetch("http://127.0.0.1:8070/get_music", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            const result = await response.json();
            console.log(result);
            return result;
        } else {
            console.log("Неполадки на сервере");
            return "server_error";
        }
    } catch (error) {
        console.log("упс");
        console.error(error);
        console.log("Сервер не отвечает");
        return "error";
    }
}

export default music_request;
