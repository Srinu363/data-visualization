import pandas as pd
import plotly.graph_objects as go
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    if 'data_file' in request.files:
        data_file = request.files['data_file']
        if data_file.filename == '':
            return render_template('nofileprovided.html')

        # Read the uploaded data file
        data = pd.read_excel(data_file)

        # Get filter values from HTML form
        math_pass_marks = request.form.get('math_pass_marks', type=int, default=35)
        science_pass_marks = request.form.get('science_pass_marks', type=int, default=35)
        social_pass_marks = request.form.get('social_pass_marks', type=int, default=35)

        # Filtering the data based on the input values
        filtered_data = data.copy()

        filtered_data['Result'] = filtered_data.apply(
            lambda row: 'Pass' if row['Maths'] >= math_pass_marks and row['Science'] >= science_pass_marks and row['Social'] >= social_pass_marks else 'Fail',
            axis=1
        )

        # Generate visualizations and data tables
        bar_plot_div = generate_bar_chart(filtered_data)
        pie_plot_div = generate_pie_chart(filtered_data)
        passed_students_table = generate_data_table(filtered_data[filtered_data['Result'] == 'Pass'])
        failed_students_table = generate_data_table(filtered_data[filtered_data['Result'] == 'Fail'])

        # Redirect to the output.html template with the generated visualizations and data tables
        return render_template('output.html', bar_plot_div=bar_plot_div, pie_plot_div=pie_plot_div,
        passed_students_table=passed_students_table, failed_students_table=failed_students_table)

    return "Error: No file provided."

def generate_bar_chart(filtered_data):
    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(x=filtered_data['Name'], y=filtered_data['Maths'], name='Maths'))
    bar_fig.add_trace(go.Bar(x=filtered_data['Name'], y=filtered_data['Science'], name='Science'))
    bar_fig.add_trace(go.Bar(x=filtered_data['Name'], y=filtered_data['Social'], name='Social'))

    bar_fig.update_layout(barmode='group', title='Student Marks', xaxis_title='Students', yaxis_title='Marks')

    return bar_fig.to_html(full_html=False)

def generate_pie_chart(filtered_data):
    pass_fail_counts = filtered_data['Result'].value_counts()
    pie_fig = go.Figure(go.Pie(labels=pass_fail_counts.index, values=pass_fail_counts.values, hole=0.3))
    pie_fig.update_layout(title='Pass/Fail Percentage')

    return pie_fig.to_html(full_html=False)

def generate_data_table(filtered_data):
    data_table = filtered_data[['Name', 'Maths', 'Science', 'Social']].to_html(index=False)
    return data_table

if __name__ == '__main__':
    app.run(debug=True)
