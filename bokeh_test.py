from bokeh.io import output_file, show, vform
from bokeh.layouts import widgetbox, column, row, gridplot, layout
from bokeh.models import OpenURL, CustomJS, ColumnDataSource
from bokeh.models.widgets import Button, DataTable, TableColumn
from bokeh.models.widgets.markups import Div
from bokeh.plotting import figure, curdoc

test_items = [
    ("Test1", "Test Item 1", "Ready"),
    ("Test2", "Test Item 2", "Ready"),
    ("Test3", "Test Item 3", "Ready"),
    ("Test4", "Test Item 4", "Ready"),
]

items = []
descriptions = []
status = []
comment = []

for t in test_items:
    items.append(t[0])
    descriptions.append(t[1])
    status.append(t[2])
    comment.append("")

data = dict(items=items, descriptions=descriptions,
            status=status, comment=comment)
source = ColumnDataSource(data)
columns = [
    TableColumn(field="items", title="Item", width=100),
    TableColumn(field="descriptions", title="Description", width=200),
    TableColumn(field="status", title="Status", width=100),
    TableColumn(field="comment", title="Comment", width=200)
]
datatable = DataTable(source=source, columns=columns, width=800, height=400,
                      editable=True, row_headers=False)


def btn_callback():
    global source, datatable
    print(btn_callback.__name__)
    patches = {
        'status': [(1, "Pass")]
    }
    data = dict(items=items, descriptions=descriptions, status=status, comment=comment)
    local_source = ColumnDataSource(datatable.source.data)
    print(source)
    local_source.patch(patches)
    print(datatable.source.data)
    datatable.source = local_source


def btn2_callback():
    global source, datatable
    print(btn2_callback.__name__)

    waiting_status = []
    for i in range(len(status)):
        waiting_status.append("Waiting")

    update_data = {
        'items': items,
        'descriptions': descriptions,
        'status': waiting_status,
        'comment': comment
    }
    data = dict(items=items, descriptions=descriptions, status=status, comment=comment)
    source = ColumnDataSource(data)
    print(source)
    source.stream(update_data, rollover=len(status))
    datatable.source = source


def table_selection_cb(attr, old, new):
    print(__name__)


def doc_change(event):
    print(__name__)
    print(event)


def update():
    patches = {
        'status': [(0, "Pass"), (1, "Pass")]
    }
    source.patch(patches)


output_file("test.html")

button = Button(label="Test", button_type="success", width=150)
button2 = Button(label="Run", button_type="success", width=150)
div = Div(text="""<b>Test Status</b>""", width=800, height=200)

button.on_click(btn_callback)
button2.on_click(btn2_callback)
source.on_change('selected', table_selection_cb)
#source.on_change('modified', table_selection_cb)

#show(widgetbox(button))
#grid = gridplot([[widgetbox(datatable, sizing_mode="scale_width", responsive=True)], [widgetbox(button, button2, sizing_mode="stretch_both")]],
#                toolbar_location=None)
l = layout([
    [datatable],
    [div],
    [button],
    [button2]])

doc = curdoc()
#doc.add_periodic_callback(update, 1000)
doc.title = "Factory Test"
doc.add_root(l)
#doc.on_change(doc_change)
#curdoc().add_root(column(vform(datatable)))
#curdoc().add(row(vform(button), vform(button2)))
