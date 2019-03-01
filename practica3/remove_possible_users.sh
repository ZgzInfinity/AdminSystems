#!/bin/bash

files="./incorrect_user_list_add_multiple_no_passwd.txt ./incorrect_user_list_remove_non_existing_user.txt ./incorrect_user_list_add_3_fields.txt ./correct_user_list.txt ./incorrect_user_list_add_no_passwd.txt"

for file in ${files}
do
    while read LINE
    do
        user=$(echo "$LINE" | cut -d',' -f1)
        sudo -i -- /bin/bash -c "id ${user} > /dev/null 2>&1 && /usr/sbin/userdel -r -f ${user} > /dev/null 2>&1"
    done < "$file"
done

# ensure return 0 status
exit 0
