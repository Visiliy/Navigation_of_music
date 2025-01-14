import { useState } from "react";
import axios from "axios";
import "./ux_ui/main.css";
import "./ux_ui/main2.css";
import "./ux_ui/form.css";
import "./ux_ui/btn1.css";
import "./ux_ui/sending_audio_form.css";
import Name from "./components/name";
import getCookie from "./modules/getCookie";

function Page1() {
    const [openForm, setOpenForm] = useState(true);
    const [openRegForm, setOpenRegForm] = useState(false);
    const [sending, setSending] = useState(false);
    const [response, setResponse] = useState([[undefined, undefined]]);

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
                console.log(response.data[0]);
                let ans = response.data[0];
                if (ans[0] == false && ans[1] == false) {
                    alert("Неверный пароль");
                } else if (ans[0] == false && ans[1] == true) {
                    alert("Ошибка на сервере");
                } else if (ans[0] == true && ans[1] == true) {
                    document.cookie = `nickname=${nickname1};max-age=2592000`;
                    document.cookie = `name=${ans[2]};max-age=2592000`;
                    openLoginForm();
                } else {
                    alert("Нет такого аккаунта");
                }
            })
            .catch((error) => {
                console.log(error);
                alert("Ошибка на сервере или проблема с интернетом");
            });
    };

    const registration = () => {
        if (
            password2_1 == password2_2 &&
            password2_1.split(" ").length == 1 &&
            password2_1 != "" &&
            name.split(" ").length == 1 &&
            name != "" &&
            nickname2.split(" ").length == 1 &&
            nickname2 != "" &&
            password2_2.split(" ").length == 1 &&
            password2_2 != ""
        ) {
            var data = [name, nickname2, password2_1];
            axios
                .post("http://127.0.0.1:8070/user_registration", data)
                .then((response) => {
                    console.log(response.data[0]);
                    let ans = response.data[0];
                    if (ans[0] == false && ans[1] == false) {
                        alert("Такой никнейм есть, придумайте новый");
                    } else if (ans[0] == false && ans[1] == true) {
                        alert("Ошибка на сервере");
                    } else {
                        document.cookie = `nickname=${nickname2};max-age=2592000`;
                        document.cookie = `name=${name};max-age=2592000`;
                        openLoginForm();
                    }
                })
                .catch((error) => {
                    console.log(error);
                    alert("Ошибка на сервере или проблема с интернетом");
                });
        } else {
            alert("Пароли не совпадают или введено недопустимое значение");
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

    const toHome = () => {
        window.location.href = "/home";
    };

    const closeMusicForm = () => {
        list1 = "display_none";
        list2 = "display_none";
        setResponse([[undefined, undefined]]);
    }

    const sendAudioContentToServer = () => {
        if (getCookie("name") == undefined) {
            alert("Вы не авторизовались");
        } else {
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
                    const audioBlob = new Blob(audioChunks, {
                        type: "audio/wav",
                    });
                    audioChunks = [];
                    const formData = new FormData();
                    formData.append("audio", audioBlob);
                    axios
                        .post("http://127.0.0.1:8070/get_music", formData)
                        .then((response) => {
                            console.log(response.data[0]);
                            setResponse(response.data[0]);
                            setSending(false);
                        })
                        .catch((error) => {
                            console.log(error);
                            alert(
                                "Ошибка на сервере или проблема с интернетом"
                            );
                        });
                };

                mediaRecorder.start();
            }
            getAudio();
            const stopRecords = () => {
                mediaRecorder.stop();
            };
            setTimeout(stopRecords, 15000);
        }
    };

    var close_form = "display_none";
    var close_playe1 = "";
    var close_playe2 = "";
    var close_playe3 = "display_none";
    var not_fon = "";
    var close_reg_form = "display_none";
    var close_send_form = "display_none";
    var close_playe4 = "display_none";
    var close_playe5 = "";
    var close_playe6 = "display_none";
    var close_btn = "";
    var list1 = "";
    var list2 = "display_none";

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
        close_playe4 = "display_none";
    }

    if (sending) {
        not_fon = "main_2_0";
        close_send_form = "";
        close_playe2 = "display_none";
        close_playe4 = "display_none";
    }

    if (getCookie("nickname") != undefined) {
        close_playe4 = "";
        close_btn = "display_none";
    }

    if (response[0][0] != undefined) {
        if (response[0][0] == 0) {
            list1 = "display_none";
            list2 = "";
        }
        not_fon = "main_2_0";
        close_playe5 = "display_none";
        close_playe6 = "";
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
                    className={`btn1 ${close_playe1} ${close_btn}`}
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
                <button
                    className={`btn1 ${close_playe4}`}
                    style={{ zIndex: 10 }}
                    onClick={toHome}
                >
                    Аккаунт
                </button>
            </div>
            <button className="about">О проекте</button>
            <div
                className={`player ${close_playe1} ${close_playe2} ${close_playe5}`}
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
                    type="password"
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
                    maxLength={10}
                ></input>
                <input
                    className="input top2_2"
                    placeholder="Никнейм"
                    onChange={(e) => setNickname2(e.target.value)}
                ></input>
                <input
                    type="password"
                    className="input top3"
                    placeholder="Пароль"
                    onChange={(e) => setPassword2_1(e.target.value)}
                ></input>
                <input
                    type="password"
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
            <div className={`music_response ${close_playe6}`}>
                <div className={`list1 ${list1}`}>
                    <center>
                        <h2 className="main_music">{response[0][1]}<p className="service_img">💜</p></h2>
                    </center>
                    <center>
                        <h2 className="service_text">
                            Возможно, вы искали это:
                        </h2>
                    </center>
                    {response.slice(1).map((text) => (
                        <h2 key={text[0]} className="main_music_2">
                            {text[1]}
                            <p className="service_img">💜</p>
                        </h2>
                    ))}
                </div>
                <div className={`list2 ${list2}`}>
                    <center>
                        <h2 className="service_text" style={{ color: "aqua" }}>
                            Ничего не найдено
                        </h2>
                    </center>
                    <center>
                        <h2 style={{ color: "aqua", userSelect: "none" }}>
                            Упс :(
                        </h2>
                    </center>
                </div>
                <div onClick={closeMusicForm} className="close"></div>
            </div>
        </div>
    );
}

export default Page1;
