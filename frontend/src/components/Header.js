import React from "react";
import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";

function Header({ onSignOut, email }) {
    const location = useLocation();

    return (
        <header className="header">
            <div className="header__logo"></div>
            <div className="header__links">
                {email && <div className="header__email">{email}</div>}
                {location.pathname === '/' && <button onClick={onSignOut} className="header__link" type="button">Выйти</button>}
                {location.pathname === '/sign-up' && <Link to="/sign-in" className="header__link">Войти</Link>}
                {location.pathname === '/sign-in' && <Link to="/sign-up" className="header__link">Регистрация</Link>}
            </div>
        </header>
    );
}

export default Header;
