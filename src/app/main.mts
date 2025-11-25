import Dashboard from "./lib/dashboard.mts";
import "./plugin/core/bootstrap3/css/theme-lumen.css";

import {Theme, Window} from "./plugin/core/core.mjs";

const MyApp = new Window();

MyApp.Navigate(new Dashboard());

MyApp.Run();

export default MyApp;


/// attribute in the html tag for dark mode and light mode: data-bs-theme="dark"