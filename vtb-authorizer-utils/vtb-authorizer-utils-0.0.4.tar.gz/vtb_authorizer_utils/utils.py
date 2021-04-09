from typing import Union, Optional, List, Dict

from vtb_authorizer_utils.data_objects import Organization, Project, Folder, Children
from vtb_authorizer_utils.errors import NotInHierarchyError
from vtb_authorizer_utils.gateway import AuthorizerGateway


async def generate_full_structure_path(gateway: AuthorizerGateway,
                                       context_object: Union[Organization, Project, Folder]) -> Optional[str]:
    """
    Генерация полного пути объекта контекста в иерархии
    :param gateway: AuthorizerGateway
    :param context_object: объект контекста
    :return: полный путь объекта контекста в иерархии
    """
    if isinstance(context_object, Organization):
        return f"/organization/{context_object.name}/"

    structure = await gateway.get_organization_structure(context_object.organization)

    if not structure:
        return None

    structure = _prepare_structure(structure)

    finger_in_structure = structure.get(context_object.name, None)
    if not finger_in_structure:
        raise NotInHierarchyError(context_object.name)

    finger = Children(name=context_object.name,
                      parent=finger_in_structure.parent,
                      type="project" if isinstance(context_object, Project) else "folder")

    result = ''
    while True:
        result = f"{finger.type}/{finger.name}/{result}"
        if finger.type == "organization":
            break

        finger = structure.get(finger.parent, None)
        if not finger:
            raise NotInHierarchyError(finger.name)

    return f"/{result}"


def _prepare_structure(structure: List[Children]) -> Dict[str, Children]:
    data = {}

    for children in structure:
        data[children.name] = children

    return data
