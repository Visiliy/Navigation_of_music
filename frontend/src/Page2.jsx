import "./ux_ui/page_two.css";
import "./ux_ui/btn1.css";
import getCookie from "./modules/getCookie";
import { useState } from "react";

const Page2 = () => {
    if (getCookie("nickname") == undefined) {
        window.location.href = "/";
    }

    const [data1, setData1] = useState([[1, "Музыкальные произведения", "Три белых коня"]]);
    const [data2, setData2] = useState([
        [1, "15:01:2025", "День Победы", "Месяц май", "Три белых коня"],
        [2, "15:01:2025", "День Победы", "Месяц май", "Три белых коня"],
    ]);
    const [switch_w, setSwitch] = useState(true);

    const toMain = () => {
        window.location.href = "/";
    };

    const switch_form = () => {
        setSwitch(!switch_w);
    };

    const exit = () => {
        document.cookie = "nickname=;max-age=-1";
        document.cookie = "name=;max-age=-1";
        console.log("exit");
        window.location.href = "/";
    };

    let one = "";
    let two = "display_none";

    if (switch_w == false) {
        one = "display_none";
        two = "";
    }

    return (
        <div className="main">
            <button className="btn1" onClick={toMain}>
                Назад
            </button>
            <div className="center">
                <img className="img4" src="src/img/j.png" />
                <span className="span">{getCookie("name")}</span>
                <button className={`btn3 margin_left1 btn_fon1 ${one}`}>
                    Избранное
                </button>
                <button
                    onClick={switch_form}
                    className={`btn3 margin_right2 btn_fon2 ${one}`}
                >
                    История
                </button>
                <button
                    onClick={switch_form}
                    className={`btn3 margin_left1 btn_fon2 ${two}`}
                >
                    Избранное
                </button>
                <button className={`btn3 margin_right2 btn_fon1 ${two}`}>
                    История
                </button>
                <div className={`favourites_data ${one}`}>
                    {data1.map((data) => (
                        <div key={data[0]} className="favorites_div">
                            <h2 key={data[0]} className="favorites_text">
                                {data[1]}
                            </h2>
                            {data.slice(2).map((music_name) => (
                                <h2 key={data[0]} className="favourites_h2">{music_name}</h2>
                            ))}
                        </div>
                    ))}
                </div>
                <div className={`favourites_data ${two}`}>
                    {data2.map((data) => (
                        <div key={data[0]} className="favorites_div">
                            <h2 key={data[0]} className="favorites_text">
                                {data[1]}
                            </h2>
                            {data.slice(2).map((music_name) => (
                                <h2 key={data[0]} className="favourites_h2">{music_name}</h2>
                            ))}
                        </div>
                    ))}
                </div>
            </div>
            <a className="link" onClick={exit}>
                Выход
            </a>
        </div>
    );
};

export default Page2;
