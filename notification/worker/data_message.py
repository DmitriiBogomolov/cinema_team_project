from string import Template

TEMPLATE_TEXT = {
    'review_like_received': {
        'subject': 'Вашу запись оценили :)',
        'title': 'Новые уведомления',
        'text': Template('У вас 1 новое уведомление\nПользователь $like_owner_id оценил вашу запись'),
        'image': 'https://pictures.s3.yandex.net:443/resources/news_1682073799.jpeg',
    },
    'mail_multiple': {
        'subject': 'Важное уведомление!',
        'title': 'Важное уведомление',
        'text': Template('Дорогой $email сообщаем Вам важную информацию\n...'),
        'image': 'https://pictures.s3.yandex.net:443/resources/news_1682073799.jpeg',
    },
    'welcome': {
        'subject': 'Welcome!',
        'title': 'Подтверждение email',
        'text': Template('Дорогой $email чтобы пожтвердить email перейдите по ссылке\n $message_data'),
        'image': 'https://pictures.s3.yandex.net:443/resources/news_1682073799.jpeg',
    }
}
