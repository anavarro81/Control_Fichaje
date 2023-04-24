class modelFichaje:
    @classmethod
    def check_date(self, fecha, db):
        try:
            # Crea un cursor para operar sobre la base de datos
            cursor = db.connection.cursor()

            # Comprobamos si existe en el usuario introducido en la BBDD.
            # Sentencia SQL a ejecutar. Selecciona todo para el usuario introducido.
            sql_select = """ SELECT Fecha, H_entrada, H_salida, Comentario FROM horario_fichaje WHERE Fecha='{}'""".format(
                fecha
            )

            # Se ejecuta el curso con la sentencia Sql generada.
            cursor.execute(sql_select)

            # Se lee del cursor una fila (row).
            # Devuelve una tupla donde cada campo de la tabla devuelto es una posición.
            row = cursor.fetchone()
            cursor.close()
            return row

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_clock_in(self, db, fecha, h_entrada="", h_salida="", comentario=""):
        try:
            # Crea un cursor para operar sobre la base de datos
            cursor = db.connection.cursor()

            # Comprobamos si existe la fecha en la base de datos
            fichaje = self.check_date(fecha, db)

            # Si ha encontrado la fila con el fichaje de esa fecha, la actualiza
            if fichaje != None:
                fecha_bd, h_entrada_bd, h_salida_bd, comentario_bd = fichaje

                if h_entrada > "":
                    h_entrada_bd = h_entrada

                if h_salida > "":
                    h_salida_bd = h_salida

                if comentario > "":
                    comentario_bd = comentario

                sql_upd_sal = """ UPDATE horario_fichaje
                     SET  H_entrada = '{}',
                          H_salida  = '{}',
                          Comentario = '{}'
                     WHERE Fecha ='{}' """.format(
                    h_entrada_bd, h_salida_bd, comentario_bd, fecha_bd
                )

                print(f"sql_upd_sal = {sql_upd_sal}")

                cursor.execute(sql_upd_sal)
                db.connection.commit()

            else:
                return None

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def insert_nuevo_dia(self, db, fecha):
        try:
            cursor = db.connection.cursor()
            # Inserta una nuevo dia en el calendario de fichaje, con la informacion inicializada.
            sql_insert_nuevo = """ INSERT INTO horario_fichaje (Fecha, H_entrada, H_salida, Comentario)
                                 VALUES ('{}', "00:00", "00:00", "" )""".format(
                fecha
            )

            print(sql_insert_nuevo)

            # Se ejecuta el insert
            cursor.execute(sql_insert_nuevo)
            cursor.close()

        except Exception as ex:
            raise Exception(ex)
