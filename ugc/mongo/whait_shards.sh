# Принимает название контейнера и проверяет статус шарда
# например, mongors1n1, mongors2n1

while :

do

    for status in $(docker exec -it "$1" bash -c 'echo "rs.status()" | mongosh')
    do
    if [ "$status" = "ok:" ]; then
        exit 0
    fi
    done

    sleep 1

done
