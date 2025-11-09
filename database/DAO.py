from database.DB_connect import DBConnect
from model.arco import Arco
from model.comune import Comune

class DAO():
    def getAllComuni(provincia):
        cnx = DBConnect.get_connection()
        result = []
        cursor = cnx.cursor(dictionary=True)
        query = """ select a.CODICE_ISTAT as codice,
                    a.comune as nome, a.provincia as provincia , a.sigla as codiceP,
                    a.elettori as elettori, a.affluenza as affluenza,
                    a.affluenza_percentuale as affluenza_percentuale 
                    from affluenzacomuni a
                    where a.provincia = %s
                    order by a.comune"""
        cursor.execute(query, (provincia,))
        for row in cursor:
            row["punteggio"] = 0
            result.append(Comune(**row))
        cursor.close()
        cnx.close()
        return result

    def getAllEdges(provincia):
        cnx = DBConnect.get_connection()
        result = []

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT 
                    c1.codiceComune AS codice1,
                    c1.nome         AS comune1,
                    c2.codiceComune AS codice2,
                    c2.nome         AS comune2,
                    2 * 6371.0088 * ASIN(
                    SQRT(
                    POW(SIN(RADIANS(c2.latitudine - c1.latitudine) / 2), 2) +
                    COS(RADIANS(c1.latitudine)) *
                    COS(RADIANS(c2.latitudine)) *
                    POW(SIN(RADIANS(c2.longitudine - c1.longitudine) / 2), 2))) AS distanza_km
                    FROM comuni_geocoded AS c1
                    JOIN comuni_geocoded AS c2
                    ON c1.codiceComune > c2.codiceComune
                    WHERE c1.latitudine IS NOT NULL
                    AND c2.latitudine IS NOT NULL
                    AND c1.longitudine IS NOT NULL
                    AND c2.longitudine IS NOT NULL
                    AND c1.nomeProvincia = c2.nomeProvincia
                    AND c1.nomeProvincia = %s
                    order by codice1;
        """ # formula di Haversine
        cursor.execute(query, (provincia,))
        for row in cursor:
            result.append(Arco(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getProvince():
        cnx = DBConnect.get_connection()
        result = []

        cursor = cnx.cursor(dictionary=True)
        query = """ select distinct cg.nomeProvincia as provincia
                    from comuni_geocoded cg 
                    order by cg.nomeProvincia 
                """
        cursor.execute(query,)
        for row in cursor:
            result.append(row["provincia"])
        cursor.close()
        cnx.close()
        return result

