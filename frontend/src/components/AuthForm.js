import React from "react";
import { useFormAndValidation } from "../hooks/useFormAndValidation";

function AuthForm({ onSubmit, name, buttonText }) {
    const initialState = { email: '', password: ''};
    const { values, handleChange, errors, isValid, setValues, resetForm } = useFormAndValidation(initialState);

    React.useEffect(() => {
        resetForm(initialState, initialState);
    }, []);

    function handleSubmit(e) {
        e.preventDefault();
        if (isValid) {
            onSubmit(values.password, values.email);
        }
    }

    return (
        <form onSubmit={handleSubmit} name={`form-${name}`} className="form" noValidate>
            <input id="email" value={values.email} onChange={handleChange} name="email" type="email" className="form__input" placeholder="Email" minLength="2" maxLength="40" required />
            <span className="form__input-error">{errors.email}</span>
            <input id="password" value={values.password} onChange={handleChange} name="password" type="password" className="form__input" placeholder="Password" minLength="6" maxLength="200" required />
            <span className="form__input-error">{errors.password}</span>
            <button className="form__save-btn form__save-btn_theme_dark" type="submit">{buttonText}</button>
        </form>
    );
}

export default AuthForm;
