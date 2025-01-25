import os
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared, operations
from unstructured.staging.base import dict_to_elements

def process_pdf(pdf_path, config):
    client = UnstructuredClient(
        api_key_auth=config["UNSTRUCTURED_API_KEY"],
        server_url=config["UNSTRUCTURED_API_URL"]
    )
    with open(pdf_path, "rb") as f:
        files = shared.Files(content=f.read(), file_name=os.path.basename(pdf_path))
    req = operations.PartitionRequest(
        partition_parameters=shared.PartitionParameters(
            files=files,
            strategy="hi_res",
            hi_res_model_name="yolox",
            skip_infer_table_types=[],
            pdf_infer_table_structure=True
        )
    )
    resp = client.general.partition(request=req)
    elements = dict_to_elements(resp.elements)
    return elements