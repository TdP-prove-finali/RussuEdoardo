from database.DB_connect import DBConnect

class DAO():
    @staticmethod
    def getAllComuni():
        cnx = DBConnect.get_connection()
        result = []

        cursor = cnx.cursor(dictionary=True)
        query = """select * 
                   from affluenzacomuni"""
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        cursor.close()
        cnx.close()
        return result
