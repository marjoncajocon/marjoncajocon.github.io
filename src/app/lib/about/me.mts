import { Button, CardV2, Html, Panel } from "../../plugin/core/bs.3.mts";

class AboutMe extends Panel {
    constructor() {
        super();

        super.Add(new CardV2({body: new Html({text: `
            <style>
                body {
                    font-family: "Poppins", sans-serif;
                    margin: 0;
                    padding: 0;
                    background: #f5f6fa;
                    color: #333;
                    line-height: 1.7;
                }

                .container {
                    max-width: 900px;
                    margin: 60px auto;
                    padding: 20px 30px;
                    background: #ffffff;
                    border-radius: 12px;
                    box-shadow: 0 12px 25px rgba(0,0,0,0.08);
                    animation: fadeIn 0.8s ease;
                }

                h1 {
                    text-align: center;
                    margin-bottom: 25px;
                    font-size: 34px;
                    color: #2c3e50;
                }

                p {
                    font-size: 17px;
                    margin-bottom: 18px;
                    text-align: justify;
                }

                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
            </style>

            <h1>About Me</h1>

            <p>
                I am a passionate programmer and full-stack designer with a strong dedication
                to building clean, efficient, and user-centered digital experiences. With a solid
                foundation across both frontend and backend development, I enjoy turning concepts
                into fully functioning applications that balance performance, usability, and
                visual appeal.
            </p>

            <p>
                On the frontend, I specialize in TypeScript, where I focus on creating dynamic,
                responsive, and intuitive interfaces. My design background allows me to create
                visually appealing layouts while maintaining functional clarity, ensuring every
                project looks polished and performs smoothly.
            </p>

            <p>
                For backend development, I work with Go, Python, PHP, and C/C++. This diverse
                technology stack enables me to choose the most effective language for each
                project's needs—whether it's high-performance APIs in Go, automation tools in
                Python, robust services in PHP, or performance-critical components in C/C++.
            </p>

            <p>
                I strongly believe in clean code, scalable architecture, and thoughtful design.
                Problem-solving, performance optimization, and seamless user experience are at the
                core of my development approach. I stay committed to continuous learning to keep
                my skills sharp and modern.
            </p>

            <p>
                My goal moving forward is to take on more challenging full-stack projects and
                contribute to innovative software solutions. I aim to combine advanced backend
                systems with intuitive frontend experiences, creating applications that are both
                powerful and beautifully designed.
            </p>    
        `})}).AddStyle({
            "padding": "10px"
        }));
    }
}

export default AboutMe;