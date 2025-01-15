import "./ux_ui/page3.css";
import "./ux_ui/btn1.css";

const Page3 = () => {

    const toMain = () => {
        window.location.href = "/";
    };

    return (
        <div className="main">
            <button className="btn1" onClick={toMain}>
                Назад
            </button>
            <div className="wrapper">

            </div>
        </div>
    );
}

export default Page3;