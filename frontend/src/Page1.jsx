import { useState } from "react";
import axios from "axios";
import "./ux_ui/main.css";
import "./ux_ui/main2.css";
import "./ux_ui/btn1.css";
import "./ux_ui/sending_audio_form.css";
import Name from "./components/name";

function Page1() {
    const [openForm, setOpenForm] = useState(true);
    const [openRegForm, setOpenRegForm] = useState(false);
    const [sending, setSending] = useState(false);
    const [response, setResponse] = useState("");

    const [nickname1, setNickname1] = useState("");
    const [password1, setPassword1] = useState("");

    const [name, setName] = useState("");
    const [nickname2, setNickname2] = useState("");
    const [password2_1, setPassword2_1] = useState("");
    const [password2_2, setPassword2_2] = useState("");

    const login = () => {
        var data = [nickname1, password1];
        axios
            .post("http://127.0.0.1:8070/login_user", data)
            .then((response) => {
                console.log(response.statusText);
                openLoginForm();
            })
            .catch((error) => {
                console.log(error);
                alert("Ошибка на сервере или проблема с интернетом");
            });
    };

    const registration = () => {
        if (
            password2_1 == password2_2 &&
            password2_1 != "" &&
            name != "" &&
            nickname2 != "" &&
            password2_2 != ""
        ) {
            var data = [name, nickname2, password2_1];
            axios
                .post("http://127.0.0.1:8070/user_registration", data)
                .then((response) => {
                    console.log(response.statusText);
                    openLoginForm();
                })
                .catch((error) => {
                    console.log(error);
                    alert("Ошибка на сервере или проблема с интернетом");
                });
        } else {
            alert("Пароли не совпадают или введено пустое значение");
        }
    };

    const openLoginForm = () => {
        if (openRegForm) {
            setOpenRegForm(!openRegForm);
        }
        setOpenForm(!openForm);
    };

    const openRegistrationsForm = () => {
        setOpenRegForm(!openRegForm);
    };

    const sendAudioContentToServer = () => {
        setSending(true);

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
                const formData = new FormData();
                formData.append("audio", audioBlob);
                axios
                    .post("http://127.0.0.1:8070/get_music", formData)
                    .then((response) => {
                        setResponse(response);
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            };

            mediaRecorder.start();
        }
        getAudio();
        const stopRecords = () => {
            mediaRecorder.stop();
            setSending(false);
        };
        setTimeout(stopRecords, 15000);
    };

    var close_form = "display_none";
    var close_playe1 = "";
    var close_playe2 = "";
    var close_playe3 = "display_none";
    var not_fon = "";
    var close_reg_form = "display_none";
    var close_send_form = "display_none";
    if (!openForm) {
        close_form = "";
        close_playe1 = "display_none";
        not_fon = "main_2_0";
        close_playe3 = "";
    }

    if (openRegForm && not_fon != "") {
        close_reg_form = "";
        close_form = "display_none";
        close_playe3 = "";
    }

    if (sending) {
        not_fon = "main_2_0";
        close_send_form = "";
        close_playe2 = "display_none";
    }

    return (
        <div className={`main ${not_fon}`}>
            <div className="left">
                <Name></Name>
                <div className="slogan">
                    <center>
                        <h2 className="text">
                            Сервис, который сделает поиск музыки быстрым и
                            удобным!
                        </h2>
                    </center>
                    <center>
                        <img className="img2" src="src/img/one.png"></img>
                    </center>
                    <center>
                        <h2 className="text">Заряжайся музыкой!</h2>
                    </center>
                </div>
            </div>
            <div className="right_block">
                <img src="src/img/i.jpg" className="img"></img>
                <button
                    className={`btn1 ${close_playe1}`}
                    onClick={openLoginForm}
                >
                    Войти
                </button>
                <button
                    className={`btn1 ${close_playe3}`}
                    style={{ zIndex: 10 }}
                    onClick={openLoginForm}
                >
                    Назад
                </button>
            </div>
            <button className="about">О проекте</button>
            <div
                className={`player ${close_playe1} ${close_playe2}`}
                onClick={sendAudioContentToServer}
            >
                <img src="src/img/player.png" className="img3"></img>
            </div>
            <div className={`sending_form ${close_send_form}`}>
                <div id="preloader__wrapper" className="preloader__wrapper">
                    <div id="preloader" className="preloader"></div>
                    <div className="preloader_div"></div>
                </div>
            </div>
            <div className={`login_form ${close_form}`}>
                <h3 className="h3_1_1">Вход</h3>
                <h3 className="h3_2" onClick={openRegistrationsForm}>
                    Регистрация
                </h3>
                <input
                    className="input top1"
                    onChange={(e) => setNickname1(e.target.value)}
                    placeholder="Никнейм"
                ></input>
                <input
                    className="input top2"
                    onChange={(e) => setPassword1(e.target.value)}
                    placeholder="Пароль"
                ></input>
                <button className="bnt_login_form" onClick={login}>
                    Войти
                </button>
            </div>
            <div className={`login_form reg_form ${close_reg_form}`}>
                <h3 className="h3_1" onClick={openRegistrationsForm}>
                    Вход
                </h3>
                <h3 className="h3_2_1">Регистрация</h3>
                <input
                    className="input top1_1"
                    placeholder="Имя"
                    onChange={(e) => setName(e.target.value)}
                ></input>
                <input
                    className="input top2_2"
                    placeholder="Никнейм"
                    onChange={(e) => setNickname2(e.target.value)}
                ></input>
                <input
                    className="input top3"
                    placeholder="Пароль"
                    onChange={(e) => setPassword2_1(e.target.value)}
                ></input>
                <input
                    className="input top4"
                    placeholder="Повторите пароль"
                    onChange={(e) => setPassword2_2(e.target.value)}
                ></input>
                <button
                    className="bnt_login_form dop_styles"
                    onClick={registration}
                >
                    Зарегистрироваться
                </button>
            </div>
        </div>
    );
}

export default Page1;
