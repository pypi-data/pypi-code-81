class DataSource():
    def get_sprite_types_enumerator(self):
        assert "Method should be overrided!"

    def get_sprite_type_costumes_enumerator(self, sprite_type_id):
        assert "Method should be overrided!"

    def get_sprite_type_costume_data(self, sprite_type_id, costume_id):
        """
        Should return False if loading failed.

        :param sprite_type_id:
        :param costume_id:
        :return:
        """
        assert "Method should be overrided!"