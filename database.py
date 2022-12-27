import psycopg2


class User:
    is_auth = False
    user_id = -1

    cursor = None
    connection = None

    def __init__(self):
        self.connection = psycopg2.connect(dbname='postgres',
                                           user='postgres',
                                           password='Pir2002pir',
                                           host='localhost',
                                           port=5432)
        self.cursor = self.connection.cursor()

    def can_report_check(self):
        cmd = f'''SELECT COUNT(*) <> 0 FROM chpe.admins WHERE chpe.admins.id_user = '{self.user_id}';'''
        self.cursor.execute(cmd)
        return self.cursor.fetchall()

    def can_report(self):
        cmd = f'''SELECT COUNT(*) <> 0 FROM chpe.reporters WHERE chpe.reporters.id_user = '{self.user_id}';'''
        self.cursor.execute(cmd)
        return self.cursor.fetchall()

    def get_unchecked_reports(self):
        cmd = '''
            SELECT 
                reports.id_report,
                characteristics_emergency.id_characteristics,
                emergency.id_chpe,
                emergency.name,
                characteristics_emergency.description,
                characteristics_emergency.point,
                characteristics_emergency.photo
            FROM chpe.reports
            JOIN chpe.emergency ON chpe.emergency.id_chpe = chpe.reports.id_chpe
            JOIN chpe.characteristics_emergency ON chpe.characteristics_emergency.id_characteristics = chpe.reports.id_chpe;
        '''

        self.cursor.execute(cmd)
        return self.cursor.fetchall()

    def get_checked_reports(self):
        cmd = '''
            SELECT 
                emergency.name,
                characteristics_emergency.description,
                characteristics_emergency.point,
                characteristics_emergency.photo
            FROM chpe.checks 
            JOIN chpe.emergency ON chpe.emergency.id_chpe = chpe.checks.id_chpe
            JOIN chpe.characteristics_emergency ON chpe.characteristics_emergency.id_characteristics = chpe.checks.id_chpe
            WHERE chpe.checks.check_report;
        '''

        self.cursor.execute(cmd)
        return self.cursor.fetchall()

    def try_auth(self, login, password):
        cmd = f'''SELECT * FROM chpe.users, chpe.users_characteristics 
                    WHERE chpe.users.user_password = MD5('{password}') 
                    AND chpe.users_characteristics.login = '{login}';
                '''
        self.cursor.execute(cmd)
        return self.cursor.fetchall()

    def add_report(self, title, description, location, files):
        cmd = f'''
            INSERT INTO
                chpe.actual_reports (id_a_report, data, id_report) 
            VALUES 
            (
                (SELECT count(id_a_report) FROM chpe.actual_reports) + 1,
                now(),
                1
            );
        
            INSERT INTO 
                chpe.characteristics_emergency (id_characteristics, description, type, photo, point) 
            VALUES 
            (
                (SELECT count(id_characteristics) FROM chpe.characteristics_emergency) + 1,
                '{description}',
                '{title}',
                '{files}',
                '(0, 0)'
            );
                
            INSERT INTO chpe.emergency (id_chpe, name, id_characteristics) 
            VALUES 
            (
                (SELECT count(id_chpe) FROM chpe.emergency) + 1,
                '{title}',
                (SELECT count(id_characteristics) FROM chpe.characteristics_emergency)
            );
            
            INSERT INTO chpe.reports (id_report, id_chpe, id_check, data_report) VALUES 
            (
                (SELECT count(id_report) FROM chpe.reports) + 1,
                (SELECT count(id_characteristics) FROM chpe.characteristics_emergency),
                (SELECT count(checks.id_check) FROM chpe.checks),
                now()
            );
            
        '''
        self.cursor.execute(cmd)
        self.connection.commit()

    def set_checked(self, ID):
        cmd = f'''
                UPDATE chpe.checks SET check_report = True WHERE id_check = {ID};
                UPDATE chpe.checks SET check_report = True WHERE id_chpe = {ID};
            '''
        self.cursor.execute(cmd)
        self.connection.commit()
