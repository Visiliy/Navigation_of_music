import "./ux_ui/btn1.css";
import "./ux_ui/page3_2.css";

const Page3_2 = () => {
    const toMain = () => {
        window.location.href = "/";
    };

    const open = (div, btn, i, div_wrapper) => {
        if (i % 2 == 0) {
            div.style.height = "70%";
            btn.textContent = "Закрыть";
            div_wrapper.classList.remove("display_none");
            div_wrapper.style.opacity = 0;
            setTimeout(() => {
                const interval = setInterval(() => {
                    div_wrapper.style.opacity =
                        parseFloat(div_wrapper.style.opacity) + 0.05;
                    if (div_wrapper.style.opacity >= 1) {
                        clearInterval(interval);
                    }
                }, 20);
            }, 1500);
        } else {
            div.style.height = "15%";
            btn.textContent = "Открыть";
            div_wrapper.classList.add("display_none");
        }
    };

    const openForm = (img, i) => {
        if (i % 2 == 0) {
            img.style.opacity = 1;
            setTimeout(() => {
                const interval = setInterval(() => {
                    img.style.opacity = parseFloat(img.style.opacity) - 0.02;
                    if (img.style.opacity <= 0) {
                        clearInterval(interval);
                    }
                }, 50);
            }, 500);
        } else {
            img.style.opacity = 0;
            setTimeout(() => {
                const interval = setInterval(() => {
                    img.style.opacity = parseFloat(img.style.opacity) + 0.02;
                    if (img.style.opacity >= 1) {
                        clearInterval(interval);
                    }
                }, 50);
            }, 500);
        }
    };

    let i1 = 0;
    let i2 = 0;
    let i3 = 0;

    let i4 = 0;
    let i5 = 0;
    let i6 = 0;

    const open1 = () => {
        const div1 = document.querySelector(".div1");
        const btn = document.querySelector("#btn1");
        const div_wrapper1 = document.querySelector(".div_wrapper1");

        open(div1, btn, i1, div_wrapper1);
        i1++;
    };

    const open2 = () => {
        const div2 = document.querySelector(".div2");
        const btn = document.querySelector("#btn2");
        const div_wrapper2 = document.querySelector(".div_wrapper2");

        open(div2, btn, i2, div_wrapper2);
        i2++;
    };

    const open3 = () => {
        const div3 = document.querySelector(".div3");
        const btn = document.querySelector("#btn3");
        const div_wrapper3 = document.querySelector(".div_wrapper3");

        open(div3, btn, i3, div_wrapper3);
        i3++;
    };

    const openForm1 = () => {
        const img = document.querySelector(".sticer1");

        openForm(img, i4);
        i4++;
    };

    const openForm2 = () => {
        const img = document.querySelector(".sticer2");

        openForm(img, i5);
        i5++;
    };

    const openForm3 = () => {
        const img = document.querySelector(".sticer3");

        openForm(img, i6);
        i6++;
    };

    return (
        <div className="main">
            <button className="btn1" onClick={toMain}>
                Назад
            </button>
            <div className="wrapper_div div1">
                <h1 className="text_h1">Введение</h1>
                <div className="div_wrapper1 display_none">
                    <h2 className="text_h2" id="text">
                        Цель нашего проекта – улучшить поиск музыки, сделать его
                        быстрым и удобным. Мы в начале большого пути. Нам ещё
                        много предстоит сделать, чтобы добиться желаемого
                        результата. Впереди много вызовов, задач, проблем, но мы
                        смело смотрим в будущее и приложим все усилия, чтобы
                        довести дело до конца. То, что вы видите – это немалая
                        часть упорной работы, в которую были вложены силы, время
                        и душа. Мы уверены, что пользование веб-приложением
                        принесёт вам пользу и положительные эмоции.
                    </h2>
                </div>
                <button
                    onClick={open1}
                    className="open_and_close_btn"
                    id="btn1"
                >
                    Открыть
                </button>
            </div>
            <div className="wrapper_div div2">
                <h1 className="text_h1">Инструкция</h1>
                <div className="div_wrapper2 display_none">
                    <h2 className="text_h2_2">
                        1. Авторизуйтесь в веб-приложении (войдите в аккаунт или
                        зарегистрируйтесь).
                    </h2>
                    <h2 className="text_h2_2">2. Нажмите на кнопку «Плеер».</h2>
                    <h2 className="text_h2_2">
                        3. Спойте отрывок из песни, находясь недалеко от
                        микрофона.
                    </h2>
                    <h2 className="text_h2_2">
                        4. Полученный результат можете добавить в «Избранное».
                    </h2>
                    <h2 className="text_h2_2">
                        5. На странице «Аккаунт» отображаются избранные песни и
                        история поиска.
                    </h2>
                    <h2 className="text_h2_2">
                        6. Чтобы выйти из аккаунта, нажмите на кнопку «Выйти» в
                        левом нижнем углу веб-приложения.
                    </h2>
                </div>
                <button
                    onClick={open2}
                    className="open_and_close_btn"
                    id="btn2"
                >
                    Открыть
                </button>
            </div>
            <div className="wrapper_div div3">
                <h1 className="text_h1">Прогнозируемый результат</h1>
                <div className="div_wrapper3 display_none">
                    <h2 className="text_h2_2">
                        1. Определять музыку по тону и частоте.
                    </h2>
                    <h2 className="text_h2_2">
                        2. Определять музыку за меньшее время.
                    </h2>
                    <h2 className="text_h2_2">
                        3. Добавить генерацию мелодий по настроению.
                    </h2>
                    <h2 className="text_h2_2">4. Улучшение качества поиска.</h2>
                    <h2 className="text_h2_2">
                        5. Интеграция с Яндекс Музыкой.
                    </h2>
                    <h2 className="text_h2_2">6. Монетизация проекта.</h2>
                    <h2 className="text_h2_2">
                        7. Запуск мобильного приложения.
                    </h2>
                </div>
                <button
                    onClick={open3}
                    className="open_and_close_btn"
                    id="btn3"
                >
                    Открыть
                </button>
            </div>
            <img
                className="sticer1"
                src="src/img/photo_2025-02-01_21-29-23.jpg"
                onClick={openForm1}
            ></img>
            <img
                className="sticer2"
                src="src/img/i (2).jpg"
                onClick={openForm2}
            ></img>
            <img
                className="sticer3"
                src="src/img/i (1).jpg"
                onClick={openForm3}
            ></img>
            <div className="content div1">
                <h1 className="text_h1">Авторы</h1>
                <div style={{ marginTop: "25%" }}>
                    <h1 className="text_h1">Шкуратов Василий</h1>
                    <h1 className="text_h1">Быканова Наталья</h1>
                </div>
            </div>
            <div className="content div2">
                <h1 className="text_h1">Затраченное время</h1>
                <div style={{ marginTop: "25%" }}>
                    <h1 className="text_h1">1,5 мясяца упорной работы</h1>
                </div>
            </div>
            <div className="content div3">
                <h1 className="text_h1">Место разработки</h1>
                <div style={{ marginTop: "25%" }}>
                    <h1 className="text_h1">
                        GitHub
                    </h1>
                </div>
            </div>
        </div>
    );
};

export default Page3_2;
