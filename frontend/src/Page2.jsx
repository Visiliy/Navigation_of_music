import "./ux_ui/page_two.css";
import "./ux_ui/btn1.css";
import getCookie from "./modules/getCookie";

const Page2 = () => {

    const toMain = () => {
        window.location.href = "/";
    }

    const exit = () => {
        document.cookie = "nickname=;max-age=-1";
        document.cookie = "name=;max-age=-1";
        console.log("exit");
        window.location.href = "/";
    }

    if (getCookie("nickname") == undefined) {
        window.location.href = "/";
    }

    return (
        <div className="main">
            <button className="btn1" onClick={toMain}>Назад</button>
            <div className="center">
                <img className="img4" src="src/img/j.png" />
                <span className="span">{getCookie("name")}</span>
                <button className="btn3 margin_left1 btn_fon1">Избранное</button>
                <button className="btn3 margin_right2 btn_fon2">История</button>
            </div>
            <a className="link" onClick={exit}>Выход</a>
        </div>
    );
};

export default Page2;
