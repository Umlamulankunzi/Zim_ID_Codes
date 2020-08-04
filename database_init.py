import sqlite3
from typing import List, Any, Union, Tuple

__data__: List[Union[Tuple[str, str, str], Any]] = [
    ('Bulawayo', 'Bulawayo', '08'), ('Harare', 'Harare', '63'),
    ('Manicaland', 'Buhera', '07'), ('Manicaland', 'Chimanimani', '44'),
    ('Manicaland', 'Chipinge', '13'), ('Manicaland', 'Makoni', '42'),
    ('Manicaland', 'Mutare', '75'), ('Manicaland', 'Mutasa', '50'),
    ('Manicaland', 'Nyanga', '34'), ('Mashonaland Central', 'Bindura', '05'),
    ('Mashonaland Central', 'Guruve', '71'),
    ('Mashonaland Central', 'Mazowe', '15'),
    ('Mashonaland Central', 'Mt Darwin', '45'),
    ('Mashonaland Central', 'Muzarabani', '11'),
    ('Mashonaland Central', 'Rushinga', '61'),
    ('Mashonaland Central', 'Shamva', '68'),
    ('Mashonaland East', 'Chikomba', '18'),
    ('Mashonaland East', 'Goromonzi', '25'),
    ('Mashonaland East', 'Hwedza', '80'),
    ('Mashonaland East', 'Marondera', '43'),
    ('Mashonaland East', 'Mudzi', '49'), ('Mashonaland East', 'Murehwa', '47'),
    ('Mashonaland East', 'Mutoko', '48'), ('Mashonaland East', 'Seke', '59'),
    ('Mashonaland East', 'Uzumba Maramba Pfungwe', '85'),
    ('Mashonaland West', 'Chegutu', '32'),
    ('Mashonaland West', 'Hurungwe', '38'),
    ('Mashonaland West', 'Kadoma', '24'), ('Mashonaland West', 'Kariba', '37'),
    ('Mashonaland West', 'Makonde', '70'),
    ('Mashonaland West', 'Zvimba', '86'),
    ('Masvingo', 'Bikita', '04'), ('Masvingo', 'Chiredzi', '14'),
    ('Masvingo', 'Chivi', '13'), ('Masvingo', 'Gutu', '27'),
    ('Masvingo', 'Masvingo', '22'), ('Masvingo', 'Mwenezi', '54'),
    ('Masvingo', 'Zaka', '83'), ('Matabeleland North', 'Binga', '06'),
    ('Matabeleland North', 'Bubi', '35'),
    ('Matabeleland North', 'Hwange', '79'),
    ('Matabeleland North', 'Lupane', '41'),
    ('Matabeleland North', 'Nkayi', '53'),
    ('Matabeleland North', 'Tsholotsho', '73'),
    ('Matabeleland North', 'Umguza', '84'),
    ('Matabeleland South', 'Beitbridge', '02'),
    ('Matabeleland South', 'Bulilimamangwe', '56'),
    ('Matabeleland South', 'Gwanda', '28'),
    ('Matabeleland South', 'Insiza', '21'),
    ('Matabeleland South', 'Matobo', '39'),
    ('Matabeleland South', 'Umzingwane', '19'),
    ('Matabeleland South', 'Plumtree', '56'),
    ('Midlands', 'Chirumanzu', '77'), ('Midlands', 'Gokwe North', '26'),
    ('Midlands', 'Gokwe South', '23'), ('Midlands', 'Gweru', '29'),
    ('Midlands', 'Kwekwe', '58'), ('Midlands', 'Mberengwa', '03'),
    ('Midlands', 'Shurugwi', '66'), ('Midlands', 'Zvishavane', '67')]

short_hand = {
    'Mat North': 'Matabeleland North',
    'Mat South': 'Matabeleland South',
    'Byo': 'Bulawayo', 'Hre': 'Harare',
    'Mtre': 'Mutare', 'Wedza': 'Hwedza',
    'Mash East': 'Mashonaland East',
    'Mash Central': 'Mashonaland Central',
    'Mash West': 'Mashonaland West',
    'Zvish': 'Zvishavane',
    'U M P': 'Uzumba Maramba Pfungwe',
    'Ump': 'Uzumba Maramba Pfungwe',
    '2': '02', '3': '03', '4': '04',
    '5': '05', '6': '06', '7': '07', 
    '8': '08',

}


class Data:
    """Database manipulation class

    Creates database if it does not exist and connects to database
    manages queries, updates to existing entries and new additions"""

    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()

        # Create tables if it does not exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS 
                        IdCodes (
                        province varchar(100),
                        district varchar(100),
                        code varchar(100))''')
        self.initialize_db()

    def add_entry(self, province, district, code):
        """Add an entry into the Database"""
        self.c.execute('''INSERT INTO IdCodes
                          VALUES ( ?, ?, ?)''', (province, district, code))
        self.conn.commit()

    def query(self, query_val=None, column=None, **kwargs):
        """Database query

        return the result of the query
        parameters:
            query_val:  value for query to return results with similar value
                        i.e database search constraint value
            column:     column in database to search for query_val in

            kwargs:     dict of  columns in database to return after 
                        search complete
                        kwargs columns named col1, col2, col3, ... , col'n'
                        where coln is the nth column
                        kwargs[col] being reserved to select all from database
                        i.e kwargs[col] == "all" """

        if query_val and kwargs and column:
            if len(kwargs) > 1:
                cmd = "SELECT " + ", ".join(kwargs.values()) + \
                      " FROM IdCodes WHERE " \
                      + column + " = :" + column + " ORDER BY district ASC"
            else:
                cmd = "SELECT " + list(kwargs.values())[0] + " FROM IdCodes " \
                      + "WHERE " + column + " = :" + column + \
                      " ORDER BY district ASC"

            self.c.execute(cmd, {column: query_val.strip()})

        elif kwargs and not query_val and not column:
            if kwargs.get("col", None) == "all":
                cmd = "SELECT * FROM IdCodes"
            elif len(kwargs) > 1:
                cmd = "SELECT " + ", ".join(kwargs.values()) + " FROM IdCodes "
            else:
                cmd = "SELECT " + list(kwargs.values())[0] + " FROM IdCodes "

            self.c.execute(cmd)

        elif query_val and column and not kwargs:
            cmd = "SELECT * FROM IdCodes WHERE " + column + "= :" + column
            self.c.execute(cmd, {column: query_val})

        result = self.c.fetchall()
        return result

    def get(self, value):
        choice_dict = {"prov": "province", "dist": "district", "code": "code"}
        # return list
        return sorted(
            list(
                set(
                    [val[0] for val in self.query(col1=choice_dict[value])]
                )))

    def initialize_db(self):
        for info in __data__:
            self.add_entry(*info)


