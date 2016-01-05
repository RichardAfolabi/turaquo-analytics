
from flask import Flask, render_template, request, redirect, url_for
from bokeh.embed import components
from bokeh.palettes import brewer

# from us_map_dataplot import make_us_map
from about_plots import *
from fiber_optics_dataset import *
from plotters import plot_stacked_bar_chart, make_us_map


TOOLS = "pan,reset,hover,save"


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['submit'] == 'city_btn1':
            desc = city_btn1_desc
            df = highest_incoming_loc.head()
            plot_colors = brewer["Purples"][3]
            label_x = "Long-haul fiber optics conduit"
            label_y = "Nos of fiber-optics connections"
            about_plot = 'Top 5 locations with HIGHEST incoming fiber links'
            bar = plot_stacked_bar_chart(df, label_x, label_y, plot_colors, is_stacked=True)
            script, div = components(bar)
            return render_template('index.html', script=script, div=div, about=about_plot, description=desc)

        elif request.form['submit'] == 'city_btn2':
            desc = city_btn2_desc
            df = lowest_outgoing_loc.head()
            plot_colors = brewer["Reds"][3]
            label_x = "Long-haul fiber optics conduit"
            label_y = "Nos of fiber-optics connections"
            about_plot = 'Top 5 Locations with LOWEST OUTGOING Fiber-optics Connections'
            bar = plot_stacked_bar_chart(df, label_x, label_y, plot_colors, is_stacked=True)
            script, div = components(bar)
            return render_template('index.html', script=script, div=div, about=about_plot, description=desc)

        elif request.form['submit'] == 'city_btn3':
            desc = city_btn3_desc
            plot_colors = brewer["Spectral"][10]
            label_y = "Average Link Utilization Difference (%)"
            label_x = "Top 5 and Lowest 5 Cities"
            city_diff = pd.DataFrame(top5_low5.City_Difference).transpose()
            about_plot = 'Differences between Incoming and Outgoing Links for Top 5 & Lowest 5 Cities (%)'
            b = plot_stacked_bar_chart(city_diff, label_x, label_y, plot_colors, lg_pos='bottom_left')
            script, div = components(b)
            return render_template('index.html', script=script, div=div, about=about_plot, description=desc)

        elif request.form['submit'] == 'city_btn4':
            desc = city_btn4_desc
            about_plot = 'Correlation information on the locations of Fiber optic conduits - CITY'
            plot_images = ['img/city_out_vs_in.png', 'img/city_in_vs_diff.png', 'img/city_out_vs_diff.png']
            return render_template('index.html', about=about_plot, plot_images=plot_images, description=desc)

        elif request.form['submit'] == 'state_btn1':
            desc = state_btn1_desc
            plot_colors = brewer["RdPu"][3]
            label_x = "States"
            label_y = "No of incoming & outgoing links"
            about_plot = 'Top 10 States by highest incoming & outgoing links'
            bar = plot_stacked_bar_chart(top_states_inc, label_x, label_y, plot_colors, is_stacked=True)
            script, div = components(bar)
            return render_template('index.html', script=script, div=div, about=about_plot, description=desc)

        elif request.form['submit'] == 'state_btn2':
            desc = state_btn2_desc
            plot_colors = brewer["OrRd"][3]
            label_x = "States"
            label_y = "No of incoming & outgoing links"
            about_plot = 'States with LOWEST Outgoing links'
            bar = plot_stacked_bar_chart(low_states_outg, label_x, label_y, plot_colors, is_stacked=True)
            script, div = components(bar)
            return render_template('index.html', script=script, div=div, about=about_plot, description=desc)

        elif request.form['submit'] == 'state_btn3':
            desc = state_btn3_desc
            plot_colors = brewer["PiYG"][state_diff.size]
            about_plot = 'Differences between Incoming and Outgoing Links for selected States'
            label_x = 'States'
            label_y = 'Utilization Differences'
            bar = plot_stacked_bar_chart(state_diff, label_x, label_y, plot_colors, lg_pos='bottom_left')
            script, div = components(bar)
            return render_template('index.html', script=script, div=div, about=about_plot, description=desc)

        elif request.form['submit'] == 'state_btn4':
            desc = state_btn4_desc
            about_plot = 'Correlation information on the locations of Fiber optic conduits - STATES'
            plot_images = ['img/state_out_vs_in.png', 'img/state_in_vs_diff.png', 'img/state_out_vs_diff.png']
            return render_template('index.html', about=about_plot, plot_images=plot_images, description=desc)

        elif request.form['submit'] == 'analysis_btn1':
            desc = analysis_btn1_desc
            about_plot = 'Fiber optics links within United States'
            hover_text, plot_fig = make_us_map(state_map)
            script, div = components(plot_fig)
            return render_template('index.html', about=about_plot, script=script, div=div, hover=hover_text,
                                   description=desc)

        elif request.form['submit'] == 'analysis_btn2':
            return render_template('tester.html')
        elif request.form['submit'] == 'analysis_btn3':
            return render_template('tester.html')
        elif request.form['submit'] == 'analysis_btn4':
            return render_template('tester.html')
        else:
            return redirect(url_for('index'))    # Unknown. Return home.

    else:            # request.method == 'GET'
        desc = analysis_btn1_desc
        about_plot = 'Fiber optics links within United States'
        hover_text, plot_fig = make_us_map(state_map)
        script, div = components(plot_fig)
        return render_template('index.html', about=about_plot, script=script, div=div, hover=hover_text,
                               description=desc)
        # return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
