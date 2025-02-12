import Page1 from "./Page1";
import Page2 from "./Page2";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Page3_2 from "./Page3_2";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="" element={<Page1 />} />
                <Route path="home" element={<Page2 />} />
                <Route path="about" element={<Page3_2 />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
