import os
import streamlit as st
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _query_builder = components.declare_component(
        "query_builder",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _query_builder = components.declare_component("query_builder", path=build_dir)
