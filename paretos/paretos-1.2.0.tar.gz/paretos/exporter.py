from typing import Dict, List

from sqlalchemy import create_engine, text


def export(data_source_name: str, project_name: str) -> List[Dict]:
    database_url = data_source_name
    engine = create_engine(database_url)

    with engine.connect() as con:
        statement = text(
            """
            SELECT
                project.id as project_id,
                simulation.id as simulation_id,
                simulation.is_pareto as simulation_is_pareto,
                `parameter`.name as parameter_name,
                parameter_type.name as parameter_type,
                parameter_value.id as parameter_value_id,
                parameter_value.number_value as parameter_value
            FROM project
            LEFT JOIN simulation ON (simulation.project_id = project.id)
            LEFT JOIN simulation_values ON (simulation_values.simulation_id = simulation.id)
            LEFT JOIN parameter_value ON (parameter_value.id = simulation_values.parameter_value_id)
            LEFT JOIN `parameter` ON (`parameter`.id = parameter_value.parameter_id)
            LEFT JOIN parameter_type ON (parameter_type.id = `parameter`.parameter_type_id)
            WHERE project.name = :project_name
            ORDER BY
                project.time_created ASC,
                simulation.time_created ASC,
                parameter_type.name ASC,
                parameter_value.time_created ASC
            """
        )

        sql_result = con.execute(statement.params(project_name=project_name))

        parameters_by_simulation_id = {}

        for row in sql_result:
            project_id = row["project_id"]
            simulation_id = row["simulation_id"]
            simulation_is_pareto = row["simulation_is_pareto"]
            parameter_name = row["parameter_name"]
            parameter_type = row["parameter_type"]
            parameter_value_id = row["parameter_value_id"]
            parameter_value = row["parameter_value"]

            if simulation_id not in parameters_by_simulation_id:
                parameters_by_simulation_id[simulation_id] = {}

            parameters = parameters_by_simulation_id[simulation_id]

            parameters[parameter_value_id] = {
                "project_id": project_id,
                "evaluation_id": simulation_id,
                "parameter_name": parameter_name,
                "parameter_type": parameter_type,
                "parameter_value": parameter_value,
                "simulation_is_pareto": simulation_is_pareto,
            }

        export_data = []

        for simulation_id in parameters_by_simulation_id:
            simulation = parameters_by_simulation_id[simulation_id]

            simulation_export = {}

            for parameter_id in simulation:
                parameter_data = simulation[parameter_id]

                if "evaluation_id" not in simulation_export:
                    simulation_export["project_id"] = parameter_data["project_id"]
                    simulation_export["evaluation_id"] = parameter_data["evaluation_id"]
                    simulation_export["is_pareto_optimal"] = parameter_data[
                        "simulation_is_pareto"
                    ]

                column_name = (
                    parameter_data["parameter_type"]
                    + "__"
                    + parameter_data["parameter_name"]
                )

                simulation_export[column_name] = parameter_data["parameter_value"]

            export_data.append(simulation_export)

        return export_data
