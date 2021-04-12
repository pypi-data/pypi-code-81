from ipywidgets import Box, Label, HTML


class MetadataFormatter:
    @staticmethod
    def from_box(box: Box):
        metadata = {}
        if (
            hasattr(box, "description")
            and hasattr(box, "value")
            and not isinstance(box, Label)
            and not isinstance(box, HTML)
        ):
            key = box.description.lower().replace(" ", "_")
            metadata[key] = box.value
        else:
            if hasattr(box, "children"):
                for children_box in box.children:
                    metadata_children = MetadataFormatter.from_box(children_box)
                    metadata = {**metadata, **metadata_children}
        return metadata
