from dataclasses import dataclass

import streamlit as st

from src.gdrive import GDriveCredential, GDriveDownloader
from src.image import download_image, get_images, render_image
from src.label import get_default_quality, save_quality
from src.sidebar import (
    get_cell_number,
    get_cell_type,
    get_patient_list,
    get_project_list,
)


def main():
    credentials = GDriveCredential().credentials
    downloader = GDriveDownloader(credentials)

    st.title("""Tomocube Image Quality Labeller""")

    with st.sidebar:
        project_name = st.selectbox("Tomocube project", (get_project_list()))
        patient_id = st.selectbox(
            "Patient ID", (get_patient_list(project_name))
        )
        cell_type = st.selectbox("Cell type", (get_cell_type(project_name)))
        cell_number = st.selectbox(
            "Cell number",
            (get_cell_number(project_name, patient_id, cell_type)),
        )

    bf_cellimage, mip_cellimage, _ = get_images(
        project_name, patient_id, cell_type, cell_number
    )
    bf_path = download_image(
        downloader, bf_cellimage.image_google_id, "image", "bf.tiff"
    )
    mip_path = download_image(
        downloader, mip_cellimage.image_google_id, "image", "mip.tiff"
    )

    col1, col2 = st.columns(2)
    with col1:
        render_image(bf_path)
        bf_quality = get_default_quality(project_name, bf_cellimage.image_id)
        if bf_quality == "Good":
            st.success("Good")
        elif bf_quality == "Bad":
            st.error("Bad")
        elif bf_quality is None:
            st.warning("No quality label")

    with col2:
        render_image(mip_path)
        mip_default_quality = get_default_quality(
            project_name, mip_cellimage.image_id
        )
        if mip_default_quality == "Good":
            st.success("Good")
        elif mip_default_quality == "Bad":
            st.error("Bad")
        elif mip_default_quality is None:
            st.warning("No quality label")

    col1, col2, col3, col4 = st.columns(4)
    col1.button(
        "Good",
        on_click=save_quality,
        args=(project_name, bf_cellimage.image_id, "Good"),
        key="bf_good",
    )
    col2.button(
        "Bad",
        on_click=save_quality,
        args=(project_name, bf_cellimage.image_id, "Bad"),
        key="bf_bad",
    )
    col3.button(
        "Good",
        on_click=save_quality,
        args=(project_name, mip_cellimage.image_id, "Good"),
        key="mip_good",
    )
    col4.button(
        "Bad",
        on_click=save_quality,
        args=(project_name, mip_cellimage.image_id, "Bad"),
        key="mip_bad",
    )


if __name__ == "__main__":
    main()
