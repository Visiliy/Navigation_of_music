import { useState } from "react";
import "./ux_ui/main.css";
import "./ux_ui/main2.css";
import "./ux_ui/sending_audio_form.css";
//import sendingMusic from "./modules/sendingMusic";

function App() {
    const [openForm, setOpenForm] = useState(true);
    const [openRegForm, setOpenRegForm] = useState(false);
    const [sending, setSending] = useState(false);

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
        //const answer = sendingMusic();
        //console.log(answer, "100");
    };

    var close_form = "display_none";
    var close_playe1 = "";
    var close_playe2 = "";
    var not_fon = "";
    var close_reg_form = "display_none";
    var close_send_form = "display_none";

    if (!openForm) {
        close_form = "";
        close_playe1 = "display_none";
        not_fon = "main_2_0";
    }

    if (openRegForm && not_fon != "") {
        close_reg_form = "";
        close_form = "display_none";
    }

    if (sending) {
        not_fon = "main_2_0";
        close_send_form = "";
        close_playe2 = "display_none";
    }

    return (
        <div className={`main ${not_fon}`}>
            <div className="left">
                <h1 className="name">Navigation of music</h1>
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
                <input className="input top1" placeholder="Имя"></input>
                <input className="input top2" placeholder="Никнейм"></input>
                <button className="bnt_login_form" onClick={openLoginForm}>
                    Войти
                </button>
            </div>
            <div className={`login_form reg_form ${close_reg_form}`}>
                <h3 className="h3_1" onClick={openRegistrationsForm}>
                    Вход
                </h3>
                <h3 className="h3_2_1">Регистрация</h3>
                <input className="input top1_1" placeholder="Имя"></input>
                <input className="input top2_2" placeholder="Никнейм"></input>
                <input className="input top3" placeholder="Пароль"></input>
                <input
                    className="input top4"
                    placeholder="Повторите пароль"
                ></input>
                <button
                    className="bnt_login_form dop_styles"
                    onClick={openLoginForm}
                >
                    Зарегистрироваться
                </button>
            </div>
        </div>
    );
}

export default App;
