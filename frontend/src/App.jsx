import Page1 from "./Page1";
import Page2 from "./Page2";
import { BrowserRouter, Route, Routes } from "react-router-dom";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="" element={<Page1 />} />
                <Route path="home" element={<Page2 />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
