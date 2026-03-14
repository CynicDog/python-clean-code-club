import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium", layout_file="layouts/main.slides.json")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # In Memory Analytics with Apache Arrow 🏹
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dependencies
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pyarrow as pa
    import numpy as np 

    return mo, pa


@app.class_definition
class SVGResource:
    def __init__(self, path):
        self.path = "./images/" + path

    def _repr_svg_(self):
        try:
            with open(self.path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return f"<text>File {self.path} not found.</text>"


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Chapter 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Primitive fixed-length value arrays
    """)
    return


@app.cell(hide_code=True)
def _():
    SVGResource("physical_layout_primitive_fixed_array.svg")
    return


@app.cell
def _(pa):
    data_list = [1, None, 2, 4, 8] 

    data = [pa.array([val]) for val in data_list]
    cols = ['c' + str(i) for i in range(5)]

    pa.RecordBatch.from_arrays(data, cols).schema
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Dictionary-encoded arrays
    """)
    return


@app.cell(hide_code=True)
def _():
    SVGResource("physical_layout_dictionary_encoded_arrays.svg")
    return


@app.cell
def _(pa):
    values = ["foo", "bar", "foo", "barc", None, "baz"]

    pa.array(values).dictionary_encode()
    return


if __name__ == "__main__":
    app.run()
