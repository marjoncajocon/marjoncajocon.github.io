import { Button, Html, Panel } from "../../plugin/core/bs.3.mts";

class Projects extends Panel {
    constructor() {
        super();

        super.Add(new Html({text: `

            <style>
            body {
                font-family: "Poppins", sans-serif;
                margin: 0;
                padding: 0;
                background: #f4f6f9;
                color: #333;
                line-height: 1.7;
            }

            .section {
                max-width: 900px;
                margin: 30px auto;
                padding: 25px 30px;
                background: #fff;
                border-radius: 12px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.08);
                animation: fadeIn 0.6s ease;
            }

            h2 {
                color: #2c3e50;
                margin-bottom: 10px;
            }

            p {
                text-align: justify;
                font-size: 16px;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            h1 {
                text-align: center;
                margin-bottom: 25px;
                font-size: 34px;
                color: #2c3e50;
            }

            </style>
            <br>
            <h1>About My Projects</h1>

            <!-- HRMS -->
            <div class="section" id="hrms">
                <h2>Human Resource Management System</h2>
                <p>
                    The Human Resource Management System is designed to streamline and automate the essential
                    processes within an organization’s HR department. It centralizes employee records, attendance
                    tracking, leave management, and performance evaluations into one efficient platform. By
                    reducing manual work and minimizing errors, the system improves overall workflow and helps HR
                    teams focus more on strategic planning. Its user-friendly interface and secure data handling
                    ensure that employees and administrators can access information quickly and safely.
                </p>
            </div>

            <!-- Payroll -->
            <div class="section" id="payroll">
                <h2>Payroll System</h2>
                <p>
                    The Payroll System is built to manage salary computation with accuracy, speed, and consistency.
                    It automates calculations for wages, deductions, taxes, and benefits to ensure employees are
                    paid correctly and on time. The system also generates detailed reports that assist in financial
                    planning and compliance with government regulations. By integrating payroll with attendance and
                    HR data, it eliminates repetitive work and significantly reduces the risk of human error.
                </p>
            </div>

            <!-- Ticketing -->
            <div class="section" id="ticketing">
                <h2>Ticketing System</h2>
                <p>
                    The Ticketing System provides an organized platform for handling support requests, technical
                    issues, and customer inquiries. It allows users to submit tickets, track their progress, and
                    receive timely updates. For administrators, the system includes features such as priority
                    tagging, assignment tools, status monitoring, and performance reporting. This helps teams
                    resolve issues faster, improve service quality, and maintain smooth communication between users
                    and support personnel.
                </p>
            </div>

            <!-- Financial System -->
            <div class="section" id="financial">
                <h2>Financial System (Current Project)</h2>
                <p>
                    The Financial System is my current and most advanced project, focused on managing an
                    organization’s financial operations with precision and transparency. It includes modules for
                    budgeting, expense tracking, revenue monitoring, audits, and financial reporting. The system is
                    designed to provide real-time insights into financial health, helping decision-makers plan
                    effectively and maintain full control over resources. With secure data handling and optimized
                    performance, this platform aims to become a reliable and scalable tool for long-term financial
                    management.
                </p>
            </div>

            <!-- Frontend Framework -->
            <div class="section" id="framework">
                <h2>Custom Front-End Framework (In Development)</h2>
                <p>
                    I am also developing my own custom front-end framework aimed at providing a robust, scalable,
                    and developer-friendly environment for building modern web applications. This framework focuses
                    on improving performance, simplifying UI logic, and offering reusable components that speed up
                    development. Although it is still under active development and not yet publicly announced or
                    released, the framework represents my commitment to advancing efficient front-end engineering
                    and contributing new ideas to the development community.
                </p>
            </div>

            <div class="section" id="game-dev">
                <h2>2D Game Developer (Self-Business)</h2>
                <p>
                    I also work as a 2D game developer, creating small-scale games through my own self-run
                    business. Although I am not yet fully experienced in the field, I continue to learn and
                    experiment with game mechanics, design principles, and interactive storytelling. This ongoing
                    journey allows me to enhance my creativity and technical skills while exploring different tools
                    and engines for game development. My goal is to eventually expand this passion into a more
                    established game development line of work.
                </p>
            </div>

            <!-- Other Projects -->
            <div class="section" id="other-projects">
                <h2>Other Projects</h2>
                <p>
                    Over the past years, I have also built nearly 10 other projects that span various categories
                    including automation tools, management systems, custom utilities, and experimental prototypes.
                    Each project has contributed to my growth as a developer, allowing me to explore new
                    technologies, improve my coding practices, and gain hands-on experience in solving real-world
                    problems. These additional works highlight my consistency, creativity, and dedication to
                    continuous improvement in software development.
                </p>
            </div>
    
        `}));
    }
}
export default Projects;