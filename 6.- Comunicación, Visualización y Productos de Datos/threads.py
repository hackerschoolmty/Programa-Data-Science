from functools import partial
import time
from concurrent.futures import ThreadPoolExecutor
from tornado import gen
from bokeh.document import without_document_lock
from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure

source = ColumnDataSource(data=dict(x=[0], y=[0], color=["blue"]))
i = 0
doc = curdoc()
executor = ThreadPoolExecutor(max_workers=2)

def blocking_task(i):
    time.sleep(1)
    return i

# the unlocked callback uses this locked callback to safely update
@gen.coroutine
def locked_update(i):
    source.stream(dict(x=[source.data['x'][-1]+1], y=[i], color=["blue"]))

# this unclocked callback will not prevent other session callbacks from
# executing while it is in flight
@gen.coroutine
@without_document_lock
def unlocked_task():
    global i
    i += 1
    res = yield executor.submit(blocking_task, i)
    doc.add_next_tick_callback(partial(locked_update, i=res))

@gen.coroutine
def update():
    source.stream(dict(x=[source.data['x'][-1]+1], y=[i], color=["red"]))

p = figure(x_range=[0, 100], y_range=[0,20])
l = p.circle(x='x', y='y', color='color', source=source)

doc.add_periodic_callback(unlocked_task, 1000)
doc.add_periodic_callback(update, 200)
doc.add_root(p)


