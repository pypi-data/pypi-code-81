import collections
import logging
from .exceptions import NoIDPassed

class Mongo:
    def __init__(self,**kwargs):
        self.connection_url = kwargs.get("connection_url")
        self.collection_name = kwargs.get("dbname")
        self.db = self.connection_url[self.collection_name]

    async def update(self, dict):
        """|coro|

        For simpler calls, points to self.update_by_id
        """
        await self.update_by_id(dict)

    async def get_by_id(self, id):
        """|coro|

        This is essentially find_by_id so point to that
        """
        return await self.find_by_id(id)

    async def find(self, id):
        """|coro|

        For simpler calls, points to self.find_by_id
        """
        return await self.find_by_id(id)

    async def delete(self, id):
        """|coro|

        For simpler calls, points to self.delete_by_id
        """
        await self.delete_by_id(id)

    # <-- Actual Methods -->
    async def find_by_id(self, id):
        """|coro|

        Returns the data found under `id`

        Parameters
        -----------

         -  id () : The id to search for

        Returns
        --------

         - None if nothing is found
         - If somethings found, return that
        """
        return await self.db.find_one({"_id": id})

    async def delete_by_id(self, id):
        """|coro|

        Deletes all items found with _id: `id`

        Parameters
        -----------

        -  id () : The id to search for and delete
        """
        if not await self.find_by_id(id):
            return

        await self.db.delete_many({"_id": id})

    async def insert(self, dict):
        """|coro|

        insert something into the db

        Parameters
        -----------

        - dict (Dictionary) : The Dictionary to insert
        """
        # Check if its actually a Dictionary
        if not isinstance(dict, collections.abc.Mapping):
            raise TypeError("Expected Dictionary.")

        if not dict["_id"]:
            raise NoIDPassed("id not found in supplied dict.")

        await self.db.insert_one(dict)

    async def upsert(self, dict):
        """|coro|

        Makes a new item in the document, if it already exists
        it will update that item instead
        This function parses an input Dictionary to get
        the relevant information needed to insert.
        Supports inserting when the document already exists

        Parameters
        -----------

         - dict (Dictionary) : The dict to insert
        """
        if await self.__get_raw(dict["_id"]) != None:
            await self.update_by_id(dict)
        else:
            await self.db.insert_one(dict)

    async def update_by_id(self, dict):
        """|coro|

        For when a document already exists in the data
        and you want to update something in it
        This function parses an input Dictionary to get
        the relevant information needed to update.

        Parameters
        ------------

         - dict (Dictionary) : The dict to insert
        """
        # Check if its actually a Dictionary
        if not isinstance(dict, collections.abc.Mapping):
            raise TypeError("Expected Dictionary.")

        if not dict["_id"]:
            raise NoIDPassed("id not found in supplied dict.")

        if not await self.find_by_id(dict["_id"]):
            return

        id = dict["_id"]
        dict.pop("_id")
        await self.db.update_one({"_id": id}, {"$set": dict})

    async def unset(self, dict):
        """|coro|

        For when you want to remove a field from
        a pre-existing document in the collection
        This function parses an input Dictionary to get
        the relevant information needed to unset.

        Parameters
        ----------

         - dict (Dictionary) : Dictionary to parse for info
        """
        # Check if its actually a Dictionary
        if not isinstance(dict, collections.abc.Mapping):
            raise TypeError("Expected Dictionary.")

        if not dict["_id"]:
            raise NoIDPassed("id not found in supplied dict.")

        if not await self.find_by_id(dict["_id"]):
            return

        id = dict["_id"]
        dict.pop("_id")
        await self.db.update_one({"_id": id}, {"$unset": dict})

    async def increment(self, id, amount, field):
        """|coro|

        Increment a given `field` by `amount`

        Parameters
        -----------
        id:
            The id to check for.

        amount:
            The amount the number goes up by

        field:
            The key in the data to increase/decrease the increment
        """
        if not await self.find_by_id(id):
            return

        await self.db.update_one({"_id": id}, {"$inc": {field: amount}})

    async def get_all(self):
        """|coro|

        Returns a list of all data in the document
        """
        data = []
        async for document in self.db.find({}):
            data.append(document)
        return data

    async def __get_raw(self, id):
        """
        An internal private method used to eval certain checks
        within other methods which require the actual data
        """
        return await self.db.find_one({"_id": id})
