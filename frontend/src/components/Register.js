import React from "react";
import { Link } from "react-router-dom";
import AuthForm from "./AuthForm";

function Register({ onRegister, name, buttonText, message }) {
    return (
        <div className='auth'>
            {message.text && <h2 className={`auth__message_${message.type} auth__message`}>{message.text}</h2>}
            <AuthForm onSubmit={onRegister} name={name} buttonText={buttonText} />
            <Link to='/sign-in' className="auth__login-link">Уже зарегистрированы? Войти</Link>
        </div>
    )
}

export default Register;
