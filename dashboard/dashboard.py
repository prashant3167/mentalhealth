from dash import Dash, dcc, html, Input, Output, State
from dash import dash_table
import dash_bootstrap_components as dbc
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load data from the parquet files
data = pd.read_parquet("/Users/prashant/project/kaggle/remote_health/persistent_db/predicted_mental_satisfaction")
feature_importance = pd.read_parquet("/Users/prashant/project/kaggle/remote_health/persistent_db/feature_importance")
target = ["Satisfaction_with_Remote_Work"]
# Ensure that company names and employee IDs are strings
data['company'] = data['company'].astype(str)
data['Employee_ID'] = data['Employee_ID'].astype(str)

# Sort feature importance to get the top 5
feature_importance_sorted = feature_importance.sort_values(by="Importance", ascending=False)
top_features = feature_importance_sorted.head(10)["Feature"].tolist()
top_features = top_features + target

# Initialize the app layout
app.layout = html.Div(
    [
        html.Div([       
            html.H1('Remote Work & Mental Health 🌍🧠', style={'textAlign': 'center'})
        ]),

        html.Button("Show Feature Importance", id="toggle-feature-importance", n_clicks=0),
        dbc.Collapse(
            html.Div(
                dash_table.DataTable(
                    id='feature-importance-table',
                    columns=[
                        {"name": "Feature", "id": "Feature"},
                        {"name": "Importance", "id": "Importance"}
                    ],
                    data=[],  # Initially empty
                    page_size=5,  # Show top 5 features
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'left',
                        'padding': '5px'
                    },
                ),
                id="feature-table-container"
            ),
            id="collapse-feature-importance",
            is_open=False  # Initially collapsed
        ),

        # Dropdown for selecting company name
        html.Div([
            html.Label("Select Company:"),
            dcc.Dropdown(
                id="company-dropdown",
                options=[],
                placeholder="Select a company",
                clearable=False,
            ),
        ]),

        # Dropdown for selecting employee ID
        html.Div([
            html.Label("Select Employee ID:"),
            dcc.Dropdown(
                id="employee-dropdown",
                placeholder="Select an employee",
                clearable=False,
            ),
        ]),

        # Collapsible section for employee data table
        html.Button("Show Employee Data", id="toggle-employee-data", n_clicks=0),
        dbc.Collapse(
            html.Div(
                dash_table.DataTable(
                    id='employee-data-table',
                    columns=[
                        {"name": feature, "id": feature} for feature in top_features
                    ],
                    data=[],  # Initially empty
                    page_size=10,
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'left',
                        'padding': '5px'
                    }
                ),
                id="employee-table-container"
            ),
            id="collapse-employee-data",
            is_open=False  # Initially collapsed
        ),
    ]
)

# Load company names from the existing data DataFrame dynamically
@app.callback(
    Output('company-dropdown', 'options'),
    Input('company-dropdown', 'value')  # Trigger this when the dropdown is interacted with
)
def load_company_options(selected_value):
    companies = data['company'].unique()
    return [{"label": company, "value": company} for company in companies]

# Load employee options based on selected company
@app.callback(
    Output('employee-dropdown', 'options'),
    Input('company-dropdown', 'value')
)
def load_employee_options(selected_company):
    if selected_company:
        filtered_employees = data[data['company'] == selected_company]['Employee_ID'].unique()
        return [{"label": emp, "value": emp} for emp in filtered_employees]
    return []

# Update employee data table based on selected employee
@app.callback(
    Output('employee-data-table', 'data'),
    Input('employee-dropdown', 'value'),
    State('company-dropdown', 'value')
)
def update_employee_data(selected_employee, selected_company):
    if selected_employee and selected_company:
        # Filter data based on the selected company and employee
        employee_data = data[(data['company'] == selected_company) & (data['Employee_ID'] == selected_employee)]
        # Select only the top features from employee data
        return employee_data[top_features].to_dict('records')  # Show only the important features
    return []

# Callback to toggle visibility of the feature importance table
@app.callback(
    Output('collapse-feature-importance', 'is_open'),
    Input('toggle-feature-importance', 'n_clicks'),
    State('collapse-feature-importance', 'is_open')
)
def toggle_feature_importance(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Callback to toggle visibility of the employee data table
@app.callback(
    Output('collapse-employee-data', 'is_open'),
    Input('toggle-employee-data', 'n_clicks'),
    State('collapse-employee-data', 'is_open')
)
def toggle_employee_data(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Update feature importance table when the feature importance data is required
@app.callback(
    Output('feature-importance-table', 'data'),
    Input('toggle-feature-importance', 'n_clicks'),
    prevent_initial_call=True  # Prevent the callback from firing on app start
)
def update_feature_importance_table(n_clicks):
    # Load only the top features data
    return feature_importance_sorted.head(5).to_dict('records')

if __name__ == "__main__":
    app.run_server(debug=False)
