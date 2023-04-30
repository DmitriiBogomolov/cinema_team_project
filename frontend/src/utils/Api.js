/** API */
import { serverUrl, groupId, personalToken } from "./constants";

class Api {
    constructor({ baseUrl, headers }) {
        this._baseUrl = baseUrl;
        this._headers = headers;
    }

    _request(url, options) {
        return fetch(url, options)
            .then(res => {
                return this._getResponseData(res);
            })
    }

    _getResponseData(res) {
        if (!res.ok) {
            return Promise.reject(`Ошибка: ${res.status}`);
        }
        return res.json();
    }

    getUserInfo() {
        return this._request(`${this._baseUrl}/users/me`, {
            headers: this._headers
        })
    }

    updateUserInfo(userInfo) {
        return this._request(`${this._baseUrl}/users/me`, {
            headers: this._headers,
            method: 'PATCH',
            body: JSON.stringify(userInfo)
        })
    }

    updateAvatar(url) {
        return this._request(`${this._baseUrl}/users/me/avatar`, {
            headers: this._headers,
            method: 'PATCH',
            body: JSON.stringify(url)
        })
    }

    getInitialCards() {
        return this._request(`${this._baseUrl}/cards`, {
            headers: this._headers
        })
    }

    addCard(card) {
        return this._request(`${this._baseUrl}/cards`, {
            headers: this._headers,
            method: 'POST',
            body: JSON.stringify(card)
        })
    }

    removeCard(cardId) {
        return this._request(`${this._baseUrl}/cards/${cardId}`, {
            headers: this._headers,
            method: 'DELETE'
        })
    }

    addLike(cardId) {
        return this._request(`${this._baseUrl}/cards/${cardId}/likes`, {
            headers: this._headers,
            method: 'PUT'
        })
    }

    removeLike(cardId) {
        return this._request(`${this._baseUrl}/cards/${cardId}/likes`, {
            headers: this._headers,
            method: 'DELETE'
        })
    }

    changeLikeCardStatus(cardId, isLiked) {
        if (isLiked) {
            return this.removeLike(cardId);
        } else {
            return this.addLike(cardId);
        }
    }
}

export const api = new Api({
    baseUrl: `${serverUrl}/v1/${groupId}`,
    headers: {
        authorization: personalToken,
        'Content-Type': 'application/json'
    }
});
