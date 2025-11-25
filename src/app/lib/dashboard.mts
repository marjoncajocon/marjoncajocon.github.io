import { CardV2, FaIcon, FaIcons } from "../plugin/core/bs.3.mts";
import LTEApp, { LTEMenuButton } from "../plugin/core/lte.3.mts";
import AboutMe from "./about/me.mts";
import Projects from "./project/proj.mts";

class Dashboard extends LTEApp {

  constructor() {
    super({
      userName: "MARJ",
      logo: "res/profile.jpg",
      userPhoto: "res/profile.jpg",
      title: "MARJON CAJOCON",
      sideMenu: [
        new LTEMenuButton({
          icon: FaIcons.QuestionCircle,
          title: "About Me",
          fn: () => {
            this.route({
              title: "About Me",
              page: ["MARJ", "About Me"],
              body: new AboutMe()
            });
          }
        }),
        new LTEMenuButton({
          icon: FaIcons.FolderOpen,
          title: "My Projects",
          fn: () => {
            this.route({
              title: "About Me",
              page: ["MARJ", "My Project"],
              body: new Projects()
            });
          }
        })
      ]
    });

    this.route({
      title: "About Me",
      page: ["MARJ", "About Me"],
      body: new AboutMe()
    });
  }

}

export default Dashboard;