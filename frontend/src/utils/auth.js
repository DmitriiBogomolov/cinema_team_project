const BASE_URL = 'http://localhost:5000/api/v1';

const headers = {
  "Content-Type": "application/json"
}

const _request = (url, options) => {
  return fetch(url, options)
    .then(res => {
      return _getResponseData(res);
    })
}

const _getResponseData = (res) => {
  if (!res.ok) {
    return Promise.reject(`Ошибка: ${res.status}`);
  }
  return res.json();
}

export const register = (email, password) => {
  return _request(`${BASE_URL}/register`, {
    headers: {
      "Accept": "application/json",
      ...headers
    },
    method: 'POST',
    body: JSON.stringify({ email, password })
  });
};

export const login = (username, password) => {
  return _request(`${BASE_URL}/login`, {
    headers: {
      "Accept": "application/json",
      ...headers
    },
    method: 'POST',
    body: JSON.stringify({ username, password })
  });
};

export const validateToken = (jwt) => {
  return _request(`${BASE_URL}/users/me`, {
    headers: {
      "Authorization": `Bearer ${jwt}`,
      ...headers
    },
    method: 'GET'
  });
};
