import pymysql

from config import host, user, password, db_name

def use_db(command, user_id, crToken = '', priceBuy = '', count = ''):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print('Successfully connection')
        try:
            if command == 'create_table':
                with connection.cursor() as cursor:
                    query = "CREATE TABLE `crypto`(" \
                                         " id int AUTO_INCREMENT," \
                                         " `user_id` int," \
                                         " `token` varchar(32)," \
                                         " `price_buy` varchar(32)," \
                                         " `count` varchar(32)," \
                                         " PRIMARY KEY(id));"
                    cursor.execute(query)
                    print('Table create successfully')
            if command == 'add':
                with connection.cursor() as cursor:
                    user_id = "%70s" % user_id
                    query = "SELECT `price_buy` FROM `crypto` WHERE `user_id` = " + user_id.strip() + " AND `token` = '" + crToken.strip() + "';"
                    cursor.execute(query)
                    pr_buy = cursor.fetchall()[0]['price_buy']

                    query = "SELECT `count` FROM `crypto` WHERE `user_id` = '" + user_id.strip() + "' AND `token` = '" + crToken.strip() + "';"
                    cursor.execute(query)
                    c = cursor.fetchall()[0]['count']

                    if cursor.execute("SELECT `token` FROM `crypto` WHERE `user_id` = '" + user_id.strip() + "' AND `token` = '" + crToken.strip() + "';"):
                        cursor.execute("UPDATE `crypto` SET price_buy = " + "%70s" % ((
                                    float(priceBuy) + float(pr_buy))/2.0) + ", count = "
                                    + "%70s" % (float(c) + float(count)) +
                                " WHERE `user_id` = " + user_id.strip() + " AND `token` = '" + crToken + "';")
                    else:
                        query = "INSERT INTO `crypto`(user_id, token, price_buy, count) VALUES (" + user_id + ", '" + crToken +"', '"+ priceBuy + "', '" + count + "');"
                        cursor.execute(query)
                    connection.commit()
                    print('Data was inserted')
            if command == 'select':
                with connection.cursor() as cursor:
                    user_id = "%70s" % user_id
                    query = "SELECT * FROM `crypto` WHERE `user_id` = " + user_id.strip() + " AND `token` = '" + crToken + "';"
                    cursor.execute(query)
                    list = []
                    price_buy = 0
                    count = 0
                    for data in cursor:
                        price_buy = price_buy + float(data['price_buy'])
                        count = count + float(data['count'])
                    if price_buy != 0:
                        list.append(crToken)
                        list.append(price_buy)
                        list.append(count)
                    return list
            if command == 'delete_token':
                with connection.cursor() as cursor:
                    user_id = "%70s" % user_id
                    query = "SELECT `price_buy` FROM `crypto` WHERE `user_id` = " + user_id.strip() + " AND `token` = '" + crToken.strip() + "';"
                    cursor.execute(query)
                    pr_buy = cursor.fetchall()[0]['price_buy']

                    query = "SELECT `count` FROM `crypto` WHERE `user_id` = '" + user_id.strip() + "' AND `token` = '" + crToken.strip() + "';"
                    cursor.execute(query)
                    c = cursor.fetchall()[0]['count']

                    if cursor.execute("SELECT `token` FROM `crypto` WHERE `user_id` = '" + user_id.strip() + "' AND `token` = '" + crToken.strip() + "';"):
                        count = (float(c) - float(count))
                        print(count)
                        if count < 0:
                            cursor.execute("UPDATE `crypto` SET price_buy = " + "%70s" % ((
                                                                                                  float(
                                                                                                      priceBuy) + float(
                                                                                              pr_buy)) / 2.0) + ", count = "
                                           + "%70s" % 0 +
                                           " WHERE `user_id` = " + user_id.strip() + " AND `token` = '" + crToken + "';")
                        else:
                            cursor.execute("UPDATE `crypto` SET price_buy = " + "%70s" % ((
                                    float(priceBuy) + float(pr_buy))/2.0) + ", count = "
                                    + "%70s" % count +
                                " WHERE `user_id` = " + user_id.strip() + " AND `token` = '" + crToken + "';")
                    else:
                        query = "INSERT INTO `crypto`(user_id, token, price_buy, count) VALUES (" + user_id + ", '" + crToken +"', '"+ priceBuy + "', '" + count + "');"
                        cursor.execute(query)
                    connection.commit()
                    print('Data was inserted')
        finally:
            connection.close()
    except Exception as ex:
        print('Connection error')
        print(ex)