import { CardV2, FaIcon, FaIcons } from "../plugin/core/bs.3.mts";
import MarAdmin, { MarMenu } from "../plugin/core/theme/mar/mar.mts";
import AboutMe from "./about/me.mts";
import Projects from "./project/proj.mts";

class Dashboard extends MarAdmin {

  constructor() {
    super({
      title: "Marjon Cajocon",
      topBarColor: "#00C853",
      sideMenu: [
        new MarMenu({
          logo: new FaIcon(FaIcons.QuestionCircle),
          title: "About Me",
          click: () => {
            this.route(new CardV2({body: new AboutMe(), bodyPadding: true}));
          }
        }),
        new MarMenu({
          logo: new FaIcon(FaIcons.FolderOpen),
          title: "Projects",
          click: () => {
            this.route(new Projects());
          }
        })
      ]
    });

    this.route(new CardV2({body: new AboutMe(), bodyPadding: true}));
  }

}

export default Dashboard;