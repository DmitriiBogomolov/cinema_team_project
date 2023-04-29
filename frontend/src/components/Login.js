import React from "react";
import AuthForm from "./AuthForm";

function Login({ onLogin, name, buttonText, message }) {
    return (
        <div className='auth'>
            {message.text && <h2 className={`auth__message_${message.type} auth__message`}>{message.text}</h2>}
            <AuthForm onSubmit={onLogin} name={name} buttonText={buttonText} />
        </div>
    )
}

export default Login
