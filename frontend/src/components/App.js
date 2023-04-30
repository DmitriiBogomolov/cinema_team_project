import React from "react";
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import ProtectedRoute from "./ProtectedRoute.js";
import Header from "./Header.js";
import Main from "./Main.js";
import Footer from "./Footer.js";
import Login from "./Login.js";
import { api } from "../utils/Api";
import { currentUser, CurrentUserContext } from "../contexts/CurrentUserContext.js";
import Register from "./Register.js";
import * as auth from '../utils/auth.js';

function App() {
  const [currentUserState, setCurrentUser] = React.useState(currentUser);
  const [cards, setCards] = React.useState([]);
  const [email, setEmail] = React.useState(null);
  const [userId, setUserId] = React.useState(null);
  const [message, setMessage] = React.useState({ type: '', text: '' });

  // React.useEffect(() => {
  //   auth.validateToken(localStorage.getItem('token'))
  //     .then((data) => {
  //       if (data) {
  //         setEmail(data.data.email);
  //       }
  //     })
  //     .catch(err => {
  //       console.error(err);
  //     })
  // }, []);

  // React.useEffect(() => {
  //   Promise.all(
  //     [api.getUserInfo(),
  //     api.getInitialCards()])
  //     .then(([userData, cards]) => {
  //       setCurrentUser(userData);
  //       setCards(cards);
  //     })
  //     .catch(err => {
  //       console.error(err);
  //     })
  // }, []);

  const handleRegisterUser = (password, email) => {
    auth.register(email, password)
      .then(res => {
        console.log(res);
        setUserId(res.id);
        setMessage({ type: 'success', text: 'Вы успешно зарегистрировались!' });
      }).catch(err => {
        console.log(err);
        setMessage({ type: 'error', text: 'Что-то пошло не так! Попробуйте ещё раз.' });
      }).finally(() => {
      });
  }

  const handleLoginUser = (password, email) => {
    auth.login(email, password)
      .then(res => {
        console.log(res);
        localStorage.setItem('token', res.token);
        setEmail(email);
      }).catch(err => {
        console.log(err);
        setMessage({ type: 'error', text: 'Что-то пошло не так! Попробуйте ещё раз.' });
      });
  }

  const handleSignOut = () => {
    localStorage.removeItem('token');
    setEmail(null);
  }

  return (
    <CurrentUserContext.Provider value={currentUserState}>
      <BrowserRouter>
        <Header email={email} onSignOut={handleSignOut} />
        <Routes>
          <Route path='/'
            element={<ProtectedRoute
              element={Main}
              loggedIn={email}
              cards={cards}
            />}
          />
          <Route path='/sign-in' element={email ? <Navigate to="/" replace /> : <Login message={message} onLogin={handleLoginUser} name='login' buttonText='Войти'/>} />
          <Route path='/sign-up' element={email ? <Navigate to="/" replace /> : <Register message={message} onRegister={handleRegisterUser} name='register' buttonText='Зарегистрироваться' />} />
        </Routes>
        <Footer />

      </BrowserRouter>
    </CurrentUserContext.Provider>
  );
}

export default App;
