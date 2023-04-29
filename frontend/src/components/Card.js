import React from "react";
import { CurrentUserContext } from "../contexts/CurrentUserContext";

function Card({ card, cardId, onCardClick, onLikeClick, onCardDelete }) {
    const currentUser = React.useContext(CurrentUserContext);

    const isOwn = card.owner._id === currentUser._id;
    const isLiked = card.likes.some(i => i._id === currentUser._id);
    const cardLikeButtonClassName = `card__like-btn ${isLiked && 'card__like-btn_active'}`

    const handleLikeClick = () => {
        onLikeClick(card);
    }

    const handleDeleteClick = () => {
        onCardDelete(card);
    }

    return (
        <article className="card" key={cardId}>
            {isOwn && <button className='card__trash-btn' onClick={handleDeleteClick} type="button"></button>}

            <img onClick={onCardClick} className="card__image" src={card.link} alt={card.name} />
            <div className="card__caption">
                <h2 className="card__title">{card.name}</h2>
                <div className="card__like">
                    <button onClick={handleLikeClick} className={cardLikeButtonClassName} type="button"></button>
                    <h3 className="card__like-counter">{card.likes.length}</h3>
                </div>
            </div>
        </article>
    );
}

export default Card;
