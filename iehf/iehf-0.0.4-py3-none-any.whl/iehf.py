import numpy as np
import inflect
from scipy.stats import iqr


class PandasTransformFuncs:
    @staticmethod
    def calc_mean(x):
        return np.mean(x)

    @staticmethod
    def calc_iqr(x):
        return iqr(x)

    @staticmethod
    def calc_median(x):
        return np.median(x)

    @staticmethod
    def calc_iqr_score(x):
        return (x-np.median(x))/iqr(x)

    @staticmethod
    def calc_row_count(x):
        return len(x)


class HumanReadableTextFormatting:
    @staticmethod
    def format_col(x, method):
        if method == 'dollar':
            return f'${round(x):,}'
        if method == 'percent':
            return f'{round(x*1000)/10}%'
        if method == 'inflect':
            return inflect.engine().number_to_words(x)

    @staticmethod
    def html_text_augment(x, methods):
        tags = {
            'bold': 'b',
            'italics': 'i'
        }

        for m in methods:
            x = f"<{tags[m]}>{x}</{tags[m]}>"
        return x

    @staticmethod
    def add_br_to_title(x, n_chars):

        arr = x.split()

        counter = 0
        out_str = ''
        for w in arr:
            counter += len(w)
            if counter >= n_chars:
                out_str += f'<br>{w}'
                counter = 0
            else:
                out_str += w

        return out_str.strip()


def decimal_2_percent(x, n_decimals=0):
    return round(x*10**(n_decimals+2))/10**(n_decimals)


def distlr_fig_formatting(fig):
    fig = format_fig_layout(fig)
    fig.for_each_trace(
        lambda trace: UpdateTraceClass(trace).update_parent()
    )

    return fig


def format_fig_layout(fig):
    n_figs = len(fig._grid_ref)
    print(f'formatting {n_figs}')

    # adjust fig height based on number of figures
    # .75 fig_height for every fig greater than 1
    fig_height = 225
    fig_height = n_figs * fig_height + (n_figs-1)*.5 * fig_height
    fig_width = 282

    print(f'height:{fig_height}, width:{fig_width}')

    fig.update_layout(
        titlefont_size=12,
        width=fig_width,
        height=fig_height,
        margin=dict(l=5, r=5, t=50, b=5),
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        font_family="'Roboto' sans-serif",
    )

    fig.update_annotations(font_size=12)
    fig.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor='#C8CDD5',
        titlefont_size=10,
        tickfont_size=10
    )

    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor='#C8CDD5',
        titlefont_size=10,
        tickfont_size=10
    )

    fig = update_plot_grid(fig)

    return fig

# iterate through fig data, applies grid to bar graphs


def update_plot_grid(fig):
    for idx in range(len(fig.data)):
        if fig.data[idx].type == 'bar':
            fig = add_grid_update_yaxis(fig, idx)
    return fig


def downsample_steps(tick_steps, max_val, max_ticks=4):
    n_ticks = len(tick_steps)
    if n_ticks > max_ticks:
        sample_factor = int(np.ceil(n_ticks / max_ticks))
        tick_steps = np.array([tick_steps[idx]
                               for idx in range(0, n_ticks, sample_factor)])

    # max_tick_idx = np.where(tick_steps > max_val)[0][0] + 1
    return tick_steps


def add_grid_update_yaxis(fig, idx):
    fig_data = fig.data[idx]
    n_bars = len(fig_data.x)
    ymin, ymax, step = get_new_axis_range(fig_data.y)

    # exception for very small range values
    if step > 0:
        tick_steps = np.arange(ymin, ymax, step)
        tick_steps = downsample_steps(tick_steps, ymax)

        # probably no need to cap ymax, just keep it at original calculated ymax
        # ymax=cap_ymax(ymax, tick_steps, fig_data.y)
        print('yaxis details:')
        print(ymin, ymax)
        print(tick_steps)

        fig.update_yaxes(
            tickmode='array',
            tickvals=tick_steps,
            range=[ymin, ymax],
            row=idx+1, col=1
        )

        # dont draw line for first tick
        for y in tick_steps[1:]:
            fig.add_shape(type="line",
                          xref='paper', x0=-0.5, y0=y, x1=n_bars-0.5, y1=y,
                          line=dict(
                              color="#C8CDD5",
                              width=1.5,
                              dash="dot",

                          ),
                          layer='below',
                          row=idx+1, col=1
                          )
    return fig

# cap the max value if the maximum tick value is already
# larger than the max y value


def cap_ymax(ymax, tick_steps, ydata):
    if tick_steps[-1] > np.max(ydata):
        ymax = tick_steps[-1]

    return ymax


def get_new_axis_range(fig_data):
    ymin = np.min(fig_data) * .9
    ymax = np.max(fig_data) * 1.1
    rng = ymax-ymin

    step = rng/4
    step = adjust_step(step)

    # round ymin only, to set starting point for tick steps
    # ymax not necessary
    ymin = round_x_to_nearest_y(ymin, step, method='floor')
    # ymax=round_x_to_nearest_y(ymax, step, method = 'ceil')

    return ymin, ymax, step


def adjust_step(step):
    modifier = 5
    return np.power(10, np.floor(np.log10(step))) * modifier


def round_x_to_nearest_y(x, y, method='ceil'):
    if method == 'ceil':
        return np.ceil(x/y)*y
    elif method == 'floor':
        return np.floor(x/y)*y


class UpdateTraceClass():
    def __init__(self, trace):
        self.trace = trace
        self.theme = [
            '#0071EB',
            '#001A70',
            '#838D9C',
            '#05152D'
        ]

        self.trace_width = 268
        self.target_bar_width = 40
        self.axis_font_size = 10
        self.data_label_font_size = 10

    def update_parent(self):
        if self.trace.type == 'bar':
            self.update_bar()

        if self.trace.type == 'table':
            self.update_table()

        # if self.trace.type == 'scatter':
        #   self.update_scatter()

    def update_scatter(self):
        # self._update_bar_xlabels()

        update_dict = {
            'mode': 'lines+markers',
            'line': dict(color=self._get_bar_colors)
        }
        self.trace.update(update_dict)

    def update_bar(self):
        self._update_bar_xlabels()

        update_dict = {
            'marker_color': self._get_bar_colors(),
            'width': self._get_bar_width(),
            'textposition': 'outside',
            'outsidetextfont': {'size': self.axis_font_size},
        }
        self.trace.update(update_dict)

    def _get_bar_colors(self):
        n_colors = len(self.theme)
        color_array = [self.theme[idx % n_colors]
                       for idx, c in enumerate(self.trace.x)]
        return color_array

    def _get_bar_width(self):
        n_bars = len(self.trace.x)
        full_bar_width = self.trace_width/n_bars
        return np.min((1, self.target_bar_width/full_bar_width))

    def _update_bar_xlabels(self):
        n_labels = len(self.trace.x)
        n_chars = self.trace_width/(n_labels+2)/self.axis_font_size

        self.trace.x = [HumanReadableTextFormatting.add_br_to_title(
            label, n_chars) for label in self.trace.x]

    def update_table(self):
        self.trace.update({
            'cells': {
                'fill_color': '#FFFFFF',
                'line_color': '#C8CDD5',
                'line_width': 1,
                'font': {'size': self.data_label_font_size}
            },
            'header': {
                'fill_color':  '#001A70',
                'line_color': '#C8CDD5',
                'line_width': 1,
                'font': {'size': self.axis_font_size, 'color': 'white'}
            }
        })
