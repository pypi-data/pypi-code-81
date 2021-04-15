from .db_status import DBStatus

class HealthcheckList(object):

    @staticmethod
    def setup(healthcheck, service_list):
        HealthcheckList.__healthcheck = healthcheck
        HealthcheckList.__dbstatus = DBStatus()

        service_enum = {
            'mongoengine': lambda x, y: HealthcheckList.__dbstatus.mongo_checker(x, y),
            'postgres': lambda x, y: HealthcheckList.__dbstatus.pgsql_checker(x),
            'mysql': lambda x, y: HealthcheckList.__dbstatus.mysql_checker(x),
            'redis': lambda x, y: HealthcheckList.__dbstatus.redis_checker()
        }
        

        for key, value in service_list.items():
            check_result = service_enum[key](
                value['connection'],
                value['lib_list'] if 'lib_list' in value else None) if value != None else service_enum[key](None, None)
            if isinstance(check_result, list):
                for temp in check_result:
                    HealthcheckList.__healthcheck.add_check(temp)
            else:
                HealthcheckList.__healthcheck.add_check(check_result)
        return HealthcheckList.__healthcheck
