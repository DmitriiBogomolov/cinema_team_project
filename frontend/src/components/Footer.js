import React from "react";

function Footer() {
    return (
        <footer className="footer">
            <p className="footer__copyright">© {new Date().getFullYear()} Filmworks Service <a className="footer__copyright" href='https://github.com/wrawka/Team-12-Async-API' target="_blank">GitHub</a>
            </p>
        </footer>
    );
}

export default Footer;
