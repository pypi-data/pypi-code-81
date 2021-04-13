import aiosqlite
import sqlite3,os
Database_dir = ""
default_extra={}
columns=["balance","bank","item1","item2","item3"]
run = 0
item = 0
item2 = 0
item3 = "0"
default_balance = 0
bank = 0
allowed_types=["INTEGER","TEXT"]
async def startup_items():
    if os.path.isfile(Database_dir+"main.db"):
        connection = sqlite3.connect(Database_dir+"main.db")
        cursor = connection.execute('SELECT * FROM users')
        columns_temp = [description[0] for description in cursor.description]
        connection.close()
        for item in columns_temp:
            if item not in columns:
                columns.append(item)
async def get_ready_for_insert():
    global item, item2, item3, default_balance, bank,default_extra
    if len(columns) > 5:
        for item in columns:
            if not default_extra.get(item,False): default_extra.update({item:0})
        text_ins_i=""
        text_ins_m=""
        for item in columns:
            text_ins_i+=","+item
            text_ins_m+=",?"
        return f"INSERT INTO users({text_ins_i}) VALUES({text_ins_m})"
    else:
        return "INSERT INTO users(balance,bank,userid,item,item2,item3) VALUES(?,?,?,?,?,?)"
                
async def get_leaderboard(column="balance",limit:int=10):
    """
    Returns leaderboard by a column such as bank,balance and a limit which is set default as 10"""
    try:
        db = await aiosqlite.connect(Database_dir+"main.db")
        limit=str(limit)
        item = await db.execute(f"SELECT {column},userid FROM users ORDER BY {column} DESC limit {limit}")
        item = await item.fetchall()
        leaderboard=[]
        for user in item:
            leaderboard.append({"userid":user[1],column:user[0]})
        await db.close()
        return leaderboard
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def get_item(userid):
    """
    Returns an integer from the database"""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item = await db.execute("SELECT item FROM users WHERE userid = ?", (userid,))
        item = await item.fetchall()
        item = item[0][0]
        await db.close()
        return item
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def get_item_2(userid):
    """
    Returns an integer from the database"""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item2 = await db.execute("SELECT item2 FROM users WHERE userid = ?", (userid,))
        item2 = await item2.fetchall()
        item2 = item2[0][0]
        await db.close()
        return item2
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def get_item_3(userid):
    """
    Returns an string from the database"""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item3 = await db.execute("SELECT item3 FROM users WHERE userid = ?", (userid,))
        item3 = await item3.fetchall()
        item3 = item3[0][0]
        await db.close()
        return item3
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def add_item(userid, amount:int):
    """
    Adds items to the database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item = await db.execute("SELECT item FROM users WHERE userid = ?", (userid,))
        item = await item.fetchall()
        item = item[0][0]
        item += amount
        await db.execute("UPDATE users SET item = ? WHERE userid = ?", (item, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def remove_item(userid, amount:int):
    """
    Removes items to the database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item = await db.execute("SELECT item FROM users WHERE userid = ?", (userid,))
        item = await item.fetchall()
        item = item[0][0]
        item = item - amount
        await db.execute("UPDATE users SET item = ? WHERE userid = ?", (item, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def set_item(userid, amount:int):
    """
    Sets items to the database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item = await db.execute("SELECT item FROM users WHERE userid = ?", (userid,))
        item = await item.fetchall()
        item = item[0][0]
        item = amount
        await db.execute("UPDATE users SET item = ? WHERE userid = ?", (item, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def add_item_2(userid, amount:int):
    """
    Adds item2 to the database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item2 = await db.execute("SELECT item2 FROM users WHERE userid = ?", (userid,))
        item2 = await item2.fetchall()
        item2 = item2[0][0]
        item2 += amount
        await db.execute("UPDATE users SET item2 = ? WHERE userid = ?", (item2, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def remove_item_2(userid, amount:int):
    """
    Removes item2 from the by the amount database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item2 = await db.execute("SELECT item2 FROM users WHERE userid = ?", (userid,))
        item2 = await item2.fetchall()
        item2 = item2[0][0]
        item2 = item2 - amount
        await db.execute("UPDATE users SET item2 = ? WHERE userid = ?", (item2, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def set_item_2(userid, amount:int):
    """
    Set item2 to the database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item2 = await db.execute("SELECT item2 FROM users WHERE userid = ?", (userid,))
        item2 = await item2.fetchall()
        item2 = item2[0][0]
        item2 = amount
        await db.execute("UPDATE users SET item2 = ? WHERE userid = ?", (item2, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def remove_item_3(userid, amount:int):
    """
    Remove item3 from the database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item3 = await db.execute("SELECT item3 FROM users WHERE userid = ?", (userid,))
        item3 = await item3.fetchall()
        item3 = item3[0][0]
        item3 = item3 - amount
        await db.execute("UPDATE users SET item3 = ? WHERE userid = ?", (item3, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def set_item_3(userid, text):
    """
    Set item3 to the database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item3 = await db.execute("SELECT item3 FROM users WHERE userid = ?", (userid,))
        item3 = await item3.fetchall()
        item3 = item3[0][0]
        item3 = text
        await db.execute("UPDATE users SET item3 = ? WHERE userid = ?", (item3, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def get_bank(userid):
    """
    Returns the bank balance of the userid provided."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        bank = await db.execute("SELECT bank FROM users WHERE userid = ?", (userid,))
        bank = await bank.fetchall()
        bank = bank[0][0]
        await db.close()
        return bank
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def add_bank(userid, amount:int):
    """
    Adds balance to the userid."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        bank = await db.execute("SELECT bank FROM users WHERE userid = ?", (userid,))
        bank = await bank.fetchall()
        bank = bank[0][0]
        bank += amount
        await db.execute("UPDATE users SET bank = ? WHERE userid = ?", (bank, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def add_citem(column,userid, amount):
    """
    Adds balance to the userid."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        bank = await db.execute(f"SELECT {column} FROM users WHERE userid = ?", (userid,))
        bank = await bank.fetchall()
        bank = bank[0][0]
        bank += amount
        await db.execute(f"UPDATE users SET {column} = ? WHERE userid = ?", (bank, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def remove_citem(column,userid, amount:int):
    """
    Adds balance to the userid."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        bank = await db.execute(f"SELECT {column} FROM users WHERE userid = ?", (userid,))
        bank = await bank.fetchall()
        bank = bank[0][0]
        bank -= amount
        await db.execute(f"UPDATE users SET {column} = ? WHERE userid = ?", (bank, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def set_citem(column,userid, amount):
    """
    Adds balance to the userid."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        await db.execute(f"UPDATE users SET {column} = ? WHERE userid = ?", (amount, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def remove_bank(userid, amount:int):
    """
    Remove from the bank balance from the userid."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        bank = await db.execute("SELECT bank FROM users WHERE userid = ?", (userid,))
        bank = await bank.fetchall()
        bank = bank[0][0]
        bank = bank - amount
        await db.execute("UPDATE users SET bank = ? WHERE userid = ?", (bank, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def get_balance(userid):
    """
    Returns the balance of the userid provided."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        balance = await db.execute("SELECT balance FROM users WHERE userid = ?", (userid,))
        balance = await balance.fetchall()
        balance = balance[0][0]
        await db.close()
        return balance
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def get_citem(column,userid):
    """
    Returns the balance of the userid provided."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        balance = await db.execute(f"SELECT {column} FROM users WHERE userid = ?", (userid,))
        balance = await balance.fetchall()
        balance = balance[0][0]
        await db.close()
        return balance
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def add_balance(userid, amount:int):
    """
    Adds balance to the userid."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        balance = await db.execute("SELECT balance FROM users WHERE userid = ?", (userid,))
        balance = await balance.fetchall()
        balance = balance[0][0]
        balance += amount
        await db.execute("UPDATE users SET balance = ? WHERE userid = ?", (balance, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def remove_balance(userid, amount:int):
    """
    Remove balance from the userid."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        balance = await db.execute("SELECT balance FROM users WHERE userid = ?", (userid,))
        balance = await balance.fetchall()
        balance = balance[0][0]
        balance = balance - amount
        await db.execute("UPDATE users SET balance = ? WHERE userid = ?", (balance, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def add_user(userid):
    """
    Adds user to the database with the default values."""
    try:
        global item, item2, item3, default_balance, bank,default_extra
        db = await aiosqlite.connect(Database_dir + "main.db")
        sql=await get_ready_for_insert()
        values=[default_balance, bank, userid,item,item2, item3]
        for value in default_extra.values():
            values.append(value)
        await db.execute(sql, values)
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def set_balance(userid, amount):
    """
    Sets choosen balance to the userid."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        balance = amount
        await db.execute("UPDATE users SET balance = ? WHERE userid = ?", (balance, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def set_bank(userid, amount):
    """
    Sets choosen balance to the userid."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        bank = amount
        await db.execute("UPDATE users SET bank = ? WHERE userid = ?", (bank, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def basic_user_check(userid):
    "Checks if user is in database returns a boolean."
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        user = await db.execute("SELECT userid FROM users WHERE userid = ?", (userid,))
        user = await user.fetchall()
        await db.close()
        if not user:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def user_check(userid):
    """
    Checks if user is in the database and if not adds him by the default values."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        user = await db.execute("SELECT userid FROM users WHERE userid = ?", (userid,))
        user = await user.fetchall()
        if not user:
            await db.execute("INSERT INTO users(balance,bank,userid,item,item2,item3) VALUES(?,?,?,?,?,?)", (default_balance, bank, userid,item,item2, item3))
            await db.commit()
        else:
            pass
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
async def setup_database(dir,**items):
    """
    Creates the db file and the table in your chosen directory."""
    try:
        global run
        if run == 0:
            run = 1
            db = await aiosqlite.connect(dir + "main.db")
            print(items)
            if len(items) > 1:
                item_txt=""
                print("1")
                for item in items.values():
                    print("2")
                    if item["type"] in allowed_types:
                        item_txt+=", "+item["name"]+" "+item["type"]
                print(f"CREATE TABLE users(balance INTEGER, bank INTEGER, userid INTEGER, item INTEGER, item2 INTEGER, item3 TEXT{item_txt})")
                await db.execute(f"CREATE TABLE users(balance INTEGER, bank INTEGER, userid INTEGER, item INTEGER, item2 INTEGER, item3 TEXT{item_txt})")
                await db.commit()
                await db.close()
            else:
                await db.execute(f"CREATE TABLE users(balance INTEGER, bank INTEGER, userid INTEGER, item INTEGER, item2 INTEGER, item3 TEXT)")
                await db.commit()
                await db.close()
            print(bcolors.OKGREEN+"Database setup done! Please remove the line from the code to prevent data loss. RESTART REQUIRED"+bcolors.ENDC)
    except Exception as e:
        try:
            await db.close()
        except:
            pass
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass


async def check_balance(userid, amount):
    "Checks if user has the amount or more in balance. Returns a boolean"
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        balance = await db.execute("SELECT balance FROM users WHERE userid = ?", (userid,))
        balance = await balance.fetchall()
        balance = balance[0][0]
        await db.close()
        if balance >= amount:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def check_bank(userid, amount):
    "Checks if user has the amount or more in bank. Returns a boolean"
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        bank = await db.execute("SELECT bank FROM users WHERE userid = ?", (userid,))
        bank = await bank.fetchall()
        bank = bank[0][0]
        await db.close()
        if bank >= amount:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def transfer_balance(from_userid:int, to_userid:int, amount:int):
    "Transfers money from 1 userid to another"
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        balance = await db.execute("SELECT balance FROM users WHERE userid = ?", (from_userid,))
        balance = await balance.fetchall()
        balance = balance[0][0]
        to_balance = await db.execute("SELECT balance FROM users WHERE userid = ?", (to_userid,))
        to_balance = await to_balance.fetchall()
        to_balance = to_balance[0][0]
        balance = balance - amount
        to_balance += amount
        await db.execute("UPDATE users SET balance = ? WHERE userid = ?", (balance, from_userid))
        await db.commit()
        await db.execute("UPDATE users SET balance = ? WHERE userid = ?", (to_balance, to_userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass