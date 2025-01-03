import Name from "./components/name";
import "./ux_ui/page_two.css";
import "./ux_ui/btn1.css";

const Page2 = () => {
    return (
        <div className="main">
            <div className="left">
                <Name></Name>
            </div>
            <button className="btn1">Назад</button>
            <div className="center">
                <img className="img2" src="src/img/j.png" />
                <span className="span">Username</span>
                <button className="btn3">Избранное</button>
            </div>
        </div>
    );
};

export default Page2;
